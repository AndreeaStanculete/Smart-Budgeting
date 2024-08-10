from django.db import models

class Currencies(models.Model):
    Name = models.CharField(max_length=50)
    # toEur = models.FloatField() 
    # fromEur = models.FloatField() 

    @staticmethod
    def getObjects() -> list:
        """
        Returns all objects from table
        """
        return Currencies.objects.all()
    
    def getObjectByName( name: str ):
        """
        Returns one object who matches the name
        """
        return Currencies.objects.filter(Name = name)
    
    @staticmethod
    def createNewObject( name: str ):
                        # toE: float,
                        # fromE: float ):
        """
        Creates a new object and saves it to database.

        Args:
            - Name: name of currency
            - toE: exchange rate to Eur
            - fromE: exchange rate from Eur
        """
        obj = Currencies(
            Name = name)
            # toEur = toE,
            # fromEur = fromE )
        obj.save()

    def deleteObject(self):
        self.delete()

    