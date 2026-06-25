import os
import pandas as pd
from pypdf import PdfReader


def load_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def load_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = []

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text.append(page_text)

    return "\n".join(text)


def load_csv(file_path: str) -> str:
    df = pd.read_csv(file_path)

    summary = []
    summary.append(f"Dataset shape: {df.shape}")
    summary.append(f"Columns: {list(df.columns)}")
    summary.append("\nFirst rows:")
    summary.append(df.head(10).to_string())

    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:
        summary.append("\nNumeric summary:")
        summary.append(df[numeric_cols].describe().to_string())

    return "\n".join(summary)


def load_document(file_path: str) -> str:
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".txt":
        return load_txt(file_path)

    if extension == ".pdf":
        return load_pdf(file_path)

    if extension == ".csv":
        return load_csv(file_path)

    raise ValueError(f"Unsupported file type: {extension}")