from django.contrib import admin
from .models import Mercado, Unidade, Categoria, Marca, Produto, ListaCompra, ProdutoLista

class ProdutoAdmin(admin.ModelAdmin):
    list_filter = ['nome', 'unidade', 'categoria']
    list_display = ['nome', 'categoria', 'unidade']
    search_fields = [ "nome", "categoria__nome" ]

class CategoriaAdmin(admin.ModelAdmin):
    list_filter = [ 'nome' ]
    search_fields = [ "nome" ]

class MarcaAdmin(admin.ModelAdmin):
    list_filter = [ 'nome' ]
    search_fields = [ "nome" ]

class MercadoAdmin(admin.ModelAdmin):
    list_filter = [ 'nome' ]
    search_fields = [ "nome" ]

class UnidadeAdmin(admin.ModelAdmin):
    list_filter = [ 'nome' ]
    search_fields = [ "nome" ]

class ListaCompraAdmin(admin.ModelAdmin):
    list_filter = [ 'nome', 'data_criacao', 'finalizada']
    list_filter = [ 'nome', 'data_criacao', 'finalizada' ]
    search_fields = [ 'nome', 'data_criacao', 'finalizada' ]

admin.site.register(Mercado, MercadoAdmin)
admin.site.register(Unidade, UnidadeAdmin)
admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(ListaCompra, ListaCompraAdmin)
admin.site.register(ProdutoLista)


