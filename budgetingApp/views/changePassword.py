from django.contrib.auth.models import User

from budgetingApp.models import OneTimeLink
from budgetingApp.decorators.security import require_authentication
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

@require_authentication(False)
@require_http_methods(['HEAD', 'GET', 'POST'])
def ChangeAccountPassword(request, code):
    if not OneTimeLink.isValid(code):
        return redirect('/')
    
    if request.method == 'POST':
        email = OneTimeLink.objects.get(UniqueCode = code).AssociatedEMail
        current_user = User.objects.get(email = email)

        new_password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if new_password == confirm_password:
            current_user.set_password(new_password)
            current_user.save()
        
        OneTimeLink.deleteObject(code)
        return redirect('/account/login')

    return render(request, 'forgot_password.html')