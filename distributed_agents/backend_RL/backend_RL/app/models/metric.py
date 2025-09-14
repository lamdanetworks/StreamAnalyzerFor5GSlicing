from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db.base_class import Base
   
class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    IMSI_UE1 = Column(String)
    waiting_time_UE1 = Column(Integer)
    time_requested_UE1 = Column(Integer)
    IMSI_UE2 = Column(String)
    waiting_time_UE2 = Column(Integer)
    time_requested_UE2 = Column(Integer)
    IMSI_UE3 = Column(String)
    waiting_time_UE3 = Column(Integer)
    time_requested_UE3 = Column(Integer)
    episode_done = Column (String)   
    action = Column (Integer)
    reward = Column (Float)

    
   