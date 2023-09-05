from flask import Flask, render_template, request
import random
import re

app = Flask(__name__)

# Initialize an empty list to store chat messages
chat_history = []

# Function to add a message to the chat history
def add_message(sender, text):
    chat_history.append({'sender': sender, 'text': text})

def calculate(operation, *numbers):
    try:
        # Convert input numbers to floats
        num_list = [float(num) for num in numbers]

        if operation == "add":
            result = sum(num_list)
        elif operation == "minus":
            result = num_list[0] - sum(num_list[1:])
        elif operation == "multiply":
            result = 1
            for num in num_list:
                result *= num
        elif operation == "divide":
            if 0 in num_list[1:]:
                return "Simple Chatbot: Error: Division by zero"
            result = num_list[0]
            for num in num_list[1:]:
                result /= num
        else:
            return "Simple Chatbot: Error: Invalid operation"

        return f"Simple Chatbot: Result: {result:.2f}"

    except Exception as e:
        return f"Simple Chatbot: Error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html', messages=chat_history)

@app.route('/chat', methods=['POST'])
def simple_chatbot_web():
    user_input = request.form['user_input'].strip().lower()
    response = ""
    
    greetings = ["hello", "hi", "hey", "greetings"]
    responses = {
        "how are you": ["I'm good, thanks!", "I'm doing well.", "I'm just a computer program, but I'm here to help."],
        "what's your name": ["I'm a chatbot.", "I'm just a program, so I don't have a name."],
        "bye": ["Goodbye!", "See you later!", "Bye-bye!"],
        "help me with calculations": ["Please go ahead.", "Sure."]
    }

    if user_input == 'help me with calculations':
        response = "Simple Chatbot: Please go ahead." 

    if user_input == 'bye':
        response = "Simple Chatbot: Goodbye!"

    if any(word in user_input.split() for word in greetings):
        response = "Simple Chatbot: Hello! How can I assist you today?"

    if user_input in responses:
        response = "Simple Chatbot: " + random.choice(responses[user_input])

    if not response:
        # Check for mathematical keywords
        if "add" in user_input or "plus" in user_input:
            operation = "add"
        elif "minus" in user_input or "subtract" in user_input:
            operation = "minus"
        elif "multiply" in user_input or "times" in user_input:
            operation = "multiply"
        elif "divide" in user_input:
            operation = "divide"
        else:
            response = "Simple Chatbot: I'm not sure how to respond to that."

        # If a mathematical keyword is found, extract numbers
        if operation:
            numbers = re.findall(r"([-+]?\d*\.\d+|\d+)", user_input)
            if len(numbers) >= 2:
                response = calculate(operation, *numbers)
            else:
                response = "Simple Chatbot: Error: Please provide two or more numbers."
    
    # Add the user's message to the chat history
    add_message('user', user_input)

    # Add the chatbot's response to the chat history
    add_message('chatbot', response)

    return render_template('index.html', messages=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
