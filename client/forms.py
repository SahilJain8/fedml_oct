from django import forms

class MultiCategoryImageForm(forms.Form):
    CATEGORY_CHOICES = [
        ('CNV', 'CNV'),
        ('DME', 'DME'),
        ('DRUSEN', 'DRUSEN'),
        ('NORMAL', 'NORMAL')
    ]
    
    CNV_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    DME_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    DRUSEN_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    NORMAL_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    
    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        category_images = cleaned_data.get(f'{category}_images')
        if not category_images:
            raise forms.ValidationError(f'Please upload at least one image for category {category}.')
