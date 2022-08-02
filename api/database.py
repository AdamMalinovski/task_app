# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy import create_engine
# from sqlalchemy.orm import create_session, session, sessionmaker, relationship
# from sqlalchemy.ext.declarative import declarative_base






# if __name__ == "__main__":
#     session = create_session()

#     flask_server_issue_topic = Topic(title="Flask server is not running")
#     session.add(flask_server_issue_topic)
#     session.commit()

#     task = Task(description="Execute the current python script in the terminal",
#                 topic_id=flask_server_issue_topic.topic_id)
#     session.add(task)
#     session.commit()
