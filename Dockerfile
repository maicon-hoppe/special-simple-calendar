FROM python:3.13.13-alpine

WORKDIR /root/
COPY . .

RUN ["pip", "install", "-r", "./requirements.txt"]
RUN ["python3", "./manage.py", "collectstatic"]

ENTRYPOINT ["uvicorn", "special_simple_calendar.asgi:application", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80
