var brandModal = document.getElementById('modal_brand')
var productModal = document.getElementById('modal_product')

// todos os campos type=input recebem foco com texto selecionado
$("input:text").focus(function() { $(this).select(); } );

//button lista compras toggle (active / deactive)
last_price = null
last_brand = null

$('#div-items-list').on( "click", 'button', function() {
    btn = $(this)
    btn.button('toggle')
})

function alert_message_show(elem){
    setInterval(function(){
        elem.hide('slow')
    }, 3000)
}

//criacao da lista de compras
$('#btn_create_list').click(function(){
    name_field = $('#listName')
    if (name_field.val() == ''){
        $('#alert_nome').show()
        alert_message_show($('#alert_nome'))
        name_field.focus()
        return false
    }
    name_value = name_field.val()

    //verifica os produtos selecionados
    array_products = []
    $( ".btn-secondary.active" ).each(function( index ) {
        id = $( this ).attr('id').split('_')[1]
        array_products.push(id)
    });

    url = '/mercado/createList?nameList='+name_value+'&products='+array_products
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then(function(result){
        return result.json()
    }).then(function(data){
        field_result = $('#alert_create')
        if (data['error'] == 0){
            field_result.removeClass('alert-danger')
            field_result.addClass('alert-success')
        } else {
            field_result.removeClass('alert-success')
            field_result.addClass('alert-danger')
        }

        field_result.children('span').html('<strong>' + data['msg'] + '</strong>')
        field_result.show()
        alert_message_show(field_result)
        if (data['error'] == 0){
            window.location = 'showList/' + data['id']
        }
             
    })  
})

// Escolha do mercado no grid da lista de compras
$('[name=select-market]').change(function(){
    let select = $(this)
    market_id = select.val()
    if (market_id == 0) return

    let first_market = 'False'
    new_market_flag = select.parent().parent().attr('id').split('_')[1]
    if (new_market_flag == '1'){ //primeiro mercado da lista
        first_market = 'True'
    } 
    let list_id = $('#hidden-id-list').val()

    url = '/mercado/newMarketInList?list_id=' + list_id + '&market_id=' + market_id + '&first=' + first_market
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then(function(result){
        return result.json()
    }).then(function(data){
        window.location.reload()
    })  
})

$('[name=select-brand]').change(function(){
    let select = $(this)
    let brand_id = select.val()
    if (brand_id == '0' || brand_id == last_brand){
        select.val(last_brand)
        return 
    } 
    let product_list_id = select.attr('id').split('_')[1]

    // console.log(`BRAND ID: ${brand_id} | NOME: ${brand_name} | PRODUTO LISTA: ${product_lista_id} | LIST: ${list_id}`)
    url = `/mercado/newBrandInList?brand_id=${brand_id}&product_list_id=${product_list_id}`//&field_id=${select.attr('id')}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then( result => {
        return result.json()
    }).then( data => {
        console.log(data)
        // window.location.reload()
    }).catch( e => console.log('Error: ' + e.message))
})

$('[name=select-brand]').focus(function(){
    last_brand = $(this).val()
})

//campo monetario
$('[name=input-preco]').bind('keypress', numbersOnly);

$('[name=input-preco]').focus(function(){
    last_price = $(this).val()
})

// Alteracao de preco da lista
$('[name=input-preco]').blur(function(){
    let self = $(this)
    val = self.val()
    const format = getCurrencyFormatNumbersOnly('BRL')
    let price_format = formatCurrency(val.replace(',', '.'), format, 'pt-BR')
    if (price_format == 'NaN' || price_format == last_price) {
        self.val(last_price) //retorna para valor antes da edicao
        return
    }
    self.val(price_format)

    let prod_list_id = self.attr('id').split('_')[1]

    url = `/mercado/newPrice?product_list_id=${prod_list_id}&price=${price_format}`//&field_id=${self.attr('id')}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then( result => {
        return result.json()
    }).then( data => {
        console.log(data)
        if (data['item_minor_price']){
            td_prod_list = $('#tdPrecoProduto_'+data['item_minor_price']['item_id'])
            // encontra cada TD dentro da TR atual e retira a classe que da o destaque
            td_prod_list.parent().find('td').each (function() {
                $(this).removeClass('bg-success')
            });
            td_prod_list.addClass('bg-success')
        }
        // window.location.reload()
    }).catch( e => console.log('Error: ' + e.message))
})

// Cadastra nova marca
function form_new_brand(){
    let brand_name = $('#brand-name').val()
    if (brand_name == '') return
    url = `/mercado/newBrand?new_brand_name=${brand_name}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then( result => {
        return result.json()
    }).then( data => {
        console.log(data)
        if (data['msg']){ 
            let alert = $('#alert_error')
            alert.children('span').html('<strong>' + data['msg'] + '</strong>')
            alert.show()
            console.error(data['msg']) 
        } else {
            window.location.reload()
        }
    }).catch( e => console.log('Error: ' + e.message))
}

// Evento disparado ao abrir modal de inclusao de produto na lista
productModal.addEventListener('show.bs.modal', function (event) {
    let list_id = $('#hidden-id-list').val()
    if (!list_id) return
    let url = `/mercado/newProductInList?list_id=${list_id}`
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then( result => {
        return result.json()
    }).then( data => {
        console.log(data)
        var div_items = productModal.querySelector('#div-items-list')
        html = ''
        data['products'].forEach(elem => {
            html += `<button type="button" name="prod_item" id="prod_${elem.id}" 
                class="btn btn-xs btn-secondary rounded-pill m-1 shadow" 
                data-toggle="button" aria-pressed="false" autocomplete="off">
                ${elem.nome}</button>`
        });
        div_items.innerHTML = html

    }).catch( e => console.log('Error: ' + e.message))
})

function form_new_product_list(){
    let list_id = $('#hidden-id-list').val()
    if (!list_id) return
    //verifica os produtos selecionados
    let array_products = []
    $( ".btn-secondary.active" ).each(function( index ) {
        id = $( this ).attr('id').split('_')[1]
        array_products.push(id)
    });
    if (array_products.length == 0) return

    url = '/mercado/insertProductsList?idList='+list_id+'&products='+array_products
    fetch(url, {
        method: 'GET',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
    }).then(function(result){
        return result.json()
    }).then(function(data){
        console.log(data)
        if (data['msg']) console.error(data['msg'])
        else {
            window.location.reload()
        }
    }).catch( e => console.log('Error: ' + e.message))
}

function marcar_vendido(produto_list_id){
    url = `/mercado/produtoVendido?id=${produto_list_id}`
    fetch(url)
        .then(result => {return result.json()})
        .then(data => {
            console.log(data)
            if (data['msg']) console.error(data['msg'])
            else {
                window.location.reload()
            }
        })
        .catch( e => console.log('Error: ' + e.message))
}