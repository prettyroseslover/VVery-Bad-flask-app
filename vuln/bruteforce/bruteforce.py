from flask import render_template, make_response
import hashlib

def brute_page(request, app):
    return make_response(render_template('bruteforce.html', user=None), 404)


def brute_api(request, app):
    form = request.form

    username = form.get('username')
    password = form.get('password')
    password = hashlib.md5(password.encode('utf-8')).hexdigest()

    db_result = app.db_helper.execute_read(
        f"SELECT * FROM users WHERE username=:username AND password=:password",
        { 'username': username, 'password': password }
    )

    if len(db_result) == 0:
        return make_response(render_template('bruteforce.html', user=None), 404)

    user = list(
        map(
            lambda u: app.db_models.UserDbModel(u), 
            db_result
        )
    ).pop()

    return make_response(render_template('bruteforce.html', user=user.username), 200)