from django.urls import path

from . import views

urlpatterns = [
    # --- Finances operations ---
    path("finance/periodical/update", views.UpdatePeriodicalFinanceData, name="Update peridocal finances"),
    path("finance/update", views.UpdateFinanceData, name="Update existing finances"),

    # --- Account operations ---
    path("account/export_data", views.ExportUserData, name="Export Data"),
    path("account/change_month", views.UpdateSiteInformation, name="Update month to display"),
    path("account/update", views.UpdateAccountInformation, name="Update account settings"),
    path("account/login", views.AuthenticateAccount, name="User authentication"),
    path("account/register", views.RegisterAccount, name="User registration"),
    path("account/logout", views.DeauthenticateAccount, name="User de-authentication"),
    path("account/password_reset/<str:code>", views.ChangeAccountPassword, name="User change password"),
    path("account/generate_unique_link", views.GenerateOneTimeLink, name="Generate unique link"),

    # --- Visible pages ---
    path("learn/smart_budgeting", views.DisplaySiteInformation, name="Learn more about the app"),
    path("learn/tips", views.DisplayBudgetingTips, name="Learn more about budgeting"),

    path("main/profile", views.DisplayUserProfile, name="Display user profile"),
    path("main", views.DisplayUserData, name="Display main page"),

    path("", views.Index, name="Display default page"),
]