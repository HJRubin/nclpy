"""Main module for the utils package."""
import random
import string

def random_string(string_length=3, use_seed=False):    
    """Generates a random string of fixed length.
    Args:
        string_length(int, optional)" Fixed length. Defaults to 3.
    Returns:
        str: A random string.
    """    
    if use_seed:
        random.seed(1001)
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))