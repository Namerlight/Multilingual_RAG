import gradio as gr
import requests


API_URL = "http://127.0.0.1:8005/rag_chat"


def call_api(user_input):
    response = requests.post(API_URL, json={"text": user_input})
    if response.status_code == 200:
        return response.json()["Answer"]
    else:
        return "Error calling API"


with gr.Blocks() as demo:
    gr.Markdown("# Multilingual RAG")

    with gr.Column():
        user_input = gr.Textbox(lines=4, label="Enter the question.")
        output = gr.Textbox(lines=6, label="Answer from book")
        submit_btn = gr.Button("Submit")
        submit_btn.click(fn=call_api, inputs=user_input, outputs=output)


if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=3005)