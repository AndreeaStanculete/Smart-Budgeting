from django.db import models

class OneTimeLink(models.Model):
    UniqueCode = models.CharField(max_length=20)
    AssociatedEMail = models.CharField(max_length=50)

    @staticmethod
    def createNewObject(email: str, code: str):
        """
        Creates a new one time link and saves it to database

        Args:
            - email: the email associated with the link
            - code: the unique code of the link
        """
        obj = OneTimeLink(UniqueCode = code, AssociatedEMail = email)
        obj.save()

    @staticmethod
    def isValid(code: str) -> bool:
        """
        Validates the code of the link

        Args:
            - code: the unique code of the link
        """
        try:
            _ = OneTimeLink.objects.get(UniqueCode = code)
            return True
        except OneTimeLink.DoesNotExist:
            return False

    @staticmethod
    def deleteObject(code: str):
        """
        Deletes the one-time link

        Args:
            - code: the unique code of the link
        """
        try:
            obj = OneTimeLink.objects.get(UniqueCode = code)
            obj.delete()
        except OneTimeLink.DoesNotExist:
            pass
