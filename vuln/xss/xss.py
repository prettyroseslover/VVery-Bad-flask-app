from flask import render_template

def xss_page(request, app):
    search = request.args.get('search')

    books = app.db_helper.execute_read(
        f"SELECT * FROM books WHERE name LIKE :search",
        { 'search': f'%{search}%' }
    )

    books = list(
        map(
            lambda b: {
                'id': b[0],
                'name': b[1],
                'price': b[2]
            },
            books
        )
    )
    return render_template('xss.html', books=books)