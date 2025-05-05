from app import app

def test_home_route():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code in (200, 404)  # 404 if no short_hash
