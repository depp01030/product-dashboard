from sqlalchemy import Column, Integer, String, Text, JSON, TIMESTAMP, func
from app.utils.db import Base

class ListingLog(Base):
    __tablename__ = "listing_log"

    log_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer)
    action = Column(String(50))
    request_data = Column(JSON)
    response_data = Column(JSON)
    status = Column(String(50))
    error_message = Column(Text)
    executed_at = Column(TIMESTAMP, server_default=func.now())
