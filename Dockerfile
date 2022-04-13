FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .


EXPOSE 8000
RUN python manage.py createsuperuser
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
