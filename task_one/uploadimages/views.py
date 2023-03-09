
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Images
from .forms import ImageForm, MagicLinkForm, CreateUserForm
from .decorators import unauthenticated_user, allowed_users, Enterprise_only
from PIL import Image
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')

def upload_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)  # save the original image
            image.uploaded_by = request.user  # associate the image with the current user
            image.save()
            try:
                # create a thumbnail with 200px height
                img = Image.open(image.original_images.path)
                width, height = img.size
                ratio = height / width
                thumbnail_height = 200
                thumbnail_width = int(thumbnail_height / ratio)
                img.thumbnail((thumbnail_width, thumbnail_height))
                # save the thumbnail
                thumbnail_filename_200 = f'{image.original_images.name.split(".")[0]}_thumbnail_200.jpg'
                thumbnail_path = f'{settings.MEDIA_ROOT}/{thumbnail_filename_200}'
                img.save(thumbnail_path, 'JPEG')
                # set the thumbnail_200 field in the image instance
                image.thumbnail_200.name = thumbnail_filename_200
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
    return render(request, 'uploadimages/upload.html', {'form': form})





#@allowed_users(allowed_roles=['Enterprise'])
#@login_required(login_url='login')
#def original_images(request):
#    original_images = Images.objects.filter(uploaded_by=request.user).values_list('original_images', flat=True)
#    return render(request, 'uploadimages/original_images.html', {'original_images': original_images})
#
#
#
#@allowed_users(allowed_roles=['Enterprise'])
#@login_required(login_url='login')
#def thumbnail_400(request):
#    thumbnail_400 = Images.objects.filter(uploaded_by=request.user).values_list('thumbnail_400', flat=True)
#    return render(request, 'uploadimages/thumbnail_400px.html', {'thumbnail_400': thumbnail_400})
#
#

 #good version
@login_required(login_url='login')
def image_list(request):
    images = Images.objects.filter(uploaded_by=request.user)
    return render(request, 'uploadimages/image_list.html', {'images': images})





@login_required(login_url='login')
def magiclink(request):
    last_login = request.user.last_login
    images = Images.objects.filter(uploaded_by=request.user)
    if request.method == 'POST':
        form = MagicLinkForm(request.POST)
        if form.is_valid():
            expiration_time = form.cleaned_data['expiration_time']
            links = form.generate_links(images, request)
            return render(request, 'uploadimages/image_list.html', {'links': links})
    else:
        form = MagicLinkForm(initial={'expiration_time': 3600})

    return render(request, 'uploadimages/magiclink.html', {'form': form, 'last_login': last_login})



@unauthenticated_user
def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='Basic')
            user.groups.add(group)

            return redirect('login')
    context = {'form': form}
    return render(request, 'uploadimages/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('image_list')
    context = {}
    return render(request, 'uploadimages/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')


