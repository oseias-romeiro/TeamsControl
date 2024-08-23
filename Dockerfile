FROM python

WORKDIR /app

COPY requirements-prd.txt .

RUN pip install --no-cache-dir -r requirements-prd.txt
# install db client
RUN pip install mysqlclient

COPY . .

## set environment variables
ENV DEBUG=False
ENV SECRET_KEY=S3cr3t
# default -> sqlite
ENV DBNAME=
ENV DBUSER=
ENV DBPASSWORD=
ENV DBHOST=
ENV DBPORT=

# setup db
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# load users
RUN python3 manage.py loaddata users
RUN python3 manage.py loaddata team
RUN python3 manage.py loaddata team_invites
RUN python3 manage.py loaddata team_participants
RUN python3 manage.py loaddata goal
RUN python3 manage.py loaddata goals

CMD ["gunicorn", "TeamsControl.wsgi", "--bind", "0.0.0.0", "--log-file", "logs/gunicorn.log"]

EXPOSE 8000