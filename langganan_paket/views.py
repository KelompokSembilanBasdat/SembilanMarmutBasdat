from django.shortcuts import render, redirect
from django.http import HttpResponse
from utils.db import data_from_db
import uuid
import datetime

def show_paket(request):
    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM paket")
    paket_list = cur.fetchall()
    cur.close()
    conn.close()

    context = {
        'paket_list': [{'jenis': paket[0], 'harga': paket[1]} for paket in paket_list]
    }

    return render(request, 'langganan_paket.html', context)

def laman_pembayaran_view(request):
    if request.method == 'POST':
        jenis_paket = request.POST.get('jenis')
        harga = request.POST.get('harga')
        metode_pembayaran = ['Credit Card', 'Bank Transfer', 'PayPal']

        context = {
            'jenis': jenis_paket,
            'harga': harga,
            'metode_pembayaran': metode_pembayaran
        }

        return render(request, 'laman_pembayaran.html', context)
    return redirect('show_paket')

def pembayaran(request):
    if request.method == 'POST':
        email = request.session.get('email')
        jenis_paket = request.POST.get('jenis')
        nominal = request.POST.get('harga')
        metode_bayar = request.POST.get('metode')

        transaction_id = str(uuid.uuid4())

        conn = data_from_db()
        cur = conn.cursor()

        try:
            if jenis_paket == '1 bulan':
                end_time = datetime.datetime.now() + datetime.timedelta(days=30)
            elif jenis_paket == '3 bulan':
                end_time = datetime.datetime.now() + datetime.timedelta(days=90)
            elif jenis_paket == '6 bulan':
                end_time = datetime.datetime.now() + datetime.timedelta(days=180)
            elif jenis_paket == '1 tahun':
                end_time = datetime.datetime.now() + datetime.timedelta(days=365)

            cur.execute("""
                INSERT INTO transaction (id, jenis_paket, email, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal)
                VALUES (%s, %s, %s, NOW(), %s, %s, %s)
            """, (transaction_id, jenis_paket, email, end_time, metode_bayar, nominal))
            conn.commit()
        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return render(request, 'laman_pembayaran.html', {
                'error_message':  str(e).split('CONTEXT:')[0].strip(),
                'jenis': jenis_paket,
                'harga': nominal,
                'metode_pembayaran': ['Credit Card', 'Bank Transfer', 'PayPal']
            })

        cur.close()
        conn.close()

        return redirect('dashboard')
    return redirect('show_paket')

def riwayat_transaksi_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('login')

    conn = data_from_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT jenis_paket, timestamp_dimulai, timestamp_berakhir, metode_bayar, nominal
        FROM transaction
        WHERE email = %s
        ORDER BY timestamp_dimulai DESC
    """, (email,))
    transaksi_list = cur.fetchall()
    cur.close()
    conn.close()

    context = {
        'transaksi_list': [{'jenis_paket': transaksi[0], 'timestamp_dimulai': transaksi[1], 'timestamp_berakhir': transaksi[2], 'metode_bayar': transaksi[3], 'nominal': transaksi[4]} for transaksi in transaksi_list]
    }

    return render(request, 'riwayat_transaksi.html', context)