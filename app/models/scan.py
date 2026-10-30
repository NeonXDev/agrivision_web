from datetime import datetime, timezone

from ..extensions import db


class ScanHistory(db.Model):
    """One saved scan: photo, identified plant, and the market-price
    snapshot at scan time.
    """

    __tablename__ = 'scan_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey('users.id'), nullable=True, index=True
    )
    image_path = db.Column(db.String(500), nullable=False)

    common_name = db.Column(db.String(200))
    common_name_ne = db.Column(db.String(200))
    scientific_name = db.Column(db.String(200))
    family = db.Column(db.String(100))
    confidence = db.Column(db.Float)
    description = db.Column(db.Text)
    description_ne = db.Column(db.Text)
    growing_tips = db.Column(db.JSON)  # list[str] (English)
    growing_tips_ne = db.Column(db.JSON)  # list[str] (Nepali)

    # Detailed Agronomic & Market Intelligence (Bilingual)
    planting_season = db.Column(db.String(250))
    planting_season_ne = db.Column(db.String(250))
    growth_duration = db.Column(db.String(200))
    growth_duration_ne = db.Column(db.String(200))
    fertilizer_guide = db.Column(db.JSON)  # list[str]
    fertilizer_guide_ne = db.Column(db.JSON)  # list[str]
    optimal_climate = db.Column(db.Text)
    optimal_climate_ne = db.Column(db.Text)
    unfavorable_climate = db.Column(db.Text)
    unfavorable_climate_ne = db.Column(db.Text)
    profitability_window = db.Column(db.JSON)  # dict {rating, peak_months, off_season_advantage, selling_strategy}
    profitability_window_ne = db.Column(db.JSON)  # dict in Nepali

    ai_provider = db.Column(db.String(100))

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
