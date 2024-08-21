from datetime import datetime, timedelta
import locale


def check_future_date(day, month):
    """
    Check if the provided date is in the future.

    Parameters:
    day (str): The day of the month as a string.
    month (str): The month name as a string.

    Returns:
    None
    """
    locale.setlocale(locale.LC_TIME, "de_DE")
    current_date = datetime.now()
    given_date = datetime(current_date.year, datetime.strptime(month, "%B").month, int(day))
    
    if given_date > current_date:
        return True
    
def get_preceding_7_days_with_year(day, month):
    locale.setlocale(locale.LC_TIME, "de_DE")
    current_year = datetime.now().year
    given_date = datetime(current_year, datetime.strptime(month, "%B").month, int(day))
        
    locale.setlocale(locale.LC_TIME, "en_US")    
    preceding_days = [
        (str((given_date - timedelta(days=i)).day),   
         (given_date - timedelta(days=i)).strftime("%B"),
         str((given_date - timedelta(days=i)).year)) 
        for i in range(1, 8)
        ]
    
    return preceding_days