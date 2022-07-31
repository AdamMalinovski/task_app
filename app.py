

from flask import Flask , render_template,request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://am:1234567@localhost:5432/blog_poster"

app.config['SECRET_KEY'] = '1234567'

db = SQLAlchemy(app)


class Topic(db.Model):
    __tablename__ = 'topics'

    topic_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=255))
    
    
class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    description = db.Column(db.String(length=255))

    topic = db.relationship("Topic")
    
    

@app.route('/')
def display_topics():
    return render_template('home.html', topics=Topic.query.all())


@app.route('/topic/<topic_id>')
def display_tasks(topic_id):
    return render_template('topic-tasks.html', topic= Topic.query.filter_by(topic_id=topic_id).first(),
                           tasks=Task.query.filter_by(topic_id=topic_id).all())


@app.route('/add/topic', methods=['POST'])
def add_topic():
    if not request.form['topic-title']:
        flash('Enter title for topic', 'tomato')
    else:
        topic = Topic(title=request.form['topic-title'])
        db.session.add(topic)
        db.session.commit()
        flash('Topic Added Succesfully', 'lawngreen')
    return redirect(url_for('display_topics'))


@app.route('/add/task/<topic_id>', methods=['POST'])
def add_task(topic_id):
    if not request.form['task-description']:
        flash('Enter Description for your new task', 'tomato')
    else:
        task = Task(description=request.form['task-description'], topic_id=topic_id)
        db.session.add(task)
        db.session.commit()
        flash('Task Added Succesfully', 'lawngreen')
    return redirect(url_for('display_tasks', topic_id=topic_id))


if __name__ == '__main__':
    app.run(debug=True)