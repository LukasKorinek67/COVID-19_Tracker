#!/bin/env python
# -*- coding: utf-8 -*-

"""
STI - Request Handler
"""

import requests
import json
import csv
import re
from datetime import datetime
from datetime import date
from Logger import Logger

name = __name__
logger = Logger()
logger = Logger.init(logger, name, 'info.log')


class RequestHandler():
    """
    RequestHandler
    """
    def load_mz_data(self):
        """
        Načtení dat z MZ ČR
        """
        try:
            URL = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/zakladni-prehled.json"
            r = requests.get(URL)
            r = r.json()

            published = r["modified"]
            published = published[0:19]
            published = datetime.strptime(published, "%Y-%m-%dT%H:%M:%S")

            data = r["data"]
            data = data[0]

            daily_gain = data["potvrzene_pripady_vcerejsi_den"]
            total_amount = data["potvrzene_pripady_celkem"]
            loaded_date = data["datum"]

            loaded_data = {
                "date": loaded_date,
                "daily gain": daily_gain,
                "total amount": total_amount,
                "published": published
            }
            msg = "Načtení dat z MZ ČR - Success."
            logger.info(msg)
            return loaded_data
        except Exception as e:
            msg = "Chyba při získávání URL nebo načítání dat u MZ ČR."
            logger.exception(msg)

    def load_who_data(self):
        """
        Načtení dat z WHO
        """
        try:
            URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
            r = requests.get(URL)

            with requests.Session() as s:
                download = s.get(URL)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                data = list(cr)
                czech_data = []

                for row in data:
                    if(row[2] == "Czechia"):
                        czech_data.append(row)

                last_day = czech_data[-1]
                loaded_date = last_day[0]
                daily_gain = last_day[4]
                total_amount = last_day[5]
                published = datetime.now()

                loaded_data = {
                    "date": loaded_date,
                    "daily gain": int(daily_gain),
                    "total amount": int(total_amount),
                    "published": published
                }
                msg = "Načtení dat z WHO - Success."
                logger.info(msg)
                return loaded_data
        except Exception as e:
            msg = "Chyba při získávání URL nebo načítání dat u  WHO."
            logger.exception(msg)

    def load_who_data_by_date(self, date):
        """
        Načtení dat z WHO
        """
        try:
            URL = "https://covid19.who.int/WHO-COVID-19-global-data.csv"
            r = requests.get(URL)

            with requests.Session() as s:
                download = s.get(URL)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                data = list(cr)
                czech_data = []

                for row in data:
                    if(row[2] == "Czechia"):
                        czech_data.append(row)

                for day in czech_data:
                    if(day[0] == date):
                        daily_gain = day[4]
                        total_amount = day[5]
                        published = datetime.now()
                        loaded_data = {
                            "date": date,
                            "daily gain": int(daily_gain),
                            "total amount": int(total_amount),
                            "published": published
                        }
                        return loaded_data
                msg = "Načtení dat z WHO by date - Success."
                logger.info(msg)
                return None
        except Exception as e:
            msg = "Chyba při získávání URL nebo načítání dat pro Česko u  WHO."
            logger.exception(msg)

    def load_vaccination_data(self):
        """
        Načtení dat o vakcinaci z WHO
        """
        try:
            URL = "https://covid19.who.int/who-data/vaccination-data.csv"
            r = requests.get(URL)

            with requests.Session() as s:
                download = s.get(URL)
                decoded_content = download.content.decode('utf-8')
                cr = csv.reader(decoded_content.splitlines(), delimiter=',')
                data = list(cr)
                states = []

                for i, row in enumerate(data):
                    if i != 0:
                        name = row[0]
                        updated = row[4]
                        percentage_vaccinated = row[8]
                        if percentage_vaccinated == "":
                            percentage_vaccinated = row[7]
                        today = date.today()
                        name_clear = re.sub(r"\([^()]*\)", "", name).strip()

                        loaded_data = {
                            "name": name_clear,
                            "date": today,
                            "percentage vaccinated": percentage_vaccinated,
                            "last updated": updated
                        }
                        states.append(loaded_data)
                msg = "Načtení dat o vakcinaci z WHO - Success."
                logger.info(msg)
                return states
        except Exception as e:
            msg = "Chyba při získávání URL nebo načítání dat vakcinace u  WHO."
            logger.exception(msg)


if __name__ == "__main__":
    pass
