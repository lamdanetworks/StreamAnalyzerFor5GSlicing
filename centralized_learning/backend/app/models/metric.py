from sqlalchemy import Column, Integer, String, DateTime
from app.db.base_class import Base


class Metric(Base):
    __tablename__ = "metrics"
    id = Column(Integer, primary_key=True, index=True)
    imsi = Column(String)
    device = Column(String)
    timestamp = Column(DateTime)
    rtt = Column(String)
    upf = Column(String)
    cpu = Column(String)
    ram = Column(String)
    bw_requested= Column(String)
    bw_received=Column(String)
    slice1_active_ues = Column(Integer)
    slice2_active_ues = Column(Integer)
    active_ues = Column(Integer)
    admission_flag=Column(Integer)

   