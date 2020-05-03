from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={"placeholder": "Your title"})
    )  # Overriding a widget for a field

    class Meta:
        model = Product
        fields = [
            'title',
            'description',
            'price'
        ]

    def clean_title(self, *args, **kwargs):
        title = self.cleaned_data.get('title')
        if 'fuck' in title.lower():
            raise forms.ValidationError("This is not a valid title")
        else:
            return title
