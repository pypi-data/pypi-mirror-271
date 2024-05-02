import requests
import os
import json
from datetime import date
from finfo.exceptions import InvalidCategory, InvalidSeason

# Get the absolute path to the directory containing this script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Getting the path to the JSON file
historical_rankings = os.path.join(current_dir, "historical_rankings.json")

# Todays date
today = date.today()

# Getting the JSON data
with open(historical_rankings, "r") as file:
    json_data = json.load(file)


# Getting the categories
categories = [category[:-4] for seasons in json_data.values() for category in seasons]


# function for downloading all files (with no arguments needed)
def _download_pdfs(urls, season):

    # Construct the absolute path to the pdf directory within your package
    pdf_dir = os.path.join(current_dir, 'pdf')

    sucess = 0
    failed = 0

    # Creating the PDF folder if it does not exist
    if not os.path.exists(pdf_dir):
        os.mkdir(pdf_dir)

    # Send GET request
    for key, value in urls.items():

        response = requests.get(value.get("link")) 

        #Getting the file name
        file_name = os.path.join(pdf_dir, key)

        # Save the PDF
        if response.status_code == 200:
            sucess += 1
            with open(file_name, "wb") as f:
                f.write(response.content)
            print(f"Downloading PDF: {file_name}")

            with open(historical_rankings, "w") as f:
                string_today = today.strftime("%Y-%m-%d")
                json_data[season][key]["date"] = string_today
                f.seek(0)
                f.write(json.dumps(json_data))
        else:
            failed += 1
            print(response.status_code)
            print(f"Downloading PDF: {file_name} FAILED")
    print(f"Sucess {sucess}")
    print(f"Fuilure {failed}")


def _download_pdf(url, season, name):

    # Get the absolute path to the directory containing this script
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the absolute path to the pdf directory within your package
    pdf_dir = os.path.join(current_dir, 'pdf')

    # Creating the PDF folder if it does not exist
    if not os.path.exists(pdf_dir):
        os.mkdir(pdf_dir)

    # Send GET request
    response = requests.get(url.get("link")) 

    #Getting the file name
    file_name = os.path.join(pdf_dir, name)

    # Save the PDF
    if response.status_code == 200:

        # Creating the file
        with open(file_name, "wb") as f:
            f.write(response.content)
            print(f"Downloading PDF: {file_name}")

        # Giving it todays date as date value
        with open(historical_rankings, "w") as f:
            string_today = today.strftime("%Y-%m-%d")
            json_data[season][name]["date"] = string_today
            f.seek(0)
            f.write(json.dumps(json_data))
    else:
        print(response.status_code)
        print(f"Downloading PDF: {file_name} FAILED")

        
def download_pdf(name):
    name = name + '.pdf'
    for season in json_data:
        for category in json_data[season]:
            if name == category:
                url = json_data[season][name]
                return(_download_pdf(url, season, name))
            else:
                continue

    raise InvalidCategory(name, categories)


def download_pdfs(season):
    if season not in json_data.keys():
        raise InvalidSeason(season, json_data.keys())
    else:
        urls = json_data[season]
        return(_download_pdfs(urls, season))


# Maybe bring the singular pdf downloader back. So if the pdf_reader sees that the date is old, it only redownloads that file and not every file in that season.
# Remember it should only do this with the current season, because the older season cannot change.
