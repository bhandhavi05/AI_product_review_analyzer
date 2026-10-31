<<<<<<< HEAD
# AI Product Review Analyzer

A Django web application for analyzing product reviews, detecting suspicious reviews, generating reviews automatically, and comparing products based on customer feedback.

The app supports both manual review entry and automatic review generation. It can use the Gemini API when available, and it also includes a local fallback generator so review generation still works when the API is unavailable.

## Features

- Product listing and search
- Product detail pages
- Manual customer review submission
- Automatic review generation
- Optional Gemini API review generation
- Local API-free review generation fallback
- Sentiment analysis for reviews
- Fake review detection
- Review analytics dashboard
- Sentiment distribution chart
- Product comparison dashboard
- AI-style recommendation score
- Red and black themed UI

## Tech Stack

- Python
- Django 5.2
- SQLite
- HTML
- CSS
- Bootstrap 5
- Chart.js
- TextBlob
- Gemini REST API
- Django Templates

## Main Modules

- `reviews/models.py`  
  Defines `Product`, `Review`, and `MonthlyReport` models.

- `reviews/views.py`  
  Handles product listing, product details, manual review saving, generated review saving, analytics, and comparison.

- `reviews/ai.py`  
  Uses TextBlob to classify reviews as `Positive`, `Negative`, or `Neutral`.

- `reviews/fake_review.py`  
  Detects suspicious reviews using spam keywords, repeated characters, short text, and repeated-word patterns.

- `reviews/review_generator.py`  
  Generates reviews using Gemini API first, with a local fallback generator when the API fails or is unavailable.

- `reviews/templates/`  
  Contains the HTML templates for home, products, product detail, and comparison pages.

- `static/css/style.css`  
  Main red and black website theme.

## Setup Instructions

1. Clone or open the project folder.

```bash
cd AI_Product_Review_Analyzer
```

2. Create and activate a virtual environment.

```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies.

```bash
pip install django textblob
```

4. Run migrations.

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Start the development server.

```bash
python manage.py runserver
```

6. Open the app in your browser.

```text
http://127.0.0.1:8000/
```

## Gemini API Key Setup

The project can generate reviews without an API key using the local fallback generator. If you want Gemini-powered review generation, create this file:

```text
reviews/local_config.py
```

Add your Gemini API key:

```python
GEMINI_API_KEY = "your-gemini-api-key"
```

Do not commit `reviews/local_config.py`. It is ignored in `.gitignore`.

## How Review Generation Works

On a product detail page:

1. Choose the number of reviews.
2. Choose the target rating from 1 to 5.
3. Click `Generate AI Reviews`.

The app will:

- Try to generate reviews using Gemini.
- If Gemini is unavailable, generate reviews locally.
- Save generated reviews into the database.
- Run sentiment analysis.
- Run fake review detection.
- Include generated reviews in analytics and comparison.

## Product Comparison Logic

The comparison page compares two products using:

- Average rating
- Positive review percentage
- Negative review percentage
- Neutral review percentage
- Fake review count
- Total reviews

The recommendation score is calculated from rating, sentiment percentages, and fake-review penalty.

## Routes

| Page | URL |
| --- | --- |
| Home | `/` |
| Products | `/products/` |
| Product Detail | `/product/<product_id>/` |
| Generate Reviews | `/product/<product_id>/generate-reviews/` |
| Compare Products | `/compare/` |

## Project Structure

```text
AI_Product_Review_Analyzer/
  manage.py
  db.sqlite3
  reviewanalyzer/
    settings.py
    urls.py
  reviews/
    models.py
    views.py
    forms.py
    ai.py
    fake_review.py
    review_generator.py
    local_config.py.example
    templates/
      base.html
      home.html
      products.html
      product_detail.html
      compare.html
    static/
      css/
        style.css
  static/
    css/
      style.css
```

## Verification Commands

Run these commands to check the project:

```bash
python -m py_compile reviews/review_generator.py reviews/views.py reviews/urls.py
python manage.py check
```

Expected result:

```text
System check identified no issues.
```

## Notes

- This project is currently configured for development with `DEBUG = True`.
- SQLite is used as the default database.
- The UI theme is red and black.
- Bootstrap and Chart.js are loaded through CDN links.
- Gemini API errors such as `503 UNAVAILABLE` are handled by falling back to local review generation.

=======
# AI_product_review_analyzer
>>>>>>> af22593e56c9240f2eba693cf4b252a39d22bb5c
