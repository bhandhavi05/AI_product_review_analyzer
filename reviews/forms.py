from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review

        fields = [
            'username',
            'rating',
            'review_text'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'rating': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': 1,
                    'max': 5
                }
            ),

            'review_text': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4
                }
            )
        }