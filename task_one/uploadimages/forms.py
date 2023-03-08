from django import forms
from .models import Images

class ImageForm(forms.ModelForm):
    class Meta:
        model = Images
        fields = ('original_images',)


from django import forms
from .models import Images


class MagicLinkForm(forms.Form):
    expiration_time = forms.IntegerField(
        label='Expiration time (in seconds)',
        min_value=300,
        max_value=30000,
        initial=3600,
        help_text='Links will expire after the specified time.'
    )

    def generate_links(self, images, request):
        from django.contrib.auth.tokens import PasswordResetTokenGenerator
        from django.utils.http import urlsafe_base64_encode
        from django.core.signing import TimestampSigner

        links = []
        signer = TimestampSigner()

        for image in images:
            signed_value = signer.sign(image.original_images.path)
            uidb64 = urlsafe_base64_encode(signed_value.encode())
            token = PasswordResetTokenGenerator().make_token(image)
            expiration_time = self.cleaned_data['expiration_time']
            link = f"{request.scheme}://{request.get_host()}/image/{uidb64}/{token}/?expires={expiration_time}"
            links.append((image, link))

        return links

