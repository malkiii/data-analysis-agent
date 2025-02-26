import gradio as gr
import pandas as pd
from agent import chat
from base64 import b64encode
import os


def chat_with_agent(query: str, history):
    """
    Function to handle chat interactions with the SmartDataframe.
    """
    try:
        # Execute the query on SmartDataframe
        result = chat(query)

        # For dataframe results
        if isinstance(result, pd.DataFrame):
            return result.to_html()

        # For image results
        elif os.path.exists(str(result)):
            return f'<img src="{image_to_base64(result)}" alt="{result}" />'

        # For other results
        else:
            return str(result)

    except Exception as e:
        return f"CHAT_ERROR: {e}"


def image_to_base64(image_path):
    # Read the image file in binary mode
    with open(image_path, "rb") as img_file:
        base64_string = b64encode(img_file.read()).decode("utf-8")

    ext = os.path.splitext(image_path)[1].lower()
    mime_type = f"image/{ext[1:]}"

    return f"data:{mime_type};base64,{base64_string}"


app = gr.ChatInterface(
    type="messages",
    fn=chat_with_agent,
    chatbot=gr.Chatbot(height=500, type="messages"),
    css_paths=["public/styles.css"],
    stop_btn=True,
    editable=True,
    autoscroll=True,
    save_history=True,
    show_progress=False,
)

if __name__ == "__main__":
    app.launch()
