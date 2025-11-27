from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
# Create your views here.

def create_user(request):
    user = User.objects.create_user(firstname, )
    user.save()

@login_required
def dashboard(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # create the user
            return redirect('login')  # send them to login page after signup
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})