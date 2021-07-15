from django.urls import path

from . import views

app_name = 'playerinterface'

urlpatterns = [
    path('', views.index, name='index'),
    path('download_youtube/', views.download_youtube,
         name='download_youtube'),
    path('upload_song/', views.upload_song,
         name='upload_song'),
    path('delete_song/', views.delete_song,
         name='delete_song'),
    path('<int:settings_id>/change_play/', views.change_play,
         name='change_play'),
    path('<int:settings_id>/change_volume/', views.change_volume,
         name='change_volume'),
    path('<int:settings_id>/change_loop/', views.change_loop,
         name='change_loop'),
    path('<int:settings_id>/change_timer/', views.change_timer,
         name='change_timer'),
    path('<int:settings_id>/change_random/', views.change_random,
         name='change_random'),
]
