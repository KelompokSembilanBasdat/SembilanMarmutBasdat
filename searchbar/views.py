from django.shortcuts import render

# Create your views here.
def show_hasil_searchbar(request):

    return render(request, 'result.html')