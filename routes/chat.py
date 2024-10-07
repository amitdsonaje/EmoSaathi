from flask import Blueprint, render_template, request, redirect, url_for, session
from config import Config
from groq import Groq

chat_bp = Blueprint('chat', __name__)
client = Groq(api_key=Config.GROQ_API_KEY)

class_options = {
    0: "angry",
    1: "disgust",
    2: "fear",
    3: "happy",
    4: "neutral",
    5: "sad",
    6: "surprise"
}

conversation_history = []

@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    global conversation_history
    
    # Retrieve the predicted class from the session
    selected_class = session.get('selected_class', 4)  
    
    if request.method == 'GET' and not conversation_history:
        # Initialize conversation with assistant's message based on detected emotion
        initial_prompt = f"The user is feeling {class_options[selected_class]}. Initiate a conversation with them. Your first message should be empathetic and encouraging, indirectly acknowledging their emotional state without explicitly mentioning it. It should be of only one line with greeting a quote maybe motiviating or overwhelming."
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": initial_prompt,
                }
            ],
            model="llama3-8b-8192",
        )
        
        initial_response = chat_completion.choices[0].message.content
        conversation_history = [{"role": "assistant", "content": initial_response}]
    
    elif request.method == 'POST':
        user_input = request.form.get('user_input')
        
        # Append the user's input to the conversation history
        conversation_history.append({
            "role": "user",
            "content": user_input,
        })
        
        # Prepare the messages for the API call
        api_messages = [
            {
                "role": "system",
                "content": f"Remember, the user is feeling {class_options[selected_class]}. Maintain an empathetic and supportive tone throughout the conversation."
            }
        ] + conversation_history
        
        # Generate the model's response based on the updated conversation history
        chat_completion = client.chat.completions.create(
            messages=api_messages,
            model="llama3-8b-8192",
        )
        
        # Get and display the model's response
        response = chat_completion.choices[0].message.content
        conversation_history.append({
            "role": "assistant",
            "content": response,
        })
        
        return redirect(url_for('chat.chat'))
    
    return render_template('chat.html', class_options=class_options, conversation_history=conversation_history)