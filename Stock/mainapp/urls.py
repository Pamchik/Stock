from django.urls import path
from . import views

# app_name = 'Stock'
urlpatterns = [
   path('home/', views.home, name='home'),
   path('', views.home, name='home'),
   # path('test/', views.test, name='test'),
   path('stock/', views.stock, name='stock'),
   path('history/', views.history, name='history'),
   path('create/', views.ProductCreateView.as_view(), name='create'),
   path('stock/<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
   path('stock/<str:slug>/update/', views.ProductUpdateView.as_view(), name='product-update'),
   path('stock/<str:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
   path('stock/<str:slug>/add/', views.AddQtyView.as_view(), name='add-qty'),
   path('stock/<str:slug>/move/', views.MoveQtyView, name='move-qty'),
   path('stock/<str:slug>/write-off/', views.WriteOffQtyView.as_view(), name='write-off-qty'),
   # path('test/', views.export_data, name='test'),


]
