from datetime import datetime, timedelta

def to_unix_time(date_str):
    """
    Takes a date str in the format of
    (ex) 2024/01/19 12:20:46 PM AST,
    removes timezone (AST) from str, 
    returns unix time interval conversion
    """

    date_format = "%Y/%m/%d %I:%M:%S %p"

    dt_naive = datetime.strptime(date_str[:-4], date_format)  # Exclude ' AST'

    dt_utc = dt_naive - timedelta(hours=4)

    unix_time = int(dt_utc.timestamp())
    
    return unix_time