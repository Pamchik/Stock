from django.contrib.auth import views
# from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
   path('login/', views.LoginCustomView.as_view(), name='login'),
   path('logout/', views.LogoutView.as_view(), name='logout'),
   path('password-change/', views.PasswordChangeCustomView.as_view(), name='password_change'),
   path('password-change/done/', views.PasswordChangeDoneCustomView.as_view(), name='password_change_done'),


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
