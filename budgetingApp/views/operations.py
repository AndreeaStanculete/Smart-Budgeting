from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods

from budgetingApp.decorators.security import require_authentication
from budgetingApp.models import Finances, PeriodicalFinances
from budgetingApp.models import UserSettings, OneTimeLink

from budgetingApp.utils.email import sendPasswordResetEmail

from random import sample

@require_http_methods(['POST'])
@require_authentication()
def UpdatePeriodicalFinanceData(request):
    if request.POST['_method'] == 'PUT':
        financeType = 0
        if request.POST["operationType"] == "Expense":
            financeType = 1

        PeriodicalFinances.createNewObject(
            request.user,
            financeType,
            request.POST["category"],
            request.POST["amount"],
            request.POST["currency"],
            request.POST["period"])
        return redirect("/main")
    objectId = request.POST["updateId"]
    object = PeriodicalFinances.getObjectById(objectId)[0]

    if "delete" in request.POST:
        object.deleteObject()
    else:
        object.updateObject(
            request.POST["typeShow"],
            request.POST["amountShow"],
            request.POST["currencyShow"], 
            request.POST["periodicalShow"])
    return redirect("/main/profile")

@require_http_methods(['POST'])
@require_authentication()
def UpdateFinanceData(request):
    if request.POST["_method"] == 'PUT':
        financeType = 0
        if request.POST["operationType"] == "Expense":
            financeType = 1

        if "multiOperation" not in request.POST:
            Finances.createNewObject(
                request.user,
                financeType,
                request.POST["category"],
                request.POST["amount"],
                request.POST["currency"],
                request.POST["period"])
            
            if request.POST["period"] != "None":
                return UpdatePeriodicalFinanceData(request)
        else:
            items = (len(request.POST.keys()) - 5) // 2
            print(items)

            for i in range(1,items+1):
                Finances.createNewObject(
                    request.user,
                    financeType,
                    request.POST['T' + str(i)],
                    request.POST['A' + str(i)],
                    request.POST["currencyExp"],
                    "None")
    else:
        objectId = request.POST["updateId"]
        object = Finances.getObjectById(objectId)[0]

        if "delete" in request.POST:
            object.deleteObject()
        else:
            object.updateObject(
                request.POST["typeShow"],
                request.POST["amountShow"],
                request.POST["currencyShow"],
                request.POST["periodicalShow"],
                request.POST["dateShow"])
    return redirect("/main")


@require_http_methods(['POST'])
@require_authentication()
def UpdateAccountInformation(request):
    settings = UserSettings.getObjectsByUser(request.user)[0]
    option = request.POST["updateOption"]

    if option == "picture":
        picNumber = int(request.POST["newData"]) 
        picURLs = [
            '/static/data/images/avatars/male_avatar.svg',
            '/static/data/images/avatars/female_avatar.svg',
            '/static/data/images/avatars/male_avatar2.svg',
            '/static/data/images/avatars/female_avatar2.svg'
        ]

        settings.updateProfilePicture(picURLs[picNumber])
    elif option == "email":
        settings.User.email = request.POST['newData']
        settings.User.save()
    elif option == "username":
        try:
            User.objects.get(username=request.POST["newData"])
        except User.DoesNotExist:
            settings.User.username = request.POST['newData']
            settings.User.save()
    else:
        settings.updateCurrency(request.POST["newData"])
    settings.save()

    return redirect("/main/profile")

@require_authentication(False)
@require_http_methods(['HEAD', 'GET', 'POST'])
def GenerateOneTimeLink(request):
    if request.method == 'POST':
        try:
            _ = User.objects.get(email = request.POST['email'])

            characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
            unique_code = "".join(sample(characters, 20))

            sendPasswordResetEmail(request.POST['email'], unique_code)
            OneTimeLink.createNewObject(request.POST['email'], unique_code)
            return redirect('/')
        except User.DoesNotExist:
            return redirect('/')