from django import forms

class MultipleImagesForm(forms.Form):
    cnv_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    drusen_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    normal_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    dmv_images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

