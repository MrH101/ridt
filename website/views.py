from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def index(request):
    user = request.user if request.user.is_authenticated else None
    return render(request, 'main/index.html', {'user': user})