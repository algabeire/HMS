from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, MedicalRecord, Patient, Doctor

emr_bp = Blueprint('emr', __name__)


@emr_bp.route('/')
@login_required
def list_emr():
    records = MedicalRecord.query.order_by(MedicalRecord.date.desc()).all()
    return render_template('emr.html', records=records)


@emr_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_emr():
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        treatment = request.form.get('treatment')
        notes = request.form.get('notes')
        patient_id = request.form.get('patient_id')
        doctor_id = request.form.get('doctor_id')

        rec = MedicalRecord(diagnosis=diagnosis, treatment=treatment, notes=notes, patient_id=patient_id, doctor_id=doctor_id)
        db.session.add(rec)
        db.session.commit()
        flash('Medical record added!', 'success')
        return redirect(url_for('emr.list_emr'))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('emr_form.html', record=None, patients=patients, doctors=doctors)


@emr_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_emr(id):
    record = MedicalRecord.query.get_or_404(id)
    if request.method == 'POST':
        record.diagnosis = request.form.get('diagnosis')
        record.treatment = request.form.get('treatment')
        record.notes = request.form.get('notes')
        record.patient_id = request.form.get('patient_id')
        record.doctor_id = request.form.get('doctor_id')
        db.session.commit()
        flash('Medical record updated!', 'success')
        return redirect(url_for('emr.list_emr'))

    patients = Patient.query.all()
    doctors = Doctor.query.all()
    return render_template('emr_form.html', record=record, patients=patients, doctors=doctors)


@emr_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_emr(id):
    record = MedicalRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Medical record deleted!', 'success')
    return redirect(url_for('emr.list_emr'))
