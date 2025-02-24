import os
import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(model_name="llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"])
