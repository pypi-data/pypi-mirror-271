from pypdf import PdfReader
import re
import os
import json
from datetime import datetime, date
from finfo.PDF_replacer import download_pdf
from finfo.exceptions import InvalidCategory

country_codes = {'AIN', 'VIE', 'TUN', 'JOR', 'AZE', 'BOL', 'CAN', 'TKM', 'NGR', 
                 'ROU', 'GRE', 'MAR', 'UZB', 'IRI', 'NCA', 'EST', 'PHI', 'LBA', 
                 'UAE', 'LBN', 'MKD', 'TPE', 'BUL', 'IRL', 'CYP', 'MGL', 'SEN', 
                 'POL', 'POR', 'QAT', 'SUI', 'KSA', 'MAS', 'CZE', 'PAR', 'KGZ', 
                 'TUR', 'MEX', 'BRA', 'ALG', 'IND', 'INA', 'ARM', 'PAN', 'DEN', 
                 'CRC', 'ESP', 'EGY', 'THA', 'SRB', 'PUR', 'RSA', 'CHN', 'FIN', 
                 'GBR', 'KUW', 'MDA', 'MAC', 'ITA', 'COD', 'AUS', 'CHI', 'ARG', 
                 'ANG', 'USA', 'OMA', 'PER', 'KOR', 'FRA', 'JPN', 'NZL', 'NOR', 
                 'UKR', 'SVK', 'MLT', 'HKG', 'SGP', 'COL', 'GER', 'SWE', 'ESA', 
                 'JAM', 'LAT', 'VEN', 'SLO', 'LUX', 'BRN', 'GEO', 'CRO', 'BEL', 
                 'AUT', 'NED', 'ISR', 'ISV', 'LTU', 'HUN', 'KAZ', 'DOM', 'ECU', 
                 'GUA', 'URU', 'NIG', 'IRQ', 'GHA', 'BER', 'ISL', 'TOG', 'PAK'
                 'BAR', 'RUS', 'CPV', 'MLI', 'CIV', 'BAH', 'MRI', 'CUB', 'MNE'
                 'GUY', 'TJK', 'BEN', 'PAK', 'SRI', 'KEN', 'BUR', 'HON', 'NEP',
                 'BRU', 'UGA', 'CMR', 'RWA', 'BAR', 'HAI', 'YEM', 'ARU', 'SYR', 
                 'MNE', 'MON', 'SUD'}

# For some reason it says that MNE, and GUY is not part of the list. FIX

# Get the absolute path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))


# Getting the path to the JSON file
historical_rankings = os.path.join(current_dir, "historical_rankings.json")

# Get JSON data
with open(historical_rankings, "r") as file:
    json_data = json.load(file)


# Get all the categories
categories = [category[:-4] for seasons in json_data.values() for category in seasons]


def _read_pdf(pdf, season, category):

    today = date.today()
    athlete_dict = {}
    dict_index = 1
    list_index = 0
    letters_in_text = ''
    removal_start = ''
    country_code_pattern = r'\b[A-Z]{3}\b'
    name_country_split = r'(?<=[a-z])(?=[A-Z])'
    removal_start_pattern = r'T\d+T'

    if season == "2023_2024":
        with open(historical_rankings, 'w') as file:
            
            # Getting the date the pdf was downloaded
            pdf_date = json_data[season][category]["date"]

            # Turning the date string into a datetime object
            datetime_date = datetime.strptime(pdf_date,'%Y-%m-%d')
            
            # Calculating the days between today and the last download
            time_difference = datetime.today() - datetime_date
            days_difference = time_difference.days

            if (days_difference >= 7):
                download_pdf(category)
                print("Auto updating PDF to not miss changes in the ranking")

                # Setting the last date downloaded to today
                string_today = today.strftime("%Y-%m-%d")
                json_data[season][category]["date"] = string_today
            
            file.seek(0)
            file.write(json.dumps(json_data))

    # Setting up the reader
    try:
        reader = PdfReader(pdf)
    except FileNotFoundError:
        download_pdf(category)
        print("Downloading ranking, because is it missing.")
        reader = PdfReader(pdf)

    # Getting all the text
    for i in range(len(reader.pages)):
        page = reader.pages[i].extract_text()
        letters_in_text += page

    # Splitting the text up into words so I can find the removal_start
    words_in_text = letters_in_text.split()

    # Finding the indecator for when the "athletes" actually begin coming
    for item in words_in_text:
        if re.search(removal_start_pattern, item):
            removal_start = item
            break

    # Removing everything before the "removal_start" parameter, because it has nothing to do with athletes.
    athletes_letters = letters_in_text.split(removal_start, 1)[1]

    # Removing everything after the text 'all assigned competitions' because it has nothing to do with athletes.
    athletes_letters = athletes_letters.split("all assigned competitions", 1)[0]

    #This removes all '/', numbers and '.' from the string.
    athletes_letters = re.sub(r'[./()\d]', '', athletes_letters)

    #This removes all "'" from the string.
    athletes_letters = re.sub(r"'", '', athletes_letters)

    # Sometimes the countryCode and name clumps togeter, this splits them apart, and puts a space between them.
    athletes_letters = re.sub(name_country_split, ' ', athletes_letters)

    # This splits the string up into a list.
    athletes_words = athletes_letters.split()


    while list_index < len(athletes_words):
        word = athletes_words[list_index]
        match_country = re.search(country_code_pattern, word)
        if match_country:
            if list_index < 2 or word not in country_codes:
                list_index += 1
                continue
            #elif word not in country_codes:
            #    print(word)
             #   list_index += 1
              #  continue
            athlete = athletes_words[:list_index + 1]
            del athletes_words[:list_index + 1]
            athlete_obj = {
                "Lastname": athlete[0].lower(),
                "Firstname": athlete[-2].lower(),
                "CountryCode": athlete[-1],
                "Rank": dict_index
            }
            athlete_dict[dict_index] = athlete_obj
            dict_index += 1
            list_index = 0
            continue

        list_index += 1

    return athlete_dict

def read_pdf(category):
    # Construct the absolute path to the pdf directory within your package
    pdf_dir = os.path.join(current_dir, 'pdf')
    
    #Check if category exists
    for cat in categories:
        if cat == category:
            file_path = os.path.join(pdf_dir, cat + ".pdf")
            season = cat.split(cat[:-9], 1)[1]
            return _read_pdf(file_path, season, cat)
    
    raise InvalidCategory(category, categories)
