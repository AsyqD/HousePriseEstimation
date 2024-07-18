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


file_from_extract = 'parsing_results/txt/parsing_result_240717_almaty_18000.txt'
file_to_save = f'{file_from_extract.split('/')[0]}/csv/{file_from_extract.split('/')[2].split('.')[0]}.csv'
with open(file_from_extract, "r", encoding="utf-8") as f:
    lines = f.readlines()
    i = 0
    # columns
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
    ll = set()
    ss = set()
    anomals = []
    for line in lines:
        line = line.strip()
        line = line.split('|')

        first = line[0].split(', ')

        # no. of rooms
        number_of_rooms.append(int(first[0].split('-')[0]))

        # owners
        own = line[-5]
        if 'хозяин' in own:
            owners.append('хозяин недвижимости')
        elif 'cпец' in own:
            owners.append('cпециалист')
        elif 'крыша' in own:
            owners.append('крыша агент')
        else:
            owners.append('новостройка')

        # area
        areas.append(float(first[1].split()[0]))
        
        # level of building
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

        # price
        second = line[1]
        if "от" in second:
            prices.append(int(''.join(second.split()[1:-1])))
            isnewbuilding.append(True)
        else:
            prices.append(int(''.join(second.split()[:-1])))
            isnewbuilding.append(False)

        # location
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

        # build year
        by = search_fn(line, 'г.п.')
        if by:
            years.append(int(by.split()[0]))
        else:
            by = search_fn(line, 'г.п')
            if by:
                years.append(int(by.split()[0]))
            else:
                print(line)

        # ceiling height
        ceiling = search_fn(line, 'потолки')
        try:

            if ceiling:
                ceilings.append(float(ceiling.split()[1][:-2]))
            else:
                ceilings.append(np.nan)
        except Exception as e:
            ceilings.append(np.nan)

        # type of bathroom
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

        # type of repair
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
    for ii in anomals:
        print(ii, end='\n\n')
    print(len(anomals))
    """-------------- Write all data to CSV fie----------------------------------------------------------------"""
    rows = zip(number_of_rooms, areas, levels, level, prices, districts,
               microdistricts, streets, years, ceilings, owners, bathrooms, repairs)

    # Specify the CSV file path
    # Write the data to the CSV file
    with open(file_to_save, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header row if needed
        writer.writerow(['numrooms', 'sqauremeters', 'levels_on_building', 'level', 'price', 'distrcit',
                        'microdistrict', 'street', 'builtyear', 'ceilinghight', 'seller', 'bathroomtype', 'repaired'])

        # Write the data rows
        writer.writerows(rows)
