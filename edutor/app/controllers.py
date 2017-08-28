# -*- coding: utf-8 -*-
from app.database import init_db
from flask import Flask, request, session, redirect, url_for, abort, render_template, flash
from app.modelDao import insertUser, selectUser

from app import app

@app.route('/')

@app.route('/index')
def index():
    return None

@app.route('/login-form')
def loginForm():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = selectUser(email, password)

        if (user):
            session['logged_in'] = True
            session['name'] = user.name
            session['email'] = user.email
            return redirect('/index', name=user.name)
        else:
            return '로그인 정보가 맞지 않습니다.'
    else:
        return '잘못된 접근'

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session.clear()
    return redirect(url_for('login'))

@app.route('/join')
def join():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['password2']

        if password == password2:
            insertUser(name, email, password)
            return render_template('login.html')
        else:
            return '비밀번호를 다시 확인해주세요.'
    else:
        return '잘못된 접근'

@app.route('/join-form')
def joinForm():
    return render_template('join.html')









# def main():
#     selectUser('wlsgk0323@naver.com')
#     insertUser('김두수', 'kds@naver.com', 'password01')
#     selectUser('kds@naver.com')
#     db_session.close()
#
# if __name__=="__main__":
#     main()
#     show_tables()

