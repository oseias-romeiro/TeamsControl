# Teams Control: web application for manage work teams

With this application you can create a team and work together sharing gools. Your team can be public too and any other user in plataform with account can join it and help you.

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
flask run
```
> access [localhost:8000](http://localhost:8000)

- Production
```sh
gunicorn DjangoCRUD.wsgi --bind 0.0.0.0 --log-file logs/gunicorn.log
```

> access [localhost:8000](http://localhost:8000)
