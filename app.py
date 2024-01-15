from flask import Flask,render_template

app = Flask(__name__)     
@app.route('/')
@app.route('/home')
def home():
    title = "طبيبي - Home"
    return render_template('homepage.html',title=title)

@app.route('/sign-in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/login', methods=['POST'])
def login():
    return "Login logic goes here"

@app.route('/forgot_password')
def forgot_password():
    return "Forgot password logic goes here"

@app.route('/auth_google')
def auth_google():
    return "Google authentication logic goes here"

@app.route('/signup')
def signup():
    return render_template('sign_up.html')



if __name__ == '__main__':
    app.run(debug=True)
