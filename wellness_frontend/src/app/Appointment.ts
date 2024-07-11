// appointment.ts
export class Appointment {
    constructor(
      public id: number,
      public username: string,
      public services: string,
      public date: Date,
      public time: string,
      public created_at?: string
    ) {}
}
  