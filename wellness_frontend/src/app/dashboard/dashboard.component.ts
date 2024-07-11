import { Component } from '@angular/core';
import { Appointment } from '../Appointment';
import { AppointmentService } from '../appointment.service';
import { UserService } from '../user.service';
import { Router } from '@angular/router';
import { trigger, state, style, transition, animate } from '@angular/animations';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css'],
  animations: [
    trigger('fadeInOut', [
      state('void', style({
        opacity: 0
      })),
      transition('void <=> *', animate(500)),
    ])
  ]
})
export class DashboardComponent {
  appointments: Appointment[] = [];
  displayAddForm: boolean = false;
  displayUpdateForm: boolean = false;
  addOrUpdateTitle: string = '';
  appointment: Appointment = new Appointment(0, '', '', new Date(), '', '');
  username: string | null = null;
  currentView: string = 'home'; // Default view is 'home'
  displayAppointments: boolean = false;

  constructor(
    private appointmentService: AppointmentService,
    private userService: UserService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.getAppointments();
    this.username = this.userService.getCurrentUser();
  }
  
  getAppointments() {
    const username = this.userService.getCurrentUser();
    if (username !== null) {
      this.appointmentService.getAppointments(username).subscribe(
        (response) => {
          this.appointments = response;
        },
        (error) => console.log(error)
      );
    } else {
      console.log('Current user is null. Unable to fetch appointments.');
    }
  }

  addAppointment(event: Event) {
    event.preventDefault(); // Prevent default form submission
    const username = this.userService.getCurrentUser();
    if (username !== null) {
      this.displayAddForm = true;
      this.displayUpdateForm = false;
      this.addOrUpdateTitle = 'Add Appointment';
      this.appointment = new Appointment(0, username, '', new Date(), '', '');
      // this.currentView = 'bookAppointment';
    } else {
      console.log('Current user is null. Cannot add appointment.');
    }
  }

  createOrUpdateAppointment() {
    if (this.addOrUpdateTitle === 'Add Appointment') {
      this.appointmentService.createAppointment(this.appointment).subscribe(
        (response) => { 
          console.log('Appointment created successfully.');
          alert('Appointment created successfully.');
          this.getAppointments();
          this.displayAddForm = false; // Hide the form after successful creation
        },
        (error) => {
          console.log(error);
          alert("Slots not available");
        } 
      );
    } else if (this.addOrUpdateTitle === 'Update Appointment') {
      this.appointmentService.updateAppointment(this.appointment).subscribe(
        (response) => { 
          console.log('Appointment updated successfully.'); 
          alert("Appointment updated successfully");
          this.getAppointments();
          this.displayUpdateForm = false; // Hide the form after successful update
        },
        (error) => {
          console.log(error);
          alert("Slot not available");
        }
      );
    }
  }

  updateAppointment(appointment: Appointment, event: Event) {
    event.preventDefault(); // Prevent default form submission
    this.displayUpdateForm = true;
    this.displayAddForm = false;
    this.addOrUpdateTitle = 'Update Appointment';
    this.appointment = { ...appointment };
    // this.currentView = 'bookAppointment';
  }

  deleteAppointment(appointmentId: number) {
    this.appointmentService.deleteAppointment(appointmentId).subscribe(
      (response) => { 
        console.log('Appointment deleted successfully.'); 
        alert("Appointment cancelled successfully");
        this.getAppointments(); 
      },
      (error) => console.log(error)
    );
  }

  navigateTo(view: string) {
    this.currentView = view;
  }

  logout() {
    this.userService.logout();
    this.router.navigate(['/login']); // Assuming login route exists
  }

  toggleAppointments() {
    if (!this.displayAppointments) {
      this.getAppointments();
    }
    this.displayAppointments = !this.displayAppointments;
  }
}
