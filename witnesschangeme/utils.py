import string, random

def append_random_characters(base_str, length=6):
    # Define the characters to choose from (letters and digits)
    characters = string.ascii_letters + string.digits

    # Generate random characters
    random_suffix = ''.join(random.choices(characters, k=length))

    # Append the random characters to the base string
    return base_str + random_suffix