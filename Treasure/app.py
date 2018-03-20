from __future__ import print_function
from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

import sys

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'treasure'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)

#Articles = Articles() used to test import without DB connection

# Index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get keyword (query)
        query = request.form['query']

        # Create Cursor
        cur = mysql.connection.cursor()

        # Get results by keywrod
        result = cur.execute("SELECT * FROM stores WHERE name LIKE %s", [query]) # only able to search store exactly match
        stores = cur.fetchall()
        if result > 0:
            return render_template('stores.html', stores=stores)

            # Close connection
            cur.close()
        else:
            error = 'Record not found'
            return render_template('home.html', error=error)
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Stores
@app.route('/stores')
def stores():
    #Create cursor
    cur = mysql.connection.cursor()

    #Connection
    #get akk stores
    result = cur.execute("SELECT * FROM stores")

    stores = cur.fetchall()

    if result > 0:
        return render_template('stores.html', stores=stores)
    else:
        msg = 'No Stores Found'
        return render_template('stores.html', msg=msg)
    # Close connection
    cur.close()


#Store
@app.route('/store/<string:id>/')
def store(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
# GROUP_CONCAT should be uesed
    result = cur.execute("SELECT * FROM books LEFT JOIN stores ON stores.id = books.store_id WHERE books.store_id = %s", [id])
# result = cur.execute("SELECT * FROM stores WHERE id = %s", [id])
    books = cur.fetchall()

    #get store infomation by id
    temp = cur.execute("SELECT * FROM stores WHERE id = %s", [id])
    info = cur.fetchall()

    return render_template('store.html', info=info, books=books)


# Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()


#Article
@app.route('/article/<string:id>/')
def article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()

    return render_template('article.html', article=article)


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.connection.cursor()

        # Get user by username
        result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            password = data['password']

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection
            cur.close()
        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')

# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles ----Plan one
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    result= cur.execute("SELECT * FROM users")

    users = cur.fetchall()

    if result > 0:
        return render_template('dashboard.html', articles=articles, users=users)
    else:
        msg = 'No Articles Found'
        return render_template('dashboard.html', msg=msg)
    # Close connection
    cur.close()

# Article Form Class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=200)])
    body = TextAreaField('Body', [validators.Length(min=30)])


#View details by user ID
@app.route('/user/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def user(id):
    cur = mysql.connection.cursor()

    # Get user info by user ID
    result = cur.execute("SELECT stores.id, stores.name, stores.profile, stores.contact, stores.address FROM stores  WHERE user_id = %s", [id])

    info = cur.fetchall()

    result = cur.execute("SELECT id, name FROM users  WHERE id = %s", [id])

    UserInfo = cur.fetchone()

    return render_template('user.html', info=info, UserInfo=UserInfo)


# Add Article
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body = form.body.data

        # Create Cursor
        cur = mysql.connection.cursor()

        # Execute
        cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)",(title, body, session['username']))

        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Created', 'success')

        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


# Edit Article
@app.route('/edit_article/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def edit_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])

    article = cur.fetchone()
    cur.close()
    # Get form
    form = ArticleForm(request.form)

    # Populate article form fields
    form.title.data = article['title']
    form.body.data = article['body']

    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body = request.form['body']

        # Create Cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        # Execute
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        # Commit to DB
        mysql.connection.commit()

        #Close connection
        cur.close()

        flash('Article Updated', 'success')

        return redirect(url_for('dashboard'))

    return render_template('edit_article.html', form=form)

# Delete Article
@app.route('/delete_article/<string:id>', methods=['POST'])
@is_logged_in
def delete_article(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM articles WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Article Deleted', 'success')

    return redirect(url_for('dashboard'))


# Delete user
@app.route('/delete_user/<string:id>', methods=['POST'])
@is_logged_in
def delete_user(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM users WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('User Deleted', 'success')

    return redirect(url_for('dashboard'))


# Delete user
@app.route('/delete_item/<string:id>', methods=['POST'])
@is_logged_in
def delete_item(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM books WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Book item Deleted', 'success')

    return redirect(url_for('dashboard'))

# Delete shop
@app.route('/delete_shop/<string:id>', methods=['POST'])
@is_logged_in
def delete_shop(id):
    # Create cursor
    cur = mysql.connection.cursor()

    # Execute
    cur.execute("DELETE FROM stores WHERE id = %s", [id])

    # Commit to DB
    mysql.connection.commit()

    #Close connection
    cur.close()

    flash('Shop have been Deleted', 'success')

    return redirect(url_for('dashboard'))
# @app.route('/add_shop/')
# def add_store():
#     return render_template('add_shop.html')



#Add store
@app.route('/add_shop/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def add_shop(id):

        # Create cursor
        cur = mysql.connection.cursor()

        #Get user info
        result = cur.execute("SELECT id, name FROM users WHERE id = %s", [id])

        name = cur.fetchone()
        cur.close()
        return render_template('add_shop.html', name=name)



@app.route('/create_shop/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def create_shop(id):
        if request.method == 'POST':
            # Get keyword (query)
            name = request.form['s_name']
            contact = request.form['s_contact']
            profile = request.form['s_profile']
            address = request.form['s_address']

            # Create Cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO stores(name, contact, profile, address, user_id) VALUES(%s, %s, %s, %s, %s)", (name, contact, profile, address, id))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()


        flash('Shop have been created', 'success')

        return redirect(url_for('dashboard'))

@app.route('/change_item/<string:id>', methods=['GET', 'POST'])
@is_logged_in
def change_item(id):
        if request.method == 'POST':
            # Get keyword (query)
            store_id = request.form['store_id']
            # cate = request.form['cate']

            name = request.form['b_name']
            author = request.form['author']
            pub = request.form['pub']
            date = request.form['date']
            price = request.form['price']




            # Create Cursor
            cur = mysql.connection.cursor()

            # Execute query
            cur.execute("INSERT INTO books( book_name, author, publisher, issue_date, price, store_id) VALUES(%s, %s, %s, %s, %s, %s)", (name, author, pub, date, price, store_id))

            # Commit to DB
            mysql.connection.commit()

            # Close connection
            cur.close()


        flash('Item change have been saved', 'success')

        return redirect(url_for('dashboard'))




#view shop
@app.route('/view_shop/<string:id>')
@is_logged_in
def view_shop(id):

	# Create cursor
	cur = mysql.connection.cursor()

    #Get user info
	result = cur.execute("SELECT * FROM stores WHERE id = %s", [id])

	shopInfo = cur.fetchone()
	cur.close()

	return render_template('view_shop.html', shopInfo=shopInfo)




#view item
@app.route('/view_item/<string:id>')
@is_logged_in
def view_item(id):

	# Create cursor
	cur = mysql.connection.cursor()

	result = cur.execute("SELECT * FROM books WHERE store_id = %s", [id])

	items = cur.fetchall()

	result = cur.execute("SELECT user_id, name FROM stores WHERE id = %s", [id])

	name = cur.fetchone()

	cur.close()

	return render_template('view_item.html', items=items, name=name)


@app.route('/edit_item/<string:id>')
@is_logged_in
def edit_item(id):

	# Create cursor
	cur = mysql.connection.cursor()

    #Get user info
	result = cur.execute("SELECT * FROM books LEFT JOIN categories ON categories.id = books.category_id WHERE books.id = %s", [id])

	itemInfo = cur.fetchall()
	result = cur.execute("SELECT * FROM categories")

	cate = cur.fetchall()


	cur.close()

	return render_template('edit_item.html', itemInfo=itemInfo, cate=cate)



if __name__ == '__main__':
    app.secret_key='treasure'
    app.run(debug=True)
