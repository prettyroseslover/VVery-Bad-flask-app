from flask import render_template, make_response, redirect, url_for
import hashlib

def idor_page(request, app):
    return render_template('idor.html', error=False)

def idor_api(request, app):
    form = request.form

    username = form.get('username')
    password = form.get('password')
    password = hashlib.md5(password.encode('utf-8')).hexdigest()

    db_result = app.db_helper.execute_read(
        f"SELECT * FROM users WHERE username=:username AND password=:password",
        { 'username': username, 'password': password }
    )

    if len(db_result) == 0:
        return render_template('idor.html', error=True)

    user = list(
        map(
            lambda u: app.db_models.UserDbModel(u), 
            db_result
        )
    ).pop()

    resp = make_response(redirect(url_for('idor_profile')))

    resp.set_cookie('user_id', str(user.id))
    resp.set_cookie('session_token', str(user.password))

    return resp

def idor_next_page(request, app):

    user_id = request.cookies.get('user_id')

    db_result = app.db_helper.execute_read(
        f"SELECT * FROM users WHERE id=:user_id",
        { 'user_id': user_id }
    )

    if len(db_result) == 0:
        return render_template('idor_profile.html', user=None), 404

    user = list(
        map(
            lambda u: app.db_models.UserDbModel(u),
            db_result
        )
    ).pop()

    return render_template('idor_profile.html', user=user.username)