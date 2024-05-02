import unittest
from finfo.FIE import FIE, all_fencing_categories

class TestFIEClass(unittest.TestCase):

    def test_find_fencer_by_rank(self):
        fie = FIE("foil_senior_men_2022_2023")
        rank_1 = fie.find_fencer_by_rank(1)
        self.assertEqual(rank_1, {'Lastname': 'massialas', 'Firstname': 'alexander', 'CountryCode': 'USA', 'Rank': 1})

    def test_find_fencer_by_name(self):
        fie = FIE("foil_senior_men_2022_2023")
        massiales = fie.find_fencer_by_name("alexander", "massialas")
        self.assertEqual(massiales, {'Lastname': 'massialas', 'Firstname': 'alexander', 'CountryCode': 'USA', 'Rank': 1})

    def test_get_all_fencers_from_country(self):
        fie = FIE("foil_senior_men_2022_2023")
        cypern = fie.get_all_fencers_from_country("CYP")
        self.assertEqual(cypern, [{'Lastname': 'tofalides', 'Firstname': 'alex', 'CountryCode': 'CYP', 'Rank': 68}, {'Lastname': 'kiayias', 'Firstname': 'william', 'CountryCode': 'CYP', 'Rank': 762}])

    def test_get_all_categories(self):
        self.assertEqual(all_fencing_categories(), ['foil_senior_men_2023_2024', 'epee_senior_men_2023_2024', 'sabre_senior_men_2023_2024', 'foil_senior_woman_2023_2024', 'epee_senior_woman_2023_2024', 'sabre_senior_woman_2023_2024', 'foil_junior_men_2023_2024', 'epee_junior_men_2023_2024', 'sabre_junior_men_2023_2024', 'foil_junior_woman_2023_2024', 'epee_junior_woman_2023_2024', 'sabre_junior_woman_2023_2024', 'foil_cadet_men_eu_2023_2024', 'epee_cadet_men_eu_2023_2024', 'sabre_cadet_men_eu_2023_2024', 'foil_cadet_woman_eu_2023_2024', 'epee_cadet_woman_eu_2023_2024', 'sabre_cadet_woman_eu_2023_2024', 'foil_senior_men_2022_2023', 'epee_senior_men_2022_2023', 'sabre_senior_men_2022_2023', 'foil_senior_woman_2022_2023', 'epee_senior_woman_2022_2023', 'sabre_senior_woman_2022_2023', 'foil_junior_men_2022_2023', 'epee_junior_men_2022_2023', 'sabre_junior_men_2022_2023', 'foil_junior_woman_2022_2023', 'epee_junior_woman_2022_2023', 'sabre_junior_woman_2022_2023', 'foil_cadet_men_eu_2022_2023', 'epee_cadet_men_eu_2022_2023', 'sabre_cadet_men_eu_2022_2023', 'foil_cadet_woman_eu_2022_2023', 'epee_cadet_woman_eu_2022_2023', 'sabre_cadet_woman_eu_2022_2023', 'foil_senior_men_2021_2022', 'epee_senior_men_2021_2022', 'sabre_senior_men_2021_2022', 'foil_senior_woman_2021_2022', 'epee_senior_woman_2021_2022', 'sabre_senior_woman_2021_2022', 'foil_junior_men_2021_2022', 'epee_junior_men_2021_2022', 'sabre_junior_men_2021_2022', 'foil_junior_woman_2021_2022', 'epee_junior_woman_2021_2022', 'sabre_junior_woman_2021_2022', 'foil_cadet_men_eu_2021_2022', 'epee_cadet_men_eu_2021_2022', 'sabre_cadet_men_eu_2021_2022', 'foil_cadet_woman_eu_2021_2022', 'epee_cadet_woman_eu_2021_2022', 'sabre_cadet_woman_eu_2021_2022', 'foil_senior_men_2020_2021', 'epee_senior_men_2020_2021', 'sabre_senior_men_2020_2021', 'foil_senior_woman_2020_2021', 'epee_senior_woman_2020_2021', 'sabre_senior_woman_2020_2021', 'foil_junior_men_2020_2021', 'epee_junior_men_2020_2021', 'sabre_junior_men_2020_2021', 'foil_junior_woman_2020_2021', 'epee_junior_woman_2020_2021', 'sabre_junior_woman_2020_2021', 'foil_cadet_men_eu_2020_2021', 'epee_cadet_men_eu_2020_2021', 'sabre_cadet_men_eu_2020_2021', 'foil_cadet_woman_eu_2020_2021', 'epee_cadet_woman_eu_2020_2021', 'sabre_cadet_woman_eu_2020_2021', 'foil_senior_men_2019_2020', 'epee_senior_men_2019_2020', 'sabre_senior_men_2019_2020', 'foil_senior_woman_2019_2020', 'epee_senior_woman_2019_2020', 'sabre_senior_woman_2019_2020', 'foil_junior_men_2019_2020', 'epee_junior_men_2019_2020', 'sabre_junior_men_2019_2020', 'foil_junior_woman_2019_2020', 'epee_junior_woman_2019_2020', 'sabre_junior_woman_2019_2020', 'foil_cadet_men_eu_2019_2020', 'epee_cadet_men_eu_2019_2020', 'sabre_cadet_men_eu_2019_2020', 'foil_cadet_woman_eu_2019_2020', 'epee_cadet_woman_eu_2019_2020', 'sabre_cadet_woman_eu_2019_2020']
)

if __name__ == '__main__':
    unittest.main()

