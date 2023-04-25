from django import forms

class UploadForm(forms.Form):
    images_1 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    images_2 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    images_3 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    images_4 = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
