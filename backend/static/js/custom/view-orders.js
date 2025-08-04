$(document).ready(function () {
    $.get('/getOrderDetails', function (orders) {
        const tbody = $('#orders-table tbody');
        tbody.empty();

        orders.forEach(order => {
            let itemsHtml = '<ul>';
            order.items.forEach(item => {
                itemsHtml += `<li>${item.name} - Qty: ${item.quantity}, Price: ₹${item.price}</li>`;
            });
            itemsHtml += '</ul>';

            const row = `
                <tr>
                    <td>${order.order_id}</td>
                    <td>${order.datetime}</td>
                    <td>${order.customer_name}</td>
                    <td>₹${order.total}</td>
                    <td>${itemsHtml}</td>
                </tr>
            `;
            tbody.append(row);
        });
    });
});
