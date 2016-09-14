# CCD Portal

Source code of new CCD Portal

## Installation
    
    sudo apt-get install python-dev
    pip install -r requirments.txt

## Setting up Database

This project uses Sqlite3 database.
    
    sudo apt-get install sqlite3 libsqlite3-dev
    
## Migrating Database

If you have made any change to `models.py`, then run makemigrations command to create new migrations
 based on the changes.
 
    ./manage.py makemigrations
    
Apply/unapply the migrations.

    ./manage.py migrate


## Links

* [TODOs](TODO.md)
* [Issues](https://github.com/narenchoudhary/CCD/issues)
