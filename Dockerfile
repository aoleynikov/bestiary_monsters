 FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /code
 WORKDIR /code
 ENV FLASK_APP monsters_app.py
 COPY . /code
 RUN pip install -r requirements.txt