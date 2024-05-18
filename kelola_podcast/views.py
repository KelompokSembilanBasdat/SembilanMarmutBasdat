from django.shortcuts import render, redirect
from utils.db import data_from_db

def podcast_list(request):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("""
        SELECT Podcast.id, Podcast.title, COUNT(Episode.id) AS episode_count, SUM(Episode.duration) AS total_duration 
        FROM Podcast 
        LEFT JOIN Episode ON Podcast.id = Episode.podcast_id 
        GROUP BY Podcast.id, Podcast.title
    """)
    podcasts = cur.fetchall()
    return render(request, 'PodcastManagement.html', {'podcasts': podcasts})

def create_podcast(request):
    if request.method == 'POST':
        con = data_from_db()
        cur = con.cursor()
        title = request.POST.get('title')
        genre = request.POST.getlist('genre')
        cur.execute("INSERT INTO Podcast (title, genre) VALUES (%s, %s)", (title, ','.join(genre)))
        con.commit()
        return redirect('podcast_management')
    else:
        return render(request, 'PodcastManagement.html')

def view_podcast(request, podcast_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM Podcast WHERE id = %s", (podcast_id,))
    podcast = cur.fetchone()
    # Fetch episodes for the podcast
    cur.execute("SELECT * FROM Episode WHERE podcast_id = %s", (podcast_id,))
    episodes = cur.fetchall()
    return render(request, 'PodcastEpisodeManagement.html', {'podcast': podcast, 'episodes': episodes})

def delete_podcast(request, podcast_id):
    if request.method == 'POST':
        con = data_from_db()
        cur = con.cursor()
        cur.execute("DELETE FROM Podcast WHERE id = %s", (podcast_id,))
        con.commit()
        return redirect('podcast_management')
    
def view_episode(request, podcast_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("SELECT * FROM Episode WHERE podcast_id = %s", (podcast_id,))
    episodes = cur.fetchall()
    
    context = {
        'episodes': episodes
    }
    return render(request, 'PodcastEpisodeManagement.html', context)

def add_episode(request, podcast_id):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        duration = request.POST['duration']
        
        con = data_from_db()
        cur = con.cursor()
        cur.execute("INSERT INTO Episode (title, description, duration, podcast_id) VALUES (%s, %s, %s, %s)",
                    (title, description, duration, podcast_id))
        con.commit()
        
        return redirect('view_episode', podcast_id=podcast_id)
    else:
        return render(request, 'PodcastEpisodeManagement.html')
    
def delete_episode(request, episode_id):
    con = data_from_db()
    cur = con.cursor()
    cur.execute("DELETE FROM Episode WHERE id = %s", (episode_id,))
    con.commit()
    return redirect(request.META.get('HTTP_REFERER', 'podcast_episode_management'))
