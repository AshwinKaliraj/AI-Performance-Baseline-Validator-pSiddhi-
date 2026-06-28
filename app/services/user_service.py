users=[
    {
        "id":1,
        "name":"Ashwin",
        "role":"Admin"
    },
    {
        "id":2,
        "name":"Virat",
        "role":"User"
    },
    {
        "id":3,
        "name":"Dhoni",
        "role":"Manager"
    }
]

def get_all_users():
    return users

def get_user_by_id(user_id:int):

    for user in users:
        if user["id"]==user_id:
            return user

    return {"message":"User not found"}