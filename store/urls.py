from django.urls import path
import store.views as views

urlpatterns = [
    path('', views.home, name='home'),
    path('store/', views.store, name='store'),
    path('store/category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('store/category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('store/search/', views.search, name='search'),
    path('submit_review/<int:product_id>/', views.submit_review, name='submit_review'),
]
