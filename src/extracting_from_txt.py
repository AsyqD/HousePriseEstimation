import pandas as pd
import numpy as np
import csv
import os

"""_______________Extract data from TXT file_______________________________________________"""
# search for specific target


def search_fn(line, target):
    for i in line:
        i = i.lower()
        if target in i:
            for item in i.split(', '):
                if target in item:
                    return item
    return None

def extract(file_from_extract):
    # file_from_extract = 'parsing_results/txt/parsing_result_240717_almaty_18000.txt'
    file_to_save = f'{file_from_extract.split('/')[0]}/csv/{file_from_extract.split('/')[2].split('.')[0]}.csv'
    with open(file_from_extract, "r", encoding="utf-8") as f:
        lines = f.readlines()
        i = 0
        """_______________Columns_________________"""
        number_of_rooms = []
        areas = []
        levels = []
        level = []
        prices = []
        districts = []
        microdistricts = []
        streets = []
        years = []
        isnewbuilding = []
        ceilings = []
        owners = []
        bathrooms = []
        repairs = []
        citys = []
        
        
        ll = set()
        ss = set()
        anomals = []
        for line in lines:
            """
            * Get the lines of txt data which should look like this:
            * 
            * "1-комнатная квартира, 40 м², 9/9 этаж|18 990 000 〒|Наурызбайский р-н, мкр Шугыла, Райымбека — Жуалы|жил. комплекс Nurly Dala, монолитный дом, 2023 г.п., состояние: хорошее, потолки 2.62м., санузел совмещенный, меблирована частично, Продается квартира в жк Нурлы дала от застройщика Базис-А рядом находится: - Апорт мол - Леруа Мерлен Планируются открыть две станции метро! Квартира чистая, светла…|Крыша Агент|Алматы|17 июл.|201|Оставить заметку"
            * 
            * Then split this `line` by `|` and get list which will look like this:
            * [
            *     '4-комнатная квартира, 160.85 м²', 
            *     'от 129 645 100 〒', 
            *     'Бостандыкский р-н, Лебедева 1/1', 
            *     'жил. комплекс Verdi, 9 этажей, 2025 г.п., потолки 3м., санузел 2 с/у и более, Преимущества💥Workout зона💥Тихий дв…', 
            *     'Новостройка', 'ЖК «Verdi»', 
            *     'от застройщика «BI Group»', 
            *     'Алматы', 
            *     '17 июл.', 
            *     '788', 
            *     'Оставить заметку'
            * ]
            """
            line = line.strip()
            line = line.split('|')
            
            
            """
            ______________Number of rooms_________________
            * The logic is to get first item of `line` which should look like this:
            * '4-комнатная квартира, 160.85 м²'
            * And get the number
            """
            first = line[0].split(', ')
            number_of_rooms.append(int(first[0].split('-')[0]))
            
            
            """
            _________________Owner_______________________
            * Here is the idea get -5th item of `line`, which should look like this:
            * 'от застройщика «BI Group»' or 'Хозяин недвижимости'. And there is only 4 types how this might be:
            * 1. 'xозяин недвижимости'
            * 2. 'cпециалист'
            * 3. 'крыша агент'
            * 4. 'новостройка'
            """
            own = line[-5]
            if 'хозяин' in own:
                owners.append('хозяин недвижимости')
            elif 'cпец' in own:
                owners.append('cпециалист')
            elif 'крыша' in own:
                owners.append('крыша агент')
            else:
                owners.append('новостройка')


            """
            _____________Area__________________________
            * This column is are of house on square meters `xx m^2`
            * The way to get it pretty simple:
            * frist item of line looks like this:
            * '4-комнатная квартира, 160.85 м²'
            * We just take this value
            """
            areas.append(float(first[1].split()[0]))
            
            
            """
            _______________level(floor)______________
            * This section for extract `level`(I have no idea why I named this `level` but anyway),
            * to do it we get also get first item of `line` which might look like this:
            * '1-комнатная квартира, 33 м², 5/5 этаж' or '3-комнатная квартира, 83 м²'
            * What we looking for is '5/5' frist is level of a house, second is level of a building
            * So just take them if there any
            """
            if len(first) < 3:
                levels.append(np.nan)
                level.append(np.nan)
            else:
                level.append(int(line[0].split(', ')[2].split()[0].split('/')[0]))
                try:

                    levels.append(
                        int(line[0].split(', ')[2].split()[0].split('/')[1]))
                except Exception as e:
                    levels.append(np.nan)


            """
            ________________Price(target)______________
            * It is pretty simple to take a price of a house, in second item of `line`
            * we get values: '20 500 000 〒' or 'от 52 955 000 〒'
            * Get rid of spaces and '〒' also 'от ' if needed
            """
            second = line[1]
            if "от" in second:
                prices.append(int(''.join(second.split()[1:-1])))
                isnewbuilding.append(True)
            else:
                prices.append(int(''.join(second.split()[:-1])))
                isnewbuilding.append(False)
               
                
            """
            ___________________City_____________________
            * Jus take the -4th item of `line` nothing special
            """
            citys.append(line[-4])


            """
            * TODO #1
            * Problem 1: Can get `districts` properly
            * need to code for searching `districts` by 'р-н'
            * Problem 2: Should get `microdistrits` properly if possible unless just drop the columns
            * Problem 3: Column `streets` is one HUGE problem... I haven no idea how to get street name from this random block
            * maybe we will be need LLM for that, I look for that and maybe also LLM for entire Information Extraction
            """
            third = line[2].lower().split(', ')

            microdistrict = np.nan
            street = np.nan
            if len(third) > 2:
                districts.append(third[0].split()[0])
                if 'мкр' in third[1] or 'микрорайон' in third[1]:
                    microdistrict = third[1]
                else:
                    street = third[1]
            elif len(third) < 2:
                districts.append(np.nan)
                if 'асыл арман' in third[0]:
                    districts.append('асыл арман')
                elif 'мкр' in third[0] or 'микрорайон' in third[0]:
                    microdistrict = third[0]
                else:
                    street = third[0]
            else:
                districts.append(third[0].split()[0])
                if 'мкр' in third[1] or 'микрорайон' in third[1]:
                    microdistrict = third[1]
                else:
                    street = third[1]

            microdistricts.append(microdistrict)
            streets.append(street)


            """
            _______________Build year________________
            * Search for 'г.п.' or 'г.п' and take the number before that
            """
            by = search_fn(line, 'г.п.')
            if by:
                years.append(int(by.split()[0]))
            else:
                by = search_fn(line, 'г.п')
                if by:
                    years.append(int(by.split()[0]))
                else: 
                    print(line)


            """
            ________________Ceiling hight___________________
            * Searh for keyword 'потолки' as a result you will get something like this:
            * 'потолки 3м.' if we get this result just take the number(floating number sometimes)
            * unless np.nan
            """
            ceiling = search_fn(line, 'потолки')
            try:

                if ceiling:
                    ceilings.append(float(ceiling.split()[1][:-2]))
                else:
                    ceilings.append(np.nan)
            except Exception as e:
                ceilings.append(np.nan)


            """
            _________________Type of bathroom_____________________
            * There is 4 types of bathroom on data:
            * 'совмещенный'
            * 'раздельный'
            * '2 с/у и более'
            * 'общий'
            * search for them.
            * If got different result add 'другой'
            * If got nothinng np.nan
            """
            bathroom = search_fn(line, 'санузел')
            if bathroom:
                bathroom = bathroom.lower()
                bb = ''
                if 'раздельный' in bathroom:
                    bb = 'раздельный'
                elif 'совмещен' in bathroom or 'совместный' in bathroom:
                    bb = 'совмещенный'
                elif '2' in bathroom:
                    bb = '2 с/у и более'
                elif 'общий' in bathroom:
                    bb = 'общий'
                else:
                    bb = 'другой'
                bathrooms.append(bb)
            else:
                bathrooms.append(np.nan)

            
            """
            __________________Type of repair_______________________
            * Here is the some types of repair on text
            * 'черновая отделка'
            * 'чистовая отделка'
            * 'предчистовая отделка'
            * 'требует ремонта'
            * 'хороший ремонт'
            * etc.
            * Algorithm is simple: check repair types above and if meet new just addd it)
            * If there is no any result for keyword 'ремонт' np.nan
            """
            repaired = search_fn(line, 'ремонт')
            dirty_repair = search_fn(line, 'чернов')
            clean_repair = search_fn(line, 'чистов')

            if repaired:
                repaired = repaired.lower()
                if 'требует ремонта' in repaired or 'требуется ремонта' in repaired:
                    repairs.append('требует ремонта')
                elif 'хороший ремонт' in repaired or 'хорошим ремонтом' in repaired or 'хорошего ремонта' in repaired:
                    repairs.append('хороший ремонт')
                elif 'свежий ремонт' in repaired or 'свежего ремонта' in repaired or 'свежим ремонтом' in repaired:
                    repairs.append('свежий ремонт')
                elif 'качественный ремонт' in repaired or 'качественным ремонтом' in repaired or 'качественного ремонта' in repaired:
                    repairs.append('качественный ремонт')
                elif 'капитальный ремонт' in repaired or 'капитального ремонта' in repaired or 'капитальным ремонтом' in repaired:
                    repairs.append('капитальный ремонт')
                elif 'после ремонта' in repaired:
                    repairs.append('после ремонта')
                elif 'евроремонт' in repaired or 'евро ремонт' in repaired:
                    repairs.append('евроремонт')
                elif 'дизайнер' in repaired:
                    repairs.append('дизайнерский ремонт')
                else:
                    repairs.append('дргуой ремонт')
            elif dirty_repair:
                dirty_repair = dirty_repair.lower()
                repairs.append('черновая отделка')

            elif clean_repair:
                clean_repair = clean_repair.lower()
                if 'предчистов' in clean_repair:
                    repairs.append('предчистовая отделка')
                else:
                    repairs.append('чистовая отделка')

            else:
                repairs.append(np.nan)
                
                
        """________________________Write all data to CSV fie________________________"""
        rows = zip(number_of_rooms, areas, levels, level, prices, districts,
                microdistricts, streets, years, ceilings, isnewbuilding, owners, bathrooms, repairs)

        # Write the data to the CSV file
        with open(file_to_save, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # Write the header row if needed
            writer.writerow(['numrooms', 'squaremeters', 'levels_on_building', 'level', 'price', 'district',
                            'microdistrict', 'street', 'builtyear', 'ceilinghight', 'isnewbuilding', 'seller', 'bathroomtype', 'repaired'])

            # Write the data rows
            writer.writerows(rows)


if __name__ == "__main__":
    files = os.listdir('parsing_results/txt')
    for file in files:
        extract(f'parsing_results/txt/{file}')
        print(f'file {file} done extracting')