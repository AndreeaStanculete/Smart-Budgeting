from django.views.decorators.http import require_safe
from django.shortcuts import render

from budgetingApp.decorators.security import require_authentication


@require_safe
@require_authentication(required=False, redirect_url='/main')
def Index(request):
    return render(request, 'index.html')

@require_safe
def DisplayError(request, errorCode: int):
    return render(request, 'errorPage.html', context={'errorCode': errorCode})