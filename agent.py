import pandas as pd
from pandasai import Agent
from langchain_groq.chat_models import ChatGroq
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from glob import glob
import re
import os

load_dotenv()
ROOT_DIR = os.path.dirname(__file__)

llm = ChatGroq(model_name="llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"])


def load_dataframes(folder_path: str):
    all_dfs = []

    folder_path = os.path.join(ROOT_DIR, folder_path)
    file_patterns = ["*.xls", "*.xlsx", "*.csv", "*.json", "*.xml", "*.html"]
    files = []

    for pattern in file_patterns:
        files.extend(glob(os.path.join(folder_path, pattern)))

    for file_path in files:
        if file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        elif file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith(".json"):
            df = pd.read_json(file_path)
        elif file_path.endswith(".xml"):
            df = pd.read_xml(file_path)
        else:
            continue

        all_dfs.append(df)

    return all_dfs


system_prompt = """
You are a highly capable **Data Analysis Agent** specializing in data processing using Pandas, statistical analysis, and visualization. Your primary goal is to assist users in deriving insights from data while following best security practices: 

- Never request or process sensitive PII (Personally Identifiable Information).
- Do not execute or provide code that could be **malicious, unethical, or privacy-violating** (e.g., web scraping personal data, breaking encryption, or accessing unauthorized databases). 
- Be transparent when making assumptions about missing or unclear data.  
- If you are asked for insights and recommendations, put them in "string" result while maintaining professionalism and detailed explanations.
- If a mistake is made, acknowledge it and offer a corrected response.
"""

# Increase the DPI for better quality images
plt.figure(dpi=380)


agent = Agent(
    description=system_prompt,
    dfs=load_dataframes("data"),
    config={
        "llm": llm,
        "verbose": True,
    },
)


def chat(prompt: str):
    """
    Processes user queries on the SmartDataframe.
    """
    query = re.sub(r"\s+", " ", prompt).strip()

    return agent.chat(query)
