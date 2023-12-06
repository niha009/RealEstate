from django import forms
from .models import Property, Property_Address, Property_Image
 
 
class ListingUploadForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['property_title', 'property_description', 'property_type', 'property_neighborhood', 'property_price', 'property_price_range', 'property_feature_status']
        
class AddressUploadForm(forms.ModelForm):
    class Meta:
        model = Property_Address
        fields = ['property_address_street', 'property_address_city', 'property_address_zip', 'property_address_state']
        
  
# General multiple file input     
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

# General multiple file field
class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

# Image Upload Form consisting of multiple file field        
class ListingImagesUploadForm(forms.ModelForm):
    image = MultipleFileField()
    class Meta:
        model = Property_Image
        fields = ('image', )
    