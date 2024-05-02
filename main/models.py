import uuid
from django.db import models
from uuid import uuid4

# Create your models here.
class Akun(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=50)
    nama = models.CharField(max_length=100)
    gender = models.IntegerField(choices=((0, 'Female'), (1, 'Male')))
    tempat_lahir = models.CharField(max_length=50)
    tanggal_lahir = models.DateField()
    is_verified = models.BooleanField(default=False)
    kota_asal = models.CharField(max_length=50)

class Paket(models.Model):
    jenis = models.CharField(max_length=50, primary_key=True)
    harga = models.IntegerField()

class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    jenis_paket = models.ForeignKey(Paket, on_delete=models.CASCADE)
    email = models.ForeignKey(Akun, on_delete=models.CASCADE)
    timestamp_dimulai = models.DateTimeField()
    timestamp_berakhir = models.DateTimeField()
    metode_bayar = models.CharField(max_length=50)
    nominal = models.IntegerField()

class Premium(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE, primary_key=True)

class NonPremium(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE, primary_key=True)


class Konten(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    tanggal_rilis = models.DateField()
    tahun = models.IntegerField()
    durasi = models.IntegerField()

class Genre(models.Model):
    id_konten = models.ForeignKey(Konten, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50)

    class Meta:
        unique_together = ('id_konten', 'genre')

class Podcaster(models.Model):
    email = models.OneToOneField(Akun, on_delete=models.CASCADE, primary_key=True)

class Podcast(models.Model):
    id_konten = models.OneToOneField(Konten, on_delete=models.CASCADE, primary_key=True)
    email_podcaster = models.ForeignKey(Podcaster, on_delete=models.CASCADE)

class Episode(models.Model):
    id_episode = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    id_konten_podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    judul = models.CharField(max_length=100)
    deskripsi = models.CharField(max_length=500)
    durasi = models.IntegerField()
    tanggal_rilis = models.DateField()

class PemilikHakCipta(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    rate_royalti = models.IntegerField()

class Artist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email_akun = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)

class Songwriter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email_akun = models.ForeignKey(Akun, on_delete=models.CASCADE)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)

class Label(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    nama = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    kontak = models.CharField(max_length=50)
    id_pemilik_hak_cipta = models.ForeignKey(PemilikHakCipta, on_delete=models.CASCADE)

class Album(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    judul = models.CharField(max_length=100)
    jumlah_lagu = models.IntegerField(default=0)
    id_label = models.ForeignKey(Label, on_delete=models.CASCADE)
    total_durasi = models.IntegerField(default=0)

class Song(models.Model):
    id_konten = models.OneToOneField(Konten, on_delete=models.CASCADE, primary_key=True)
    id_artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    id_album = models.ForeignKey(Album, on_delete=models.CASCADE)
    total_play = models.IntegerField(default=0)
    total_download = models.IntegerField(default=0)

class SongwriterWriteSong(models.Model):
    id_songwriter = models.ForeignKey(Songwriter, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_songwriter', 'id_song')


class DownloadedSong(models.Model):
    id_song = models.OneToOneField(Song, on_delete=models.CASCADE, primary_key=True)
    email_downloader = models.ForeignKey(Premium, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_song', 'email_downloader')


class Playlist(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Chart(models.Model):
    tipe = models.CharField(max_length=50, primary_key=True)
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)

class UserPlaylist(models.Model):
    email_pembuat = models.ForeignKey(Akun, on_delete=models.CASCADE, db_column='email_pembuat')
    id_user_playlist = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    judul = models.CharField(max_length=100, null=False)
    deskripsi = models.CharField(max_length=500, null=False)
    jumlah_lagu = models.IntegerField(null=False)
    tanggal_dibuat = models.DateField(null=False)
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    total_durasi = models.IntegerField(default=0, null=False)

    class Meta:
        unique_together = ('email_pembuat', 'id_user_playlist')

class Royalti(models.Model):
    id_pemilik_hak_cipta = models.OneToOneField(PemilikHakCipta, on_delete=models.CASCADE, primary_key=True)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    jumlah = models.IntegerField(null=False)

    class Meta:
        unique_together = ('id_pemilik_hak_cipta', 'id_song')


class AkunPlayUserPlaylist(models.Model):
    email_pemain = models.ForeignKey(Akun, on_delete=models.CASCADE, db_column='email_pemain')
    id_user_playlist = models.ForeignKey(UserPlaylist, on_delete=models.CASCADE)
    email_pembuat = models.ForeignKey(Akun, on_delete=models.CASCADE, related_name='playlist_creator')
    waktu = models.DateTimeField(primary_key=True)

    class Meta:
        unique_together = ('email_pemain', 'id_user_playlist', 'waktu')

class AkunPlaySong(models.Model):
    email_pemain = models.ForeignKey(Akun, on_delete=models.CASCADE, db_column='email_pemain')
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)
    waktu = models.DateTimeField(primary_key=True)

    class Meta:
        unique_together = ('email_pemain', 'id_song', 'waktu')

class PlaylistSong(models.Model):
    id_playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    id_song = models.ForeignKey(Song, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('id_playlist', 'id_song')
