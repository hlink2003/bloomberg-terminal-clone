def format_price_change(change, change_pct):
    """Format price change with color coding"""
    if change >= 0:
        return f'<span style="color: #00ff00;">+${change:.2f} (+{change_pct:.2f}%)</span>'
    else:
        return f'<span style="color: #ff0000;">${change:.2f} ({change_pct:.2f}%)</span>'

def format_large_number(number):
    """Format large numbers with commas"""
    return f"{number:,.0f}"

def format_currency(amount):
    """Format currency with proper decimal places"""
    return f"${amount:.2f}"