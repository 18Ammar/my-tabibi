from flask import Blueprint,render_template,request,jsonify
import random
chat_ai = Blueprint('chat',__name__)
random_words = ["Hello", "Howdy", "Greetings", "Salutations", "Hi", "Hola"]

@chat_ai.route('/chat-ai',methods=['GET','POST'])
def chat():
   return render_template('chat_ai.html')

@chat_ai.route('/send_message', methods=['POST'])
def send_message():
    message_text = request.form.get('message-input')  # Use the correct key 'message-input'
    if message_text:
        # Simulate AI response with a random word
        ai_response = f"{random.choice(random_words)}!"

        # Simulate processing time (you can remove this line)

        # User message
        user_message = f"<a href='user'>user</a>: {message_text}"
        print(ai_response)
        return jsonify({'user_message': user_message, 'ai_response': ai_response})
    
    return jsonify({'error': 'Message is empty'}), 400

