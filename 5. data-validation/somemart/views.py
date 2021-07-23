import json

from django.views.decorators.csrf import csrf_exempt
from marshmallow import Schema, fields
from marshmallow.validate import Length, Range
from marshmallow.exceptions import ValidationError
from django.utils.decorators import method_decorator


from django.http import HttpResponse, JsonResponse
from django.views import View

from .models import Item, Review


class AddItemReviewSchema(Schema):
    title = fields.Str(validate=Length(1, 64), required=True)
    description = fields.Str(validate=Length(1, 1024), required=True)
    price = fields.Int(validate=Range(1, 1000000), required=True)


class PostReviewReviewSchema(Schema):
    text = fields.Str(validate=Length(1, 1024), required=True)
    grade = fields.Int(validate=Range(1, 10), required=True)


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            schema = AddItemReviewSchema(strict=True)
            document = schema.loads(request.body)
            data = schema.load(document.data).data
            pk = Item.objects.create(title=data['title'], description=data['description'],
                                     price=int(data['price'])).pk
            return JsonResponse({'id': pk}, status=201)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)


@method_decorator(csrf_exempt, name='dispatch')
class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        try:
            schema = PostReviewReviewSchema(strict=True)
            document = schema.loads(request.body)
            data = schema.load(document.data).data
            Item.objects.get(pk=item_id)
            pk = Review.objects.create(text=data['text'], grade=int(data['grade']), item_id=item_id).pk
            return JsonResponse({'id': pk}, status=201)
        except json.JSONDecodeError:
            return HttpResponse(status=400)
        except ValidationError:
            return HttpResponse(status=400)
        except Item.DoesNotExist:
            return HttpResponse(status=404)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        try:
            item = Item.objects.get(pk=item_id)
            reviews = [{'id': review.pk, 'text': review.text, 'grade': review.grade}
                       for review in Review.objects.filter(item_id=item_id).order_by('-pk')[:5]]
            response = {'id': item.pk, 'title': item.title, 'description': item.description,
                        'price': item.price, 'reviews': reviews}
            return JsonResponse(response, status=200)
        except Item.DoesNotExist:
            return HttpResponse(status=404)
