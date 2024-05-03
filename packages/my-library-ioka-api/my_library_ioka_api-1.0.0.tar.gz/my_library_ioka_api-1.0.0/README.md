How to quickstart: 
# Creating an order
        order = example_order
        make_order = ioka.create_order(order.amount, order.currency)
# Getting all orders
        all_orders = ioka.get_all_orders()
# Getting an order by id
        order_by_id = ioka.get_order_by_id(make_order["order"]["id"])
# Creating a payment
        payment = example_payment
        make_payment = ioka.create_card_payment(make_order["order"]["id"], payment.pan, payment.exp, payment.holder,
                                                payment.cvc)
 # Getting a payment by id
        payment_by_id = ioka.get_payment(make_order["order"]["id"], make_payment["id"])
