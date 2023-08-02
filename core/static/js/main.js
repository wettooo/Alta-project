fetch('/addcartitem', {
    method:'GET',
}).then(response => response.json())
  .then(data => {
    if (data != 0){
        document.getElementById('cart').innerHTML = data
        }
    });


count = 0
const addcart = (productId) => {
    console.log('Product Id',productId)
    fetch('/addcartitem', {
        method:'POST',
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify({'PID':productId})
    }).then(response => response.json())
    .then(data => {
        if (data != 0){
            document.getElementById('cart').innerHTML = data
            }
        }
    )
}
const deleteitem = (productId, rowId) => {
    fetch('/addcartitem', {
        method:'DELETE',
        headers: {'Content-Type': 'application/json'}, 
        body: JSON.stringify({'PID':productId})
    }).then(response => response.json())
    .then(data =>{
        console.log(data)
        if (data.res == "Success"){
            document.getElementById(rowId).remove()
            calc_cart_total()
        }
    })
    
}
const cartchange = (e, productId, price) => {
    document.getElementById(productId+'_item_total').innerHTML = '$ ' + (price * e.value)
    calc_cart_total()
}

