orders=[
    {
        "id":1,
        "customer":"Ashwin",
        "product":"Laptop",
        "status":"Delivered"
    },
    {
        "id":2,
        "customer":"Virat",
        "product":"Mobile",
        "status":"Processing"
    },
    {
        "id":3,
        "customer":"Dhoni",
        "product":"Headphones",
        "status":"Cancelled"
    }
]

def get_all_orders():
    return orders

def get_order_by_id(order_id:int):

    for order in orders:
        if order["id"]==order_id:
            return order

    return {"message":"Order not found"}