import unittest
import data


class TestData(unittest.TestCase):
    def test_get_player_info(self):
        test_table: list[dict] = [
            {
                "player_name": "saquon-barkley",
                "expected_info": {
                    "name": "Saquon Barkley",
                    "picture": "https://static.www.nfl.com/image/private/t_player_profile_landscape_2x/f_auto/league/o8tlhps5u1tvnaaxlpjk",
                },
                "expected_exeption": None,
            },
            {
                "player_name": "func-foo",
                "expected_info": None,
                "expected_exeption": data.PlayerNotFound,
            },
        ]

        for t in test_table:
            try:
                info = data.get_player_info(t["player_name"])

                if t["expected_exeption"] is not None:
                    self.fail("Exception should be thrown, but wasn't")

                self.assertDictEqual(info, t["expected_info"])
            except AssertionError as e:
                raise e
            except Exception as e:
                self.assertIs(type(e), t["expected_exeption"])

    def test_get_career_stat_sheet(self):
        test_table: list[dict] = [
            {
                "player_name": "saquon-barkley",
                "expected_stats": True,
                "expected_exeption": None,
            },
            {
                "player_name": "func-foo",
                "expected_stats": False,
                "expected_exeption": data.PlayerNotFound,
            },
        ]

        for t in test_table:
            try:
                stats = data.get_career_stat_sheet(t["player_name"])

                if t["expected_exeption"] is not None:
                    self.fail("Exception should be thrown, but wasn't")

                self.assertEqual(stats is not None, t["expected_stats"])
            except AssertionError as e:
                raise e
            except Exception as e:
                self.assertIs(type(e), t["expected_exeption"])

    def test_get_week_stat_sheet(self):
        test_table: list[dict] = [
            {
                "player_name": "saquon-barkley",
                "year": "2022",
                "expected_stats": {
                    "Week 18": {
                        "Game Date": "01/08/2023",
                        "OPP": "@Eagles",
                        "RESULT": "L 16 - 22",
                        "ATT": "",
                        "YDS": " : ",
                        "AVG": " : ",
                        "LNG": " : ",
                        "TD": " : ",
                        "REC": "",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 17": {
                        "Game Date": "01/01/2023",
                        "OPP": "Colts",
                        "RESULT": "W 38 - 10",
                        "ATT": "12",
                        "YDS": "58 : -5",
                        "AVG": "4.8 : -2.5",
                        "LNG": "19 : -2",
                        "TD": "0 : 0",
                        "REC": "2",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 16": {
                        "Game Date": "12/24/2022",
                        "OPP": "@Vikings",
                        "RESULT": "L 24 - 27",
                        "ATT": "14",
                        "YDS": "84 : 49",
                        "AVG": "6 : 6.1",
                        "LNG": "27 : 18",
                        "TD": "1 : 0",
                        "REC": "8",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 15": {
                        "Game Date": "12/19/2022",
                        "OPP": "@Commanders",
                        "RESULT": "W 20 - 12",
                        "ATT": "18",
                        "YDS": "87 : 33",
                        "AVG": "4.8 : 6.6",
                        "LNG": "15 : 9",
                        "TD": "1 : 0",
                        "REC": "5",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 14": {
                        "Game Date": "12/11/2022",
                        "OPP": "Eagles",
                        "RESULT": "L 22 - 48",
                        "ATT": "9",
                        "YDS": "28 : 20",
                        "AVG": "3.1 : 10",
                        "LNG": "9 : 16",
                        "TD": "0 : 0",
                        "REC": "2",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 13": {
                        "Game Date": "12/04/2022",
                        "OPP": "Commanders",
                        "RESULT": "T 20 - 20",
                        "ATT": "18",
                        "YDS": "63 : 18",
                        "AVG": "3.5 : 3.6",
                        "LNG": "21 : 7",
                        "TD": "1 : 0",
                        "REC": "5",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 12": {
                        "Game Date": "11/24/2022",
                        "OPP": "@Cowboys",
                        "RESULT": "L 20 - 28",
                        "ATT": "11",
                        "YDS": "39 : 13",
                        "AVG": "3.6 : 3.2",
                        "LNG": "10 : 5",
                        "TD": "1 : 0",
                        "REC": "4",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 11": {
                        "Game Date": "11/20/2022",
                        "OPP": "Lions",
                        "RESULT": "L 18 - 31",
                        "ATT": "15",
                        "YDS": "22 : 13",
                        "AVG": "1.5 : 6.5",
                        "LNG": "4 : 7",
                        "TD": "0 : 0",
                        "REC": "2",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 10": {
                        "Game Date": "11/13/2022",
                        "OPP": "Texans",
                        "RESULT": "W 24 - 16",
                        "ATT": "35",
                        "YDS": "152 : 8",
                        "AVG": "4.3 : 8",
                        "LNG": "27 : 8",
                        "TD": "1 : 0",
                        "REC": "1",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 8": {
                        "Game Date": "10/30/2022",
                        "OPP": "@Seahawks",
                        "RESULT": "L 13 - 27",
                        "ATT": "20",
                        "YDS": "53 : 9",
                        "AVG": "2.6 : 3",
                        "LNG": "15 : 12",
                        "TD": "1 : 0",
                        "REC": "3",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 7": {
                        "Game Date": "10/23/2022",
                        "OPP": "@Jaguars",
                        "RESULT": "W 23 - 17",
                        "ATT": "24",
                        "YDS": "110 : 25",
                        "AVG": "4.6 : 6.2",
                        "LNG": "20 : 9",
                        "TD": "0 : 0",
                        "REC": "4",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 6": {
                        "Game Date": "10/16/2022",
                        "OPP": "Ravens",
                        "RESULT": "W 24 - 20",
                        "ATT": "22",
                        "YDS": "83 : 12",
                        "AVG": "3.8 : 4",
                        "LNG": "8 : 5",
                        "TD": "1 : 0",
                        "REC": "3",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 5": {
                        "Game Date": "10/09/2022",
                        "OPP": "@Packers",
                        "RESULT": "W 27 - 22",
                        "ATT": "13",
                        "YDS": "70 : 36",
                        "AVG": "5.4 : 12",
                        "LNG": "40 : 41",
                        "TD": "1 : 0",
                        "REC": "3",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 4": {
                        "Game Date": "10/02/2022",
                        "OPP": "Bears",
                        "RESULT": "W 20 - 12",
                        "ATT": "31",
                        "YDS": "146 : 16",
                        "AVG": "4.7 : 8",
                        "LNG": "29 : 15",
                        "TD": "0 : 0",
                        "REC": "2",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 3": {
                        "Game Date": "09/27/2022",
                        "OPP": "Cowboys",
                        "RESULT": "L 16 - 23",
                        "ATT": "14",
                        "YDS": "81 : 45",
                        "AVG": "5.8 : 11.2",
                        "LNG": "36 : 21",
                        "TD": "1 : 0",
                        "REC": "4",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 2": {
                        "Game Date": "09/18/2022",
                        "OPP": "Panthers",
                        "RESULT": "W 19 - 16",
                        "ATT": "21",
                        "YDS": "72 : 16",
                        "AVG": "3.4 : 5.3",
                        "LNG": "16 : 9",
                        "TD": "0 : 0",
                        "REC": "3",
                        "FUM": "",
                        "LOST": "",
                    },
                    "Week 1": {
                        "Game Date": "09/11/2022",
                        "OPP": "@Titans",
                        "RESULT": "W 21 - 20",
                        "ATT": "18",
                        "YDS": "164 : 30",
                        "AVG": "9.1 : 5",
                        "LNG": "68 : 7",
                        "TD": "1 : 0",
                        "REC": "6",
                        "FUM": "1",
                        "LOST": "0",
                    },
                    "(post) Week 2": {
                        "Game Date": "01/22/2023",
                        "OPP": "@Eagles",
                        "RESULT": "L 7 - 38",
                        "ATT": "9",
                        "YDS": "61 : 21",
                        "AVG": "6.8 : 10.5",
                        "LNG": "39 : 19",
                        "TD": "0 : 0",
                        "REC": "2",
                        "FUM": "",
                        "LOST": "",
                    },
                    "(post) Week 1": {
                        "Game Date": "01/15/2023",
                        "OPP": "@Vikings",
                        "RESULT": "W 31 - 24",
                        "ATT": "9",
                        "YDS": "53 : 56",
                        "AVG": "5.9 : 11.2",
                        "LNG": "28 : 24",
                        "TD": "2 : 0",
                        "REC": "5",
                        "FUM": "",
                        "LOST": "",
                    },
                },
                "expected_exeption": None,
            },
            {
                "player_name": "func-foo",
                "year": "2022",
                "expected_stats": {},
                "expected_exeption": data.PlayerNotFound,
            },
        ]

        for t in test_table:
            try:
                stats = data.get_week_stat_sheet(t["player_name"], t["year"])

                if t["expected_exeption"] is not None:
                    self.fail("Exception should be thrown, but wasn't")

                self.assertEqual(stats, t["expected_stats"])
            except AssertionError as e:
                raise e
            except Exception as e:
                self.assertIs(type(e), t["expected_exeption"])


if __name__ == "__main__":
    unittest.main()
