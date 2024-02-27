from flask import Blueprint,render_template

per_to_per_chat = Blueprint('per_to_per',__name__)

@per_to_per_chat.route('/messenger', methods=['GET', 'POST'])
def conversion():
    return render_template('chat_per_to_per.html')