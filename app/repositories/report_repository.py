from app.models.user_report import UserReport
from app import db

class ReportRepository:
    def count_pending(self):
        return UserReport.query.filter_by(status='pending').count()

    def update_status(self, report_id, status):
        report = UserReport.query.get(report_id)
        if report:
            report.status = status
            db.session.commit()
            return True
        return False

    def get_by_id(self, report_id):
        return UserReport.query.get(report_id)

    def count_all(self):
        return UserReport.query.count()

    def count_by_status(self, status):
        return UserReport.query.filter_by(status=status).count()

    def get_recent(self, limit=None):
        query = UserReport.query.order_by(UserReport.created_at.desc())
        if limit:
            query = query.limit(limit)
        return query.all()

    def update(self, report_id, data):
        try:
            report = self.get_by_id(report_id)
            if report:
                for key, value in data.items():
                    setattr(report, key, value)
                db.session.commit()
                return True
            return False
        except:
            db.session.rollback()
            return False
