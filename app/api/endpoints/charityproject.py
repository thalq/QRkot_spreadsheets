from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_active,
                                check_charity_project_exists,
                                check_charity_project_update,
                                check_charity_project_was_invested,
                                check_name_duplicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charity_project_crud
from app.models import Donation
from app.schemas.charityproject import (CharityProjectCreate, CharityProjectDB,
                                        CharityProjectUpdate)
from app.services.investment import investing_process

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_meeting_room(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Возможность создания проектов только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    project_id = await charity_project_crud.get_project_id_by_name(charity_project.name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=422,
            detail="Такой проект уже существует!",
        )
    new_charity_project = await charity_project_crud.create(charity_project, session)
    await investing_process(new_charity_project, Donation, session)
    await session.refresh(new_charity_project)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Суперюзер может изменять название и описание
    существующего проекта,устанавливать для него новую требуемую сумму
    (но не меньше уже внесённой).
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    charity_project = await check_charity_project_active(charity_project, session)

    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount:
        await check_charity_project_update(project_id, session, obj_in.full_amount)
    charity_project = await charity_project_crud.update(
        charity_project,
        obj_in,
        session
    )
    charity_project = await investing_process(charity_project, Donation, session)
    return charity_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получить список всех проектов может любой юзер
    """
    return await charity_project_crud.get_multi(session)


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def remove_meeting_room(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Суперюзер может удалить только проекты,
    в которые не было внесено средств.
    """
    charity_project = await check_charity_project_exists(
        project_id, session
    )
    check_charity_project_was_invested(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
