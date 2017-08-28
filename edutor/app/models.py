# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, relationship
from app.database import Base

class User(Base):
    __tablename__ = 'user'
    name = Column(String(30), nullable=False)
    email = Column(String(50), primary_key=True)
    password = Column(String(30), nullable=False)

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password
    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.email, self.password)

class Bot(Base):
    __tablename__ = 'bot'
    name = Column(String(30), primary_key=True)

    def __init__(self, name=None):
        self.name = name
    def __repr__(self):
        return "<Bot('%s')>" % (self.name)

class Term(Base):
    __tablename__ = 'term'
    year = Column(Integer)
    month = Column(Integer, primary_key=True)
    subject = Column(String(10))
    termtype = Column(String(5))

    def __init__(self, year=None, month=None, subject=None, termtype=None):
        self.year = year
        self.month = month
        self.subject = subject
        self.termtype = termtype
    def __repr__(self):
        return "<Term('%s', '%s', '%s', '%s')>" % (self.year, self.month, self.subject, self.termtype)
