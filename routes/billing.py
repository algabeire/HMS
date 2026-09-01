from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from models import db, Billing, Patient

billing_bp = Blueprint('billing', __name__)


@billing_bp.route('/')
@login_required
def list_billing():
    bills = Billing.query.order_by(Billing.date.desc()).all()
    return render_template('billing.html', bills=bills)


@billing_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_billing():
    if request.method == 'POST':
        amount = request.form.get('amount')
        description = request.form.get('description')
        status = request.form.get('status')
        patient_id = request.form.get('patient_id')

        bill = Billing(amount=amount, description=description, status=status, patient_id=patient_id)
        db.session.add(bill)
        db.session.commit()
        flash('Billing record added!', 'success')
        return redirect(url_for('billing.list_billing'))

    patients = Patient.query.all()
    return render_template('billing_form.html', bill=None, patients=patients)


@billing_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_billing(id):
    bill = Billing.query.get_or_404(id)
    if request.method == 'POST':
        bill.amount = request.form.get('amount')
        bill.description = request.form.get('description')
        bill.status = request.form.get('status')
        bill.patient_id = request.form.get('patient_id')
        db.session.commit()
        flash('Billing record updated!', 'success')
        return redirect(url_for('billing.list_billing'))

    patients = Patient.query.all()
    return render_template('billing_form.html', bill=bill, patients=patients)


@billing_bp.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_billing(id):
    bill = Billing.query.get_or_404(id)
    db.session.delete(bill)
    db.session.commit()
    flash('Billing record deleted!', 'success')
    return redirect(url_for('billing.list_billing'))
