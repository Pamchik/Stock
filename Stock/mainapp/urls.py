from django.urls import path
from . import views


urlpatterns = [
   path('home/', views.home, name='home'),
   path('', views.home, name='home'),
   path('stock/', views.stock, name='stock'),
   path('history/', views.history, name='history'),
   path('create/', views.create, name='create'),
   # path('stock/<str:pk>/', views.stock, name='stock-category'),det_view
   path('stock/<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
   # path('stock/<str:category>/<str:slug>/', views.CategoryDetailView.as_view(), name='product-detail'),

   # path('stock/<int:pk>/', views.stock_category_filter, name='category-filter'),
   path('stock/<str:slug>/update/', views.ProductUpdateView.as_view(), name='product-update'),
   path('stock/<str:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
   path('stock/<str:slug>/add/', views.AddQtyView.as_view(), name='add-qty')
]
