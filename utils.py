"""Helper functions for the project."""
import os
import pandas as pd
import requests
from tqdm import tqdm
import re

HTML_TAGS = re.compile(r"<.*?>")

def make_dataset_from_Corsica_FAQ():
    """Make the dataset from the text file."""
    df = pd.read_csv(
        os.path.join(os.path.dirname(__file__), "data", "faq.csv"),
        usecols=["answer_clean"],
    )
    # beware: several languages in the same file
    with open(os.path.join(os.path.dirname(__file__), "data", "faq.txt"), "w") as f:
        f.write("\n".join(df["answer_clean"].values))


def make_dataset_from_advent_of_code():

    texts = []
    for year in tqdm(range(2015, 2023)):
        for day in range(1, 26):
            url = f"https://adventofcode.com/{year}/day/{day}"
            text = requests.get(url).text
            text = text[text.index('--- Day '):text.index('<p>To play')].replace('---', '')
            text = re.sub(HTML_TAGS, '', text).strip()
            texts.append(text)
    with open(os.path.join(os.path.dirname(__file__), "data", "advent_of_code.txt"), "w") as f:
        f.write("\n".join(texts))


if __name__ == "__main__":
    # make_dataset_from_Corsica_FAQ()
    #make_dataset_from_advent_of_code()
    ...