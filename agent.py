import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv
import re
import os

load_dotenv()

llm = ChatGroq(model_name="llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"])

df = pd.read_excel("example/data.xlsx")
sdf = SmartDataframe(df, config={"llm": llm})


def chat(prompt: str):
    """Processes user queries on the SmartDataframe."""

    query = re.sub(r"\s+", " ", prompt).strip()

    return sdf.chat(query)
