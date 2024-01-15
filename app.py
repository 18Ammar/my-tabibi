from flask import Flask

app = Flask(__name__)     

@app.route('/')
def login():
    return "this is a login page"


if __name__ == '__main__':
    app.run(debug=True)
    