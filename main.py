import datetime
import time
from project.count_easter import easter
from project.astro import find_full_moon_jpl
from project.astro import get_illumination


# oblicz datę Wielkanocy dla wybranych lat
for rok in range(2053, 3001):
    print(f"\033[91m___________________________________{rok}__________________________________________\033[0m")
    easter_date = easter(rok)
    print(f"Easter: {easter_date.strftime('%Y-%m-%d')}", end="")
    dzień_tygodnia = easter_date.strftime('%A')
    print(f" ({dzień_tygodnia})") # tylko dla sprawdzenia, czy na pewno niedziela
    
    # oblicz illuminację Księżyc w dniu Wielkanocy obliczonej metodą nicejską
    easter_illumination = get_illumination(easter_date)
    print(f"Oświetlenie Księżyca dla {easter_date.strftime('%Y-%m-%d %H:%M')}: {easter_illumination:.2f}%")

    # szukaj pełni księżyca przed datą Wielkanocy (obliczoną metodą nicejską) ____________________
    found = False  
    try_count = 1 
    start_date = easter_date 
    while not found and try_count < 5:
        found, best_time, best_angle, best_illum = find_full_moon_jpl(start_date) # szukaj pełni przez 8 dni - zakończ w sobotę przed Wielkanocą
        if not found:
            #odejmij od start_date 8 dni
            start_date = start_date - datetime.timedelta(days=8)
            print(f"Nie znaleziono pełni {8*try_count} dni przed Wielkanocą. Szukam wcześniej od {(start_date - datetime.timedelta(days=8)).strftime('%Y-%m-%d')}")
            try_count += 1

    if found:
        # przeszukaj teraz moment pełni rozszerzony o 2 godziny w przód i w tył z dokładnością do 1 minuty
        print(f"Zakres precyzyjnego przeszukowania bazy +/-2h: {best_time.strftime('%Y-%m-%d %H:%M')} UTC")
        found_prec, best_time_prec, best_angle_prec, best_illum_prec = find_full_moon_jpl(best_time, days=0, step='1m')
        print(f">>> Pełnia księżyca: {best_time_prec.strftime('%Y-%m-%d %H:%M')} UTC", end="")
        dzień_tygodnia_fm = best_time_prec.strftime('%A')
        print(f" ({dzień_tygodnia_fm}) ", end="")
        delta_days = (best_time_prec - easter_date).days
        print(f"({delta_days} dni przed Wielkanocą)")
        print(f"Alpha: {best_angle_prec:.2f}°")
        print(f"Procent oświetlenia: {best_illum_prec:.2f}%")
    
        # zapisz dane do pliku easter_data.txt, kolejność: 
        # data Wielkanocy, dzień tygodnia, data pełni, godzina pełni, dzień tygodnia pełni, delta dni między pełnią a Wielkanocą, elongacja, oświetlenie    
        with open(f"easter_data.txt", "a") as file:
            file.write(f"{easter_date.strftime('%Y-%m-%d')}\t")
            file.write(f"{easter_date.strftime('%A')}\t")
            file.write(f"{easter_illumination:.2f}\t") # oświetlenie Księżyca w dniu Wielkanocy
            file.write(f"{best_time_prec.strftime('%Y-%m-%d %H:%M')}\t")
            file.write(f"{dzień_tygodnia_fm}\t")
            file.write(f"{delta_days}\t")
            file.write(f"{best_angle_prec:.2f}\t") # elongacja
            file.write(f"{best_illum_prec:.2f}\t") # oświetlenie w procentach
        time.sleep(5) # zatrzymaj program na 5 sekund żeby nie przeciążyć serwera JPL 
    
    else:
        print("Nie znaleziono pełni w zadanym przedziale. Spróbuj zmienić search_days lub step.")


    # szukaj pełni PO dacie Wielkanocy (obliczonej metodą nicejską) -
    # przydatne do porównania, czy pełnia przed Wielkanocą jest bliżej niż po Wielkanocy albo w samą Wielkanoc
    found = False # resetuj zmienną
    try_count = 1 
    start_date = best_time_prec + datetime.timedelta(days=30) # dodaj 30 dni do daty pełni i szukaj wstecz
    while not found and try_count < 5:
        found, best_time, best_angle, best_illum = find_full_moon_jpl(start_date, 1, '1h') # szukaj pełni 
        if not found:
            #odejmij od start_date 8 dni
            start_date = start_date - datetime.timedelta(days=8)
            print(f"Nie znaleziono pełni {8*try_count} dni przed Wielkanocą. Szukam wcześniej od {(start_date - datetime.timedelta(days=8)).strftime('%Y-%m-%d')}")
            try_count += 1

    if found:
        # przeszukaj teraz moment pełni rozszerzony o 2 godziny w przód i w tył z dokładnością do 1 minuty
        print("\033[94m________________Kolejna pełnia\033[0m")
        print(f"\033[94mZakres precyzyjnego przeszukowania bazy +/-2h: {best_time.strftime('%Y-%m-%d %H:%M')} UTC\033[0m")
        found_prec, best_time_prec, best_angle_prec, best_illum_prec = find_full_moon_jpl(best_time, days=0, step='1m')
        print(f"\033[94m>>> Pełnia księżyca po WLK: {best_time_prec.strftime('%Y-%m-%d %H:%M')} UTC\033[0m", end="")
        dzień_tygodnia_fm = best_time_prec.strftime('%A')
        print(f"\033[94m ({dzień_tygodnia_fm}) \033[0m", end="")
        delta_days = (best_time_prec - easter_date).days
        print(f"\033[94m({delta_days} dni po Wielkanocy)\033[0m")
        print(f"\033[94mAlpha: {best_angle_prec:.2f}°\033[0m")
        print(f"\033[94mProcent oświetlenia: {best_illum_prec:.2f}%\033[0m")
        print("\033[94m________________\033[0m")
    
        # zapisz dane do pliku easter_data.txt, kolejność: 
        # data Wielkanocy, dzień tygodnia, data pełni, godzina pełni, dzień tygodnia pełni, delta dni między pełnią a Wielkanocą, elongacja, oświetlenie    
        with open(f"easter_data.txt", "a") as file:
            file.write(f"{best_time_prec.strftime('%Y-%m-%d %H:%M')}\t") # data pełni po WLK
            file.write(f"{dzień_tygodnia_fm}\t")
            file.write(f"{delta_days}\t")
            file.write(f"{best_angle_prec:.2f}\t") # elongacja
            file.write(f"{best_illum_prec:.2f}\t") # oświetlenie w procentach
        time.sleep(5) # zatrzymaj program na 5 sekund żeby nie przeciążyć serwera JPL 
    
    else:
        print("Nie znaleziono pełni w zadanym przedziale. Spróbuj zmienić search_days lub step.")
    

    #teraz zaproponuj korektę daty Wielkanocy, tak, żeby w niedzielę wielkanocną było najbliżej pełni księżyca
    # warunek: Wielkanoc po 21 marca
    # zaproponuj wielkanoc w niedzielę przed pełnią i oblicz illuminację
    easter_date_corrected = easter_date - datetime.timedelta(days=7) # zmień datę Wielkanocy na tydzień wcześniej
    print("\033[92m________________WLK tydzień wcześniej\033[0m")
    print(f"\033[92mKorekta daty Wielkanocy -7 dni: {easter_date_corrected.strftime('%Y-%m-%d')}\033[0m", end="")
    dzień_tygodnia = easter_date_corrected.strftime('%A')
    print(f"\033[92m ({dzień_tygodnia})\033[0m") # tylko dla sprawdzenia, czy na pewno niedziela
    #oblicz illuminację Księżyca dla nowej daty Wielkanocy
    easter_illumination_corrected = get_illumination(easter_date_corrected)
    print(f"\033[92mOświetlenie Księżyca dla {easter_date_corrected.strftime('%Y-%m-%d %H:%M')}: {easter_illumination_corrected:.2f}%\033[0m")
    # wylicz różnicę w oświetleniu między Wielkanocą i Wielkanocą po korekcie
    diff_illumination = easter_illumination_corrected - easter_illumination
    print(f"\033[92mRóżnica oświetlenia: {diff_illumination:.2f}%\033[0m")
    print("\033[92m________________\033[0m")
    print("\n")

    # zapisz dane do pliku easter_data.txt,
    with open(f"easter_data.txt", "a") as file:
        file.write(f"{easter_date_corrected.strftime('%Y-%m-%d')}\t") # data pełni po WLK
        file.write(f"{dzień_tygodnia}\t")
        file.write(f"{easter_illumination_corrected:.2f}\t") # oświetlenie w procentach
        file.write(f"{diff_illumination:.2f}\n")

