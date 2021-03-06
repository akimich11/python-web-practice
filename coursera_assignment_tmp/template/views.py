from django.shortcuts import render


# Create your views here.

def echo(request):
    return render(request, 'echo.html', context={
        'get': request.GET,
        'post': request.POST,
        'x': request.META.get('HTTP_X_PRINT_STATEMENT', '')
    }, status=200)


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
