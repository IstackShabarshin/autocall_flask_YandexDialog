#python3.5

from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = 'some key'

from autocall import views
