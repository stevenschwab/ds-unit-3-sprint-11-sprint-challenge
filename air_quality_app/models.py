from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Record(DB.Model):
    """Model for storing air quality measurement records."""
    id = DB.Column(DB.BigInteger().with_variant(DB.Integer, "sqlite"), primary_key=True)
    datetime_utc = DB.Column(DB.String, nullable=False)
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"<Record id={self.id} datetime_utc={self.datetime_utc} value={self.value}"