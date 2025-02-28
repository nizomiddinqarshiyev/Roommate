from typing import Optional
from pydantic import BaseModel

from auth.scheme import University_list, faculty_list, district_list, district_list_admin


class Register_stuff(BaseModel):
    first_name: str
    last_name: str
    phone: str
    password_1: str
    password_2: str
    role_id:int
    email:str


class Login_stuff(BaseModel):
    phone:str
    password:str

class University_add(BaseModel):
    name_uz:str
    name_ru:str
    acronym_uz:str
    acronym_ru:str
    longitude:float
    latitude:float




class UserData_info_admin(BaseModel):
    firstname: str
    lastname: str
    phone:str
    university_id:Optional[University_list] = None
    faculty_id:Optional[faculty_list] =  None
    grade:Optional[int] = None
    district_id:Optional[district_list_admin] = None