import pandas as pd
from pandasai import SmartDataframe
from langchain_groq.chat_models import ChatGroq
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from glob import glob
import re
import os

load_dotenv()
ROOT_DIR = os.path.dirname(__file__)

llm = ChatGroq(model_name="llama3-70b-8192", api_key=os.environ["GROQ_API_KEY"])


def load_dataframe(folder_path: str):
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

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()


df = load_dataframe("data")

# Increase the DPI for better quality images
plt.figure(dpi=380)

sdf = SmartDataframe(df, config={"llm": llm})


def chat(prompt: str):
    """
    Processes user queries on the SmartDataframe.
    """
    query = re.sub(r"\s+", " ", prompt).strip()

    return sdf.chat(query)
