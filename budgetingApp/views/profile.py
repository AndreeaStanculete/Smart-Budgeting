from django.shortcuts import render

from budgetingApp.decorators.security import require_authentication
from budgetingApp.models import UserSettings, PeriodicalFinances
from budgetingApp.models import Expenses
from budgetingApp.models import Currencies

from budgetingApp.utils.crawler import searchForPrices


@require_authentication()
def DisplayUserProfile(request):

    searchResults = []
    if request.method == 'POST':
        if request.POST['modalId'] == '100':
            searchResult = searchForPrices(request.POST["searchInput"])
            for obj in searchResult:
                searchResults.append([contor, obj["Name"], obj["Price"], obj["URL"]])
                contor = contor + 1
    MainCurrency = UserSettings.getObjectsByUser(request.user)[0]
    img = ""
    curr = ""
    for obj in UserSettings.getObjectsByUser(request.user):
        img = obj.Picture
        curr = obj.Currency

    PeriodicalIncomes = {}
    foundIncome = 0
    PeriodicalExpenses = {}
    foundExpenses = 0
    for obj in PeriodicalFinances.getObjectsByUser(request.user):
        if obj.Type == 0:
            if obj.Periodical not in PeriodicalIncomes.keys():
                PeriodicalIncomes[obj.Periodical] = []
                PeriodicalIncomes[obj.Periodical].append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
                foundIncome = 1
            else:
                PeriodicalIncomes[obj.Periodical].append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
        elif obj.Type == 1:
            if obj.Periodical not in PeriodicalExpenses.keys():
                PeriodicalExpenses[obj.Periodical] = []
                PeriodicalExpenses[obj.Periodical].append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
                foundExpenses = 1
            else:
                PeriodicalExpenses[obj.Periodical].append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])

    expense_categories = []
    for exp in Expenses.getObjects():
        expense_categories.append(exp.Name)

    world_currencies = []
    for c in Currencies.getObjects():
        world_currencies.append(c.Name)

    context={
        'inc_sources': ['Salary', 'Stock', 'Bonus', 'Gift', 'Others'],
        'exp_sources': expense_categories,
        'currencies': world_currencies,
        'periodicities': ['None', 'Weekly', 'Bi-weekly', 'Monthly', 'Yearly'],
        "username": request.user.username,
        "email": request.user.email,
        "imageURL": img,
        "currency": curr,
        'MainCurrency': MainCurrency.Currency, 
        "verified": 0,
        "foundIncome": foundIncome,
        "PeriodicalIncomes": PeriodicalIncomes,
        "foundExpenses": foundExpenses,
        "PeriodicalExpenses": PeriodicalExpenses,
        "SearchResult": searchResults,
        "logged_in": 1,
    }

    return render(request, 'profile.html', context=context)