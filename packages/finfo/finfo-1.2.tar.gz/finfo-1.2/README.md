# Finfo
This is a python-package used to get current and histrorical rankings of fencers.

## Table of Contents

1. [Installation](#installation)
2. [Practical Information](#practical-information)
3. [Usage](#usage)
4. [Contributing](#contributing)
5. [License](#license)

## Installation

```bash
pip install finfo
```

## Practical information
Before you begin to use this package I have some practical information.

1.
There are current and historical fencing rankings you can access.
The historic ones only go back to the 2019-2020 season.

2. 
We have made out own system to classify how one should look up the rankings.
You can get all the categories when running the all_fencing_categories function.

3.
This package is built around reading the rankings from the official PDF files.
This means that sometimes the runtime is a bit slow, because it needs to pull the latest packages.

## Usage

### Table of Contents

1. [Configuring class](#Configuring-class)
2. [Getting specific fencer by rank](#Getting-specific-fencer-by-rank)
3. [Getting specific fencer by name](#Getting-specific-fencer-by-name)
4. [Getting all fencers from a specific country](#Getting-all-fencers-from-a-specific-country)
5. [Getting all categories](#Getting-all-categories)

### Configuring class
Almost all actions will be used on a class. This class will be configured like this:

```python
from finfo.FIE import FIE

fie = FIE(season)
```
An example of this can look like this:
```python
fie = FIE("foil_senior_men_2022_2023")
```

### Getting specific fencer by rank

This method takes a rank, and outputs the athlete:

```python
from finfo.FIE import FIE

fie = FIE("foil_senior_men_2022_2023")

fie.find_fencer_by_rank(1)
```

```bash
{"First name": "Alexander", "Last name": "Massiales", "CountryCode": "USA"}

```

### Getting specific fencer by name
This method takes the fencers name, and outputs the fencer as a dictionary object with rank, name and countrycode.

```python
from finfo.FIE import FIE

fie = FIE("foil_senior_men_2022_2023")

fie.find_fencer_by_name('alexander', 'massiales')
```

```bash
{"First name": "Alexander", "Last name": "Massiales", "CountryCode": "USA", "Rank": 1}

```

### Getting all fencers from a specific country
This method takes an countrycode, and outputs all the fencers from that country.

```python
from finfo.FIE import FIE

fie = FIE("foil_senior_men_2022_2023")

fie.get_all_fencers_from_country("CYP")
```

```bash
[{'Lastname': 'tofalides', 'Firstname': 'alex', 'CountryCode': 'CYP', 'Rank': 68}, {'Lastname': 'kiayias', 'Firstname': 'william', 'CountryCode': 'CYP', 'Rank': 762}]

```

### Getting all categories
This method takes no arguments, and outputs all valid categories.

```python
from finfo.FIE import all_fencing_categories

all_fencing_categories()
```

```bash
['foil_senior_men_2023_2024', 'epee_senior_men_2023_2024', 'sabre_senior_men_2023_2024', 'foil_senior_woman_2023_2024', 'epee_senior_woman_2023_2024', 'sabre_senior_woman_2023_2024', 'foil_junior_men_2023_2024', 'epee_junior_men_2023_2024', 'sabre_junior_men_2023_2024', 'foil_junior_woman_2023_2024', 'epee_junior_woman_2023_2024', 'sabre_junior_woman_2023_2024', 'foil_cadet_men_eu_2023_2024', 'epee_cadet_men_eu_2023_2024', 'sabre_cadet_men_eu_2023_2024', 'foil_cadet_woman_eu_2023_2024', 'epee_cadet_woman_eu_2023_2024', 'sabre_cadet_woman_eu_2023_2024', 'foil_senior_men_2022_2023', 'epee_senior_men_2022_2023', 'sabre_senior_men_2022_2023', 'foil_senior_woman_2022_2023', 'epee_senior_woman_2022_2023', 'sabre_senior_woman_2022_2023', 'foil_junior_men_2022_2023', 'epee_junior_men_2022_2023', 'sabre_junior_men_2022_2023', 'foil_junior_woman_2022_2023', 'epee_junior_woman_2022_2023', 'sabre_junior_woman_2022_2023', 'foil_cadet_men_eu_2022_2023', 'epee_cadet_men_eu_2022_2023', 'sabre_cadet_men_eu_2022_2023', 'foil_cadet_woman_eu_2022_2023', 'epee_cadet_woman_eu_2022_2023', 'sabre_cadet_woman_eu_2022_2023', 'foil_senior_men_2021_2022', 'epee_senior_men_2021_2022', 'sabre_senior_men_2021_2022', 'foil_senior_woman_2021_2022', 'epee_senior_woman_2021_2022', 'sabre_senior_woman_2021_2022', 'foil_junior_men_2021_2022', 'epee_junior_men_2021_2022', 'sabre_junior_men_2021_2022', 'foil_junior_woman_2021_2022', 'epee_junior_woman_2021_2022', 'sabre_junior_woman_2021_2022', 'foil_cadet_men_eu_2021_2022', 'epee_cadet_men_eu_2021_2022', 'sabre_cadet_men_eu_2021_2022', 'foil_cadet_woman_eu_2021_2022', 'epee_cadet_woman_eu_2021_2022', 'sabre_cadet_woman_eu_2021_2022', 'foil_senior_men_2020_2021', 'epee_senior_men_2020_2021', 'sabre_senior_men_2020_2021', 'foil_senior_woman_2020_2021', 'epee_senior_woman_2020_2021', 'sabre_senior_woman_2020_2021', 'foil_junior_men_2020_2021', 'epee_junior_men_2020_2021', 'sabre_junior_men_2020_2021', 'foil_junior_woman_2020_2021', 'epee_junior_woman_2020_2021', 'sabre_junior_woman_2020_2021', 'foil_cadet_men_eu_2020_2021', 'epee_cadet_men_eu_2020_2021', 'sabre_cadet_men_eu_2020_2021', 'foil_cadet_woman_eu_2020_2021', 'epee_cadet_woman_eu_2020_2021', 'sabre_cadet_woman_eu_2020_2021', 'foil_senior_men_2019_2020', 'epee_senior_men_2019_2020', 'sabre_senior_men_2019_2020', 'foil_senior_woman_2019_2020', 'epee_senior_woman_2019_2020', 'sabre_senior_woman_2019_2020', 'foil_junior_men_2019_2020', 'epee_junior_men_2019_2020', 'sabre_junior_men_2019_2020', 'foil_junior_woman_2019_2020', 'epee_junior_woman_2019_2020', 'sabre_junior_woman_2019_2020', 'foil_cadet_men_eu_2019_2020', 'epee_cadet_men_eu_2019_2020', 'sabre_cadet_men_eu_2019_2020', 'foil_cadet_woman_eu_2019_2020', 'epee_cadet_woman_eu_2019_2020', 'sabre_cadet_woman_eu_2019_2020']
```

### Getting all valid Country Codes
This methods returns all valid Country Codes, and takes no arguments.

```python
from finfo.FIE import all_valid_countrycodes

all_valid_countrycodes()
```

```bash
{'AIN', 'VIE', 'TUN', 'JOR', 'AZE', 'BOL', 'CAN', 'TKM', 'NGR', 
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
```


## Contributing
Contributing is welcome, please just email so I can get a clear understanding of the improvement.
Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)