from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def showHome(request):
    return render(request, "frontend/index.html")

def showAuth(request):
    return render(request, "frontend/auth.html")