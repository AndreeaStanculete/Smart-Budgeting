from dateutil.relativedelta import relativedelta
from datetime import date

from budgetingApp.models import Finances, PeriodicalFinances

def updateUserData(user): 
    today = date.today()

    for obj in PeriodicalFinances.getObjectsByUser(user):
        while obj.Date <= today:
            Finances.createNewObject(
                user,
                obj.Type,
                obj.Category,
                obj.Amount,
                obj.Currency,
                obj.Periodical,
                obj.Details,
                obj.Date)
            
            if obj.Periodical == 'Monthly':
                obj.Date = obj.Date + relativedelta(months=+1)
            elif obj.Periodical == 'Bi-weekly':
                obj.Date = obj.Date + relativedelta(days=+14)
            elif obj.Periodical == 'Weekly':
                obj.Date = obj.Date + relativedelta(days=+7)
            elif obj.Periodical == 'Yearly':
                obj.Date = obj.Date + relativedelta(months=+12)

        obj.UpdateDate(obj.Date)
