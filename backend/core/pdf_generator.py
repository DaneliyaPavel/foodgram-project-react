from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from recipes.models import IngredientInRecipe


def pdf_shopping_list_generator(user):
    """
    Метод для генерации pdf файла из рецепта
    в корзине пользователя.
    """
    shopping_list = IngredientInRecipe.objects.filter(
        recipe__cart_recipe__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
    ).annotate(amount=Sum('amount')).order_by()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"'
    )
    pdfmetrics.registerFont(TTFont(
        'OpenSans-Light', 'media/fonts/opensansr.ttf'
    ))
    pdfmetrics.registerFont(TTFont(
        'OpenSans-Regular', 'media/fonts/opensansl.ttf'
    ))
    page = Canvas(filename=response)
    page.setFont('OpenSans-Regular', 24)
    page.drawString(210, 800, 'Список покупок')
    page.setFont('OpenSans-Light', 14)
    height = 760
    is_page_done = False
    for idx, ingr in enumerate(shopping_list, start=1):
        is_page_done = False
        page.drawString(60, height, text=(
            f'{idx}. {ingr["ingredient__name"]} - {ingr["amount"]} '
            f'{ingr["ingredient__measurement_unit"]}'
        ))
        height -= 30
        if height <= 40:
            page.showPage()
            is_page_done = True
    if not is_page_done:
        page.showPage()
    page.save()
    return response
