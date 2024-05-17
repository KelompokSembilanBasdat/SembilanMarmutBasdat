from django.shortcuts import render
from django.http import Http404
from utils.db import data_from_db

def daftar_chart(request):
    con = data_from_db()
    cur = con.cursor()
    
    # Query untuk mendapatkan daftar chart
    cur.execute("SELECT id, nama, tipe FROM Chart")
    charts = cur.fetchall()
    
    context = {
        'charts': charts
    }
    
    return render(request, 'Chart.html', context)

def detail_chart_daily(request, chart_id):
    con = data_from_db()
    cur = con.cursor()
    
    # Query untuk mendapatkan detail chart
    cur.execute("SELECT nama, tipe, deskripsi FROM Chart WHERE id = %s AND tipe = 'daily'", (chart_id,))
    chart = cur.fetchone()
    
    if not chart:
        raise Http404("Chart tidak ditemukan")
    
    chart_name, chart_type, chart_description = chart
    
    # Query untuk mendapatkan tanggal awal (hari ini)
    cur.execute("SELECT CURRENT_DATE")
    start_date = cur.fetchone()[0]
    
    # Query untuk mendapatkan daftar lagu dalam chart harian
    cur.execute("""
        SELECT Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis, SUM(PlayLog.jumlah_play) AS total_play
        FROM Lagu
        JOIN PlayLog ON Lagu.id = PlayLog.lagu_id
        WHERE PlayLog.tanggal >= %s
        GROUP BY Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis
        HAVING SUM(PlayLog.jumlah_play) > 0
        ORDER BY total_play DESC
        LIMIT 20
    """, (start_date,))
    lagu_list = cur.fetchall()
    
    context = {
        'chart': chart,
        'lagu_list': lagu_list
    }
    
    return render(request, 'ChartDetailDaily.html', context)

def detail_chart_weekly(request, chart_id):
    con = data_from_db()
    cur = con.cursor()
    
    # Query untuk mendapatkan detail chart
    cur.execute("SELECT nama, tipe, deskripsi FROM Chart WHERE id = %s AND tipe = 'daily'", (chart_id,))
    chart = cur.fetchone()
    
    if not chart:
        raise Http404("Chart tidak ditemukan")
    
    chart_name, chart_type, chart_description = chart
    
    # Query untuk mendapatkan tanggal awal (hari ini)
    cur.execute("SELECT CURRENT_DATE")
    start_date = cur.fetchone()[0]
    
    # Query untuk mendapatkan daftar lagu dalam chart harian
    cur.execute("""
        SELECT Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis, SUM(PlayLog.jumlah_play) AS total_play
        FROM Lagu
        JOIN PlayLog ON Lagu.id = PlayLog.lagu_id
        WHERE PlayLog.tanggal >= %s
        GROUP BY Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis
        HAVING SUM(PlayLog.jumlah_play) > 0
        ORDER BY total_play DESC
        LIMIT 20
    """, (start_date,))
    lagu_list = cur.fetchall()
    
    context = {
        'chart': chart,
        'lagu_list': lagu_list
    }
    
    return render(request, 'ChartDetailWeekly.html', context)

def detail_chart_monthly(request, chart_id):
    con = data_from_db()
    cur = con.cursor()
    
    # Query untuk mendapatkan detail chart
    cur.execute("SELECT nama, tipe, deskripsi FROM Chart WHERE id = %s AND tipe = 'daily'", (chart_id,))
    chart = cur.fetchone()
    
    if not chart:
        raise Http404("Chart tidak ditemukan")
    
    chart_name, chart_type, chart_description = chart
    
    # Query untuk mendapatkan tanggal awal (hari ini)
    cur.execute("SELECT CURRENT_DATE")
    start_date = cur.fetchone()[0]
    
    # Query untuk mendapatkan daftar lagu dalam chart harian
    cur.execute("""
        SELECT Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis, SUM(PlayLog.jumlah_play) AS total_play
        FROM Lagu
        JOIN PlayLog ON Lagu.id = PlayLog.lagu_id
        WHERE PlayLog.tanggal >= %s
        GROUP BY Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis
        HAVING SUM(PlayLog.jumlah_play) > 0
        ORDER BY total_play DESC
        LIMIT 20
    """, (start_date,))
    lagu_list = cur.fetchall()
    
    context = {
        'chart': chart,
        'lagu_list': lagu_list
    }
    
    return render(request, 'ChartDetailMonthly.html', context)

def detail_chart_yearly(request, chart_id):
    con = data_from_db()
    cur = con.cursor()
    
    # Query untuk mendapatkan detail chart
    cur.execute("SELECT nama, tipe, deskripsi FROM Chart WHERE id = %s AND tipe = 'daily'", (chart_id,))
    chart = cur.fetchone()
    
    if not chart:
        raise Http404("Chart tidak ditemukan")
    
    chart_name, chart_type, chart_description = chart
    
    # Query untuk mendapatkan tanggal awal (hari ini)
    cur.execute("SELECT CURRENT_DATE")
    start_date = cur.fetchone()[0]
    
    # Query untuk mendapatkan daftar lagu dalam chart harian
    cur.execute("""
        SELECT Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis, SUM(PlayLog.jumlah_play) AS total_play
        FROM Lagu
        JOIN PlayLog ON Lagu.id = PlayLog.lagu_id
        WHERE PlayLog.tanggal >= %s
        GROUP BY Lagu.id, Lagu.judul, Lagu.artis, Lagu.tanggal_rilis
        HAVING SUM(PlayLog.jumlah_play) > 0
        ORDER BY total_play DESC
        LIMIT 20
    """, (start_date,))
    lagu_list = cur.fetchall()
    
    context = {
        'chart': chart,
        'lagu_list': lagu_list
    }
    
    return render(request, 'ChartDetailYearly.html', context)





