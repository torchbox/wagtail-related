from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^suggest_on_edit/(?P<pk>\d+)/$', views.SuggestTagsOnEditView.as_view(), name='suggest_tags_on_edit'),
    url(r'^suggest_on_create/(?P<parent_pk>\d+)/$', views.SuggestTagsOnCreateView.as_view(), name='suggest_tags_on_create'),
]
