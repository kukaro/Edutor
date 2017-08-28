# -*- coding: utf-8 -*-
from app.database import init_db, db_session
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from app.models import User, Bot, Term

def show_tables():
    queries = db_session.query(User)
    entries = [dict(name=q.name, email=q.email, password=q.password) for q in queries]
    print(entries)

def insertUser(name, email, password):
    user = User(name, email, password)
    db_session.add(user)
    db_session.commit()

def insertTerm(year, month, subject, termtype):
    term = Term(year, month, subject, termtype)
    db_session.add(term)
    db_session.commit()

def selectUserName(email):
    for name in db_session.query(User.name).filter_by(email=email):
        print(name)

def selectUser(email, password):
    user = db_session.query(User.name).filter_by(email=email).filter_by(password=password).first()
    return user

def selectTerm(year, month, subject, termtype):
    for term in db_session.query(Term).\
            filte_by(year=year).\
            filte_by(month=month).\
            filte_by(subject=subject).\
            filte_by(termtype=termtype):
        print(term.year, term.month, term.subject, term.termtype)

def deleteUser(email):
    db_session.query(User).filter(User.email==email).delete()
    db_session.commit()