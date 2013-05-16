# Deployment Instructions

This project uses a lot of different libraries to run; I found all sorts of "gotchas" crept up while creating and deploying, so I thought I'd document them here.

## General Gotchas

### 1.

Note that this project uses different `settings.py` files for local vs. production settings. Both inherit global settings from `base.py`.

This means that every time you run `manage.py` or similar you must specify the correct settings file.

For instance, to start the server on your local machine, you would run the command:

```python
python manage.py runserver --settings=neighborhood.settings.local
```

If you forget the `--settings` flag, don't be surprised to get an error like:

```python
ImportError: No module named collectstatic
```

(Type `python manage.py help` and `python manage.py help --settings=neighborhood.settings.local` and you'll see the difference in the `Available subcommands` section)

## 2.

Django and Celery have some unique undocumented requirements. The biggest one is around making sure that the Celery importer can actually find the named tasks.

To make this work, the `base.py` settings file contains the following:

```python
CELERY_IMPORTS = ("celerytest.tasks", )
```

and each defined task in a `tasks.py` file includes a parameter `name`:

```python
@task(name="tasks.foo")
def the_foo_task():
  return foobar
```

If you forget the `name=tasks.foo` parameter you'll get an error like `Received unregistered task of type 'tasks.add'.` when running the scheduler.

## 3.

The database schema in this project have changed several times and use [South](http://south.aeracode.org/) to migrate them and keep them up to date.

If you've never used South before, here's what you need to know:
* South writes incremental changes to the database schema on a per app basis. This is done by defining migrations for each incremental change
* South stores each migration as a python file in a folder called `migrations` e.g., `neighborhood\data\migrations\0001_initial.py`
* South creates a database table called `south_migrationhistory` which remembers which migrations have been called for each app in the project
* Since all the migrations exist, you can invoke them through the command: `python manage.py migrate appname --settings=path.to.settings`
  * If you look at `postinstall` you'll see that the migrations get called as part of the deploy process
  * If you run `fab migrate_local` you can invoke all the local migrations
* South intercepts `syncdb` to make sure that any apps using South (i.e., have the folder `migrations`) aren't updated by the `sycndb` process

## 4.

Make sure to run the `data.load.py` scripts that set up aggregate objects or you're going to get all kinds of errors:
* `create_fire_incident_objects()`
* `create_permit_ranges()`
* `create_violation_aggregates()`
* `create_police_detail_objects()`

## 5.

You'll need to update the files in `neighborhood/data/historical/` if you want to load historical data. You can download each CSV from the appropriate URL (see `load.py` for the URLs; you can limit them to the appropriate date range).

Note that when running locally you should set `DEBUG` to `False` to reduce memory and speed things. And when running in prod I found that I had to run each script individually; the thread would randomly halt otherwise.

I strongly recommend that you load the historical data locally, export them via `psql` and then load those files on the server.

## localhost Gotchas

### 1.

Running `fab prepare_deployment` from within the top level directory will run all the tests and sync to a github repository. You'll need to set up your own repository, otherwise comment out the lines of `fabfile.py` that push to github.

Note that this file is located in the top level directory as `git` can't commit files from higher level directories that where it is called.

### 2.

You need to create a spatial database in order to use this app. PostGIS 1.5.2 (not 2.0) must be installed. This also means that you must use a version of PostgreSQL < 9.2 as PostGIS 1.5.2 isn't compatible with 9.2 or later. On a Mac, this can lead to [implementation](http://mechanicalgirl.com/post/installing-postgis-homebrew/) [headaches](https://gist.github.com/fcurella/3188632).

### 3.

Run the celery scheduler locally through this command in a new Terminal window:

`python manage.py celery worker -B --loglevel=info --settings=neighborhood.settings.local`

or 

`python manage.py celeryd -E -B -l info -c 1 --settings=neighborhood.settings.local`

## dotCloud Gotchas

If you don't know anything about dotCloud, please read how to [get started with Django on dotCloud](http://docs.dotcloud.com/tutorials/python/django/) then [add geoDjango](http://docs.dotcloud.com/tutorials/python/geodjango/), a [Celery queue](http://docs.dotcloud.com/tutorials/python/django-celery/) powered by [Redis](http://docs.dotcloud.com/services/redis/). Any changes to these are noted below.

Note that after installation, dotCloud runs the `postinstall` script. Since we are activating two services (`python` and `python-worker`) there will actually be two installs and the script will run twice. Hence the conditional logic to make sure that only the appropriate code is run per install.

### 1.

In order to run on dotCloud you'll need to set two environment variables: `DB_POSTGIS_USER` and `DB_POSTGIS_PASSWORD`. Make sure you know [how to set environment variables](http://docs.dotcloud.com/guides/environment/).

### 2.

Deploying means setting up Nginx to serve static files like CSS, images, etc. This can cause you headaches if you set the location of your `static` directories wrong.

If you get a horrific message like:

```python
OSError: [Errno 2] No such file or directory: '/home/dotcloud/rsync-1367423258243/neighborhood/neighborhood/static'
```

you probably have a variable in your `base.py` file or similar that's pointing to the incorrect directory (in the above example, the directory `/home/dotcloud/rsync-1367423258243/neighborhood/static` - only one `neighborhood` - would have worked).

### 3.

It goes without saying, but you'll need to create a database before you can successfully load the site (you can deploy, but you'll just get a nasty error if you load the website). Here are the commands:

```
$dotcloud run db -- psql # Run this on your command line

postgres=# create database hood;
CREATE DATABASE
postgres=# create user admin with password 'strongpasswordhereplease';
CREATE ROLE
postgres=# grant all privileges on database hood to admin;
GRANT
postgres=# \q
```

This should create a spatially enabled database. You can test this by executing the following on the `psql` command line:
```
\c hood # Change to the database hood that you just created
SELECT PostGIS_full_version();
```

This should show something like:
```
                                         postgis_full_version                                          
-------------------------------------------------------------------------------------------------------
 POSTGIS="1.5.2" GEOS="3.2.2-CAPI-1.6.2" PROJ="Rel. 4.7.1, 23 September 2009" LIBXML="2.7.6" USE_STATS
(1 row)
```

### 4.

Please change the password for the `admin` user after you deploy. Since the password is in source control (file: `postinstall`), everyone knows it.

### 5.

You may have an error running initial migrations that create the geo features on tables. If they fail, make sure that your database user has sufficient permissions to access the tables `geometry_columns` and `spatial_ref_sys` (`GRANT ALL ON geometry_columns TO admin`)

### 6.

Note that the `postinstall` script includes migrations for `djcelery`. This is critical as if you don't include this, you won't get any database tables created and the queue will fail.

### 7.

The Celery workers will not start on dotCloud with the default memory levels (you'll receive an email with an Out of Memory error and then see cryptic `WorkerLostError: Could not start worker processes` message plus `SIGKILL` messages in the logs).

Scale to 128MB by typing this command:
```
dotcloud scale workers:memory=128M
```

You'll also likely have to scale the `www` (Python) process to 256MB as well.