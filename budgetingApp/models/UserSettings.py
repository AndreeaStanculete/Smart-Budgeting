from django.contrib.auth.models import User
from django.db import models

class UserSettings(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Picture = models.CharField(max_length=100)
    Currency = models.CharField(max_length=50)


    @staticmethod
    def getObjectsByUser(user: User) -> list:
        """
        Returns all objects belonging to a specific user.

        Args:
            - user (User): The user to lookup
        """
        return UserSettings.objects.filter(User = user)

    @staticmethod
    def createNewObject(username: str, email: str, password: str) -> User:
        """
        Creates a new User object and its associated settings and saves it to database.

        Args:
            - user (User): The current user
        """
        user = User.objects.create_user(username, email, password)
        user.save()
        
        obj = UserSettings(
            User = user, 
            Currency = 'EUR',
            Picture = "/static/data/images/avatars/male_avatar.svg"
        )
        obj.save()

        return user

    @staticmethod
    def createNewUser(username: str, email: str, password: str):
        user = User.objects.create_user(username, email, password)
        user.save()

    def updateProfilePicture(self, pictureURL: str):
        """
        Updates the profile picture of a user.

        Args:
            - pictureURL (str): The URL of the new picture
        """
        self.Picture = pictureURL
        self.save()

    def updateCurrency(self, currency: str):
        """
        Updates the main currency of a user.

        Args:
            - currency (str): The new currency
        """
        self.Currency = currency
        self.save()