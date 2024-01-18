from flask import Blueprint,render_template,request,jsonify
import random
chat_ai = Blueprint('chat',__name__)
random_words = ["Hello how can i help you ?", "how old are you ?", "Hi"]

@chat_ai.route('/chat-ai',methods=['GET','POST'])
def chat():
   return render_template('chat_ai.html')

@chat_ai.route('/send_message', methods=['POST'])
def send_message():
    message_text = request.form.get('message-input') 
    if message_text:
        ai_response = f"{random.choice(random_words)}!"
        return jsonify({ 'ai_response': ai_response})
    
    return jsonify({'error': 'Message is empty'}), 400

