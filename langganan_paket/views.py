from django.shortcuts import render
from utils.db import data_from_db
from django.views.decorators.http import require_http_methods

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


def show_paket(request):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("SELECT jenis, harga FROM paket")
    paket = cur.fetchall()
    cur.close()
    conn.close()
    return render(request, 'langganan_paket.html',  {'paket': paket})