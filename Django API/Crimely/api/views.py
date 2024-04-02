from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from api.models import Users, Property
from api.serializers import Userserializers, Propertyserializers
from django.views.decorators.clickjacking import xframe_options_exempt
import numpy as np
from django.shortcuts import render, redirect, reverse
from django.http import JsonResponse, HttpResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DocModel
import json
from django.views.decorators import gzip
import cv2
from .forms import DocumentForm
from django.conf import settings
from django.contrib.auth import authenticate
model = settings.MODEL
import requests
# Create your views here.
class VideoCamera(object):
    def __init__(self, url=None):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.status = True
        self.org = (50, 80)
        self.fontScale = 1.4
        self.thickness = 3
        self.SIZE = (150, 150)
        self.THRESH = 0.9
        self.url = 0 if url is None else '.'+url
        self.video = cv2.VideoCapture(self.url)
        self.skipCount = 2
        self.prev = None
        self.fcount = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, image = self.video.read()
        if not ret:
            self.status = False
            pass

        if self.fcount % self.skipCount == 0:
            tmp = cv2.resize(image, self.SIZE)
            tmp = tmp / 255.0
            pred = model.predict(np.array([tmp]))
            print(pred)
            print(pred[0][0])
            string = "Suspicious" if pred[0][0] > self.THRESH else "Peaceful"
            string += f" {str(pred[0][0])}"
            self.prev = string

        else:
            string = self.prev

        ret, jpeg = cv2.imencode('.jpg', image)
        self.fcount += 1
        return jpeg.tobytes()
    
class VideoAnalysis(object):
    def __init__(self, url=None):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.status = True
        self.org = (50, 80)
        self.fontScale = 1.4
        self.thickness = 3
        self.SIZE = (150, 150)
        self.THRESH = 0.85
        self.url = 0 if url is None else '.'+url
        self.video = cv2.VideoCapture(self.url)
        self.skipCount = 2
        self.prev = None
        self.fcount = 0

    def __del__(self):
        self.video.release()

    def get_frame(self):
        ret, image = self.video.read()
        if not ret:
            self.status = False
            pass

        if self.fcount % self.skipCount == 0:
            tmp = cv2.resize(image, self.SIZE)
            tmp = tmp / 255.0
            pred = model.predict(np.array([tmp]))
            print(pred)
            print(pred[0][0])
            string = "Suspicious" if pred[0][0] > self.THRESH else "Peaceful"
            print(string)
            self.prev = string
        else:
            string = self.prev

        if string == "Suspicious":
            flag = 1
        elif string == "Peaceful":
            flag = 0
        
        self.fcount += 1
        return flag

def gen(camera):
    result = 0
    while camera.status:
        frame = camera.get_frame()
        print(frame)
        if frame == 1:
            result = 1
            break
    return result


@gzip.gzip_page
def Stream(request):
    try:
        entry = DocModel.objects.all().last()
        return StreamingHttpResponse(gen(VideoCamera(entry.vid.url)), content_type="multipart/x-mixed-replace;boundary=frame")
    except StreamingHttpResponse.HttpResponseServerError as e:
        print("aborted")


@gzip.gzip_page
def StreamToken(request, token):
    try:
        entry = DocModel.objects.filter(stoken=token).last()
        return StreamingHttpResponse(gen(VideoCamera(entry.vid.url)), content_type="multipart/x-mixed-replace;boundary=frame")
    except StreamingHttpResponse.HttpResponseServerError as e:
        print("aborted")


def HomeView(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('streamroom')

    else:
        form = DocumentForm()
        return render(request, 'home.html', {'form': form})


# @xframe_options_exempt
def StreamView(request):
    entry = DocModel.objects.all().last()
    if entry is None:
        return JsonResponse({'message': 'No Video Files Yet!'})
    return render(request, 'stream.html')


# API End Point
def StreamTokenView(request, token):
    try:
        entry = DocModel.objects.filter(stoken=token).last()
        if entry is None:
            return JsonResponse({'message': 'Token Not Registered'})

        return render(request, 'streamtoken.html', {'token': token})

    except DocModel.DoesNotExist:
        return JsonResponse({'message': 'Token Not Registered'})
    


@csrf_exempt
def APIEnd(request):
    if request.method == 'POST':
        try:
            # stoken = request.POST['stoken']
            vidFile = request.FILES['vid']
            if vidFile:
                DocModel(stoken="Videobasedcheck", vid=vidFile).save()
                entry = DocModel.objects.all().last()
                print(entry.vid.url)
                result = gen(VideoAnalysis(entry.vid.url))
                if result == 1:
                    data = {
                        "appId": 20125,
                        "appToken": "01stPUYsdEb2jI7KABYtwf",
                        "title": "Alert",
                        "body": "There has been a crime detected on your property.",
                        "dateSent": "3-12-2024 4:38PM",
                    }
                    headers = {
                        'Content-Type': 'application/json'
                    }
                    json_data = json.dumps(data)
                    response = requests.post("https://app.nativenotify.com/api/notification", data=json_data, headers=headers)
                    if response.status_code == 200:
                       print('Post request failed')
                    else:
                        return JsonResponse({'status': 'ok', 'message': f'Files Received from sender', 'flag': f'{result}'})
                else:
                    return JsonResponse({'status': 'ok', 'message': f'Files Received from sender', 'flag': f'{result}'})
            else:
                return JsonResponse({'status': 'Notok', 'message': f'Files not Received from sender'})
        except:
            return HttpResponse(status=400)

    return JsonResponse({'status': 'Wait kro bhai'})


class RegisterViewset(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = Userserializers
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Save the validated data to the Users model
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)



class PropertyViewset(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = Propertyserializers

class UserLoginView(APIView):
    def post(self, request, format = None):
        user_obj = Users.objects.filter(email=request.data['email']).first()
        print(user_obj)
        if user_obj is not None:
            if user_obj.Pass == request.data["Pass"]:
                user_serializer = Userserializers(user_obj, context={'request': request})
                return Response(user_serializer.data, status = 200)
        
        return Response({"MSSG": "Invalid Credentials", "Flag": 0}, status = 403)
