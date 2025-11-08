import math

def make_json_safe(value):
    """Recursively converts NaN, inf, numpy types, etc. to safe JSON-compatible values."""
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            return None
        return float(value)  # ensure primitive float
    
    if isinstance(value, list):
        return [make_json_safe(v) for v in value]
    
    if isinstance(value, dict):
        return {k: make_json_safe(v) for k, v in value.items()}
    
    # Catch-all: convert to string
    return str(value)
