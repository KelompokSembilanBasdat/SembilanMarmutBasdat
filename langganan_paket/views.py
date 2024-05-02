from django.shortcuts import render
from main.models import Paket
from django.views.decorators.http import require_http_methods

# Create your views here.
def show_paket(request):
    pakets = Paket.objects.all()
    return render(request, 'langganan_paket.html', {'pakets': pakets})

@require_http_methods(["POST"])
def pembayaran(request):
    jenis = request.POST.get('jenis')
    harga = request.POST.get('harga')
    metode_pembayaran = ['Debit Card', 'Credit Card', 'PayPal', 'Bank Transfer', 'Gopay', 'Shopee']
    return render(request, 'laman_pembayaran.html', {
        'jenis': jenis,
        'harga': harga,
        'metode_pembayaran': metode_pembayaran
    })
