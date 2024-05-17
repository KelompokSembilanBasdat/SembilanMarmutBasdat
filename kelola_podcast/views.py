from django.shortcuts import render

# Create your views here.
def podcast_management(request):
    return render(request, 'PodcastManagement.html')

def podcast_episode_management(request):
    return render(request, 'PodcastEpisodeManagement.html')