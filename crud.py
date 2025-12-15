from db import get_db

db = get_db()
ingrediente = db.ingrediente
retete = db.retete

# ================= INGREDIENTE =================

def get_ingrediente(filtru=None):
    """Returneaza toate ingredientele"""
    if filtru is None:
        filtru = {}
    return list(ingrediente.find(filtru, {"_id": 0}))

def adauga_ingredient(data):
    """Adauga un ingredient"""
    return ingrediente.insert_one(data)

def update_ingredient(filtru, update):
    """Actualizeaza ingredientele care respecta filtru"""
    return ingrediente.update_many(filtru, {"$set": update})

def sterge_ingredient(filtru):
    """Sterge ingredientele care respecta filtru"""
    return ingrediente.delete_many(filtru)


# ================= RETETE =================

def get_retete(filtru=None):
    """Returneaza toate retetele"""
    if filtru is None:
        filtru = {}
    return list(retete.find(filtru, {"_id": 0}))

def adauga_reteta(data):
    """Adauga o reteta"""
    return retete.insert_one(data)

def update_reteta(filtru, update):
    """Actualizeaza retetele care respecta filtru"""
    return retete.update_many(filtru, {"$set": update})

def adauga_ingredient_la_retete(filtru, ingredient):
    """Adauga un ingredient in array-ul de ingrediente al retetelor"""
    return retete.update_many(filtru, {"$push": {"ingrediente": ingredient}})

def incrementare_timp_retete(filtru, increment):
    """Creste timpul de preparare al retetelor care respecta filtru"""
    return retete.update_many(filtru, {"$inc": {"timpPreparare": increment}})

def sterge_reteta(filtru):
    """Sterge retetele care respecta filtru"""
    return retete.delete_many(filtru)
