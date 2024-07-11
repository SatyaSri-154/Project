import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { Appointment } from './Appointment';

@Injectable({
  providedIn: 'root'
})
export class AppointmentService {
  private baseURL = 'http://localhost:5000/appointments';  // Adjust URL as per your Flask backend

  constructor(private httpClient: HttpClient) { }

  getAppointments(username: string): Observable<Appointment[]> {
    const url = `${this.baseURL}?username=${username}`; // Pass username as query parameter
    return this.httpClient.get<Appointment[]>(url);
  }

  createAppointment(appointment: Appointment): Observable<any> {
    return this.httpClient.post(this.baseURL, appointment);
  }

  updateAppointment(appointment: Appointment): Observable<any> {
    const url = `${this.baseURL}/${appointment.id}`;
    return this.httpClient.put(url, appointment);
  }

  deleteAppointment(appointmentId: number): Observable<any> {
    const url = `${this.baseURL}/${appointmentId}`;
    return this.httpClient.delete(url);
  }
}

