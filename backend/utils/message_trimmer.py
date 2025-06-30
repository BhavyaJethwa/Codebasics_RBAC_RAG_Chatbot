from math import floor

# Function to trim chat message history used in database.py
def trim_chat_history(chat_history):
    n = len(chat_history)
    if n == 0:
        return []

    # Calculate sizes
    k = max(1, floor(n * 0.2))  # At least 1 item per section

    # Indices for start, middle, and end
    first_k = chat_history[:k]
    
    # Middle 20% from the middle 60% section
    mid_start = n // 3
    mid_end = 2 * n // 3
    middle_section = chat_history[mid_start:mid_end]
    middle_k = middle_section[:k]

    # Last 20% of the whole list
    last_k = chat_history[-k:]

    # Combine results
    trimmed = first_k + middle_k + last_k
    return trimmed