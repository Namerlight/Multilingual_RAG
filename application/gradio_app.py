import gradio as gr
import requests

API_URL = "http://127.0.0.1:8000/process"

def call_api(user_input):
    response = requests.post(API_URL, json={"text": user_input})
    if response.status_code == 200:
        return response.json()["processed_text"]
    else:
        return "Error calling API"

# Gradio Interface
demo = gr.Interface(
    fn=call_api,
    inputs=gr.Textbox(label="Please enter the question you wish to ask."),
    outputs=gr.Textbox(label="Answer"),
    title="10MS_RAG"
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=3000)