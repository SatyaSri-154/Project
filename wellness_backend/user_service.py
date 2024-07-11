from models1 import db, Users_info, Appointment
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class UserService:
    @staticmethod
    def login(username, password):
        user = Users_info.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return {'status': 'success', 'message': 'Valid User'}, 200
        else:
            return {'status': 'error', 'message': 'Invalid User'}, 401

    @staticmethod
    def register(username, email, contact=None, address=None, password=None, confirmPassword=None):
        if contact and len(contact) > 15:
            return {'message': 'contact number exceeds maximum length'}

        if password != confirmPassword:
            return {'message': 'Passwords do not match plz recheck'}, 400

        existing_user = Users_info.query.filter((Users_info.username == username) | (Users_info.email == email)).first()
        if existing_user:
            return {'status': 'error', 'message': 'Username or Email already exists'}, 400

        new_user = Users_info(username=username, email=email)

        if contact:
            new_user.contact = contact
        if address:
            new_user.address = address

        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {'status': 'success', 'message': 'User Registration Successful'}, 201

class AppointmentService:
    @staticmethod
    def create_appointment(username, services, date, time):
        existing_appointment = Appointment.query.filter_by(date=date, time=time).first()
        if existing_appointment:
            return {"message": "Slot already booked. Please choose a different date/time/services."}, 409

        appointment = Appointment(username=username, services=services, date=date, time=time)
        db.session.add(appointment)
        db.session.commit()
        return {"message": "Appointment created successfully"}, 201

    @staticmethod
    def get_appointments(username):
        appointments = Appointment.query.filter_by(username=username).all()

        result = []
        for appointment in appointments:
            result.append({
                "id": appointment.id,
                "username": appointment.username,
                "services": appointment.services,
                "date": appointment.date.strftime("%Y-%m-%d"),
                "time": appointment.time.strftime("%H:%M:%S"),
                "created_at": appointment.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })

        return result, 200

    @staticmethod
    def update_appointment(appointment_id, services, date, time):
        appointment = Appointment.query.filter_by(id=appointment_id).first()
        if not appointment:
            return {"message": "Appointment not found"}, 404

        conflicting_appointment = Appointment.query.filter(
            Appointment.id != appointment_id,
            Appointment.date == date,
            Appointment.time == time
        ).first()

        if conflicting_appointment:
            return {"message": "This appointment slot is already booked. Please choose another slot."}, 400

        appointment.services = services
        appointment.date = date
        appointment.time = time
        db.session.commit()

        return {"message": "Appointment updated successfully"}, 200

    @staticmethod
    def delete_appointment(appointment_id):
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return {"message": "Appointment not found"}, 404

        db.session.delete(appointment)
        db.session.commit()
        return {"message": "Appointment deleted successfully"}, 200