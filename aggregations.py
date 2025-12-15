from db import get_db

db = get_db()
retete = db.retete

def total_calorii_per_reteta():
    pipeline = [
        {"$unwind": "$ingrediente"},
        {"$lookup": {
            "from": "ingrediente",
            "localField": "ingrediente.idIng",
            "foreignField": "_id",
            "as": "detaliiIng"
        }},
        {"$unwind": "$detaliiIng"},
        {"$group": {
            "_id": "$nume",
            "totalCalorii": {
                "$sum": {
                    "$multiply": [
                        "$ingrediente.cantitate",
                        "$detaliiIng.calorii"
                    ]
                }
            }
        }},
        {"$sort": {"totalCalorii": -1}}
    ]
    return list(retete.aggregate(pipeline))


def top_retete_dupa_nr_ingrediente():
    pipeline = [
        {"$project": {
            "nume": 1,
            "nrIngrediente": {"$size": "$ingrediente"}
        }},
        {"$sort": {"nrIngrediente": -1}},
        {"$limit": 5}
    ]
    return list(retete.aggregate(pipeline))


def nr_retete_per_categorie():
    pipeline = [
        {"$group": {
            "_id": "$categorie",
            "nrRetete": {"$sum": 1}
        }},
        {"$sort": {"nrRetete": -1}}
    ]
    return list(retete.aggregate(pipeline))


def frecventa_ingrediente():
    pipeline = [
        {"$unwind": "$ingrediente"},
        {"$group": {
            "_id": "$ingrediente.idIng",
            "frecventa": {"$sum": 1}
        }},
        {"$lookup": {
            "from": "ingrediente",
            "localField": "_id",
            "foreignField": "_id",
            "as": "detalii"
        }},
        {"$unwind": "$detalii"},
        {"$sort": {"frecventa": -1}}
    ]
    return list(retete.aggregate(pipeline))


def statistici_dupa_dificultate():
    pipeline = [
        {"$group": {
            "_id": "$dificultate",
            "nrRetete": {"$sum": 1},
            "timpMediu": {"$avg": "$timpPreparare"}
        }},
        {"$sort": {"timpMediu": 1}}
    ]
    return list(retete.aggregate(pipeline))


def retete_cu_alergeni():
    pipeline = [
        {"$unwind": "$ingrediente"},
        {"$lookup": {
            "from": "ingrediente",
            "localField": "ingrediente.idIng",
            "foreignField": "_id",
            "as": "info"
        }},
        {"$unwind": "$info"},
        {"$match": {
            "info.alergeni": {"$exists": True, "$ne": []}
        }},
        {"$group": {
            "_id": "$nume",
            "alergeni": {"$addToSet": "$info.alergeni"}
        }}
    ]
    return list(retete.aggregate(pipeline))


def top_densitate_calorica():
    pipeline = [
        {"$unwind": "$ingrediente"},
        {"$lookup": {
            "from": "ingrediente",
            "localField": "ingrediente.idIng",
            "foreignField": "_id",
            "as": "info"
        }},
        {"$unwind": "$info"},
        {"$group": {
            "_id": "$nume",
            "densitate": {"$sum": "$info.calorii"}
        }},
        {"$sort": {"densitate": -1}},
        {"$limit": 3}
    ]
    return list(retete.aggregate(pipeline))


def bucket_timp_preparare():
    pipeline = [
        {"$bucket": {
            "groupBy": "$timpPreparare",
            "boundaries": [0, 15, 30, 45, 60],
            "default": "peste 60",
            "output": {
                "nrRetete": {"$sum": 1},
                "lista": {"$push": "$nume"}
            }
        }}
    ]
    return list(retete.aggregate(pipeline))


def calorii_medii_pe_categorie():
    pipeline = [
        {"$unwind": "$ingrediente"},
        {"$lookup": {
            "from": "ingrediente",
            "localField": "ingrediente.idIng",
            "foreignField": "_id",
            "as": "info"
        }},
        {"$unwind": "$info"},
        {"$group": {
            "_id": "$categorie",
            "caloriiTotale": {
                "$sum": {
                    "$multiply": [
                        "$ingrediente.cantitate",
                        "$info.calorii"
                    ]
                }
            },
            "nrRetete": {"$sum": 1}
        }},
        {"$project": {
            "_id": 0,
            "categorie": "$_id",
            "caloriiTotale": 1,
            "caloriiMediiPeReteta": {
                "$divide": ["$caloriiTotale", "$nrRetete"]
            }
        }}
    ]
    return list(retete.aggregate(pipeline))
