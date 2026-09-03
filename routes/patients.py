from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Patient, Doctor

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/')
@login_required
def list_patients():
    search = request.args.get('search')
    if search:
        patients = Patient.query.filter(Patient.name.ilike(f'%{search}%')).all()
    else:
        patients = Patient.query.all()
    return render_template('patients.html', patients=patients)

@patients_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form.get('name')
        age = request.form.get('age')
        dob_value = request.form.get('dob')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        address = request.form.get('address')
        doctor_id = request.form.get('doctor_id')
        status = request.form.get('status')

        dob = datetime.strptime(dob_value, '%Y-%m-%d').date() if dob_value else None

        patient = Patient(name=name, age=age, dob=dob, gender=gender, phone=phone, address=address,
                          doctor_id=doctor_id if doctor_id else None, status=status)
        db.session.add(patient)
        db.session.commit()
        flash('Patient added successfully!', 'success')
        return redirect(url_for('patients.list_patients'))

    doctors = Doctor.query.all()
    return render_template('patient_form.html', patient=None, doctors=doctors)

@patients_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_patient(id):
    patient = Patient.query.get_or_404(id)

    if request.method == 'POST':
        patient.name = request.form.get('name')
        patient.age = request.form.get('age')
        dob_value = request.form.get('dob')
        patient.dob = datetime.strptime(dob_value, '%Y-%m-%d').date() if dob_value else None
        patient.gender = request.form.get('gender')
        patient.phone = request.form.get('phone')
        patient.address = request.form.get('address')
        doctor_id = request.form.get('doctor_id')
        patient.doctor_id = doctor_id if doctor_id else None
        patient.status = request.form.get('status')

        db.session.commit()
        flash('Patient updated successfully!', 'success')
        return redirect(url_for('patients.list_patients'))

    doctors = Doctor.query.all()
    return render_template('patient_form.html', patient=patient, doctors=doctors)

@patients_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_patient(id):
    patient = Patient.query.get_or_404(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!', 'success')
    return redirect(url_for('patients.list_patients'))
