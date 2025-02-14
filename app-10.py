import requests
import json
import gradio as gr

# Backend
URL = "http://localhost:11434/api/generate"
HEADERS = {"Content-Type": "application/json"}

def generate_response(prompt, history=[]):
    """
    Handles user input, sends it to the API, and returns updated chat history.
    """
    history.append((prompt, ""))  # Append user message with empty bot response

    final_prompt = "\n".join([msg[0] for msg in history])  # Use only user inputs

    data = {
        "prompt": final_prompt,
        "model": "CodeGuru",
        "stream": False
    }

    try:
        response = requests.post(url=URL, headers=HEADERS, json=data)
        response.raise_for_status()  # Raises HTTPError for bad responses

        actual_response = response.json().get("response", "No response received.")

        history[-1] = (history[-1][0], actual_response)  # Update latest tuple with bot response
        return history

    except requests.exceptions.RequestException as e:
        history[-1] = (history[-1][0], f"❌ Error: {str(e)}")
        return history

# Custom CSS for better colors & visibility
custom_css = """
#chatbox {
    background-color: #1e1e2e;
    border-radius: 10px;
    padding: 15px;
    color: white;
    font-size: 16px;
}
.gradio-container {
    background-color: #121212;
}
.user {
    background-color: #0078D7;
    color: white;
    border-radius: 15px;
    padding: 10px;
}
.assistant {
    background-color: #3A3B3C;
    color: white;
    border-radius: 15px;
    padding: 10px;
}
#submit-button {
    background-color: #ff9800;
    color: white;
    font-weight: bold;
    border-radius: 8px;
}
"""

# Frontend
with gr.Blocks(css=custom_css) as interface:
    gr.Markdown("<h1 style='color:#FF9800'>🤖 CodeGuru - Your AI Coding Assistant</h1>")
    gr.Markdown("<p style='color:white;'>🚀 Get expert coding help instantly. Ask CodeGuru anything!</p>")

    chatbot = gr.Chatbot(label="CodeGuru", elem_id="chatbox", height=400)
    input_box = gr.Textbox(placeholder="Ask your coding question here...", lines=2)
    submit_btn = gr.Button("Send ✨", elem_id="submit-button")

    def chat_logic(user_input, chat_history):
        return generate_response(user_input, chat_history)

    submit_btn.click(chat_logic, inputs=[input_box, chatbot], outputs=chatbot)

interface.launch()
