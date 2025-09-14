from fastapi import FastAPI, Depends, Request
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session
import os
from datetime import datetime, timedelta, timezone
from app.models.metric import Metric
from typing import Optional

DATABASE_URL = << your URL >> 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# FastAPI app setup
app = FastAPI(debug=True)


@app.get("/test")
async def test():
    print (DATABASE_URL)
    return {"test": "ok"}


@app.get("/metrics")
async def metrics(metric: str, ue: str, start: Optional[str] = None, end: Optional[str] = None, db: Session = Depends(get_db)):
    if start is not None:
        start_date = datetime.strptime(start, "%Y-%m-%d")
        if end is not None:
            end_date = datetime.strptime(end, "%Y-%m-%d")
        else:
            end_date = datetime.now()
    else:
        if end is not None:
            end_date = datetime.strptime(end, "%Y-%m-%d")
        else:
            end_date = datetime.now()
        start_date = end_date - timedelta(days=1)

    """
    Fetch a list of items from the database with pagination.
    """
    items = db.query(Metric).filter(Metric.ue == ue,
                                    Metric.timestamp.between(
                                        start_date, end_date),
                                    Metric.metric == metric).order_by(desc(Metric.timestamp)).all()
    return items


@app.post('/collect')
async def collect_metrics(request: Request):
    """Insert raw metric to database."""
    db = SessionLocal()
    try:
      
        json_body = await request.json()  # Parse the JSON body
        IMSI_UE1 = json_body['IMSI_UE1']
        waiting_time_UE1 = json_body['waiting_time_UE1']
        time_requested_UE1 = json_body['time_requested_UE1']
        IMSI_UE2 = json_body['IMSI_UE2']
        waiting_time_UE2 = json_body['waiting_time_UE2']
        time_requested_UE2 = json_body['time_requested_UE2']
        IMSI_UE3 = json_body['IMSI_UE3']
        waiting_time_UE3 = json_body['waiting_time_UE3']
        time_requested_UE3 = json_body['time_requested_UE3']
        episode_done = json_body['episode_done']
        action = json_body['action']
        reward = json_body['reward']

        db_metric = Metric(
            IMSI_UE1 = IMSI_UE1,
            waiting_time_UE1= waiting_time_UE1,
            time_requested_UE1=time_requested_UE1,
            IMSI_UE2 = IMSI_UE2,
            waiting_time_UE2= waiting_time_UE2,
            time_requested_UE2=time_requested_UE2,
            IMSI_UE3 = IMSI_UE3,
            waiting_time_UE3= waiting_time_UE3,
            time_requested_UE3=time_requested_UE3,
            episode_done = episode_done,   
            action = action, 
            reward = reward
            )

        db.add(db_metric)
        db.commit()
        print(json_body)
    except Exception as e:
        print ("I have a problem")
        print(e)
    finally:
        db.close()

    return {"detail": "Metric saved to the postgres database of 6G-XR metrics."}