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
        timestamp = datetime.fromtimestamp(json_body['timestamp']) 
        imsi = json_body['imsi']
        device = json_body['device']
        rtt = json_body['rtt']
        upf=json_body['upf']
        cpu = json_body['cpu']
        ram = json_body['ram']
        slice1_active_ues=json_body['slice1_active_ues']
        slice2_active_ues=json_body['slice2_active_ues']
        active_ues=json_body['active_ues']
        bw_requested = json_body['bw_requested']
        bw_received=json_body['bw_received']
        admission_flag=json_body['admission_flag']
       

        db_metric = Metric(
            timestamp = timestamp, 
            imsi = imsi,
            device = device,
            rtt = rtt,
            upf=upf,
            cpu = cpu,
            ram = ram,
            slice1_active_ues=slice1_active_ues,
            slice2_active_ues=slice2_active_ues,
            active_ues=active_ues,
            bw_requested = bw_requested,
            bw_received=bw_received,
            admission_flag=admission_flag
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
