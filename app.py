from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/email')
def email():
    return ''


@app.route('/password')
def password():
    return ''


if __name__ == '__main__':
    app.run()
