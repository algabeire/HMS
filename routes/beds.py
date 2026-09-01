from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Bed, Patient

beds_bp = Blueprint('beds', __name__)


@beds_bp.route('/')
@login_required
def list_beds():
    beds = Bed.query.order_by(Bed.ward, Bed.bed_number).all()
    return render_template('beds.html', beds=beds)


@beds_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_bed():
    if request.method == 'POST':
        bed_number = request.form.get('bed_number')
        ward = request.form.get('ward')
        status = request.form.get('status')
        patient_id = request.form.get('patient_id') or None

        bed = Bed(bed_number=bed_number, ward=ward, status=status, patient_id=patient_id)
        db.session.add(bed)
        db.session.commit()
        flash('Bed added successfully!', 'success')
        return redirect(url_for('beds.list_beds'))

    patients = Patient.query.all()
    return render_template('bed_form.html', bed=None, patients=patients)


@beds_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bed(id):
    bed = Bed.query.get_or_404(id)
    if request.method == 'POST':
        bed.bed_number = request.form.get('bed_number')
        bed.ward = request.form.get('ward')
        bed.status = request.form.get('status')
        bed.patient_id = request.form.get('patient_id') or None
        db.session.commit()
        flash('Bed updated successfully!', 'success')
        return redirect(url_for('beds.list_beds'))

    patients = Patient.query.all()
    return render_template('bed_form.html', bed=bed, patients=patients)


@beds_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_bed(id):
    bed = Bed.query.get_or_404(id)
    db.session.delete(bed)
    db.session.commit()
    flash('Bed deleted successfully!', 'success')
    return redirect(url_for('beds.list_beds'))
