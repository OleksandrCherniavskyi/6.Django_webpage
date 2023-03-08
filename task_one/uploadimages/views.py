
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.signing import TimestampSigner

from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse

from .models import Images
from .forms import ImageForm, MagicLinkForm
from PIL import Image


def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save()  # save the original image
            try:
                # create a thumbnail with 200px height
                img = Image.open(image.original_images.path)
                width, height = img.size
                ratio = height / width
                thumbnail_height = 200
                thumbnail_width = int(thumbnail_height / ratio)
                img.thumbnail((thumbnail_width, thumbnail_height))
                # save the thumbnail
                thumbnail_filename = f'{image.original_images.name.split(".")[0]}_thumbnail_200.jpg'
                thumbnail_path = f'{settings.MEDIA_ROOT}/{thumbnail_filename}'
                img.save(thumbnail_path, 'JPEG')
                # set the thumbnail_200 field in the image instance
                image.thumbnail_200.name = thumbnail_filename
                image.save()
            except Exception as e:
                print(f"Failed to create thumbnail: {str(e)}")
            try:
                # create a thumbnail with 400px height
                img = Image.open(image.original_images.path)
                width, height = img.size
                ratio = height / width
                thumbnail_height_400 = 400
                thumbnail_width = int(thumbnail_height_400 / ratio)
                img.thumbnail((thumbnail_width, thumbnail_height_400))
                # save the thumbnail
                thumbnail_filename_400 = f'{image.original_images.name.split(".")[0]}_thumbnail_400.jpg'
                thumbnail_path_400 = f'{settings.MEDIA_ROOT}/{thumbnail_filename_400}'
                img.save(thumbnail_path_400, 'JPEG')
                # set the thumbnail_400 field in the image instance
                image.thumbnail_400.name = thumbnail_filename_400
                image.save()
            except Exception as e:
                print(f"Failed to create thumbnail: {str(e)}")

            return redirect('image_list')
    else:
        form = ImageForm()
    return render(request, 'uploadimages/upload_image.html', {'form': form})



def image_list(request):
    images = Images.objects.all()

    if request.method == 'POST':
        form = MagicLinkForm(request.POST)
        if form.is_valid():
            expiration_time = form.cleaned_data['expiration_time']
            links = form.generate_links(images, request)
            return render(request, 'uploadimages/image_list.html', {'links': links})
    else:
        form = MagicLinkForm(initial={'expiration_time': 3600})

    return render(request, 'uploadimages/image_list.html', {'images': images, 'form': form})

#def image_list(request):
#    images = Images.objects.all()
#    signer = TimestampSigner()
#    if request.method == 'POST':
#        try:
#            expiration_time = int(request.POST['expiration_time'])
#            if not 300 <= expiration_time <= 30000:
#                raise ValueError()
#        except (KeyError, ValueError):
#            return HttpResponseBadRequest("Invalid expiration time")
#
#        links = []
#        for image in images:
#            signed_value = signer.sign(image.original_images.path)
#            uidb64 = urlsafe_base64_encode(signed_value.encode())
#            token = PasswordResetTokenGenerator().make_token(image)
#            link = f"{request.scheme}://{request.get_host()}/image/{uidb64}/{token}/?expires={expiration_time}"
#            links.append((image, link))
#
#        return render(request, 'uploadimages/image_list.html', {'links': links})
#
#    return render(request, 'uploadimages/image_list.html', {'images': images})



#def image_list(request):
#    images = Images.objects.all()
#    return render(request, 'uploadimages/image_list.html', {'images': images})


