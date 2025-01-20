import datetime

def easter(year):
    
    """
    Calculates the date of Easter for the given year.
    Input parameter: year (int): The year for which the date of Easter is calculated.
    Returns: the full date of Easter in datetime format (time set to 0:00).
    """

    a = year % 19
    b = year // 100
    c = year % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    month = (h + l - 7 * m + 114) // 31
    day = ((h + l - 7 * m + 114) % 31) + 1

    # convert month and day to full date, set time to 0:00
    easter_date = datetime.datetime(year, month, day, 0, 0)

    return easter_date


