from django import forms

from django import forms

class UploadImagesForm(forms.Form):
    class1_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class2_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class3_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class4_images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
