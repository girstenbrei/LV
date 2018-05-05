FROM python:3.5-jessie
EXPOSE 8080
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/
WORKDIR /code/

CMD python manage.py runserver