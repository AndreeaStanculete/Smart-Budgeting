from django.db import models

class Advices(models.Model):
    Expense = models.CharField(max_length=50)
    ShortText = models.CharField(max_length=30)
    LongText = models.CharField(max_length=300)
    
    @staticmethod
    def getObjects() -> list:
        """
        Returns all objects from table
        """
        return Advices.objects()
    
    def getObjectsByExpense( expenseName: str ):
        """
        Returns the objects who matche the expense
        """
        return Advices.objects.filter(Expense = expenseName)
    
    @staticmethod
    def createNewObject( expenseName: str,
                        text: str):
        """
        Creates a new object and saves it to database.

        Args:
            - expenseName: name of expense
            - text: advice for each expense
        """
        obj = Advices(
            Expense = expenseName,
            Text = text )
        obj.save()

    def deleteObject(self):
        self.delete()

    