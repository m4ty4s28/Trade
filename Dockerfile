FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

COPY . /home/

WORKDIR /home/trading/

RUN pip3 install -r /home/trading/requirements.txt

RUN pip3 install tzdata

CMD python3 manage.py runserver 0.0.0.0:8000
