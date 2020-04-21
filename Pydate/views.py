from django.shortcuts import render


def base(request):
    return render(request, 'html_pages/base.html',  {})