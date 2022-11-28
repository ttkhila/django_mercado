from django.contrib import admin
from .models import Mercado, Unidade, Categoria, Marca, Produto, ListaCompra, ProdutoLista

admin.site.register(Mercado)
admin.site.register(Unidade)
admin.site.register(Categoria)
admin.site.register(Marca)
admin.site.register(Produto)
# admin.site.register(ProdutoMarca)
admin.site.register(ListaCompra)
admin.site.register(ProdutoLista)
