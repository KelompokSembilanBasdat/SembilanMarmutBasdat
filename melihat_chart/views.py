from django.shortcuts import render

# Create your views here.
def chart(request):
    return render(request, 'Chart.html')

def chart_detail(request):
    return render(request, 'ChartDetail.html')