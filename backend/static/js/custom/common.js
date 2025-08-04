
var productListApiUrl = 'http://127.0.0.1:5051/getProducts';
var uomListApiUrl = 'http://127.0.0.1:5051/getUOM';
var productSaveApiUrl = 'http://127.0.0.1:5051/insertProduct';
var productDeleteApiUrl = 'http://127.0.0.1:5051/deleteProduct';
// var orderListApiUrl = 'http://127.0.0.1:5050/getAllOrders';
var orderSaveApiUrl = 'http://127.0.0.1:5051/insertOrder';
// var getOrderDetailsApiUrl = "http://127.0.0.1:5050/getOrderDetails";
var getOrderApi = "http://127.0.0.1:5051/getOrderDetails";


// For product drop in order
var productsApiUrl = 'https://fakestoreapi.com/products';
function callApi(method, url, data, successMessage = "✅ order completed!") {
    $.ajax({
        method: method,
        url: url,
        data: JSON.stringify(data),
        contentType: "application/json",
        success: function(response) {
            alert(successMessage);
            window.location.reload();
        },
        error: function(err) {
            alert("❌ Error. Check backend logs.");
            console.error(err);
        }
    });
}


function calculateValue() {
    var total = 0;
    $(".product-item").each(function( index ) {
        var qty = parseFloat($(this).find('.product-qty').val());
        var price = parseFloat($(this).find('#product_price').val());
        price = price*qty;
        $(this).find('#item_total').val(price.toFixed(2));
        total += price;
    });
    $("#product_grand_total").val(total.toFixed(2));
}

function orderParser(order) {
    return {
        id : order.id,
        date : order.employee_name,
        orderNo : order.employee_name,
        customerName : order.employee_name,
        cost : parseInt(order.employee_salary)
    }
}

function productParser(product) {
    return {
        id : product.id,
        name : product.employee_name,
        unit : product.employee_name,
        price : product.employee_name
    }
}

function productDropParser(product) {
    return {
        id : product.id,
        name : product.title
    }
}

//To enable bootstrap tooltip globally
// $(function () {
//     $('[data-toggle="tooltip"]').tooltip()
// });