from django.db import models

class Mercado(models.Model):
    nome = models.CharField(max_length=50, null=False)
    img = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.nome 

class Unidade(models.Model):
    nome = models.CharField(max_length=50, null=False)
    sigla = models.CharField(max_length=10, null=True)
    def __str__(self):
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=50, null=False)
    def __str__(self):
        return self.nome

class Marca(models.Model):
    nome = models.CharField(max_length=50, null=False)
    img = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=50, null=False)
    unidade = models.ForeignKey(Unidade, null=True, on_delete=models.SET_NULL)
    categoria = models.ForeignKey(Categoria, null=True, on_delete=models.SET_NULL)
    # marca = models.ForeignKey(Marcas, null=False, blank=True, on_delete=models.SET_DEFAULT, default=None) 
    def __str__(self):
        return self.nome
    
# class ProdutoMarca(models.Model):
#     produto = models.ForeignKey(Produto, null=False, on_delete=models.SET_DEFAULT, default='deleted')
#     marca = models.ForeignKey(Marca, null=False, blank=True, on_delete=models.SET_DEFAULT, default=None)
#     def __str__(self):
#         return self.produto 

class ListaCompra(models.Model):
    nome = models.CharField(max_length=100, null=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_fechamento = models.DateTimeField(auto_now=False, auto_now_add=False)
    finalizada = models.BooleanField(default=False)
    def __str__(self):
        return self.nome

class ProdutoLista(models.Model):
    # produto_marca = models.ForeignKey(ProdutoMarca, null=False, on_delete=models.SET_DEFAULT, default=0)
    produto = models.ForeignKey(Produto, null=False, on_delete=models.SET_DEFAULT, default=0) #pk1
    lista_compra = models.ForeignKey(ListaCompra, null=False, on_delete=models.CASCADE) #pk2
    marca = models.ForeignKey(Marca, null=True, blank=True, on_delete=models.SET_NULL) #pk3
    mercado = models.ForeignKey(Mercado, null=False, on_delete=models.SET_DEFAULT, default=0) #pk4
    preco = models.DecimalField(decimal_places=2, max_digits=8, null=True)
    indicado = models.BooleanField(default=False) #quando o preco eh o indicado na lista
    data_lancamento = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{str(self.lista_compra)} ({str(self.produto)})"
