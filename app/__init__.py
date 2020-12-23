from flask import Flask, render_template,request, url_for, flash, redirect
import sqlite3

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your secret key'

    
    @app.route('/')
    def index():
        conn = get_db_connection()
        movies = conn.execute('select * from movies order by movieId DESC limit 12 ').fetchall()
        conn.close()

        return render_template('index.html',movies=movies)

    def get_db_connection():
        conn = sqlite3.connect('data/moviesdb.db')
        conn.row_factory = sqlite3.Row
        return conn
    
   
    @app.route('/add')
    def create():
        return render_template('create.html')
    
    
    
    @app.route('/create', methods=('GET', 'POST'))
    def create_movies():
        if request.method == 'POST':
            title = request.form['title']
            genre = request.form['genre']

            if not title:
                flash('Title is required!')
            else:
                conn = get_db_connection()
                conn.execute('INSERT INTO movies (title, genres) values (?, ?)',
                            (title, genre))
                conn.commit()
                conn.close()
                return redirect(url_for('index'))

        return render_template('index.html')
    
    

    @app.route('/<int:id>/delete',methods=('GET', 'POST'))
    def delete(id):
        #title = get_post(id)
        conn = get_db_connection()
        conn.execute('DELETE FROM movies WHERE movieId = ?', (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    
    return app