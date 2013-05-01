# Deployment Instructions

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

## local Gotchas

running `fab prepare_deployment` from within the `neighborhood/neighborhood` directory will run all the tests and sync to a github repository. You'll need to set up your own repository, otherwise comment out the lines of `fabfile.py` that push to github.

## dotCloud Gotchas

If you don't know anything about dotCloud, please read how to [get started with Django on dotCloud](http://docs.dotcloud.com/tutorials/python/django/).

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

### 4.

Please change the password for the `admin` user after you deploy. Since the password is in source control (file: `postinstall`), everyone knows it.