"""The following link contains a precious notebook that I used to learn how to build a relatively simple,
pure Python, language model that predicts the next character in a sequence of characters. I have modified the code
slightly to fit my needs, but the majority of the code is from the following link. I highly recommend checking it out:
https://colab.research.google.com/github/norvig/pytudes/blob/main/ipynb/Goldberg.ipynb"""

import logging
import random
from collections import Counter, defaultdict

from tqdm import tqdm

logging.basicConfig(level=logging.INFO)
PAD = "`"  # Character to pad the beginning of a text


class LanguageModel(defaultdict):
    """A mapping from `order` history characters to possible next characters and their
    frequency, e.g. {'spea': Counter({'k': 9, 'r': 1})} lets us generate 'speak' or 'spear'."""

    def __init__(self, order: int, filepath: str) -> None:
        super().__init__(Counter)
        self.order: int = order
        self.filepath: str = filepath
        self.train()

    @classmethod
    def create_model(cls, order: int, filepath: str) -> "LanguageModel":
        """Create a new LanguageModel object."""
        return cls(order=order, filepath=filepath)

    def train(self) -> None:
        """Train a character-level language model of given order on all the text in `fname`.
        Stores a trained model, i.e. a dict that maps histories to Counter objects

        Args:
            filepath (str): the path to the data file used for training
            order (int, optional): the length of the text sequence history. Defaults to 4.
        """
        logging.info(f"Training a {self.order}-gram model.")
        logging.info("Instantiating a LanguageModel object...")
        logging.info("Opening the dataset file...")
        try:
            with open(self.filepath) as f:
                data = (self.order * PAD) + f.read()
        except FileNotFoundError as exc:
            print(f"File '{self.filepath}' not found. Model cannot be trained.")
            raise SystemExit from exc
        logging.info("Training the model...")
        for i in tqdm(range(self.order, len(data))):
            history, char = data[i - self.order : i], data[i]
            self[history][char] += 1
        logging.info("Computing total counts...")
        for counter in tqdm(self.values()):
            counter.total = sum(
                counter.values()
            )  # Cache total counts (for sample_character)
        logging.info("Training complete.")

    def sample_character(self, counter: Counter, random_: bool = False) -> str:
        """Randomly sample a character from the `counter`.
        Recoded by Clem, but it does the same thing as the original function

        Args:
            counter (Counter): a Counter object
            random_ (bool, optional): whether to pick the character regardless of likelihood or in the top 3 most likely. Defaults to False.

        Returns:
            str: the sampled character
        """
        return (
            random.choice(list(counter))
            if random_
            else random.choice(counter.most_common(3))[0]
        )

    def generate_text(self, length: int = 5_000) -> None:
        """Sample a random `length`-long passage"""
        logging.info("Generating text...")
        history = self.order * PAD
        text = []
        for _ in range(length):
            c = self.sample_character(self[history])
            history = history[1:] + c
            text.append(c)
        print("".join(text))


if __name__ == "__main__":
    lm = LanguageModel(order=10, filepath="data/advent_of_code.txt")
    lm.generate_text()
