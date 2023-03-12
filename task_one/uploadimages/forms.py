from django import forms
from .models import Images
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('original_images',)

    def clean_original_images(self):
        image = self.cleaned_data.get('original_images')
        if not image:
            raise ValidationError(_('Please select an image.'), code='invalid')

        # Limit file size to 10 MB
        if image.size > 10 * 1024 * 1024:
            raise ValidationError(_('Image file size exceeds the limit of 10 MB.'), code='invalid')

        # Allow only PNG and JPG formats
        valid_extensions = ['.png', '.jpg']
        if not any(extension in str(image) for extension in valid_extensions):
            raise ValidationError(_('Invalid file format. Only PNG and JPG formats are allowed.'), code='invalid')

        return image


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class ThumbnailForm(forms.Form):
    width = forms.IntegerField(min_value=1, max_value=1000)
    height = forms.IntegerField(min_value=1, max_value=1000)


class ExpiringLinkForm(forms.Form):
    expiration_time = forms.IntegerField(
        label='Expiration time (in seconds)',
        min_value=300,
        max_value=30000,
        initial=3600,
        help_text='Links will expire after the specified time.'
    )
