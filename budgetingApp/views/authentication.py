from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods, require_safe

from budgetingApp.decorators.security import require_authentication
from budgetingApp.models import UserSettings
from budgetingApp.utils.databaseUpdate import updateUserData
from budgetingApp.utils.email import sendEmailReport


@require_http_methods(['HEAD', 'GET', 'POST'])
@require_authentication(required=False, redirect_url='/main')
def AuthenticateAccount(request):
    context = {"mode": "login"}
    
    if request.method == 'POST':
        context["error"] = "Invalid login!"

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            updateUserData(user)
            #sendEmailReport(user)
            
            return redirect('/main')

    return render(request, 'authenticate.html', context=context)

@require_http_methods(['HEAD', 'GET', 'POST'])
@require_authentication(required=False, redirect_url='/main')
def RegisterAccount(request):
    context = {"mode": "register"}
    
    if request.method == "POST":
        context["error"] = "Username already exists!"
        
        try:
            user = User.objects.get(username=request.POST["username"])
        except User.DoesNotExist:
            user = UserSettings.createNewObject(
                request.POST["username"],
                request.POST["email"],
                request.POST["password"])
            
            login(request, user)
            return redirect('/main')
    return render(request, 'authenticate.html', context=context)

@require_safe
@require_authentication(required=True, redirect_url='')
def DeauthenticateAccount(request):
    logout(request)

    return redirect('/')