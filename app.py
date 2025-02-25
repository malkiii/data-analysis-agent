import gradio as gr
import pandas as pd
from agent import chat


def chat_with_dataframe(query, history):
    """
    Function to handle chat interactions with the SmartDataframe.
    """
    try:
        # Execute the query on SmartDataframe
        result = chat(query)

        # Handle different result types
        if isinstance(result, pd.DataFrame):
            # For dataframe results
            # return history + [[query, result.to_html()]]
            return result.to_html()
        else:
            # For other results
            # return history + [[query, str(result)]]
            return str(result)

    except Exception as e:
        return f"An error occurred: {e}"


# Gradio Interface
iface = gr.ChatInterface(
    type="messages",
    fn=chat_with_dataframe,
    title="Chat with Your DataFrame",
    description="Ask questions about your data!",
    chatbot=gr.Chatbot(height=500, type="messages"),
)

if __name__ == "__main__":
    iface.launch()
