FROM python

RUN apt update 
RUN apt install -y openssh-client pip

WORKDIR /app
COPY ./app /app

RUN pip install flask sqlalchemy

CMD ["python", "scripts/main.py"]