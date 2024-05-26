import datetime
import secrets
from typing import List

import aiofiles
from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from auth.utils import verify_token
from database import get_async_session
from mobile.scheme import RentGETScheme, RentADDScheme, FilterScheme, ReviewPostScheme, RateGetScheme
from models.models import Rent, Image, Rate

from datetime import datetime, timedelta

mobile_router = APIRouter()


@mobile_router.get('/student/rent', response_model=List[RentGETScheme])
async def get_all_rent(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        query = select(Rent).options(selectinload(Rent.jins), selectinload(Rent.category))
        rent = await session.execute(query)
        print(rent)
        rent_data = rent.scalars().all()
        return rent_data
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@mobile_router.post('/student/add-rent')
async def add_rent(
        data: RentADDScheme,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await session.execute(insert(Rent).values(**data.dict()))
        await session.commit()
    except Exception as e:
        raise HTTPException(status_code=400, detail='Error inserting request')

    return {'success': True}


@mobile_router.get('/student/home/filters-news')
async def rent_filter(
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    jins_id = token.get('jins_id')
    # Calculate the date 3 days ago
    three_days_ago = datetime.now() - timedelta(days=3)

    rents = select(Rent).options(
        selectinload(Rent.jins),
        selectinload(Rent.category),
        selectinload(Rent.renter)
    ).where(
        Rent.created_at >= three_days_ago
        , Rent.student_jins_id == jins_id
    )

    # Execute the query
    result = await session.execute(rents)
    rented_items = result.scalars().all()

    return rented_items


@mobile_router.post('/student/add-image-rent')
async def add_image_rent(
        image: UploadFile,
        rent_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    url = f'images/{image.filename}'
    async with aiofiles.open(url, 'wb') as zipf:
        content = await image.read()
        await zipf.write(content)
    hashcode = secrets.token_hex(32)
    data = insert(Image).values(url=url, hashcode=hashcode, rent_id=rent_id)
    await session.execute(data)
    await session.commit()
    return {'success': True}


@mobile_router.get('/student/image', response_class=FileResponse)
async def get_image(
        hashcode: str,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    data = await session.execute(select(Image).where(Image.hashcode == hashcode))
    image = data.scalars().first()
    if image:
        some_file_path = f"{image.url}"
        return some_file_path
    else:
        raise HTTPException(status_code=400, detail='Image is not available!')


@mobile_router.post('/student/add-review')
async def add_review(
        review_data: ReviewPostScheme,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        await session.execute(
            insert(Rate).values(
                **review_data.dict(), user_id=token['user_id'])
        )
        await session.commit()
        return {'review_data': review_data}
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Bad request!!!")


@mobile_router.get('/student/get_rents/get-review', response_model=List[RateGetScheme])
async def get_rents_review(
        rent_id: int,
        token: dict = Depends(verify_token),
        session: AsyncSession = Depends(get_async_session)
):
    query = select(Rate).options(selectinload(Rate.user)).where(Rate.rent_id == rent_id)
    data = await session.execute(query)
    rate_data = data.scalars().all()
    return rate_data
