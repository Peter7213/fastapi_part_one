from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

import models, schemas

async def add_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_data: schemas.CreateAdRequest
) -> models.Advertisement:
    new_item = orm_model(**item_data.model_dump())
    session.add(new_item)
    try:
        await session.commit()
        await session.refresh(new_item)
        return new_item
    except IntegrityError as err:
        await session.rollback()
        if isinstance(err.orig, UniqueViolationError) and err.orig.pgcode == '23505':
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with such data already exists."
            )
        else:
            raise err

async def get_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
) -> models.Advertisement:
    rqst_obj = select(orm_model).where(orm_model.id == item_id)
    result = await session.execute(rqst_obj)
    ad_item = result.scalar_one_or_none()
    if not ad_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{orm_model.__name__} with id {item_id} not found'
        )
    return ad_item


async def get_items_by_filters(
        session: AsyncSession,
        model,
        filters: schemas.AdFilter
):
    query = select(model)
    if filters.header:
        query = query.where(model.header.ilike(f"%{filters.header}%"))
    if filters.description:
        query = query.where(model.description.ilike(f"%{filters.description}%"))
    if filters.author:
        query = query.where(model.author == filters.author)
    result = await session.execute(query)
    items = result.scalars().all()
    if not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Объявлений с этими данными не найдено'
        )
    return items

async def update_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int,
        update_data: schemas.UpdateAdRequest
) -> models.Advertisement:
    item = await get_item(session, orm_model, item_id)
    update_dict = update_data.model_dump(exclude_unset=True)
    for key, value in update_dict.items():
        setattr(item, key, value)
    await session.commit()
    await session.refresh(item)
    return item

async def delete_item(
        session: AsyncSession,
        orm_model: type[models.Advertisement],
        item_id: int
) -> None:
    item = await get_item(session, orm_model, item_id)
    await session.delete(item)
    await session.commit()