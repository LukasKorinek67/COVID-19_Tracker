# -*- coding: utf-8 -*-
from pymongo import MongoClient
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
from StateVaccinationData import StateVaccinationData
from Logger import Logger

name = __name__
logger = Logger()
logger = Logger.init(logger, name, 'info.log')


class DatabaseVaccination():

    def __init__(self):
        """
        Constructor of class DatabaseVaccination. Creates local database
        covid19 with covid19_vaccination.
        And string_info about waiting for data.

        Returns
        -------
        None.

        """
        self.myclient = MongoClient(
            "mongodb+srv://Test1:Heslo123@cluster0.0gobs.mongodb.net/covid19?retryWrites=true&w=majority")
        "mongodb+srv://Test:Test123456@cluster0.0gobs.mongodb.net/covid19?retryWrites=true&w=majority"
        self.database = self.myclient["covid19"]
        self.db_vaccination = self.database["covid19_vaccination"]
        self.string_info = "Čeká se na data."

    def add_info_vaccination(self, state, date, percentage, last_updated):
        """
        Adds info about vaccination into database.

        Parameters
        ----------
        state : string
            name of state
        date : string
            Today's date and time of actualization from WHO
        percentage : int
            Percentage of vaccinated
        is_chosen : bool
            whether the state is chosen by user or not

        Returns
        -------
        None.

        """
        try:
            query = {
                "state": state
            }
            results = self.db_vaccination.find_one(query)
            if results == None:
                is_chosen = 0
                record = {
                    "state": state, \
                    "data": [{
                        "date": date,
                        "percentage": percentage,
                        "last_updated": last_updated
                    }],
                    "is_chosen": is_chosen
                }
                self.db_vaccination.insert_one(record)
            else:
                n_records = len(results["data"])
                found = False

                for i in range(0, n_records):
                    if results["data"][i]["date"] == date:
                        found = True
                        dates = results["data"]
                        results["data"][i]["percentage"] = percentage
                        results["data"][i]["last_updated"] = last_updated
                        newvalues = ({
                            "$set": {
                                "data": results["data"]
                            }
                        })
                        self.db_vaccination.update_many(query, newvalues)

                if found == False:
                    record = {
                        "date": date,
                        "percentage": percentage,
                        "last_updated": last_updated
                    }
                    self.db_vaccination.update_one(
                        {
                            "state": state
                        },
                        {
                            "$push": {
                                "data": record
                            }
                        }
                    )
            # msg = "Přidání vakcinačních dat do databáze - Success."
            # logger.info(msg)
        except Exception as e:
            msg = "Chyba při přidávání vakcinačních dat do databáze."
            logger.exception(msg)

    def find_state_vaccination(self, state):
        """
        Finds state which are chosen by user.
        And prints results - info about state.

        Parameters
        ----------
        state : string
            name of state

        Returns
        -------
        None.

        """
        try:
            query = {
                "state": state
            }
            results = self.db_vaccination.find(query)
            finded_state = None
            for state in results:
                finded_state = StateVaccinationData(state["state"], state["data"], state["is_chosen"])
            msg = "Vracení dat vakcinace vybraného států dle uživatele z databáze - Success."
            logger.info(msg)
            return finded_state
        except Exception as e:
            msg = "Chyba při hledání a vracení dat vakcinace vybraného států dle uživatele z databáze."
            logger.exception(msg)

    def find_chosen_state_vaccination(self):
        """
        Finds chosen states. Which are chosen by user.
        Value of is_chosen is True.
        Prints results.

        Returns
        -------
        None.

        """
        try:
            list_with_values = [1, 2, 3, 4, 5]

            results = self.db_vaccination.find({"is_chosen": {"$in": list_with_values}})
            states = []
            for state in results:
                states.append(StateVaccinationData(state["state"], state["data"], state["is_chosen"]))
            msg = "Vracení dat vakcinace vybraných států dle uživatele z databáze - Success."
            logger.info(msg)
            return states
        except Exception as e:
            msg = "Chyba při hledání a vracení dat vakcinace vybraných států dle uživatele z databáze."
            logger.exception(msg)

    def update_info_vaccination_chosen(self, state, is_chosen):
        """
        Updates info about state of state (country).
        Whether it is chosen or not.

        Parameters
        ----------
        state : string
            name_of_state
        is_chosen : bool
            1-5 - is chosen, 0 - isn't chosen

        Returns
        -------
        None.

        """
        try:
            myquery = {
                "state": state
            }
            newvalues = {
                "$set": {
                    "is_chosen": is_chosen
                }
            }
            self.db_vaccination.update_one(myquery, newvalues)
            msg = "Updatování položky is_chosen - vybírání nového státu do vakcinačního grafu - Success."
            logger.info(msg)
        except Exception as e:
            msg = "Chyba při updatování položky is_chosen - vybírání nového státu do vakcinačního grafu."
            logger.exception(msg)

    def is_database_empty(self):
        """
        Check if database is empty
        """
        data = list(self.db_vaccination.find())
        if (len(data) == 0):
            return True
        else:
            return False

    def print_info_vaccination(self):
        """
        Prints the whole database.

        Returns
        -------
        None.

        """
        print_list = list(self.db_vaccination.find())
        print(print_list)

    def delete_records(self):
        """
        Deletes the whole records in the database.

        Returns
        -------
        None.

        """
        self.db_vaccination.delete_many({})
        msg = "Všechny záznamy z databáze o vakcinaci vymazány."
        logger.info(msg)
