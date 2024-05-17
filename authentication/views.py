from django.shortcuts import render, redirect
from django.http import HttpResponse
import uuid
import random

from utils.db import data_from_db
from main.views import get_user_roles


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        conn = data_from_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM akun WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            request.session['email'] = user[0]
            request.session['roles'] = get_user_roles(user[0])
            request.session['is_premium'] = user[7]
            return redirect('dashboard')
        else:
            return HttpResponse('Invalid login')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('login')


def regist_option_view(request):
    return render(request, 'register_option.html')


def register_pengguna_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        gender = request.POST['gender']
        birthplace = request.POST['birthplace']
        birthdate = request.POST['birthdate']
        hometown = request.POST['hometown']
        roles = request.POST.getlist('role')  # Multiple roles are allowed

        # Check if email already exists in either akun or label table
        conn = data_from_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT email FROM akun WHERE email=%s UNION SELECT email FROM label WHERE email=%s", (email, email))
        if cur.fetchone():
            cur.close()
            conn.close()
            return HttpResponse('Email sudah terdaftar')

        # Verified if roles are selected, else non-verified
        is_verified = len(roles) > 0

        cur.execute("""
            INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (email, password, name, gender, birthplace, birthdate, hometown, is_verified))

        for role in roles:
            user_id = str(uuid.uuid4())  # Generate unique UUID for user
            if role == 'Podcaster':
                cur.execute("""
                    INSERT INTO podcaster (email)
                    VALUES (%s)
                """, (email,))
            else:
                id_pemilik_hak_cipta = str(uuid.uuid4())
                rate_royalti = random.randint(500, 950)

                cur.execute("""
                    INSERT INTO pemilik_hak_cipta (id, rate_royalti)
                    VALUES (%s, %s)
                """, (id_pemilik_hak_cipta, rate_royalti))

                if role == 'Artist':
                    cur.execute("""
                        INSERT INTO artist (id, email_akun, id_pemilik_hak_cipta)
                        VALUES (%s, %s, %s)
                    """, (user_id, email, id_pemilik_hak_cipta))
                elif role == 'Songwriter':
                    cur.execute("""
                        INSERT INTO songwriter (id, email_akun, id_pemilik_hak_cipta)
                        VALUES (%s, %s, %s)
                    """, (user_id, email, id_pemilik_hak_cipta))

        conn.commit()
        cur.close()
        conn.close()

        return redirect('login')
    return render(request, 'register_pengguna.html')


def register_label_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        contact = request.POST['contact']

        # Check if email already exists in either akun or label table
        conn = data_from_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT email FROM akun WHERE email=%s UNION SELECT email FROM label WHERE email=%s", (email, email))
        if cur.fetchone():
            cur.close()
            conn.close()
            return HttpResponse('Email sudah terdaftar')

        # Generate a unique ID for pemilik_hak_cipta
        id_pemilik_hak_cipta = str(uuid.uuid4())
        # Generate a random royalty rate between 5 and 20
        rate_royalti = random.randint(500, 950)

        cur.execute("""
            INSERT INTO pemilik_hak_cipta (id, rate_royalti)
            VALUES (%s, %s)
        """, (id_pemilik_hak_cipta, rate_royalti))

        cur.execute("""
            INSERT INTO label (id, nama, email, password, kontak, id_pemilik_hak_cipta)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (str(uuid.uuid4()), name, email, password, contact, id_pemilik_hak_cipta))

        conn.commit()
        cur.close()
        conn.close()

        return redirect('login')
    return render(request, 'register_label.html')
