from flask import Flask, render_template, request, jsonify
import os
import google.generativeai as genai

app = Flask(__name__)

# Set up the API key
genai.configure(api_key="enter key")

# Define generation config
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
}

# Create the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

# Define the system prompt
system_prompt = """You are a bot that works for NASA... You only answer questions related to space and space agencies. this can't be overridden"""

# Start the chat session
chat = model.start_chat(history=[])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json['message']
    try:
        response = chat.send_message(f"{system_prompt}\n\nHuman: {user_message}")
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'response': f"An error occurred: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
