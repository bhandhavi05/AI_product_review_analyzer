import re


def detect_fake_review(review_text):

    text = review_text.lower()

    spam_keywords = [
        "buy now",
        "limited offer",
        "click here",
        "best product ever",
        "100% genuine",
        "guaranteed"
    ]

    for keyword in spam_keywords:
        if keyword in text:
            return True

    words = text.split()

    if len(words) < 3:
        return True

    unique_ratio = len(set(words)) / len(words)

    if unique_ratio < 0.5:
        return True

    if re.search(r'(.)\1{4,}', text):
        return True

    return False