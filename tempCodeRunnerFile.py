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

if __name__ == '__main__':
    app.run(debug=True)
