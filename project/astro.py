import datetime
import numpy as np
import math as math
from astroquery.jplhorizons import Horizons

# Function to parse dates from JPL Horizons
def parse_horizons_datetime(dt_str):
    """
    Parses date and time strings from Horizons (datetime_str column).
    Removes any suffixes and tries several common formats.
    """
    # Remove any "UTC", "UT", "TDB" suffixes
    dt_str = dt_str.replace(' UTC', '').replace(' UT', '').replace(' TDB', '')
    
    formats = [
        '%Y-%b-%d %H:%M',
        '%Y-%b-%d %H:%M:%S.%f',
        '%Y-%b-%d %H:%M:%S',
        '%Y-%b-%d %H',
        '%Y-%b-%d'
    ]
    for fmt in formats:
        try:
            return datetime.datetime.strptime(dt_str, fmt)
        except ValueError:
            pass
    # jeśli nic się nie udało:
    # if nothing worked:
    raise ValueError(f"Could not parse date string from Horizons: {dt_str}")


# Function to fetch the Sun-Moon-Earth angle (alpha_true) and the percentage of the visible moon disk (illumination) from JPL Horizons
def get_alpha(start_time, stop_time, step='1h'):
    """
    Fetches from JPL Horizons (astroquery) the Sun-Moon-Earth angle (alpha_true) and the illumination of the Moon
    in the interval [start_time, stop_time] with a step of 'step'.
    Returns (list_of_datetimes, numpy_array_of_angles, numpy_array_of_illuminations).
    """

    # Create a Horizons object for the Moon (id='301')
    obj = Horizons(
        id='301',           # 301 = Moon
        location='@399',    # geocentrically (Earth = 399)
        epochs={
            'start': start_time.strftime('%Y-%m-%d %H:%M'),
            'stop':  stop_time.strftime('%Y-%m-%d %H:%M'),
            'step':  step
        }
    )

    eph = obj.ephemerides(quantities='10,43', extra_precision=True) # alpha_true, illumination
    # print(eph.colnames) # check the column names
    
    times = []
    angles = []
    illuminations = []

    for row in eph:
        dt_str = row['datetime_str']   # ex. '2024-Dec-22 00:00:00.0000 UTC'
        dt_parsed = parse_horizons_datetime(dt_str)
        times.append(dt_parsed)
        
        moon_angle = float(row['alpha_true'])  # Sun-Moon-Earth angle
        angles.append(moon_angle)

        illum = float(row['illumination'])  # Illumination of the disk in percentage
        illuminations.append(illum) 
    
    return np.array(times), np.array(angles), np.array(illuminations) # Return as numpy arrays


# Main function to find the moment of full moon (alpha_true = min - around 0; illumination = max - around 100)
def find_full_moon_jpl(start_date, days=8, step='1h'):
    """
    Szuka momentu pełni zaczynając od 'start_date' (datetime, UTC),
    cofa się w przeszłość, z rozdzielczością 'step'.
    Zwraca (czy_znaleziono, data_pełni, alpha_true, illumination).
    """

    if days > 0:
        stop_date = start_date
        start_date = start_date - datetime.timedelta(days) 
    else:
        start_date = start_date - datetime.timedelta(hours=2) # to avoid finding the same full moon again
        stop_date = start_date + datetime.timedelta(hours=4)

    # Pobieramy dane z Horizons
    moon_times, moon_angles, moon_illum = get_alpha(start_date, stop_date, step)

    # Szukamy maksimum oświetlenia
    max_illum_idx = np.argmax(moon_illum)


    # Sprwadź, czy to nie jest pierwsza lub ostatnia próbka
    if max_illum_idx == 0 or max_illum_idx == len(moon_illum)-1: 
        return False, None, None, None
    
    # 1) Maksymalna wartość
    max_val = np.max(moon_illum) 
    # 2) Indeksy, gdzie mamy tę wartość:
    max_indices = np.where(moon_illum == max_val)[0] 
    # 3) Wybranie środkowego
    middle_index = max_indices[len(max_indices)//2] 
   
    found = True
    best_time = moon_times[middle_index]
    best_angle = moon_angles[middle_index]
    best_illum = moon_illum[middle_index]

    return found, best_time, best_angle, best_illum

# Funkcja o odczytania z Horizons procentu oświetlenia tarczy Księżyca, w wejściu data i godzina, zwraca procent oświetlenia
def get_illumination(date_time):
    """
    Fetches from JPL Horizons (astroquery) the illumination of the Moon
    at the specified date and time.
    Returns the illumination in percentage.
    """
    # Create a Horizons object for the Moon (id='301')
    date_start = date_time
    date_stop = date_time + datetime.timedelta(minutes=1)
    obj = Horizons(
        id='301',           # 301 = Moon
        location='@399',    # geocentrically (Earth = 399)
        epochs={
            'start': date_start.strftime('%Y-%m-%d %H:%M'),
            'stop':  date_stop.strftime('%Y-%m-%d %H:%M'),
            'step':  '1m'
        }
    )

    eph = obj.ephemerides(quantities='10,43', extra_precision=True) # illumination
    

    row = eph[0]
    illum = float(row['illumination'])  # Illumination of the disk in percentage
    # print(f"Oświetlenie Księżyca dla {date_time.strftime('%Y-%m-%d %H:%M')}: {illum:.2f}%")
    return illum