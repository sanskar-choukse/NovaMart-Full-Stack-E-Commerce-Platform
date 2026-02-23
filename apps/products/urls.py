from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('shop/', views.ProductListView.as_view(), name='shop'),
    path('category/<slug:slug>/', views.ProductListView.as_view(), name='category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='detail'),
    path('search/', views.search_view, name='search'),
]
