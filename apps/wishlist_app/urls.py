from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^dashboard$', views.dashboard),
    url(r'^create$', views.create),
    url(r'^add_item$', views.add_item),
    url(r'^myWishlist/(?P<id>\d+)$', views.myWishlist),
    url(r'^removeItem/(?P<id>\d+)$', views.removeItem),
    url(r'^deleteItem/(?P<wishlist_id>\d+)$', views.deleteItem),
    url(r'^wish_item/(?P<id>\d+)$', views.wish_item)
]