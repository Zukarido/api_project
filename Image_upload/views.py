from django.http import HttpResponse
from rest_framework.response import Response
from .models import Image,  UserProfile
from .serializers import ImageSerializer
from django.shortcuts import redirect, render

from .utils import  verify_expiring_link, create_link_to_image, create_unique_name
from rest_framework import generics  


class FileUploadView(generics.CreateAPIView):

    serializer_class = ImageSerializer
    def post(self, request):
        if request.user.is_authenticated:          
            serializer = ImageSerializer(data = request.data)
            if serializer.is_valid():
                try:
                    image_data = serializer.validated_data.get('image')
                    if Image.objects.filter(image = f"Image_upload/static/images/{image_data.name}").exists():
                       image_data.name = create_unique_name(image_data.name)
                    exp_time = serializer.validated_data.get("exp_time")
                    exp_link = serializer.validated_data.get("exp_link")
                    user_tier = UserProfile.objects.get(user=request.user).tier
                    if not user_tier.allow_expiring_link and exp_link:
                        return Response({"response": "You are not allowed to use expiring link"})
                    elif user_tier.allow_expiring_link and exp_link:
                        if exp_time<300 or exp_time>30000:
                            return Response({"response": "Time expiration time has to be between 300 and 30000"})
                    image_instance = Image(user = request.user, image= image_data)
                    image_instance.save()
                    thumbnail_sizes = user_tier.thumbnail_sizes.split(", ")
                    links = {}
                    image_name = str(image_instance.image).split("/")[-1]
                    for x in thumbnail_sizes:
                        links[f"resolution {x}"] = create_link_to_image(image_name, resolution=x)
                    if user_tier.allow_original_link:
                        links["original"] = create_link_to_image(image_name, original=True)
                    if user_tier.allow_expiring_link and exp_link:
                        links["expiring"] = create_link_to_image(image_name, expiring=True, expiring_time=exp_time, image_instance=image_instance)
                    return Response(links)
                except Exception as e:
                    return Response({"error": f"{e}"})
            else:
                return Response({"response": "not valid data passed"})
        else:
            return redirect('login')
    def get(self, request):
        if request.user.is_authenticated:
            image_obejcts = Image.objects.filter(user = request.user).values()
            image_dict = {}
            n=1
            for x in image_obejcts:
                splited_x = x['image'].split("/")
                filename = splited_x[-1]
                image_dict[f"image{n}"] = filename
                n+=1
            if len(image_dict)==0:
                return Response({"response": "no images"})
            else:
                return Response(image_dict)       
        else:
            return redirect('login')
    
def display_image(request, image_name, resolution):

    if request.user.is_authenticated:
        try:
            image_obejct = Image.objects.get(image = f"Image_upload/static/images/{image_name}")
            user_object = UserProfile.objects.get(user=request.user)           
        except Exception as e:
            return HttpResponse({"response": "User not registered in UserProfile or no such Image", "error":f"{e}"})
        if image_obejct.user_id == request.user.id and user_object.tier.thumbnail_sizes.find(str(resolution))!=-1:
            return render(request, 'display_img.html', {'image_path': f"images/{image_name}", 'resolution': resolution})   
        else:
            if resolution == "expiring" and image_obejct.user_id == request.user.id and user_object.tier.allow_expiring_link:
                if verify_expiring_link(f"image/{image_name}/expiring"):
                    return render(request, 'display_img_original.html', {'image_path': f"images/{image_name}"})
                else:
                    return HttpResponse("Link expired")
            elif resolution=="original"and image_obejct.user_id == request.user.id and user_object.tier.allow_original_link:
                return render(request, 'display_img_original.html', {'image_path': f"images/{image_name}"})
            else:
                return HttpResponse("Not your image or you dont have permission to view it that way")
    else:
        return redirect('login')


