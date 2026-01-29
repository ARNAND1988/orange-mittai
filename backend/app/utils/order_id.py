from datetime import datetime

def generate_order_id(order_db_id: int) -> str:
    """
    Generates a unique, readable order ID like:
    ORD-20260126-00042
    """
    date_part = datetime.utcnow().strftime("%Y%m%d")
    return f"ORD-{date_part}-{str(order_db_id).zfill(5)}"
