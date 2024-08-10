from django.db import models
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta

class PeriodicalFinances(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Category = models.CharField(max_length=50)
    Details = models.CharField(max_length=100)
    Amount = models.IntegerField()
    Currency = models.CharField(max_length=50)
    Date = models.DateField()
    Periodical = models.CharField(max_length=50)

    # Type = 0 when income
    # Type = 1 when expense
    Type = models.IntegerField()

    @staticmethod
    def getObjectsByUser(user: User) -> list:
        """
        Returns all objects belonging to a specific user.

        Args:
            - user (User): The user to lookup
        """
        return PeriodicalFinances.objects.filter(User = user)
    

    def getObjectById(id: int):
        return PeriodicalFinances.objects.filter(id = id)
    
    @staticmethod
    def createNewObject(user: User, 
                        type: int, 
                        category: str, 
                        amount: int, 
                        currency: str, 
                        periodical: str, 
                        details: str = "", 
                        date: models.DateField() = date.today() ):
        """
        Creates a new object and saves it to database.

        Args:
            - user (User): The current user
            - type (int): 0 if income, 1 if expense
            - category (str): The category of object (e.g. Salary, Bonus, Rent, Groceries)
            - details (str): Text describing the object (optional)
            - amount (int): The amount of income / expense
            - currency (str): The currency regarding the amount
            - periodical (str): When the periodicity occurs (weekly, monthly)
        """

        if periodical == 'Monthly':
            date = date + relativedelta(months=+1)
        elif periodical == 'Bi-weekly':
            date = date + relativedelta(days=+14)
        elif periodical == 'Weekly':
            date = date + relativedelta(days=+7)
        elif periodical == 'Yearly':
            date = date + relativedelta(months=+12)
            
        obj = PeriodicalFinances(
            User = user, 
            Type = type,
            Category = category, 
            Details = details,
            Amount = amount, 
            Currency = currency,
            Date = date,
            Periodical = periodical)
        obj.save()

    def UpdateDate(self, date: models.DateField()):
        self.Date = date
        self.save()

    def updateObject(self, 
                    category: str, 
                    amount: int, 
                    currency: str, 
                    periodical: str ):
        """
        Update an existing object in the database

        Args:
            - user (User): The current user
            - type (int): 0 if income, 1 if expense
            - category (str): The category of object (e.g. Salary, Bonus, Rent, Groceries)
            - details (str): Text describing the object (optional)
            - amount (int): The amount of income / expense
            - currency (str): The currency regarding the amount
            - periodical (str): When the periodicity occurs (weekly, monthly)
        """
        self.Category = category
        self.Amount = amount 
        self.Currency = currency 
        self.Periodical = periodical
        self.save()

    def deleteObject(self):
        self.delete()
