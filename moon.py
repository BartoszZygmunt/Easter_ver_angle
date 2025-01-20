from astroquery.jplhorizons import Horizons

obj = Horizons(
    id='301',           # 301 = Moon
    location={'lon': 19.0238, 'lat': 50.2649, 'elevation': 274},  # Katowice, Polska
    epochs={
        'start': '2025-01-13 21:35', 
        'stop':  '2025-01-13 22:35',
        'step':  '10m'
    }
)

eph = obj.ephemerides(quantities='10,43,4,5' )  # 31 = geocentric ecliptic long. & lat.
print(eph.colnames)

#odczytaj alpha_true oraz illumination
for row in eph:
    print(f"DateTime: {row['datetime_str']}, Alpha True: {row['alpha_true']}, Illumination: {row['illumination']}, Elewacja: {row['EL']}, Azymuth: {row['AZ']}, Lunar: {row['lunar_presence']}")


#24. ilumination 0-1
#46 elong
#48 phase angle

