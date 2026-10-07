import os
os.environ['DATABASE_URL'] = 'sqlite://'
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.main import app
from app.db import Base, get_db

@pytest.fixture
def client():
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    sessions = sessionmaker(bind=engine)
    def test_db():
        with sessions() as session:
            yield session
    app.dependency_overrides[get_db] = test_db
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()
    engine.dispose()

def test_health(client):
    assert client.get('/health').json() == {'status': 'UP'}

def test_ready_queries_database(client):
    assert client.get('/ready').json() == {'status': 'READY'}

def test_empty_tasks(client):
    assert client.get('/api/tasks').json() == []

def test_create_and_get(client):
    response = client.post('/api/tasks', json={'title': 'Verify release'})
    assert response.status_code == 201
    task = response.json()
    assert client.get(f"/api/tasks/{task['id']}").json()['title'] == 'Verify release'

def test_update_and_statistics(client):
    task = client.post('/api/tasks', json={'title': 'Deploy'}).json()
    assert client.put(f"/api/tasks/{task['id']}", json={'status': 'DONE'}).json()['status'] == 'DONE'
    assert client.get('/api/tasks/stats').json() == {'total': 1, 'todo': 0, 'inProgress': 0, 'done': 1}

def test_delete(client):
    task = client.post('/api/tasks', json={'title': 'Remove'}).json()
    assert client.delete(f"/api/tasks/{task['id']}").status_code == 204
    assert client.get(f"/api/tasks/{task['id']}").status_code == 404

def test_missing_update(client):
    assert client.put('/api/tasks/999', json={'status': 'DONE'}).status_code == 404

def test_invalid_title_and_status(client):
    assert client.post('/api/tasks', json={'title': ''}).status_code == 422
    assert client.post('/api/tasks', json={'title': 'Deploy', 'status': 'INVALID'}).status_code == 422

def test_metrics(client):
    client.get('/health')
    response = client.get('/metrics')
    assert response.status_code == 200
    assert 'http_requests_total' in response.text
