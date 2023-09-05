from .models import ProdutoLista
from django.db.models import Q

def price_compare(item_list):
    items = ProdutoLista.objects.filter(Q(produto=item_list.produto) & Q(lista_compra=item_list.lista_compra)).values()

    result = {
        'minor_price': 99999.00,
        'item_id': 0
    }
    all_itens = []
    for item in items:
        all_itens.append(item['id'])
        if item['preco']:
            if item['preco'] < result['minor_price']:
                result['minor_price'] = item['preco']
                result['item_id'] = item['id']

    # print(all_itens)
    return result

def price_compare_load_list(items: dict): 
    result = []
    minor_price = 99999.00
    item_id = 0
    for product, dict_data in items.items():
        # print(f'KEY: {product} | VALUE: {dict_data}')
        for key, value in dict_data.items():
            price = value[1]
            if price:
                if price < minor_price:
                    minor_price = price
                    item_id = value[2]
        # result[item_id] = minor_price
        result.append(item_id)
        minor_price = 99999.00
        item_id = 0

    # print(result)
    return result