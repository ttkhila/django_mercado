from django.urls import path
from . import views

urlpatterns = [
    path('', views.mercado_index, name='mercado'),
    path('index', views.mercado_index, name='index'),
    path('novaLista', views.nova_lista, name='novaLista'),
    path('createList', views.create_list, name='createList'),
    path('showList/<int:id>/', views.show_list, name='showList'),
    path('newMarketInList', views.new_market_list, name='newMarketInList'),
    path('newBrandInList', views.new_brand_list, name='newBrandInList'),
    path('newPrice', views.new_price, name='newPrice'),
    path('newBrand', views.new_brand_created, name='newBrand'),
    path('newProductInList', views.new_product_list, name='newProductInList'),
    path('insertProductsList', views.insert_products_in_list, name='insertProductsList'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),

    # initial data insert
    #path('initialInsertDb', views.initialInserts, name='initialInsertDb'),
] 