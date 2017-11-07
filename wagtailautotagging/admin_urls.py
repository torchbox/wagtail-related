from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+)/$', views.SuggestTagsView.as_view(), name='suggest_tags'),
]
