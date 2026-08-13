from datetime import datetime, timezone

from ..extensions import db


class ScanHistory(db.Model):
    """One saved scan: photo, identified plant, and the market-price
    snapshot at scan time.

    STAGE 4 populates the plant_* fields (via vision_service). STAGE 5
    populates the market_* fields (via market_price_service). STAGE 6
    wires up actually saving/listing these rows.
    """

    __tablename__ = 'scan_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=False, index=True
    )
    image_path = db.Column(db.String(500), nullable=False)

    common_name = db.Column(db.String(200))
    scientific_name = db.Column(db.String(200))
    confidence = db.Column(db.Float)
    growing_tips = db.Column(db.JSON)  # list[str]

    market_crop_name = db.Column(db.String(200))
    market_min_price = db.Column(db.Float)
    market_max_price = db.Column(db.Float)
    market_avg_price = db.Column(db.Float)
    market_unit = db.Column(db.String(50))
    market_name = db.Column(db.String(200))

    scanned_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), index=True
    )

    user = db.relationship('User', backref=db.backref('scans', lazy='dynamic'))

    def __repr__(self) -> str:
        return f'<ScanHistory {self.id} {self.common_name!r}>'
