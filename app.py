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
    # Add your login logic here
    return "Login logic goes here"

@app.route('/forgot_password')
def forgot_password():
    # Add your forgot password logic here
    return "Forgot password logic goes here"

@app.route('/auth_google')
def auth_google():
    # Add your Google authentication logic here
    return "Google authentication logic goes here"

@app.route('/signup')
def signup():
    # Add your sign-up logic here
    return "Sign-up logic goes here"

if __name__ == '__main__':
    app.run(debug=True)
