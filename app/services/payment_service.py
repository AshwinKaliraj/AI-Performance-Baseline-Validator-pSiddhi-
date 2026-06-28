payments=[
    {
        "id":1,
        "amount":2500,
        "status":"Success"
    },
    {
        "id":2,
        "amount":1800,
        "status":"Pending"
    },
    {
        "id":3,
        "amount":4200,
        "status":"Failed"
    }
]

def get_all_payments():
    return payments

def get_payment_by_id(payment_id:int):

    for payment in payments:
        if payment["id"]==payment_id:
            return payment

    return {"message":"Payment not found"}