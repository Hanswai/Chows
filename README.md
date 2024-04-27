# Chows
POS System in python


## Local Setup

Python > 3.0 should be ok
```
python3 -m venv venv
```
Dependencies can be installed as such
```
pip install -r requirements.txt
```

### DB

SQLite is the DB in use. Works pretty well for machine that doesn't have access to internet.
I use [DB Browser for SQLite](https://sqlitebrowser.org/) to handle the local machine databases.

TODO: Add seed data script

## Printer to work

## Caller Display

## QtDesigner

The main bulk of the UI is using the python version of Qt.
When using the python packages `pyqt5 pyqt5-tools`, it will also installer a nice QtDesigner which you can play around with their UI to generate mocks and it will covert the mocks to real code.

![](/docs/QtDesigner_example.png)