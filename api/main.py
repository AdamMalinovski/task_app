
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session, session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


from flask import Flask , render_template,request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


engine = create_engine(
    "postgresql://postgres:1234567@postgres:5432/blog_poster")

Base = declarative_base()


class Topic(Base):
    __tablename__ = 'topics'

    topic_id = Column(Integer, primary_key=True)
    title = Column(String(length=255))

    def __repr__(self):
        return "<Topic(topic_id='{0}', title='{1}')>".format(self.topic_id, self.title)


class Task(Base):
    __tablename__ = 'tasks'

    task_id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey('topics.topic_id'))
    description = Column(String(length=255))

    topic = relationship('Topic')

    def __repr__(self):
        return "<Task(description='{0}')>".format(self.description)


Base.metadata.create_all(engine)


def create_session():
    session = sessionmaker(bind=engine)
    return session()

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234567@postgres:5432/blog_poster"

app.config['SECRET_KEY'] = '1234567'

db = SQLAlchemy(app)



class Topic(db.Model):
    __tablename__ = 'topics'

    topic_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=255))
    # find problem cascade updates task object as topic object getting
    task = db.relationship('Task', cascade='all, delete-orphan')
    
    
    
class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.topic_id'))
    description = db.Column(db.String(length=255))
    # backref allows associate topic with individual topic
    topic = db.relationship("Topic", backref='topic')
    
    

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


# adding delete func for individual tasks (without topic)

@app.route('/delete/task/<task_id>', methods=['POST'])
def delete_task(task_id):
    # selects task
    pending_delete_task = Task.query.filter_by(task_id=task_id).first()
    target_topic_id = pending_delete_task.topic.topic_id
    db.session.delete(pending_delete_task)
    db.session.commit()
    
    return redirect(url_for('display_tasks', topic_id=target_topic_id))


@app.route('/delete/topic/<topic_id>', methods=['POST'])
def delete_topic(topic_id):
    pending_delete_topic = Topic.query.filter_by(topic_id=topic_id).first()
    db.session.delete(pending_delete_topic)
    db.session.commit()
    
    return redirect(url_for('display_topics'))
    


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5533)
    session = create_session()

    flask_server_issue_topic = Topic(title="Flask server is not running")
    session.add(flask_server_issue_topic)
    session.commit()

    task = Task(description="Execute the current python script in the terminal",
                topic_id=flask_server_issue_topic.topic_id)
    session.add(task)
    session.commit()
