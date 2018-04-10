# Django template
Default settings for my Django projects.

# Requirements
* Docker
* Docker Compose

# Usage

## Initial settings
```bash
$ project="project_name"
$ container=${project}_app_1
$ app="app_name"

$ docker-compose build
$ docker-compose run app django-admin.py startproject ${project} .
$ echo PRODUCTION=False > .env
$ emacs .env # Add SECRET_KEY='hogehoge'
$ docker-compose up

$ mkdir ${project}/${app}
$ docker exec -it ${container} python manage.py startapp ${app} ${project}/${app}
...
```


## Git
```bash
$ git init
$ git config --global user.name tat3
$ git config --global user.email user@example.com
$ git remote add origin https://github.com/tat3/hoge.git
```

## Set allowed hosts
```python:setting.py
ALLOWED_HOSTS = ["localhost", "{heroku_url}"]
```

## Setting for static file
```python:setting.py
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

## Introduce whilenoise
```python:setting.py
MIDDLEWARE += (
    'whitenoise.middleware.WhiteNoiseMiddleware',
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

```

## Deploy to Heroku
```text:Procfile
gunicorn mysite.wsgi --log-file -
```
Fix `mysite.wsgi` to `{project_name}.wsgi`.

```bash
$ heroku create ${myapp}
$ heroku config:set PRODUCTION=False
$ heroku config:set SECRET_KEY='hogehoge'
$ heroku config:set DISABLE_COLLECTSTATIC=1
$ git add .; git commit -m 'Initial commit'; git push heroku master
$ heroku open # confirm whether a default page can be seen
$ heroku config:set PRODUCTION=True
```
