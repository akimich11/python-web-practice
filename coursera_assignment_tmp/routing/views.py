from django.http import HttpResponse
from django.views.decorators.http import require_GET, require_POST


def simple_route(request):
	if request.method == 'GET':
		return HttpResponse(status=200)
	return HttpResponse(status=405)


def slug_route(request, slug):
	return HttpResponse(slug)


def sum_route(request, a, b):
	return HttpResponse(str(int(a) + int(b)))


@require_GET
def sum_get_method(request):
	a = request.GET.get('a', '')
	b = request.GET.get('b', '')
	if (not a.strip('-').isdigit()) or (not b.strip('-').isdigit()):
		return HttpResponse(status=400)
	return HttpResponse(str(int(a) + int(b)))


@require_POST
def sum_post_method(request):
	a = request.POST.get('a', '')
	b = request.POST.get('b', '')
	if (not a.strip('-').isdigit()) or (not b.strip('-').isdigit()):
		return HttpResponse(status=400)
	return HttpResponse(str(int(a) + int(b)))
