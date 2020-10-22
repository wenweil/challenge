FROM python:3.9.0-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY /app .

CMD ["python","helloworld.py", "http://192.168.100.172:3000/api/auth/login"]