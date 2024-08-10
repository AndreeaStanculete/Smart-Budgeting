from django.db import models

class Expenses(models.Model):
    Name = models.CharField(max_length=50)

    @staticmethod
    def getObjects() -> list:
        """
        Returns all objects from table
        """
        return Expenses.objects.all()
    
    @staticmethod
    def createNewObject(name: str):
        """
        Creates a new object and saves it to database.

        Args:
            - name: name of the expense
        """
        obj = Expenses(Name = name)
        obj.save()

    def deleteObject(self):
        self.delete()

    