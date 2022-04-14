FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .

# ignore prev dbs and create new ones
RUN rm -f db.sqlite3 
RUN python manage.py migrate

EXPOSE 8000

#creates an admin account with creds as admin:admin
RUN python manage.py makeadmin

RUN python manage.py initDb
RUN python manage.py createMass



CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
