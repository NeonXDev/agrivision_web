"""Looks up the current Nepal market price for an identified crop.

STAGE 5 fills this in — point it at Nepal's Department of Agriculture /
Kalimati market data, or whatever source you settle on: an official feed,
a scraped dataset behind your own small endpoint, or a third-party
aggregator.
"""


def get_price_for_crop(crop_name: str) -> dict | None:
    """Returns a dict with keys: crop_name, min_price, max_price,
    avg_price, unit, market, date — or None if no match is found.

    Raises NotImplementedError until Stage 5.
    """
    raise NotImplementedError(
        'market_price_service.get_price_for_crop — Stage 5'
    )
