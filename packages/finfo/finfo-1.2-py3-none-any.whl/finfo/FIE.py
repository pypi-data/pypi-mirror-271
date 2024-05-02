from finfo.PDF_reader import read_pdf, country_codes, categories
from finfo.exceptions import InvalidFIERank, InvalidNameSearch, InvalidCountryCode

class FIE:

    def __init__(self, category) -> None:
        self.fencers = read_pdf(category)


    def find_fencer_by_rank(self, rank):
        if len(self.fencers) < rank or rank == 0:
            raise InvalidFIERank(rank)
        else:
            return self.fencers.get(rank)
        

    def find_fencer_by_name(self, firstname, lastname):
        for inside_dict in self.fencers.values():
            if firstname and lastname in inside_dict.values():
                return inside_dict
        raise InvalidNameSearch(firstname + ' ' + lastname)
    

    def all_athletes(self):
        return self.fencers
    

    def get_all_fencers_from_country(self, countrycode):
        fencers_from_country = []
        if countrycode not in country_codes:
            raise InvalidCountryCode(countrycode)
        for insidedict in self.fencers.values():
            if insidedict["CountryCode"] == countrycode:
                fencers_from_country.append(insidedict)
            else:
                continue
        return fencers_from_country


def all_fencing_categories():
        return categories

def all_valid_countrycodes():
        return country_codes



