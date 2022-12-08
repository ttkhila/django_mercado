from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from .models import Produto, ListaCompra, ProdutoLista, Mercado, Marca
from datetime import datetime
from django.db.models import Q
from .util import *
from .inserts import inserts #initial inserts DB

def mercado_index(request):
    open_lists = ListaCompra.objects.filter(Q(finalizada=False))
    closed_lists = ListaCompra.objects.filter(Q(finalizada=True))

    result_open = {}
    result_closed = {}
    for _list in open_lists:
        distinct = ProdutoLista.objects.filter(Q(lista_compra=_list.id)).values('produto').distinct().count()
        result_open[_list.id] = [_list.nome, distinct]
    
    for _list in closed_lists:
        distinct = ProdutoLista.objects.filter(Q(lista_compra=_list.id)).values('produto').distinct().count()
        result_closed[_list.id] = [_list.nome, distinct]
    return render(request, 'index.html', { 'open': result_open, 'closed': result_closed } )

def nova_lista(request):
    produtos = Produto.objects.all().order_by('nome')
    context = {'produto_list': produtos}
    return render(request, 'novaLista.html', context)

def new_product_list(request):
    list_id = request.GET.get('list_id')
    inner_qs = ProdutoLista.objects.filter(Q(lista_compra=list_id)).values_list('produto')
    # filtra somente produtos que NAO estejam na lista
    products = Produto.objects.exclude(Q(id__in=inner_qs)).order_by('nome').values()
    print(list(products))
    return JsonResponse({"products": list(products)})

# cria nova lista do ZERO
def create_list(request):
    nameList = request.GET.get('nameList')
    products = request.GET.get('products')
    if products: products = eval(products)
    #hack para corrigir o problema quando ha somente 1 item na lista
    if isinstance(products, int): products = [products]
    _list = None

    data = {
        'error': None,
        'msg': None,
        'id': None
    }

    l = ListaCompra()
    try:
        _list = ListaCompra.objects.get(nome=nameList)
    except ObjectDoesNotExist:
        l.nome =nameList
        l.data_fechamento = datetime.now()
        l.save()

    if _list: return JsonResponse( { 'error': 1, 'msg': 'Esse nome de lista já existe', 'id': None} )
    
    data['id'] = l.id
    excep = False
    for prod in products:
        print(f'PRDO: {prod} | TYPE: {type(prod)}')
        try:
            obj_prod = Produto.objects.get(id=prod)
        except ObjectDoesNotExist:
            excep = True
            data['error'] = 0
            data ['msg'] =  'Lista criada, porém houve(ram) problema(s) com algum(s) dos itens!'
            continue
        pl = ProdutoLista(
            produto = obj_prod,
            lista_compra = l
        )
        pl.save()

    if not excep: 
        data['error'] = 0
        data ['msg'] =  'Lista criada!'
    return JsonResponse(data)

#insere produtos numa lista em andamento
def insert_products_in_list(request):
    idList = request.GET.get('idList')
    products = request.GET.get('products')
    if products: products = eval(products)
    #hack para corrigir o problema quando ha somente 1 item na lista
    if isinstance(products, int): products = [products]

    mercados = ProdutoLista.objects.filter(Q(lista_compra=idList)).values('mercado').order_by('mercado').distinct()
    # print(mercados)
    # return JsonResponse({'a': 'error'})

    try: _list = ListaCompra.objects.get(Q(id=idList))
    except ObjectDoesNotExist: return JsonResponse({ 'msg': 'Erro ao recuperar a lista de produtos' })
    
    prod = None
    for p in products:
        try: prod = Produto.objects.get(Q(id=p))
        except ObjectDoesNotExist: continue

        for m in mercados:
            mercado = Mercado.objects.get(Q(id=m['mercado']))
            new_product_list = ProdutoLista(
                produto = prod,
                lista_compra = _list,
                mercado = mercado
            )
            new_product_list.save()
        
    return JsonResponse({'a': 'success'})


def show_list(request, id):
    _list = ProdutoLista.objects.filter(Q(lista_compra=id)).order_by('produto__nome')

    products = []
    markets = []
    items = {}
    for l in _list:
        if not l.produto in products:
            products.append(l.produto)
            items[l.produto] = {}

        if l.mercado: 
            if not l.mercado.id in items[l.produto].keys():
                items[l.produto][l.mercado.id] = []

            if l.marca: marca_id = l.marca.id
            else: marca_id = 0
            items[l.produto][l.mercado.id].append(marca_id)
            items[l.produto][l.mercado.id].append(l.preco)
            items[l.produto][l.mercado.id].append(l.id)

            if not l.mercado in markets:
                markets.append(l.mercado)

    #all markets and brands
    brands = Marca.objects.all().order_by('nome')
    all_markets = Mercado.objects.all()
    items_minor_price = price_compare_load_list(items) #verifica menor preco em cada produto
    if 'field_id' in request.session: field_id = request.session["field_id"]
    else: field_id = None
    result = {
        'items': items,
        'markets': markets,
        'brands': brands,
        'all_markets': all_markets,
        'id_list': id,
        'minor_prices': items_minor_price,
        'session_id': field_id,
    }

    # modelo da lista retornada:
    # items = {
    #   'produto1_lista' : {
    #       'mercado1' : [ 'marca', 'preco', 'produtoListaId' ]    
    #   },
    #    'produto2_lista' : {
    #       'mercado2' : [ 'marca', 'preco', 'produtoListaId' ]    
    #   }
    # }
    return render(request, 'lista.html', result)

def new_market_list(request):
    list_id = int(request.GET.get('list_id'))
    first = eval(request.GET.get('first'))
    market_id = int(request.GET.get('market_id'))

    items_list = ProdutoLista.objects.filter(Q(lista_compra=list_id))
    market = Mercado.objects.get(id=market_id)
    if first: #primeiro mercado numa lista
        for item in items_list:
            item.mercado = market
            item.save()
    else: #novo mercado na lista (mas nao o primeiro)
        products = []
        for item in items_list:
            if not item.produto in products:
                products.append(item.produto)
                new_product_list = ProdutoLista(
                    produto = item.produto,
                    lista_compra = item.lista_compra,
                    mercado = market,
                )
                new_product_list.save() 
    return JsonResponse({'a': 'aaaaa'})

def new_brand_list(request):
    brand_id = int(request.GET.get('brand_id'))
    product_list_id = int(request.GET.get('product_list_id'))
    # field_id = request.GET.get('field_id')
    item = None
    try:
        item = ProdutoLista.objects.get(Q(id=product_list_id))
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': e.message})

    brand = Marca.objects.get(id=brand_id)
    item.marca = brand
    item.save()
    # request.session['field_id'] = field_id
    return JsonResponse({'1': 'success'})

def new_price(request):
    price = request.GET.get('price')
    price = price.replace(',', '.')
    prod_list_id = int(request.GET.get('product_list_id'))
    # field_id = request.GET.get('field_id')

    try:
        item = ProdutoLista.objects.get(Q(id=prod_list_id))
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': e.message})
    item.preco = price
    item.save()

    #compara precos dos produtos iguais ja lancados
    item_minor_price = price_compare(item)
    print(f'MINOR: {item_minor_price}')

    # request.session['field_id'] = field_id
    # print(f'SESSION: {request.session["field_id"]}')
    return JsonResponse({'item_minor_price': item_minor_price})

def new_brand_created(request):
    brand_name = request.GET.get('new_brand_name')
    try:
        brands = Marca.objects.get(nome=brand_name)
    except ObjectDoesNotExist:
        nb = Marca(
            nome = brand_name 
        )
        nb.save()
        return JsonResponse({'brand_id':nb.id, 'brand_name': nb.nome})
    return JsonResponse({'msg': 'Marca Já existe'})

def initialInserts(request):
    inserts()
    return HttpResponse('<h1>sucesso</h1>')