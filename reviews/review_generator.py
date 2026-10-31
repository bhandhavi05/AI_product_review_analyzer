import json
import os
import random
import urllib.error
import urllib.request

GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/"
    f"models/{GEMINI_MODEL}:generateContent"
)

POSITIVE_COMMENTS = [
    "The product feels reliable in daily use and matches what I expected.",
    "Setup was simple, and the overall experience has been smooth so far.",
    "The quality feels good for the price, especially compared with similar options.",
    "I liked the design, performance, and the way it handles regular use.",
    "It has been useful, practical, and easy to recommend for this category."
]

NEUTRAL_COMMENTS = [
    "The product works as expected, but there are a few areas that could improve.",
    "It does the main job properly, though the experience is not exceptional.",
    "The quality is acceptable for the price, but I expected slightly better polish.",
    "It is useful for basic needs, although some features feel limited.",
    "Overall it is decent, with both good points and minor drawbacks."
]

NEGATIVE_COMMENTS = [
    "The product did not perform as well as I expected for regular use.",
    "I noticed a few issues that made the experience less satisfying.",
    "The quality feels below expectations when compared with similar products.",
    "It works sometimes, but the overall value could be much better.",
    "I would only recommend it if the price is lower or the issues are fixed."
]

try:
    from .local_config import GEMINI_API_KEY
except ImportError:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def get_gemini_api_key():
    if not GEMINI_API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is not set. Add it in reviews/local_config.py."
        )

    return GEMINI_API_KEY


def generate_local_review(product_name, category, rating=None):
    if rating is None:
        rating = random.randint(3, 5)

    rating = max(
        1,
        min(5, int(rating))
    )

    if rating >= 4:
        comments = POSITIVE_COMMENTS
    elif rating == 3:
        comments = NEUTRAL_COMMENTS
    else:
        comments = NEGATIVE_COMMENTS

    opening = random.choice(
        [
            f"I used {product_name} for a few days in the {category} category.",
            f"After trying {product_name}, I have a clear opinion about it.",
            f"My experience with {product_name} has been based on normal daily use."
        ]
    )

    review_text = (
        f"{opening} {random.choice(comments)} "
        f"I would rate it {rating} out of 5 because the experience feels "
        "consistent with that score."
    )

    return {
        "review_text": review_text,
        "rating": rating
    }


def parse_generated_review(response_text):
    cleaned_text = response_text.strip()

    if cleaned_text.startswith("```"):
        cleaned_text = cleaned_text.strip("`")
        cleaned_text = cleaned_text.replace("json", "", 1).strip()

    try:
        data = json.loads(cleaned_text)
    except json.JSONDecodeError:
        return {
            "review_text": response_text.strip(),
            "rating": random.randint(3, 5)
        }

    try:
        rating = int(data.get("rating", random.randint(3, 5)))
    except (TypeError, ValueError):
        rating = random.randint(3, 5)

    return {
        "review_text": str(
            data.get("review_text", response_text)
        ).strip(),
        "rating": rating
    }


def generate_review(product_name, category, rating=None, use_api=True):

    if not use_api:
        return generate_local_review(
            product_name,
            category,
            rating
        )

    prompt = f"""
    Generate one realistic customer review for:

    Product: {product_name}
    Category: {category}

    Review length: 40-60 words.
    Return only valid JSON in this exact format:
    {{
        "review_text": "customer review here",
        "rating": 1
    }}

    The rating must be an integer from 1 to 5.
    """

    if rating:
        prompt += f"\nThe review rating should be {rating} out of 5."

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.8
        }
    }

    request = urllib.request.Request(
        GEMINI_API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": get_gemini_api_key()
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            response_data = json.loads(
                response.read().decode("utf-8")
            )
    except urllib.error.HTTPError as error:
        error_body = error.read().decode("utf-8")
        raise ValueError(
            f"Gemini API error {error.code}: {error_body}"
        ) from error

    response_text = response_data[
        "candidates"
    ][0]["content"]["parts"][0]["text"]

    generated_review = parse_generated_review(
        response_text
    )

    generated_review["rating"] = max(
        1,
        min(5, generated_review["rating"])
    )

    return generated_review
