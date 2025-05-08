from flask import Blueprint, request, flash, redirect, url_for, session
from app.models.user_report import UserReport
from app import db
from app.utils.decorators import login_required

reports_bp = Blueprint('reports', __name__)

@reports_bp.route("/submit-report", methods=['POST'])
@login_required
def submit_report():
    report_type = request.form.get('report_type')
    reported_id = request.form.get('reported_id')
    context_id = request.form.get('context_id')
    reason = request.form.get('reason')

    if not all([report_type, reported_id, context_id, reason]):
        flash('Missing required information', 'danger')
        return redirect(request.referrer)

    report = UserReport(
        reporter_id=session['user_id'],
        reported_user_id=reported_id,
        reason=reason,
        type=report_type
    )

    # Add context-specific IDs based on report type
    if report_type == 'claim':
        report.claim_id = context_id
    elif report_type == 'chat':
        report.chat_id = context_id
    elif report_type == 'post':
        report.post_id = context_id

    try:
        db.session.add(report)
        db.session.commit()
        flash('Report submitted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error submitting report', 'danger')

    return redirect(request.referrer)
