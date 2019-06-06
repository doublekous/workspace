from django.shortcuts import render


def shishi(request):
    return render(request, 'shishi.html')