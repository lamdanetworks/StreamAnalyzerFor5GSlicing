FROM python:3.10-alpine
ENV PYTHONIOENCODING=utf-8
WORKDIR /app

RUN pip install 'poetry==2.0.0'
COPY ./backend /app
RUN poetry install --no-interaction

ENTRYPOINT [ "sh", "-c" , "poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000" ]
