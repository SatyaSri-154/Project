from flask_restful import Resource
from flask import request
from user_service import UserService, AppointmentService

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        return UserService.login(username, password)

class Register(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        contact = data.get('contact')
        address = data.get('address')
        password = data.get('password')
        confirmPassword = data.get('confirmPassword')
        return UserService.register(username, email, contact, address, password, confirmPassword)

class AppointmentResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        services = data.get('services')
        date = data.get('date')
        time = data.get('time')
        return AppointmentService.create_appointment(username, services, date, time)

    def get(self):
        username = request.args.get('username')
        return AppointmentService.get_appointments(username)

class AppointmentDetailResource(Resource):
    def put(self, appointment_id):
        data = request.get_json()
        services = data.get('services')
        date = data.get('date')
        time = data.get('time')
        return AppointmentService.update_appointment(appointment_id, services, date, time)

    def delete(self, appointment_id):
        return AppointmentService.delete_appointment(appointment_id)
