# Django_webpage

This project is a Django REST Framework (DRF) API that allows users to upload images in PNG or JPG format. It supports three built-in account tiers (Basic, Premium, and Enterprise) that determine the type of links users receive after uploading an image.

Setup
To run the project, make sure you have Docker and Docker Compose installed on your system. Then, follow these steps:


Open your web browser and go to http://localhost:8000 to access the API.

API endpoints
The API supports the following endpoints:
Users can register using a registration form. Upon registration, the user is automatically assigned the Basic tier. 
The user can then login to the website and upload new images. An admin can modify the tiers in the Django admin menu.

![image](https://user-images.githubusercontent.com/105165580/224565162-ac05d3aa-ae1e-417a-8d93-4cda7da2f3ac.png)


http://127.0.0.1:8000/upload/
Upload an image in PNG or JPG format. The request must include the image file and a user authentication token in the Authorization header. 
If successful, the response includes links to the image thumbnail(s) and the original image (if applicable), based on the user's account tier.

![image](https://user-images.githubusercontent.com/105165580/224563672-8b469282-77ef-4c1d-889d-1ed58b0433a1.png)


http://127.0.0.1:8000/images/
List all images uploaded by the authenticated user. The request must include a user authentication token in the Authorization header.

![image](https://user-images.githubusercontent.com/105165580/224563836-7f40920b-2eaa-49a6-bbd3-03e096ec9f03.png)


Account tiers
The API supports three built-in account tiers (Basic, Premium, and Enterprise), which determine the type of links users receive after uploading an image. 
Users with custom account tiers (defined by admins) can also receive custom links.

Basic
Users with the "Basic" plan receive a link to a thumbnail that's 200px in height.

Premium
Users with the "Premium" plan receive:

A link to a thumbnail that's 200px in height
A link to a thumbnail that's 400px in height
A link to the originally uploaded image
Enterprise
Users with the "Enterprise" plan receive:

A link to a thumbnail that's 200px in height
A link to a thumbnail that's 400px in height
A link to the originally uploaded image

Admins can create arbitrary account tiers with configurable thumbnail sizes, presence of the link to the originally uploaded file.
The admin UI can be accessed via the Django admin site (http://localhost:8000/admin).
![image](https://user-images.githubusercontent.com/105165580/224564439-09e40c6b-cff7-4b55-8015-a574b5dc2cea.png)




bash
Copy code
docker-compose exec web python manage.py test

Performance considerations



