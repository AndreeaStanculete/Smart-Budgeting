from dateutil.relativedelta import relativedelta
from random import randrange
from datetime import date, datetime

import calendar

from budgetingApp.models import Finances
from budgetingApp.models import UserSettings
from budgetingApp.models import Advices

def buildEmailMessage(user): 
    today = date.today()
    today = today + relativedelta(months=-1)
    yesterday = date.today()
    yesterday = yesterday + relativedelta(months=-2)

    income = {}
    total_income = {}
    expense = {}
    total_expense = {}

    MainCurrency = UserSettings.getObjectsByUser(user)[0].Currency

    # get all types of expenses and incomes, as well as total expenses and incomes for each month
    for obj in Finances.getObjectsByUser(user):
        if obj.Type == 0:
            if calendar.month_name[obj.Date.month] not in income.keys():
                optional = {}
                optional[obj.Category] = obj.Amount
                income[calendar.month_name[obj.Date.month]] = optional
            else:
                try:      
                    income[calendar.month_name[obj.Date.month]][obj.Category] += obj.Amount
                except KeyError:
                    income[calendar.month_name[obj.Date.month]][obj.Category] = obj.Amount

            sortedDict = sorted(income[calendar.month_name[obj.Date.month]].items(), key=lambda x:x[1], reverse=True)
            income[calendar.month_name[obj.Date.month]] = dict(sortedDict)

            try:       
                total_income[calendar.month_name[obj.Date.month]] += obj.Amount
            except KeyError:
                total_income[calendar.month_name[obj.Date.month]] = obj.Amount

        if obj.Type == 1:
            if calendar.month_name[obj.Date.month] not in expense.keys():
                optional = {}
                optional[obj.Category] = obj.Amount
                expense[calendar.month_name[obj.Date.month]] = optional
            else:
                try:      
                    expense[calendar.month_name[obj.Date.month]][obj.Category] += obj.Amount
                except KeyError:
                    expense[calendar.month_name[obj.Date.month]][obj.Category] = obj.Amount

            sortedDict = sorted(expense[calendar.month_name[obj.Date.month]].items(), key=lambda x:x[1], reverse=True)
            expense[calendar.month_name[obj.Date.month]] = dict(sortedDict)

            try:       
                total_expense[calendar.month_name[obj.Date.month]] += obj.Amount
            except KeyError:
                total_expense[calendar.month_name[obj.Date.month]] = obj.Amount

    # print(expense)
    #print(total_expense)

    # create message 
    html = """
        <html>
        <body>
            <p>This is an automatic mail through the Smart Budgeting Application. Please do not reply to it.</p> """

    html = "<h3>Your income for the month of " + str(calendar.month_name[today.month]) + " has come to a total of "
    html += str(total_income[calendar.month_name[today.month]]) + " " + MainCurrency
    html += " from which you have used " + str(total_expense[calendar.month_name[today.month]]) + " " + MainCurrency + ".</h3>"

    if calendar.month_name[yesterday.month] not in total_expense.keys():
        html += "<p>Use this application next month as well for better data analysis.</p>"
    else:
        # show difference between expenses this month and last month
        percentage = (100 * total_expense[calendar.month_name[today.month]] / total_expense[calendar.month_name[yesterday.month]]) - 100
        if percentage > 0:
            html += "<h4>Based on your data, your expenses have gone up by " + "{:.2f}".format(percentage) + "% compared to last month.</h4>"
        else:
            html += "<h4>Based on your data, your expenses have gone down by " + "{:.2f}".format(percentage) + "% compared to last month.</h4>"

        # show difference between types of incomes this month and last month
        if percentage > 0: 
            common_items = {}
            exists = 0
            rent = 0
            diff_items = {}
            for key, current_value in expense[calendar.month_name[today.month]].items():
                if key in expense[calendar.month_name[yesterday.month]].keys():
                    if key == "Rent":
                        salary = total_income[calendar.month_name[today.month]]
                        if salary / current_value <= 2:
                            rent = 1

                    last_value = expense[calendar.month_name[yesterday.month]][key]
                    common_items[key] = round((100 * current_value / last_value) - 100, 2)
                    if common_items[key] >= 50:
                        exists = exists + 1
                else:
                    diff_items[key] = current_value

            if exists != 0:
                sortedDict = sorted(common_items.items(), key=lambda x:x[1], reverse=True)
                common_items = dict(sortedDict)

                html += "<p>The following expenses have increased compared to last month: "

                for key, current_value in common_items.items():
                    if current_value >= 50:
                        exists = exists - 1
                        html += key + " by " + str(current_value) + "%"
                        if exists != 0:
                            html += ", "
                
                html += "</p>"

                html += "<p>In order to save up money you could try to reduce your expenses. The following advices can relate to your current situation: <ul>"
                for key, current_value in common_items.items():
                    if current_value >= 50:
                        advices = Advices.getObjectsByExpense(key)
                        # print(advices)
                        if len(advices) > 0:
                            advice = advices[randrange(0, len(advices), 1)]
                            html += "<li>" + advice.LongText + "</li>"
                html += "</ul></p>"

                        
    # print(common_items)
    # print(diff_items)

    html += """
        </body>
        </html>
        """

    #message += "Your biggest expense was " + str(expense[calendar.month_name[today.month]][0])


    return html



def buildExportMessage(user, month_year: date): 
    month = datetime.strptime(month_year, "%Y-%m").month
    year = datetime.strptime(month_year, "%Y-%m").year

    income = {}
    total_income = {}
    expense = {}
    total_expense = {}

    MainCurrency = UserSettings.getObjectsByUser(user)[0].Currency

    # get all types of expenses and incomes, as well as total expenses and incomes for each month
    for obj in Finances.getObjectsByUser(user):
        if obj.Type == 0:
            if obj.Date.month not in income.keys():
                optional = {}
                optional[obj.Category] = obj.Amount
                income[calendar.month_name[obj.Date.month]] = optional
            else:
                try:      
                    income[calendar.month_name[obj.Date.month]][obj.Category] += obj.Amount
                except KeyError:
                    income[calendar.month_name[obj.Date.month]][obj.Category] = obj.Amount

            sortedDict = sorted(income[calendar.month_name[obj.Date.month]].items(), key=lambda x:x[1], reverse=True)
            income[calendar.month_name[obj.Date.month]] = dict(sortedDict)

            try:       
                total_income[calendar.month_name[obj.Date.month]] += obj.Amount
            except KeyError:
                total_income[calendar.month_name[obj.Date.month]] = obj.Amount

        if obj.Type == 1:
            if calendar.month_name[obj.Date.month] not in expense.keys():
                optional = {}
                optional[obj.Category] = obj.Amount
                expense[calendar.month_name[obj.Date.month]] = optional
            else:
                try:      
                    expense[calendar.month_name[obj.Date.month]][obj.Category] += obj.Amount
                except KeyError:
                    expense[calendar.month_name[obj.Date.month]][obj.Category] = obj.Amount

            sortedDict = sorted(expense[calendar.month_name[obj.Date.month]].items(), key=lambda x:x[1], reverse=True)
            expense[calendar.month_name[obj.Date.month]] = dict(sortedDict)

            try:       
                total_expense[calendar.month_name[obj.Date.month]] += obj.Amount
            except KeyError:
                total_expense[calendar.month_name[obj.Date.month]] = obj.Amount

    # print(expense)
    #print(total_expense)

    # create message 
    html = """
        <html>
        <body>
            <p>This is an automatic mail through the Smart Budgeting Application. Please do not reply to it.</p> """

    html = "<h3>Attached you can find the export of data for the month of " + str(month) + "."
    html += "Your incomes have come to a total of "
    html += str(total_income[calendar.month_name[month]]) + " " + MainCurrency
    html += " from which you have used " + str(total_expense[calendar.month_name[month]]) + " " + MainCurrency + ".</h3>"

    html += """
        </body>
        </html>
        """

    #message += "Your biggest expense was " + str(expense[calendar.month_name[today.month]][0])

    return html
        
        

