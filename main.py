from flask import Flask, request, redirect, render_template, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(2000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog')
def blog():
    id = request.args.get('id')
    blog = Blog.query.get(id)
    title = blog.title
    body = blog.body

    return render_template('individual.html', title=title, body=body)



@app.route('/newpost', methods=['GET', 'POST'])
def new_blog():
    return render_template('newpost.html')



@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        blog_title = request.form['blog_title']
        blog = request.form['blog']
        if not blog or not blog_title:
            flash('enter a title or a body', 'error')
            return render_template('newpost.html')
        else:
            new_blog = Blog(blog_title, blog)
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/blog?id={0}'.format(new_blog.id))
    
    blogs = Blog.query.all()

    return render_template('blog.html', blogs=blogs)





if __name__=='__main__':
    app.run()