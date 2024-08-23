# Teams Control: web application for manage work teams
Teams Control is a versatile platform designed to streamline team management and project coordination. With Teams Control, you can effortlessly create, delete, and manage teams tailored to your needs. Teams can be set as public, allowing anyone to send invitations to join, or secret, accessible only via a direct link. The platform offers robust tools for defining tasks, assigning them to team members, and managing project progress, making it an essential tool for efficient collaboration and productivity.

Try: [teamcontrol](https://djangocrud.oseiasromeiro.repl.co/)

<p align="center">
    <img src="app/static/img/capa.jpg" width="500" alt="Teams Control Logo" />
</p>


## Install dependences
Choose environment requirements file to install

```shell
pip install -r requirements-{environemt}.txt
```

## Environment
Configure environment file `.env` based in `.env.example`

## Database
Set default database in DjangoCRUD/settings.py and migrate:

```sh
python3 manage.py makemigrations
python3 manage.py migrate
```

### Fixtures
Feeding database

```sh
python3 manage.py loaddata users
python3 manage.py loaddata team
python3 manage.py loaddata team_invites
python3 manage.py loaddata team_participants
python3 manage.py loaddata goal
python3 manage.py loaddata goals
```

> all user passwords are `Teams#Control`

## Execute

- Development
```sh
python3 manage.py runserver
```
> access [localhost:8000](http://localhost:8000)

- Production
```sh
gunicorn DjangoCRUD.wsgi --bind 0.0.0.0 --log-file logs/gunicorn.log
```

> access [localhost:8000](http://localhost:8000)
