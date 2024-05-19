from django.shortcuts import render, redirect
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

        cur.execute("SELECT * FROM akun WHERE email=%s AND password=%s", (email, password))
        user = cur.fetchone()
        
        if not user:
            cur.execute("SELECT * FROM label WHERE email=%s AND password=%s", (email, password))
            label = cur.fetchone()
            if label:
                request.session['email'] = label[2]
                request.session['roles'] = get_user_roles(label[2])
                request.session['is_premium'] = False
                cur.close()
                conn.close()
                return redirect('dashboard')
        else:
            request.session['email'] = user[0]
            request.session['roles'] = get_user_roles(user[0])
            request.session['is_premium'] = user[7]
            cur.close()
            conn.close()
            return redirect('dashboard')
 
        cur.close()
        conn.close()
        return render(request, 'login.html', {'error_message':  'Password yang Anda masukan SALAH'})

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
        roles = request.POST.getlist('role')

        conn = data_from_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT email FROM akun WHERE email=%s UNION SELECT email FROM label WHERE email=%s", (email, email))

            if len(roles) > 0:
                is_verified = True
            else:
                is_verified = False

            cur.execute("""
                INSERT INTO akun (email, password, nama, gender, tempat_lahir, tanggal_lahir, kota_asal, is_verified)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (email, password, name, gender, birthplace, birthdate, hometown, is_verified))

            for role in roles:
                user_id = str(uuid.uuid4())
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

        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return render(request, 'register_pengguna.html', {'error_message':  str(e).split('CONTEXT:')[0].strip()})
        
    
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

        conn = data_from_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT email FROM akun WHERE email=%s UNION SELECT email FROM label WHERE email=%s", (email, email))

            id_pemilik_hak_cipta = str(uuid.uuid4())
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

        except Exception as e:
            conn.rollback()
            cur.close()
            conn.close()
            return render(request, 'register_label.html', {'error_message':  str(e).split('CONTEXT:')[0].strip()})
    
        cur.close()
        conn.close()

        return redirect('login')
    return render(request, 'register_label.html')