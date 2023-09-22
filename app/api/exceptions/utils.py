def add_missing_punctuation(message: str) -> str:
    if message and message[-1] not in ('.', '?', '!'):
        message += '.'
    return message
