import pytest
from app import app, db
from models1 import Users_info, Appointment

@pytest.fixture(scope='module')
def test_client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()

@pytest.fixture(scope='function')
def init_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()

def test_register(test_client, init_database):
    response = test_client.post('/register', json={
        'username': 'testuser',
        'email': 'test@example.com',
        'contact': '1234567890',
        'address': '123 Test St',
          'password': 'password',
        'confirmPassword': 'password'
    })
    assert response.status_code == 201
    assert response.json['status'] == 'success'

def test_login(test_client, init_database):
    user = Users_info(username='testuser', email='test@example.com', contact='1234567890', address='123 Test St')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/login', json={
        'username': 'testuser',
        'password': 'password'
    })
    assert response.status_code == 200
    assert response.json['status'] == 'success'

def test_create_appointment(test_client, init_database):
    user = Users_info(username='testuser', email='test@example.com', contact='1234567890', address='123 Test St')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    response = test_client.post('/appointments', json={
        'username': 'testuser',
        'services': 'service1',
        'date': '2023-07-11',
        'time': '10:00:00'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'Appointment created successfully'

def test_get_appointments(test_client, init_database):
    user = Users_info(username='testuser', email='test@example.com', contact='1234567890', address='123 Test St')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    appointment = Appointment(username='testuser', services='service1', date='2023-07-11', time='10:00:00')
    db.session.add(appointment)
    db.session.commit()

    response = test_client.get('/appointments', query_string={'username': 'testuser'})
    assert response.status_code == 200
    assert len(response.json) == 1

def test_update_appointment(test_client, init_database):
    user = Users_info(username='testuser', email='test@example.com', contact='1234567890', address='123 Test St')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    appointment = Appointment(username='testuser', services='service1', date='2023-07-11', time='10:00:00')
    db.session.add(appointment)
    db.session.commit()

    response = test_client.put(f'/appointments/{appointment.id}', json={
        'services': 'service2',
        'date': '2023-07-12',
        'time': '11:00:00'
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Appointment updated successfully'

def test_delete_appointment(test_client, init_database):
    user = Users_info(username='testuser', email='test@example.com', contact='1234567890', address='123 Test St')
    user.set_password('password')
    db.session.add(user)
    db.session.commit()

    appointment = Appointment(username='testuser', services='service1', date='2023-07-11', time='10:00:00')
    db.session.add(appointment)
    db.session.commit()

    response = test_client.delete(f'/appointments/{appointment.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'Appointment deleted successfully'
