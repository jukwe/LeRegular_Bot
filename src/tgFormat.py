# format all prices
def format_prices(current_val):
    THOUSAND = 1000
    MILLION = 1000000
    BILLION = 1000000000
    TRILLION = 1000000000000
    current_val = float(current_val)
    if THOUSAND <= current_val < MILLION:
        suffix = 'K'
        formatted_value = current_val/THOUSAND
        formatted_value = round(formatted_value, 2)
        
    elif MILLION <= current_val < BILLION:
        suffix = 'M'
        formatted_value = current_val/MILLION
        formatted_value = round(formatted_value, 2)
        
    elif BILLION <= current_val < TRILLION:
        suffix = 'B'
        formatted_value = current_val/BILLION
        formatted_value = round(formatted_value, 2)
        
    elif current_val > TRILLION:
        suffix = 'T'
        formatted_value = current_val/TRILLION
        formatted_value = round(formatted_value, 2)
    return formatted_value, suffix 