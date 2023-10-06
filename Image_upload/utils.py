import secrets
from django.utils import timezone
from .models import ExpiringLink
from django.http import Http404
from django.shortcuts import get_object_or_404
from datetime import datetime


def generate_unique_token():
    return secrets.token_urlsafe(16)  # Generates a unique token



def generate_expiring_link(link, image_instance, expiration_time_seconds=60,):
    token = generate_unique_token()
    expiration_time = timezone.now() + timezone.timedelta(seconds=expiration_time_seconds)
    expiring_link = ExpiringLink(token=token, link=link, expiration_time=expiration_time, image=image_instance)
    expiring_link.save()
    return token

def verify_expiring_link(link):
    token = ExpiringLink.objects.get(link = link).token
    try:
        expiring_link = get_object_or_404(ExpiringLink, token=token)
        if timezone.now() > expiring_link.expiration_time:
            return False
        else:
            # Redirect the user to the original link or perform the desired action
            return True
    except Http404:
        # Handle expired or invalid token
        return None
    
def create_link_to_image(filename, resolution=100, original=False, expiring=False, expiring_time=60, image_instance=0):

    if original:
        link = f"image/{filename}/original"
    elif expiring:
        generate_expiring_link(f"image/{filename}/expiring", image_instance, expiring_time)
        link = f"image/{filename}/expiring"
    else:
        link = f"image/{filename}/{resolution}"
    return link

def create_unique_name(filename):
    splited = str(filename).split(".")
    file_extension = splited[-1]
    splited.pop()
    newname = ""
    for x in splited:
        newname+=x
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    newname = newname+timestamp+"."+file_extension
    return newname

