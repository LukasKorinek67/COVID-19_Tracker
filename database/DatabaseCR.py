#!/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

from datetime import date
import sys
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.abspath(os.path.join(dir_path, os.pardir)))
from DailyCasesData import DailyCasesData
from Logger import Logger

name = __name__
logger = Logger()
logger = Logger.init(logger, name, 'info.log')


class DatabaseCR():

    def __init__(self):
        """
        Constructor of class DatabaseCR. Creates local database covid19 with
        covid19_CR. And string_info about waiting for data.

        Returns
        -------
        None.

        """
        self.myclient = MongoClient(
            "mongodb+srv://Test1:Heslo123@cluster0.0gobs.mongodb.net/covid19?retryWrites=true&w=majority")
        self.database = self.myclient["covid19"]
        self.db_cr = self.database["covid19_CR"]
        self.string_info = "Čeká se na data."

    def add_info_cr(self, data_cr):
        """
        Přidání dat
        """
        try:
            query = {
                "date": data_cr.date
            }
            result = self.db_cr.find_one(query)

            diff_time = data_cr.diff_time
            if (diff_time is not None):
                diff_time = str(diff_time)

            if result == None:
                record = {
                    "date": data_cr.date,
                    "published_MZ": data_cr.published_mz, \
                    "daily_gain_MZ": data_cr.daily_gain_mz, \
                    "total_MZ": data_cr.total_amount_mz, \
                    "published_WHO": data_cr.published_who, \
                    "daily_gain_WHO": data_cr.daily_gain_who, \
                    "total_WHO": data_cr.total_amount_who, \
                    "diff_time": diff_time, \
                    "diff_daily_gain": data_cr.diff_daily_gain, \
                    "diff_total": data_cr.diff_total_amount
                }
                self.db_cr.insert_one(record)
                msg = "Přidání dat ČR - SuCC."
                logger.info(msg)
            else:
                self.update_info_cr(data_cr)
        except Exception as e:
            msg = "Chyba při přidávání infa ČR dat do databáze."
            logger.exception(msg)

    def update_info_cr(self, data_cr):
        """
        Update dat
        """
        try:
            query = {
                "date": data_cr.date
            }
            diff_time = data_cr.diff_time
            if (diff_time is not None):
                diff_time = str(diff_time)
            new_values = {
                "$set": {
                    "published_MZ": data_cr.published_mz, \
                    "daily_gain_MZ": data_cr.daily_gain_mz, \
                    "total_MZ": data_cr.total_amount_mz, \
                    "published_WHO": data_cr.published_who, \
                    "daily_gain_WHO": data_cr.daily_gain_who, \
                    "total_WHO": data_cr.total_amount_who, \
                    "diff_time": diff_time, \
                    "diff_daily_gain": data_cr.diff_daily_gain, \
                    "diff_total": data_cr.diff_total_amount
                }
            }
            self.db_cr.update_one(query, new_values)
            msg = "Update dat ČR - Success."
            logger.info(msg)
        except Exception as e:
            msg = "Chyba při updatování infa ČR dat v databázi."
            logger.exception(msg)

    def print_info_cr(self):
        """
        Prints the whole database.

        Returns
        -------
        None.

        """
        print_list = list(self.db_cr.find())
        print(print_list)

    def get_today_data(self):
        """
        Dnešní data
        """
        try:
            today = date.today()
            query = {
                "date": str(today)
            }
            result = self.db_cr.find_one(query)
            if result is not None:
                msg = "Dnešní data- Success."
                logger.info(msg)
                return DailyCasesData(result["date"], result["published_MZ"], result["daily_gain_MZ"],
                                      result["total_MZ"], result["published_WHO"], result["daily_gain_WHO"],
                                      result["total_WHO"], result["diff_daily_gain"], result["diff_total"],
                                      result["diff_time"])
            else:
                msg = "Dnešní data(None) - Success."
                logger.info(msg)
                return None
        except Exception as e:
            msg = "Chyba při hledání a vracení aktuálních dat z databáze."
            logger.exception(msg)

    def get_data_by_date(self, date):
        try:
            query = {
                "date": str(date)
            }
            result = self.db_cr.find_one(query)
            if result is not None:
                msg = "get_data_by_date - Success."
                logger.info(msg)
                return DailyCasesData(result["date"], result["published_MZ"], result["daily_gain_MZ"],
                                      result["total_MZ"], result["published_WHO"], result["daily_gain_WHO"],
                                      result["total_WHO"], result["diff_daily_gain"], result["diff_total"],
                                      result["diff_time"])
            else:
                msg = "get_data_by_date(None) - Success."
                logger.info(msg)
                return None
        except Exception as e:
            msg = "Chyba při hledání a vracení dat podle datumu z databáze."
            logger.exception(msg)

    def get_info_cr(self):
        """
        Všechna data
        """
        try:
            list_cr = list(self.db_cr.find())
            data_cr = []
            for item in list_cr:
                data_cr.append(
                    DailyCasesData(item["date"], item["published_MZ"], item["daily_gain_MZ"], item["total_MZ"],
                                   item["published_WHO"], item["daily_gain_WHO"], item["total_WHO"],
                                   item["diff_daily_gain"], item["diff_total"], item["diff_time"]))
            msg = "Všechna data CR - Success."
            logger.info(msg)
            return data_cr
        except Exception as e:
            msg = "Chyba při hledání a vracení dat ČR v databázi."
            logger.exception(msg)

    def delete_records(self):
        """
        Deletes all records in the database.

        Returns
        -------
        None.

        """
        self.db_cr.delete_many({})
        msg = "Všechny záznamy z databáze vymazány."
        logger.info(msg)
