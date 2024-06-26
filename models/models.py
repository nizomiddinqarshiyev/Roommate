from sqlalchemy import (
    Column, ForeignKey, Integer, String,
    Text, TIMESTAMP,
    MetaData, Boolean, Float
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()
metadata = MetaData()


class University(Base):
    __tablename__ = 'university'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_uz = Column(String)
    name_ru = Column(String)
    acronym_uz = Column(String)
    acronym_ru = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)

    faculty = relationship('Faculty', back_populates='university')
    user = relationship('User', back_populates='university')


class Faculty(Base):
    __tablename__ = 'faculty'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_uz = Column(String)
    name_ru = Column(String)
    university_id = Column(Integer, ForeignKey("university.id"))
    longitude = Column(Float)
    latitude = Column(Float)

    university = relationship('University', back_populates='faculty')
    user = relationship('User', back_populates='faculty')


class Region(Base):
    __tablename__ = 'region'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_uz = Column(String)
    name_ru = Column(String)

    district = relationship('District', back_populates='region')


class District(Base):
    __tablename__ = 'district'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_ru = Column(String)
    name_uz = Column(String)
    region_id = Column(Integer, ForeignKey('region.id'))

    region = relationship('Region', back_populates='district')
    user = relationship("User",back_populates='district')


class Jins(Base):
    __tablename__ = 'jins'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_uz = Column(String)
    name_ru = Column(String)

    user = relationship('User', back_populates='jins')
    rent = relationship('Rent', back_populates='jins')


class User(Base):
    __tablename__ = 'user'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String)
    jins_id = Column(Integer, ForeignKey('jins.id'))
    university_id = Column(Integer, ForeignKey("university.id"),nullable=True)
    faculty_id = Column(Integer, ForeignKey('faculty.id'),nullable=True)
    grade = Column(Integer,nullable=True)
    password = Column(String)
    image = Column(String)
    invisible = Column(Boolean, default=False)
    district_id = Column(Integer, ForeignKey("district.id"),nullable=True)
    register_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    university = relationship('University', back_populates='user')
    faculty = relationship('Faculty', back_populates='user')
    district = relationship('District', back_populates='user')
    wishlist = relationship('Wishlist', back_populates='user')
    rate = relationship('Rate', back_populates='user')
    jins = relationship('Jins', back_populates='user')
    announcement = relationship('Announcement', back_populates='user')


class Renter(Base):
    __tablename__ = 'renter'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String, unique=True)
    password = Column(String)
    image = Column(String)
    register_at = Column(TIMESTAMP, default=datetime.datetime.utcnow)

    rent = relationship('Rent', back_populates='renter')


class Category(Base):
    __tablename__ = 'category'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name_uz = Column(String)
    name_ru = Column(String)

    rent = relationship('Rent', back_populates='category')


class Rent(Base):
    __tablename__ = 'rent'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(Text)
    category_id = Column(Integer, ForeignKey('category.id'))
    contract = Column(Boolean)
    broker = Column(Boolean)
    room_count = Column(Integer)
    total_price = Column(Float)
    student_jins_id = Column(Integer, ForeignKey('jins.id'))
    student_count = Column(Integer)
    renter_id = Column(Integer, ForeignKey('renter.id'))
    location = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    wifi = Column(Boolean)
    conditioner = Column(Boolean)
    washing_machine = Column(Boolean)
    TV = Column(Boolean)
    refrigerator = Column(Boolean)
    furniture = Column(Boolean)
    other_convenience = Column(Text)
    created_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    updated_at = Column(TIMESTAMP)

    wishlist = relationship("Wishlist", back_populates='rent')
    category = relationship("Category", back_populates='rent')
    jins = relationship('Jins', back_populates='rent')
    renter = relationship("Renter",back_populates='rent')
    rate = relationship('Rate',back_populates='rent')
    image = relationship('Image', back_populates='rent')


class Rate(Base):
    __tablename__ = 'rate'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    rent_id = Column(Integer, ForeignKey('rent.id'))
    rate = Column(Integer)
    comment = Column(String)

    rent = relationship('Rent', back_populates='rate')
    user = relationship('User', back_populates='rate')


class Wishlist(Base):
    __tablename__ = 'wishlist'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    rent_id = Column(Integer, ForeignKey('rent.id'))

    rent = relationship('Rent', back_populates='wishlist')
    user = relationship('User', back_populates='wishlist')


class Image(Base):
    __tablename__ = 'image'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    rent_id = Column(Integer, ForeignKey('rent.id'))
    url = Column(String)
    hashcode = Column(String, unique=True)

    rent = relationship('Rent', back_populates='image')


class AnnouncementType(Base):
    __tablename__ = 'announcement_type'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    type_uz = Column(String)
    type_ru = Column(String)

    announcement = relationship('Announcement', back_populates='type')


class Announcement(Base):
    __tablename__ = 'announcement'
    metadata = metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(Text)
    type_id = Column(Integer, ForeignKey('announcement_type.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    type = relationship('AnnouncementType', back_populates='announcement')
    user = relationship('User', back_populates='announcement')


class Role(Base):
    __tablename__ = 'role'
    metadata=metadata
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(25))

    stuff = relationship('Stuff',back_populates='role')

class Stuff(Base):
    __tablename__ = 'stuff'
    metadata=metadata
    id = Column(Integer,primary_key=True,autoincrement=True)
    firstname = Column(String)
    lastname = Column(String)
    phone = Column(String, unique=True)
    password = Column(String)
    role_id = Column(Integer,ForeignKey('role.id'))
    email = Column(Text,unique=True)
    registred_at = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    last_login = Column(TIMESTAMP, default=datetime.datetime.utcnow())
    role = relationship('Role',back_populates='stuff')


