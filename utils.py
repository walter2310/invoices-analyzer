import fitz
from dotenv import load_dotenv
import openai
import pandas as pd
import os
from prompt import prompt
from io import StringIO

load_dotenv(".env")
OPENAI_KEY = os.getenv("OPENAI_KEY")
MODEL="gpt-4o-mini"


def extract_pdf_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text


def send_content_to_model(content):
    client = openai.OpenAI(api_key=OPENAI_KEY)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": 'system',
                "content": "You are an expert in invoice data extraction. Return only the CSV without any explanations or additional messages. If you cannot extract data, return exactly the word 'error' without quotes."
            },
            {
                "role": "user",
                "content": prompt + "\n This is the text to parse:\n" + content
            }
        ]
    )

    csv = response.choices[0].message.content.strip()
    return csv


def convert_csv_to_dataframe(csv):
    columns = {
        "invoice_date": str,
        "supplier": str,
        "description": str,
        "amount": str,
        "currency": str
    }

    df = pd.read_csv(StringIO(csv), delimiter=";", dtype=columns)
    df["amount"] = pd.to_numeric(
        df["amount"].str.replace(",", "."), errors='coerce'
    )

    return df
