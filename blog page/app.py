from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Database configuration
db_config = {
    'user': 'root',
    'password': '',
    'host': 'localhost',
    'database': 'blog.db'
}

# Function to get a database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM posts")
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('index.html', title='Blog Home', posts=posts, page='index')

@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post_detail(post_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM posts WHERE id = %s", (post_id,))
    post = cursor.fetchone()

    if request.method == 'POST':
        comment_content = request.form['comment']
        cursor.execute("INSERT INTO comments (post_id, content) VALUES (%s, %s)", (post_id, comment_content))
        conn.commit()
    
    cursor.execute("SELECT * FROM comments WHERE post_id = %s", (post_id,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('index.html', title=post['title'], post=post, comments=comments, page='post_detail')

@app.route('/add', methods=['GET', 'POST'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", (title, content))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        return redirect(url_for('index'))
    
    return render_template('index.html', title='Add New Post', page='add_post')

@app.route('/filter', methods=['GET'])
def filter_posts():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Query to filter posts by date
    cursor.execute("SELECT * FROM posts WHERE date BETWEEN %s AND %s", (start_date, end_date))
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return render_template('index.html', title='Filtered Posts', posts=posts, page='index')

if __name__ == '__main__':
    app.run(debug=True)
