from sqlalchemy import Column, Integer, String, Text
from backend.database import Base


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True)
    user_message = Column(Text)
    ai_response = Column(Text)
