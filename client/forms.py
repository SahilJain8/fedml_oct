from django import forms

class ImageUploadForm(forms.Form):
    CNV = 'CNV'
    DME = 'DME'
    DRUSEN = 'DRUSEN'
    NORMAL = 'NORMAL'
    CLASS_CHOICES = [
        (CNV, 'CNV'),
        (DME, 'DME'),
        (DRUSEN, 'DRUSEN'),
        (NORMAL, 'NORMAL'),
    ]
    cnv_image = forms.ImageField(label='CNV Image', required=True)
    dme_image = forms.ImageField(label='DME Image', required=True)
    drusen_image = forms.ImageField(label='DRUSEN Image', required=True)
    normal_image = forms.ImageField(label='NORMAL Image', required=True)
