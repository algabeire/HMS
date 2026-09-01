from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Doctor

doctors_bp = Blueprint('doctors', __name__)

@doctors_bp.route('/')
@login_required
def list_doctors():
    search = request.args.get('search')
    if search:
        doctors = Doctor.query.filter(Doctor.name.ilike(f'%{search}%')).all()
    else:
        doctors = Doctor.query.all()
    return render_template('doctors.html', doctors=doctors)

@doctors_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    if request.method == 'POST':
        name = request.form.get('name')
        specialization = request.form.get('specialization')
        phone = request.form.get('phone')
        email = request.form.get('email')
        department = request.form.get('department')
        
        doctor = Doctor(name=name, specialization=specialization, phone=phone, email=email, department=department)
        db.session.add(doctor)
        db.session.commit()
        flash('Doctor added successfully!', 'success')
        return redirect(url_for('doctors.list_doctors'))
        
    return render_template('doctor_form.html', doctor=None)

@doctors_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    
    if request.method == 'POST':
        doctor.name = request.form.get('name')
        doctor.specialization = request.form.get('specialization')
        doctor.phone = request.form.get('phone')
        doctor.email = request.form.get('email')
        doctor.department = request.form.get('department')
        
        db.session.commit()
        flash('Doctor updated successfully!', 'success')
        return redirect(url_for('doctors.list_doctors'))
        
    return render_template('doctor_form.html', doctor=doctor)

@doctors_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_doctor(id):
    doctor = Doctor.query.get_or_404(id)
    db.session.delete(doctor)
    db.session.commit()
    flash('Doctor deleted successfully!', 'success')
    return redirect(url_for('doctors.list_doctors'))
