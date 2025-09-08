from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Location(DB.Model):
    """Model for storing location metadata."""
    id = DB.Column(DB.BigInteger().with_variant(DB.Integer, "sqlite"), primary_key=True)
    location_id = DB.Column(DB.BigInteger(), nullable=False, unique=True)
    name = DB.Column(DB.String(100), nullable=False, unique=True)
    country = DB.Column(DB.String(100), nullable=True)  # ISO 2-digit code
    country_id = DB.Column(DB.BigInteger(), nullable=False, unique=True)
    records = DB.relationship('Record', backref='location', lazy=True)

    def __repr__(self):
        return f"<Location id={self.id} name={self.name} country={self.country}>"


class Record(DB.Model):
    """Model for storing air quality measurement records."""
    id = DB.Column(DB.BigInteger().with_variant(DB.Integer, "sqlite"), primary_key=True)
    location_id = DB.Column(DB.BigInteger().with_variant(DB.Integer, "sqlite"), DB.ForeignKey('location.location_id'), nullable=False)
    datetime_utc = DB.Column(DB.String, nullable=False)
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f"<Record id={self.id} location_id={self.location_id} datetime_utc={self.datetime_utc} value={self.value}"