from flask import Flask
app = Flask(__name__)
app.debug = True

app.secret_key = 'your_secret_key_here'

