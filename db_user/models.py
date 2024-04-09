from sqlalchemy import Column, Integer, String, Date
from db_user.db import Base, engine

class Currency (Base):
    __tablename__ = "Ozon_data_user"

    id = Column(Integer(), primary_key=True)
    chat_number = Column(String)# хешируем
    client_id = Column(String)# шифруем
    api_key = Column(String)# шифруем
    date = Column(Date)

    def __repr__(self):
        return f"User id: {self.id}, chat_number: {self.chat_number}"


if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)