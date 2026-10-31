from django.urls import path
from . import views

urlpatterns = [
    # Home Page
    path(
        '',
        views.home,
        name='home'
    ),

    # Products List
    path(
        'products/',
        views.product_list,
        name='products'
    ),
    # Product Detail
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    # Generate AI Reviews
    path(
        'product/<int:product_id>/generate-reviews/',
        views.generate_ai_reviews,
        name='generate_ai_reviews'
    ),

    # Product Comparison
    path(
        'compare/',
        views.compare_products,
        name='compare'
    ),
]
