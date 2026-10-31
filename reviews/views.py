from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ReviewForm
from .ai import predict_sentiment
from .fake_review import detect_fake_review
from .review_generator import generate_review
import random
from django.contrib import messages
# Home Page
def home(request):
    return render(request, 'home.html')
# Products Page
def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()
    if query:
        products = products.filter(name__icontains=query)
    return render(
        request,
        'products.html',
        {
            'products': products
        }
    )
# Product Detail Page
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review_text = form.cleaned_data['review_text']
            # Sentiment Analysis
            review.sentiment = predict_sentiment(
                review_text
            )
            # Fake Review Detection
            review.is_fake = detect_fake_review(
                review_text
            )
            review.save()
            return redirect(
                'product_detail',
                product_id=product.id
            )
    else:
        form = ReviewForm()
    # Analytics Data
    positive_count = reviews.filter(
        sentiment='Positive'
    ).count()
    negative_count = reviews.filter(
        sentiment='Negative'
    ).count()
    neutral_count = reviews.filter(
        sentiment='Neutral'
    ).count()
    fake_count = reviews.filter(
        is_fake=True
    ).count()
    total_reviews = reviews.count()
    return render(
        request,
        'product_detail.html',
        {
            'product': product,
            'form': form,
            'reviews': reviews,

            # Analytics
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'fake_count': fake_count,
            'total_reviews': total_reviews,
        }
    )
def generate_ai_reviews(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if request.method != "POST":
        return redirect(
            'product_detail',
            product_id=product.id
        )

    try:
        review_count = int(
            request.POST.get('review_count', 3)
        )

        review_count = max(
            1,
            min(10, review_count)
        )

        target_rating = int(
            request.POST.get('target_rating', 4)
        )

        target_rating = max(
            1,
            min(5, target_rating)
        )

        used_local_generator = False

        for _ in range(review_count):
            try:
                generated_review = generate_review(
                    product.name,
                    product.category,
                    rating=target_rating
                )
            except Exception:
                generated_review = generate_review(
                    product.name,
                    product.category,
                    rating=target_rating,
                    use_api=False
                )

                used_local_generator = True

            review_text = generated_review['review_text']

            Review.objects.create(
                product=product,
                username=f"AI Customer {random.randint(1000, 9999)}",
                review_text=review_text,
                rating=target_rating,
                sentiment=predict_sentiment(
                    review_text
                ),
                is_fake=detect_fake_review(
                    review_text
                )
            )

        if used_local_generator:
            messages.warning(
                request,
                (
                    f"{review_count} review(s) generated locally because "
                    "the AI API was unavailable."
                )
            )
        else:
            messages.success(
                request,
                f"{review_count} AI review(s) generated successfully."
            )

    except Exception as error:
        messages.error(
            request,
            f"Could not generate AI reviews: {error}"
        )

    return redirect(
        'product_detail',
        product_id=product.id
    )


# Compare Products
def compare_products(request):

    products = Product.objects.all()

    product1_id = request.GET.get('product1')
    product2_id = request.GET.get('product2')

    product1 = None
    product2 = None

    p1_data = None
    p2_data = None

    winner = None
    reason = None
    recommendation_score = None

    if product1_id and product2_id:

        product1 = get_object_or_404(
            Product,
            id=product1_id
        )

        product2 = get_object_or_404(
            Product,
            id=product2_id
        )

        def analyze(product):

            reviews = Review.objects.filter(
                product=product
            )

            total = reviews.count()

            if total == 0:
                return {
                    'rating': 0,
                    'positive': 0,
                    'negative': 0,
                    'neutral': 0,
                    'total_reviews': 0,
                    'fake_reviews': 0
                }

            positive = reviews.filter(
                sentiment='Positive'
            ).count()

            negative = reviews.filter(
                sentiment='Negative'
            ).count()

            neutral = reviews.filter(
                sentiment='Neutral'
            ).count()

            fake_reviews = reviews.filter(
                is_fake=True
            ).count()

            avg_rating = (
                sum(review.rating for review in reviews)
                / total
            )

            return {
                'rating': round(avg_rating, 2),
                'positive': round(
                    (positive / total) * 100,
                    2
                ),
                'negative': round(
                    (negative / total) * 100,
                    2
                ),
                'neutral': round(
                    (neutral / total) * 100,
                    2
                ),
                'fake_reviews': fake_reviews,
                'total_reviews': total
            }

        p1_data = analyze(product1)
        p2_data = analyze(product2)

        # AI Recommendation Score
        score1 = (
            (p1_data['rating'] * 20)
            + p1_data['positive']
            - p1_data['negative']
            - (p1_data['fake_reviews'] * 5)
        )

        score2 = (
            (p2_data['rating'] * 20)
            + p2_data['positive']
            - p2_data['negative']
            - (p2_data['fake_reviews'] * 5)
        )

        reasons = []

        if score1 > score2:

            winner = product1

            recommendation_score = round(
                score1,
                2
            )

            if p1_data['rating'] > p2_data['rating']:
                reasons.append(
                    "Higher average rating"
                )

            if p1_data['positive'] > p2_data['positive']:
                reasons.append(
                    "More positive reviews"
                )

            if p1_data['negative'] < p2_data['negative']:
                reasons.append(
                    "Fewer negative reviews"
                )

            if p1_data['fake_reviews'] < p2_data['fake_reviews']:
                reasons.append(
                    "Fewer suspicious reviews"
                )

        elif score2 > score1:

            winner = product2

            recommendation_score = round(
                score2,
                2
            )

            if p2_data['rating'] > p1_data['rating']:
                reasons.append(
                    "Higher average rating"
                )

            if p2_data['positive'] > p1_data['positive']:
                reasons.append(
                    "More positive reviews"
                )

            if p2_data['negative'] < p1_data['negative']:
                reasons.append(
                    "Fewer negative reviews"
                )

            if p2_data['fake_reviews'] < p1_data['fake_reviews']:
                reasons.append(
                    "Fewer suspicious reviews"
                )

        else:

            reason = (
                "Both products performed equally."
            )

        if reasons:
            reason = ", ".join(reasons)

    return render(
        request,
        'compare.html',
        {
            'products': products,
            'product1': product1,
            'product2': product2,
            'p1_data': p1_data,
            'p2_data': p2_data,
            'winner': winner,
            'reason': reason,
            'recommendation_score': recommendation_score
        }
    )
