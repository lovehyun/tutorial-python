from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine('sqlite:///board.sqlite')
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Board(Base):
    __tablename__ = 'board'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Board: {self.id}, {self.title}, {self.message}>"

def add_board(title, message):
    new_board = Board(title=title, message=message)
    session = Session()
    session.add(new_board)
    session.commit()
    session.close()

def get_all_boards():
    session = Session()
    boards = session.query(Board).all()
    session.close()
    return boards

def delete_all_boards():
    session = Session()
    session.query(Board).delete()
    session.commit()
    session.close()

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    add_board('title1', 'message1')
    add_board('title2', 'message2')

    boards = get_all_boards()
    print(boards)

    delete_all_boards()
