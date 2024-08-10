from django.views.decorators.http import require_safe
from django.shortcuts import render

from budgetingApp.decorators.security import require_authentication


@require_safe
@require_authentication(required=False, redirect_url="/main")
def DisplaySiteInformation(request):
    return render(request, 'learn_more.html')

@require_safe
def DisplayBudgetingTips(request):
    context = {
        "tips": [
            "Save at least 10% of your income and set it aside for retirement.                                                          \
                        Do not touch it until you are satisfied and believe you can live within 5% of it per year.",
            "Establish a basic budget and do not spend more than you bring.",
            "Create an emergency fund that can cover at least 3 months of your expenses if in need.",
            "Do not take on debt unless it's for a house. Nothing else is that important.",
            "But if you do have debt, focus on paying it as fast as possible. Make it a priority.",
            "If with a partner, make sure all your expenses are covered within the lower salary.                                        \
                        This way, no matter what happens, you can still pay your necessities.",
            "Rathen than buying 10 shirts each year, buy 1 or 2 quality products that will last you longer.",
            "If you can not afford to buy something 10 times, then you should not buy it once (with very few exceptions).",
            "Make better choices. Rather than spending 5.000$ on vacation,                                                              \
                        choose to spend 2.500$ and use the rest for something else, like debt or for investing.",
            "Always bring a water bottle with you.",
            "Make sure to eat before going shopping. This will save you money on dining out and on unnecessary groceries.",
            "Shop for clothes at the end of the season when they have discounts.",
            "Count for each product you buy, how it 'pays' for itself.                                                                  \
                        If you get a pair of shoes for 50$ and you wear them everyday, 7 times/week for 3 months (roughly 80 wears)     \
                        the costm is already at 50 / 80 = 0,62$ per wear.",
            "Certain books are cheaper on Kindle and it saves you space.",
            "Look for the best deals and buy in bulk. It is usually cheaper.",
            "If possible, rather than using the car everytime, choose to walk, take the bus or use a bike.",
            "Don't waste money on fancy clothes and lots of toys for children. They grow up too fast for you to keep pace.",
            "Do not subscribe for entertainment platforms unless you really use them."
        ]
    }

    if request.user.is_authenticated:
        context["logged_in"] = 1

    return render(request, 'tips.html', context=context)