from flask import Blueprint,render_template,request,jsonify,flash,url_for
# from transformers import GPT2LMHeadModel, GPT2Tokenizer, GPT2Config
import pandas as pd
from flask_login import login_required, logout_user, current_user
from appModule.appdb import Contact,User,db,Message,Room
from flask_socketio import SocketIO,join_room,rooms
# import torch


chat_ai = Blueprint('chat',__name__)

# model_name = "./gpt2-fine-tuned"
# model = GPT2LMHeadModel.from_pretrained(model_name)
# tokenizer = GPT2Tokenizer.from_pretrained(model_name)

socket = SocketIO()





# def generate_answer(prompt, model, tokenizer):
#     input_ids = tokenizer.encode(prompt, return_tensors="pt")
#     attention_mask = torch.ones_like(input_ids)  # Creating attention mask tensor
    
#     # Setting pad_token_id to eos_token_id
#     pad_token_id = tokenizer.eos_token_id
    
#     # Retrieving task-specific parameters
#     task_specific_params = model.config.task_specific_params.get("text-generation", {})
#     do_sample = task_specific_params.get("do_sample", False)
#     max_length = task_specific_params.get("max_length", 50)
    
#     output = model.generate(input_ids, attention_mask=attention_mask, max_length=max_length,
#                             num_return_sequences=1,
#                             no_repeat_ngram_size=2,
#                             top_k=50,
#                             temperature=0.7 if do_sample else None,  # Setting temperature based on do_sample
#                             pad_token_id=pad_token_id,
#                             do_sample=do_sample)  # Passing do_sample parameter
    
#     generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
#     return generated_text








@chat_ai.route('/chat-ai', methods=['GET', 'POST'])
@login_required
def chat():
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return render_template('chat_ai.html', contacts=contacts)

random_words = ["Hello how can i help you ?", "how old are you ?", "Hi"]



@chat_ai.route('/send_message', methods=['POST'])
def send_message():
    message_text = request.form.get('message-input') 
    if message_text:
        ai_response = f"{random.choice(random_words)}!"
        return jsonify({ 'ai_response': ai_response})
    
    return jsonify({'error': 'Message is empty'}), 400

@chat_ai.route('/chat-ai/<user_id>',methods=['GET', 'POST'])
@login_required
def contact(user_id):
    exist_contact = Contact.query.filter(Contact.user_id == current_user.id, Contact.contact_id == user_id).first()
    if exist_contact:
        flash("this user is already in contact list")
    else:
        contact = Contact()
        contact.user_id = current_user.id
        contact.contact_id = user_id
        db.session.add(contact)
        db.session.commit()


    return render_template('chat_ai.html')



@socket.on("new_message")
def chatting(data):
    message = data.get("message")
    sender_id = current_user.id
    receiver_name = data.get("reciver")
    receiver = User.query.filter_by(username=receiver_name).first()

    if message and receiver:
        room_name = '_'.join(sorted([receiver_name, current_user.username]))
        room = Room.query.filter_by(name=room_name).first()
        
        if not room:
            room = Room(name=room_name)
            db.session.add(room)
            db.session.commit()
        new_msg = Message(sender_id=sender_id, receiver_id=receiver.id, content=message, room=room)
        db.session.add(new_msg)
        db.session.commit()

        join_room(room_name)

        socket.emit('new_message', {'message': message, 'sender': current_user.username, "user_image": url_for('static', filename=current_user.image_file)}, room=room_name)

        return jsonify({"success": message})
    return jsonify({"error": "Message is empty or receiver does not exist"}), 400


@chat_ai.route('/get_messages', methods=['POST'])
def get_messages():
    reciver = request.form.get('reciver')
    sender = current_user.username
    room_name = "_".join(sorted([reciver,sender]))
    room = Room.query.filter_by(name=room_name).first()
    messages = Message.query.filter_by(room_id=room.id).all()
    serilized_msg = []
    if messages:
        for message in messages:
            json_msg = {
                "message": message.content,
                "sender": message.sender.username,
                "image":url_for('static', filename=message.sender.image_file)
            }
            serilized_msg.append(json_msg)

        return jsonify({"message":serilized_msg}),200

    return jsonify({'error': 'Message is empty'}), 400

online_users = set()

@socket.on("connect")
def connection():
    online_users.add(request.sid)
    socket.emit("user_status", { "status": "online"})

@socket.on("disconnect")
def disconnection():
    online_users.remove(request.sid)
    socket.emit("user_status", { "status": "offline"})

