from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


class DBUsers(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    phone_number = Column(String)
    address_id = Column(Integer, ForeignKey("addresses.id"), nullable=True)

    todos = relationship("DBTodo", back_populates="owner")
    address = relationship("DBAddresses", back_populates="users")  # Corrected here


class DBTodo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("DBUsers", back_populates="todos")


class DBAddresses(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    address1 = Column(String)  # Corrected typo here
    address2 = Column(String)
    city = Column(String)
    state = Column(String)
    country = Column(String)
    postalcode = Column(String)
    apt_num = Column(String, nullable=True)

    users = relationship("DBUsers", back_populates="address")  # Corrected here
