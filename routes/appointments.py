from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Appointment, Patient, Doctor
import datetime

appointments_bp = Blueprint('appointments', __name__)


@appointments_bp.route('/')
@login_required
def list_appointments():
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time).all()
    return render_template('appointments.html', appointments=appointments)


@appointments_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_appointment():
    if request.method == 'POST':
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')
        status = request.form.get('status')

        # Parse date/time into appropriate Python types
        try:
            date_val = datetime.date.fromisoformat(date_str) if date_str else None
            time_val = datetime.time.fromisoformat(time_str) if time_str else None
        except ValueError:
            flash('Invalid date or time format.', 'danger')
            return redirect(url_for('appointments.add_appointment'))

        appt = Appointment(date=date_val, time=time_val, patient_id=int(patient_id) if patient_id else None,
                           doctor_id=int(doctor_id) if doctor_id else None, status=status)
        db.session.add(appt)
        db.session.commit()
        flash('Appointment added successfully!', 'success')
        return redirect(url_for('appointments.list_appointments'))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointment_form.html', appointment=None, patients=patients, doctors=doctors)


@appointments_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    if request.method == 'POST':
        date_str = request.form.get('date')
        time_str = request.form.get('time')
        try:
            appointment.date = datetime.date.fromisoformat(date_str) if date_str else appointment.date
            appointment.time = datetime.time.fromisoformat(time_str) if time_str else appointment.time
        except ValueError:
            flash('Invalid date or time format.', 'danger')
            return redirect(url_for('appointments.edit_appointment', id=id))

        appointment.patient_id = int(request.form.get('patient_id')) if request.form.get('patient_id') else None
        appointment.doctor_id = int(request.form.get('doctor_id')) if request.form.get('doctor_id') else None
        appointment.status = request.form.get('status')
        db.session.commit()
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointments.list_appointments'))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('appointment_form.html', appointment=appointment, patients=patients, doctors=doctors)


@appointments_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    db.session.delete(appointment)
    db.session.commit()
    flash('Appointment deleted successfully!', 'success')
    return redirect(url_for('appointments.list_appointments'))
