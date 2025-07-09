from services.chat_interface import chat
import gradio as gr

if __name__ == "__main__":
    gr.ChatInterface(chat,type='messages').launch()