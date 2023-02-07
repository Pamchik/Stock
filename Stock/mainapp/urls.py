from django.urls import path
from . import views

urlpatterns = [
   path('', views.StockView.as_view(), name='stock'),
   path('table/', views.table, name='table'),
   path('history/', views.history, name='history'),
   path('create/', views.ProductCreateView.as_view(), name='create'),
   path('<str:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
   path('<str:slug>/update/', views.ProductUpdateView.as_view(), name='product-update'),
   path('<str:slug>/delete/', views.ProductDeleteView.as_view(), name='product-delete'),
   path('<str:slug>/add/', views.AddQtyView.as_view(), name='add-qty'),
   path('<str:slug>/move/', views.MoveQtyView, name='move-qty'),
   path('<str:slug>/write-off/', views.WriteOffQtyView.as_view(), name='write-off-qty'),
]
