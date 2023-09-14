Thanks to Peter Norvig in Pytudes, I discovered this simple yet powerful way to develop a (not Large) Language Model in Pure Python
You can do it in a few tens of locs, and with no imports at all!

it's really fun and works decently well with a big enough dataset, although obviously it's far less sophisticated than LLMs
In my experience, a human can clearly recognize the style of the dataset (e.g. "this is Shakespeare" or "This looks like a new AoC puzzle") but the sentences are rarely grammatically 
perfect.

I used the whole Advent of Code corpus (gathering all part ones) to "train" the model


