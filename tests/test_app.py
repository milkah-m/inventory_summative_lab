import pytest
from app import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    return app.test_client()

def test_read_all_items(client):
    response = client.get("/inventory")
    assert response.status_code == 200

def test_read_specific_item(client):
    response = client.get("/inventory/1")
    assert response.status_code == 200
    assert response.get_json()["id"] == 1

def test_create_item(client):
    response = client.post("/inventory", json={
     "product_name": "mint chocolate",
     "ingredients": "lots of sugar",
     "price": 12,
     "category": "confectionery",
     "quantity": 57,
     "brand": "Dairyland",
     "expiry_date": "22.12.2026"})
    assert response.status_code == 201
    assert response.get_json()["product_name"] == "mint chocolate"

def test_fetch_item(client):
    mock_product = {
        "product_name": "Oreo",
        "brands": "Nabisco",
        "ingredients_text": "sugar, flour, cocoa",
        "categories": "Biscuits"
    }
    with patch("app.external_api.requests.get") as mock_get:
        mock_get.return_value = MagicMock()
        mock_get.return_value.json.return_value = {"products": [mock_product]}
        response = client.post("/inventory/fetch", json={
            "product_name": "Oreo",
            "price": 82,
            "quantity": 27,
            "expiry_date": "29.10.2026"
        })
        assert response.status_code == 201
        assert response.get_json()["expiry_date"] == "29.10.2026"

def test_update_item(client):
    response = client.patch("/inventory/1", json={"price": 999})
    assert response.status_code == 200
    assert response.get_json()["price"] == 999

def test_delete_item(client):
    response = client.delete("/inventory/1")
    assert response.status_code == 200

def test_read_specific_item_not_found(client):
    response = client.get("/inventory/999")
    assert response.status_code == 404

def test_delete_item_not_found(client):
    response = client.delete("/inventory/999")
    assert response.status_code == 404

def test_update_item_not_found(client):
    response = client.patch("/inventory/999", json={"price": 999})
    assert response.status_code == 404

def test_get_category_not_found(client):
    response = client.get("/inventory/category/nonexistent")
    assert response.status_code == 404

def test_get_low_stock(client):
    response = client.get("/inventory/low-stock")
    assert response.status_code == 200

def test_get_expiring_soon(client):
    response = client.get("/inventory/expiring-soon")
    assert response.status_code == 200
