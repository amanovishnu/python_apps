# flask_apps
##### ways to create  a virtualenv
- anaconda: conda create --name <env name> python=<version>
- venv: py -m venv <env name>
- virtualenv: virtualenv <env name>

##### Ways to activate a virtual environment
- anaconda: conda activate <env name>
- venv:
    - <env name>/Scripts/activate (Windows)
    - <env name>/bin/activate (Linux)
- virtualenv:
    - <env name>/Scripts/activate (Windows)
    - <env name>/bin/activate (Linux)

##### Ways to deactivate a virtual environment
- anaconda: conda deactivate
- venv & virtualenv : deactivate

SET FLASK_APP = app.py

#### Ways to run a flask application
Method #1:
    `if __name__ == "__main__": app.run()`
    - Add the above piece of code to the bottom of app.py
    - python app.py (can directly run using python instead of flask run command & does not support app.run(debug=True) in new versions)
Method #2:
    - SET FLASK_APP = <filename.py> (by default app.py)
    - SET FLASK_DEBUG = 1 (To enable debugging in dev environment)
    - flask run

- The method for running a flask app in production is completely different.

#### different ways to send json data as response
    - jsonify(name="Mano", location="HYD", profile="DSE")
    - jsonify({"name":"Mano", "location":"HYD", "profile":"DSE"})
    - final output: 
        `{
            "name": "Mano",
            "location": "HYD",
            "profile": "DSE",
        }`
#### different ways to get request data 
- Query String  = request.args.get[<key>]
- form data = request.form[<key>]
- json data = request.get_json()['<key>'] 
- to know request method = request.method

#### multiple ways of enabling debugging in flask run
- SET FLASK_DEBUG=1 & flask run
- app.run(debug=True) & python app.py
- app.config['DEBUG'] = True & python app.py
- enabling debug mode provides a interactive shell kind of thing in browser in case of error for better debugging

#### how to save & retrieve data in sessions
 - prerequisites: define a secret session key using `app.config['SECRET_KEY] = 'SomeRandomKey'`
 - import session from flask `from flask import session`
 - save data = session['key']
 - fetch data = session['key]
 - remove key from session = session.pop(<key>,None)

##### ways to access content in html
- `{{ value }}` -> used for accessing a value for dynamic generation of html
- `{% text %} {% end text %}` -> used for implementing programing logic inside html using jinja
- `{% if <condition> %} {% else %} {% endif %}` & `{% for <condition> %} {% endfor %}`

#### template inheritance & include
- `{% block <blockname> %} {% endblock %}` -> to create a block in base template
- `{% extends 'base.html' %}` -> include base template in other files
- `{{ super() }}` -> use this special function to avoid overwriting of base template block contents
- `{{ url_for('static', filename='<absolute path of files form  static folder>') }}` -> to access files inside a html file
- `{% include '<filename.html>' %}` -> will include filename.html to a template, but default included file will have access to parent dynamic content & can be accessed by `{{ key }}`

- `g` is a global object in flask, which allows us to store data which is accessible to all parts of application when app is running.
- `@app.teardown_appcontext` is automatically called whenever a route returns, will be used to close db connection.
- `hasattr()` method can be used to check if a key exists in a dict or not
- `sql.connect(<path to db>)` -> to connect to sqlite db
- `sql.row_factory = sqlite3.Row`  -> to convert response from a tuple to a dict
- `db = get_db() -> cur = db.execute(<sql statement>) -> cur.fetchall()` -> steps to read data form sql
- `db = get_db() -> db.execute(<sql statement>) -> db.commit()` -> steps to write data to sql
- `db.execute('insert into users (name, location) values (?, ?)', ['Geek','USA'])` -> to prevent sql injection.
- `cur.fetchall()` fetches all records whereas `fetchone()` fetches only one record.
- `cur.fetchall()` -> returns a list of dictionaries
- `cur.fetchone()` -> returns a single dictionary

#### deploy app on amazon lightsail
- its a service for virtual servers, upload code to server and access it using ip address of server.
- other alternatives are python anywhere and heroku (easier & beginner friendly)
- `os -> ubuntu -> sudo apt-get update -> sudo apt-get install nginx`
- start nginx: `sudo /etc/init.d/nginx start`
- remove default configuration: `sudo rm /etc/nginx/sites-enabled/default`
- create a new file with flask settings: `sudo touch /etc/nginx/sites-available/flask_settings`
- create a link between files: `sudo ln -s /etc/nginx/sites-available/flask_settings /etc/nginx/sites-enabled/flask_settings`
- open the file: `sudo vi /etc/nginx/sites-enabled/flask_settings`
```
server {
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```
- proxy_pass handles/redirects the incoming https requests to application server
- nginx is a proxy server, it handles http requests
- gunicorn is a application server, similar to flask development server.
- restart the nginx service : `sudo /etc/init.d/nginx restart`
- `which python` : to check which  version of python (2/3) is installed.
- `sudo apt-get install python3-pip` : to instal pip
- `sudo pip3 install virtualenv` : to install virtualenv
- `virtualenv <env name>` :to create a new env
- `source <env name>/bin/activate` : to activate the environment
- `python -V | python --version` : to check the version of python
- `pip3 install flask gunicorn` : to install flask and gunicorn application server
- no need of `app.run()`, gunicorn will take care of this
- `gunicorn app:app` : to start the server (`gunicorn <filename>:<app name>`)
- `which git` : to check if git is installed or not, if installed where it's installed

# security in flask
- `werkzeug.security` module provides security related methods in flask
- `generate_password_hash` is used to generate a password hash.
- `check_password_hash` is used to check the password hash.
- we can import these two methods from `from werkzeug.security import generate_password_hash, check_password_hash`
- `password = generate_password_hash(<original password>, method=<hashing technique like sha256>)`
- `check_password_hash(<hashed_pwd>,<actual_pwd>)` : returns true if both passwords match else returns false

# generating session key in flask application
```
import os
app.config['SECRET_KEY'] = os.urandom(24)
```