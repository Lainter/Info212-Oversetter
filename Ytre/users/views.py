from django.shortcuts import render

# Create your views here.

def create_user(request):
    user = User.objects.create_user(firstname, )
    user.save()