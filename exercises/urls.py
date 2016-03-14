from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^exercises/$', views.index, name='exercise_index'),
    url(r'^exercises/(?P<exercise_tag>[0-9.]+)/$', views.detail, name='exercise_detail'),
    url(r'^exercises/(?P<exercise_tag>[0-9.]+)/last_submission/$', views.last_submission, name='exercise-last_submission'),
    url(r'^exercises/(?P<exercise_tag>[0-9.]+)/submit', views.submit_solution, name='submit-solution'),
    url(r'^bonus/(?P<secret>[a-zA-Z0-9]+)$', views.bonuslink),
]
