import json
import calendar

from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.core.files.storage import FileSystemStorage

from datetime import date, datetime

from budgetingApp.decorators.security import require_authentication

from budgetingApp.models import Finances
from budgetingApp.models import UserSettings
from budgetingApp.models import Expenses
from budgetingApp.models import Currencies

from budgetingApp.utils.receipt import saveReceiptToFile, parseReceiptImage
from budgetingApp.utils.crawler import searchForPrices

from budgetingApp.utils.email import sendEmailReport, exportDataToEmail

@require_authentication()
@require_http_methods(['HEAD', 'GET', 'POST'])
def DisplayUserData(request):
    newExpenses = []
    searchResults = []

    if request.method == 'POST':
        if request.POST['modalId'] == '100':
            searchResult = searchForPrices(request.POST["searchInput"])
            #print(searchResult)

            contor = 1
            for obj in searchResult:
                searchResults.append([contor, obj["Name"], obj["Price"], obj["URL"]])
                contor = contor + 1

        if request.POST["modalId"] == "1":
            #Files from upload
            contor = 1

            fs = FileSystemStorage()
            for filename, _ in request.FILES.items():
                uploadedFile = request.FILES[filename]
                
                fs.save("tmp/receipt.jpeg", uploadedFile)
                
                content = parseReceiptImage()
                print(content)
                print("NEXT")

                with open('tmp/json.json', 'w', encoding="utf-8") as file:
                    file.write(json.dumps(content))

                f = open('tmp/json.json', 'r', encoding="utf-8")
                data = json.load(f)
                print(data)
                for obj in data["receipts"]:
                    newExpenses.append([contor, obj["total"], obj["currency"]])
                    contor = contor + 1
                f.close()

        elif request.POST["modalId"] == "2":
            #File from camera
            saveReceiptToFile(request.POST.get('photoFile'))
            content = parseReceiptImage()

            with open('tmp/json.json', 'w', encoding="utf-8") as file:
                    file.write(json.dumps(content))

            f = open('tmp/json.json', 'r', encoding="utf-8")
            data = json.load(f)
            contor = 1
            for obj in data["receipts"]:
                newExpenses.append([contor, obj["total"], "Lei"])
                contor = contor + 1
            f.close()


    today = date.today()
    
    incomeList = []
    expenseList = []
    sumIncome = {}
    sumExpense = {}
    remaining = {}

    lineChartExpenseData = {}
    lineChartIncomeData = {}
    expenseChartData = {}
    incomeChartData = {}

    MainCurrency = UserSettings.getObjectsByUser(request.user)[0]

    for obj in Finances.getObjectsByUser(request.user):
        if obj.Type == 0:
            # amount = obj.Amount
            # if obj.Currency != MainCurrency:
            #     convert_money(Money(amount, obj.Currency), MainCurrency)
            # print(amount)
            try:
                lineChartIncomeData[calendar.month_name[obj.Date.month]] += obj.Amount
            except KeyError:
                lineChartIncomeData[calendar.month_name[obj.Date.month]] = obj.Amount
        elif obj.Type == 1:
            try:
                lineChartExpenseData[calendar.month_name[obj.Date.month]] += obj.Amount
            except KeyError:
                lineChartExpenseData[calendar.month_name[obj.Date.month]] = obj.Amount
        
        if "display_month" not in request.session:
            if obj.Date.month == today.month:
                # (obj.Date.month == datetime.strptime(request.session["display_month"], "%Y-%M").month):
                if obj.Type == 0:
                    incomeList.append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
                    try:
                        sumIncome[obj.Currency] += obj.Amount
                    except KeyError:
                        sumIncome[obj.Currency] = obj.Amount

                    try:
                        remaining[obj.Currency] += obj.Amount
                    except KeyError:
                        remaining[obj.Currency] = obj.Amount

                    try:
                        incomeChartData[obj.Category] += obj.Amount
                    except KeyError:
                        incomeChartData[obj.Category] = obj.Amount

                elif obj.Type == 1:
                    expenseList.append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
                    try:
                        sumExpense[obj.Currency] += obj.Amount
                    except KeyError:
                        sumExpense[obj.Currency] = obj.Amount
                        
                    try:
                        remaining[obj.Currency] -= obj.Amount
                    except KeyError:
                        remaining[obj.Currency] = -1 * obj.Amount

                    try:
                        expenseChartData[obj.Category] += obj.Amount
                    except KeyError:
                        expenseChartData[obj.Category] = obj.Amount
        else:
            if obj.Date.month == datetime.strptime(request.session["display_month"], "%Y-%m").month and obj.Date.year == datetime.strptime(request.session["display_month"], "%Y-%m").year:
                if obj.Type == 0:
                    incomeList.append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
                    try:
                        sumIncome[obj.Currency] += obj.Amount
                    except KeyError:
                        sumIncome[obj.Currency] = obj.Amount

                    try:
                        remaining[obj.Currency] += obj.Amount
                    except KeyError:
                        remaining[obj.Currency] = obj.Amount

                    try:
                        incomeChartData[obj.Category] += obj.Amount
                    except KeyError:
                        incomeChartData[obj.Category] = obj.Amount

                elif obj.Type == 1:
                    expenseList.append([obj.id, obj.Category, obj.Amount, obj.Currency, obj.Date, obj.Periodical])
                    try:
                        sumExpense[obj.Currency] += obj.Amount
                    except KeyError:
                        sumExpense[obj.Currency] = obj.Amount
                        
                    try:
                        remaining[obj.Currency] -= obj.Amount
                    except KeyError:
                        remaining[obj.Currency] = -1 * obj.Amount

                    try:
                        expenseChartData[obj.Category] += obj.Amount
                    except KeyError:
                        expenseChartData[obj.Category] = obj.Amount

    expense_categories = []
    for exp in Expenses.getObjects():
        expense_categories.append(exp.Name)

    world_currencies = []
    for c in Currencies.getObjects():
        world_currencies.append(c.Name)

    #month_to_display = today.month
    try:
        month_to_display = request.session["display_month"]
    except:
        month_to_display = today.strftime("%Y-%m")


    context={'expense_categories': expense_categories,
             'income_categories': ['Salary', 'Stock', 'Bonus', 'Gift', 'Others'],
             'currencies': world_currencies,
             'periodicities': ['None', 'Weekly', 'Bi-weekly', 'Monthly', 'Yearly'],
             'Incomes': incomeList, 
             'TotalIncome': sumIncome, 
             'Expenses': expenseList, 
             'TotalExpense': sumExpense, 
             'NewExpenses': newExpenses, 
             'MainCurrency': MainCurrency.Currency, 
             'remainingMoney': remaining, 
             'SearchResult': searchResults,
             'pieLabels': list(expenseChartData.keys()), 
             'pieData': list(expenseChartData.values()),
             'barLabels': list(incomeChartData.keys()),
             'barData': list(incomeChartData.values()),
             'lineLabels': list(lineChartExpenseData.keys()),
             'lineData': [list(lineChartExpenseData.values()), list(lineChartIncomeData.values())],
             'month': month_to_display,
             "logged_in": 1
            }

    return render(request, 'homepage.html', context=context)

@require_authentication()
@require_http_methods(['HEAD', 'GET', 'POST'])
def UpdateSiteInformation(request):
    if request.method == 'POST':
        request.session["display_month"] = request.POST["new_data"]
    return redirect("/main")

@require_authentication()
@require_http_methods(['HEAD', 'GET', 'POST'])
def ExportUserData(request):
    exportDataToEmail(request.user, request.session["display_month"])
    return redirect("/main")
    