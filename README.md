# Flask on Docker

A starter project for building Flask applications, utilizing PostgreSQL for the database and NGINX for reverse-proxy and static file serving

## Default endpoints
Endpoints are defined in `services/web/project/__init__.py`

* `/` returns json `{"hello": "world"}`
* `/static/hi.txt` returns a text file containing `hi!`
    * Any file placed in `static` folder is accessible through `/static/[filename.extension]`
* `/upload` returns a web form through which a user can upload files
    * Any file uploaded through form is accessible through `/media/[filename.extension]`

## Default commands
To execute commands against the `web` container, run: `docker-compose exec web python manage.py [command]`

For production, be sure to include `-f` flag: `-f docker-compose.prod.yml`

Commands are defined in `serrvices/web/manage.py`

* `create_db` drops the database and recreates it
    * This command is run by default when you start up the development server
    * You will need to run this manually at least once in production to set up database
* `seed_db` seeds the database with whatever is defined within

## Development

### Build and Deploy
Run `docker-compose up -d --build`

This will:
* Create the `web` and `db` containers
* Rebuild the database based on what is defined in the project
    * By default, this will create a basic `users` table (defined in `services/web/project/__init__.py`)
* Seed the database with what is defined in the `seed_db` command (defined in `services/web/manage.py`)
    * By default, this create a user with the email `test@email.com`


### Visit Page
Go to `localhost:5000` to see application run

## Production

### Create `env.prod`
Using `.env.dev` as a template, create an `.env.prod`. The only required changes for this setup is:
* Set `FLASK_ENV` to 'production'
* SET `APP_FOLDER` to '/home/app/web'

You should also set the `DATABASE_URL` to what fits for your application

### Create `env.prod.db`
This is the environment for the `db` container

You should define:
    * `POSTGRES_USER`
    * `POSTGRES_PASSWORD`
    * `POSTGRES_DB`

### ... or don't!
Of course, if you are deploying to an environment that manages your environment variables, you can define the required environment variables there instead of in files

### Build and Deploy
Run `docker-compose -f docker-compose.prod.yml up -d --build`

This will:
* Create the `web`, `db`, and `nginx` containers

### Visit Page
Go to `localhost:1337` to see application run

## Configuration

### NGINX
To change the `nginx` config, you can edit `services/nginx/nginx.conf`. This file is copied over to the `nginx` container during the build step

### Static Files
By default, static files are served out of `web/project/static/`. They are There is a sample `hello.txt` that can be deleted

## Prior Art
* [Dockerizing Flask with PosgreSQL, Gunicorn, and NGINX](https://testdriven.io/blog/dockerizing-flask-with-posgres-gunicorn-and-nginx/)
