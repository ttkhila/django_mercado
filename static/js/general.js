$(function(){
  if (typeof brandModal == "undefined") {
      console.log('disabled')
      $('#link-new-brand').addClass('visually-hidden')
      $('#link-new-product-list').addClass('visually-hidden')
  }
})

function getCurrencyFormatNumbersOnly(currencyCode) {
    return {
      style: 'currency',
      currency: currencyCode,
      currencyDisplay: 'none',
    }
}
  
function formatCurrency (value, format, lang) {
    const stripSymbols = (format.currencyDisplay === 'none')
    const localFormat = stripSymbols ? {...format, currencyDisplay: 'code'} : format
    let result = Intl.NumberFormat(lang, localFormat).format(value)
    if (stripSymbols) {
      result = result.replace(/[a-z]{3}/i, "").replace('.', '').trim()
    }
    return result
}

//aceita somente numeros e virgula (valor monetario)
function numbersOnly(event) {
    var value = String.fromCharCode(event.which);
    var pattern = new RegExp(/^(\d)*(\,)?([0-9]{1})?$/i);
    return pattern.test(value);
 }
