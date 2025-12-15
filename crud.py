from db import get_db

db = get_db()
ingrediente = db.ingrediente
retete = db.retete


def get_ingrediente(filtru=None):
    if filtru is None:
        filtru = {}
    return list(ingrediente.find(filtru, {"_id": 0}))

def adauga_ingredient(data):
    return ingrediente.insert_one(data)

def update_ingredient(filtru, update):
    return ingrediente.update_many(filtru, {"$set": update})

def sterge_ingredient(filtru):
    return ingrediente.delete_many(filtru)



def get_retete(filtru=None):
    if filtru is None:
        filtru = {}
    return list(retete.find(filtru, {"_id": 0}))

def adauga_reteta(data):
    return retete.insert_one(data)

def update_reteta(filtru, update):
    return retete.update_many(filtru, {"$set": update})

def adauga_ingredient_la_retete(filtru, ingredient):
    return retete.update_many(filtru, {"$push": {"ingrediente": ingredient}})

def incrementare_timp_retete(filtru, increment):
    return retete.update_many(filtru, {"$inc": {"timpPreparare": increment}})

def sterge_reteta(filtru):
    return retete.delete_many(filtru)
