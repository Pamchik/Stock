from django.urls import path
from . import views


urlpatterns = [
   path('home/', views.home, name='home'),
   path('', views.home, name='home'),
   path('stock/', views.stock, name='stock'),
   path('history/', views.history, name='history'),
   path('create/', views.create, name='create'),
   # path('stock/<str:category>/', views.stock, name='stock-category'),
   path('stock/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),
   # path('stock/<str:category>/<str:slug>/', views.CategoryDetailView.as_view(), name='product-detail'),

   # path('stock/<int:pk>/', views.stock_category_filter, name='category-filter'),
   path('stock/<int:pk>/update/', views.ProductUpdateView.as_view(), name='product-update'),
   path('stock/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
   path('stock/<int:pk>/add/', views.AddQtyView.as_view(), name='add-qty')
]
