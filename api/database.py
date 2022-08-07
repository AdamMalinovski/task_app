from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.orm import create_session, session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(
    "postgresql://postgres:1234567@localhost:5432/blog_poster")

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





if __name__ == "__main__":
    session = create_session()

    flask_server_issue_topic = Topic(title="Flask server is not running")
    session.add(flask_server_issue_topic)
    session.commit()

    task = Task(description="Execute the current python script in the terminal",
                topic_id=flask_server_issue_topic.topic_id)
    session.add(task)
    session.commit()
