from fastapi import FastAPI, Depends
from typing import Annotated, List
from sqlalchemy.ext.asyncio import AsyncSession
from lifespan import lifespan
import models, schemas

from dependencies import get_db_session

from services import add_item, update_item, get_item, delete_item, get_items_by_filters


app = FastAPI(
    title='Avito but worse',
    description='Place your ads here if you dare',
    version='0.0.1',
    lifespan=lifespan
)

SessionDep = Annotated[AsyncSession, Depends(get_db_session)]

@app.post('/advertisement', response_model=schemas.CreateAdResponse, summary='Создать новое объявление')
async def create_ap(
        ap_data: schemas.CreateAdRequest,
        session: SessionDep
):

    new_ad = await add_item(session, models.Advertisement, ap_data)
    return schemas.CreateAdResponse(id=new_ad.id)


@app.get('/advertisement/{ad_id}', response_model=schemas.GetAd, summary='Получить объявление по ID')
async def get_ad(
        ad_id: int,
        session: SessionDep
):
    ad = await get_item(session, models.Advertisement, ad_id)
    return schemas.GetAd(**ad.ad_dict)

@app.get('/advertisement', response_model=List[schemas.GetAd], summary='Поиск объявлений')
async def search_ads(
    session: SessionDep,
    filters: schemas.AdFilter = Depends()
):
    ads = await get_items_by_filters(
        session=session,
        model=models.Advertisement,
        filters=filters,
    )
    return [schemas.GetAd(**ad.ad_dict) for ad in ads]

@app.patch('/advertisement/{ad_id}', response_model=schemas.UpdateAdResponse, summary='Обновить объявление по ID')
async def update_ad(
        ad_id: int,
        update_data: schemas.UpdateAdRequest,
        session: SessionDep
):
    updated_ad = await update_item(session, models.Advertisement, ad_id, update_data)
    return schemas.UpdateAdResponse(**updated_ad.ad_dict)


@app.delete('/advertisement/{ad_id}', response_model=schemas.DeleteAd, summary='Удалить объявление по ID')
async def delete_ad(
        ad_id: int,
        session: SessionDep
):
    await delete_item(session, models.Advertisement, ad_id)
    return schemas.DeleteAd