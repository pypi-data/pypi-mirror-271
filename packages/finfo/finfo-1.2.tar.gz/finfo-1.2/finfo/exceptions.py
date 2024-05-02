
class InvalidCategory(Exception):

    def __init__(self, category, categories):
        self.category = category
        self.categories = categories
        self.message = f"{category} is an Invalid Category. Valid categories: {categories}"
        super().__init__(self.message)

class InvalidSeason(Exception):
     def __init__(self, season, seasons):
        self.season = season
        self.seasons = seasons
        self.message = f"{seasons} is an Invalid Season. Seasons {seasons}"
        super().__init__(self.message)

class InvalidFIERank(Exception):

    def __init__(self, rank):
        self.rank = rank
        self.message = f"{rank} is not existing in FIE officel ranking. The ranking starts at 1."
        super().__init__(self.message)

class InvalidNameSearch(Exception):
     def __init__(self, name):
        self.name = name
        self.message = f"{name} is an Invalid Name"
        super().__init__(self.message)

class InvalidCountryCode(Exception):
     def __init__(self, countrycode):
        self.countrycode = countrycode
        self.message = f"{countrycode} is an Invalid CountryCode"
        super().__init__(self.message)