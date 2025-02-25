import gradio as gr
import pandas as pd
from agent import chat
from typing import Literal, TypedDict


class Message(TypedDict):
    role: Literal["user", "assistant"]
    content: str


def chat_with_agent(query: str, history: list[Message] = []) -> str:
    """
    Function to handle chat interactions with the SmartDataframe.
    """
    try:
        # Execute the query on SmartDataframe
        result = chat(query)

        # TODO: Handle different result types
        if isinstance(result, pd.DataFrame):
            # For dataframe results
            # return history + [[query, result.to_html()]]
            return result.to_html()
        else:
            # For other results
            # return history + [[query, str(result)]]
            return str(result)

        # TODO: Save the history of the conversation

    except Exception as e:
        return f"An error occurred: {e}"


app = gr.ChatInterface(
    type="messages",
    fn=chat_with_agent,
    title="Data Analysis Agent",
    description="Ask questions about your data files!",
    chatbot=gr.Chatbot(height=500, type="messages"),
)

if __name__ == "__main__":
    app.launch()
