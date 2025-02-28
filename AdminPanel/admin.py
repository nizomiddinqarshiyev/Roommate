from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from AdminPanel.scheme import Register_stuff, Login_stuff, University_add, UserData_info_admin
from auth.auth import pwd_context
from auth.utils import verify_stuff_token, generate_token_stuff, send_mail
from database import get_async_session
from models.models import User, Stuff, Role, University

stuff_router = APIRouter()


@stuff_router.post('/stuff/add_stuff')
async def register_user_student(model: Register_stuff,
                                token: dict = Depends(verify_stuff_token),
                                session: AsyncSession = Depends(get_async_session)
                                ):
    try:
        role_name = token['role_name']
        if role_name.lower() == 'admin':
            if model.password_1 == model.password_2:
                password_hash = pwd_context.hash(model.password_2)
                query = insert(Stuff).values(firstname=model.first_name,
                                             lastname=model.last_name,
                                             phone=model.phone,
                                             password=password_hash,
                                             email=model.email,
                                             role_id=model.role_id,
                                             registred_at=datetime.utcnow())
                await session.execute(query)
                await session.commit()
                send_mail(model.email,model.phone,model.password_2)
                return HTTPException(status_code=200, detail="Registered!")
            else:
                return HTTPException(status_code=400, detail="Passwords are not same!")
    except Exception as e:
        return HTTPException(status_code=400, detail=f"{e}")


@stuff_router.post('/stuff/login/')
async def login(user: Login_stuff, session: AsyncSession = Depends(get_async_session)):
    try:
        query_user = select(Stuff).options(selectinload(Stuff.role)).where(Stuff.phone == user.phone)

        res_user = await session.execute(query_user)

        user_result = res_user.scalar_one_or_none()

        if user_result and pwd_context.verify(user.password, user_result.password):
            token = generate_token_stuff(user_result.id, user_result.role.name)
            return {"status_code": 200, "detail": token}
        else:
            return HTTPException(status_code=401, detail="Login Failed")
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))


@stuff_router.get('/admin/get_all/users', response_model=List[UserData_info_admin])
async def get_all_users(token: dict = Depends(verify_stuff_token),
                        session: AsyncSession = Depends(get_async_session)):
    try:
        role_name = token['role_name']
        print(role_name)
        if role_name.lower() == 'admin':
            query = select(User).options(selectinload(User.university),selectinload(User.faculty),selectinload(User.district))
            res_user = await session.execute(query)
            result_user = res_user.scalars().all()
            return result_user
        else:
            raise HTTPException(status_code=400, detail="Not allowed")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@stuff_router.post('/admin/add_university')
async def add_univesity(model:University_add,
                        token:dict=Depends(verify_stuff_token),
                        session:AsyncSession=Depends(get_async_session)
                        ):
    try:
        role_name = token.get('role_name')
        if role_name.lower() == 'admin':
            query= insert(University).values(**dict(model))
            await session.execute(query)
            await session.commit()
            return HTTPException(status_code=200,detail="Added")
    except Exception as e:
        return HTTPException(status_code=400,detail=str(e))