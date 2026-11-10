from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from pingwatch.core.db import SessionLocal
from pingwatch.core.models import Monitor
from pingwatch.core.schemas import MonitorCreate, MonitorRead

app = FastAPI(title="pingwatch")


def get_session() -> Iterator[Session]:
    with SessionLocal() as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@app.post("/monitors", response_model=MonitorRead, status_code=status.HTTP_201_CREATED)
def create_monitor(data: MonitorCreate, session: SessionDep) -> Monitor:
    url = str(data.url)
    existing = session.scalar(select(Monitor).where(Monitor.url == url))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This URL is already monitored",
        )
    monitor = Monitor(url=url)
    session.add(monitor)
    session.commit()
    session.refresh(monitor)
    return monitor


@app.get("/monitors", response_model=list[MonitorRead])
def list_monitors(session: SessionDep) -> list[Monitor]:
    return list(session.scalars(select(Monitor).order_by(Monitor.id)))


@app.get("/monitors/{monitor_id}", response_model=MonitorRead)
def get_monitor(monitor_id: int, session: SessionDep) -> Monitor:
    monitor = session.get(Monitor, monitor_id)
    if monitor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Monitor not found",
        )
    return monitor
