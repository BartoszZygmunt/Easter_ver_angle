# program oblicza oświetlenie księżyca w dniach podanych w liście dates_to_calc - pozycje ID 1-53

import datetime
import time
from project.astro import get_illumination

dates_to_calc = [
    "1900-04-22", "1903-04-19", "1927-04-24", "1954-04-25", "1967-04-02", 
    "1981-04-26", "2049-04-25", "2076-04-26", "2106-04-25", "2147-04-23", 
    "2150-04-19", "2170-04-08", "2174-04-24", "2201-04-26", "2245-04-20", 
    "2299-04-23", "2394-04-24", "2417-04-09", "2421-04-25", "2448-04-26", 
    "2451-04-23", "2492-04-20", "2495-04-17", "2515-04-07", "2519-04-23", 
    "2546-04-24", "2586-04-02", "2590-04-18", "2668-04-26", "2715-04-18", 
    "2725-04-26", "2739-04-23", "2742-04-19", "2762-04-08", "2766-04-24", 
    "2793-04-25", "2820-04-26", "2833-04-03", "2837-04-19", "2891-04-22", 
    "2908-04-15", "2931-04-01", "2935-04-17", "1923-04-08", "2119-04-02", 
    "2339-04-02", "2437-03-29", "2471-04-12", "2711-04-02", "2718-04-14", 
    "2491-04-01", "2738-04-03", "2133-03-22"
]

for date in dates_to_calc:
    date_obj = datetime.datetime.strptime(date, "%Y-%m-%d")
    #wyświetl godzinę tej daty
    # print(f"{date}\ttime:\t{date_obj.strftime('%H:%M')}")
    illumination = get_illumination(date_obj)
    print(f"{date}\tillumination:\t{illumination:.2f}")
    with open(f"nowe_daty.txt", "a") as file:
        file.write(f"{date}\tillumination:\t{illumination:.2f}\n")