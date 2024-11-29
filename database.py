# Mock Database
database = {
    "8902080285020": {"name": "Product A", "price": 100.0, "discount": 10.0},
    "8902080105021": {"name": "Product B", "price": 200.0, "discount": 0.0},
    "6164001011534": {"name": "Product C", "price": 300.0, "discount": 15.0},
    "1234ABCD": {"name": "Product D", "price": 150.0, "discount": 5.0},
    "0123456745650": {"name": "Product E", "price": 1050.0, "discount": 50.0},
}

def get_product_info(barcode):
    return database.get(barcode)
