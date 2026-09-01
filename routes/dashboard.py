from flask import Blueprint, render_template
from flask_login import login_required
from models import Doctor, Patient, Appointment
from datetime import datetime, date

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@dashboard_bp.route('/dashboard')
@login_required
def index():
    total_doctors = Doctor.query.count()
    total_patients = Patient.query.count()
    today = datetime.utcnow().date()
    # Count upcoming appointments (today and future)
    upcoming_appointments_count = Appointment.query.filter(Appointment.date >= today).count()
    upcoming_appointments = Appointment.query.filter(Appointment.date >= today).order_by(Appointment.date, Appointment.time).limit(5).all()
    
    # Just a placeholder for beds, assume we have 100 total
    admitted_patients = Patient.query.filter_by(status='admitted').count()
    available_beds = 100 - admitted_patients
    
    recent_patients = Patient.query.order_by(Patient.id.desc()).limit(5).all()
    
    # Mock data for chart: new patients per week over the last 4 weeks
    # In a real app we'd calculate this from admission_date, we'll pass static for demo
    chart_data = {
        'labels': ['Week 1', 'Week 2', 'Week 3', 'Week 4'],
        'data': [5, 12, 8, 15]
    }
    
    return render_template('dashboard.html', 
                           total_doctors=total_doctors,
                           total_patients=total_patients,
                           today= today,
                           today_appointments=upcoming_appointments_count,
                           upcoming_appointments=upcoming_appointments,
                           available_beds=available_beds,
                           recent_patients=recent_patients,
                           chart_data=chart_data)
