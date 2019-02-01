#!/usr/bin/python3

import csv
import sqlite3 as db
import logging
import os


# creating and configuring logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 2 Formatter objects for 2 Handlers (file handler and stream handler)
file_formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(name)s : %(message)s')
stream_formatter = logging.Formatter('%(levelname)s : %(name)s : %(message)s')

# creating two hadler object and set the formatter 
file_handler = logging.FileHandler(filename='info.log')
file_handler.setFormatter(file_formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(stream_formatter)

# add two hadlers to logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class CSVConverter:

    def __init__(self, csv_file, db_name):
        self._db_name = db_name
        self._csv_file = csv_file
        self._table_name = self._csv_file.replace('.csv', '').replace('-', '')
    
    def convert(self):
        # making the db connection
        connection = db.connect(self._db_name)
        connection.row_factory = db.Row
        cursor = connection.cursor()

        # Dropping the table if it already exists in given db file
        cursor.execute(f"DROP TABLE IF EXISTS {self._table_name}")
        connection.commit()

        # check to see if the given csv file exist on file system
        if not os.path.exists(self._csv_file):
            logger.error(f"Can't find the file ({self._csv_file}). failed to read data from csv file")
            logger.error("Migration unsuccessful!")
            return None
        
        with open(self._csv_file, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            
            # get the first line of the csv file
            # this first line (usualy) contains the headers of the csv data
            headers = next(csv_reader)
            # now curosr is at the second line of csv file
            # crating the db table using extracted data from csv file
            # evert column type will be text, when extacting data don't forget to cast the values
            sql_statement = f"CREATE TABLE {self._table_name} ("
            for i in range(len(headers)):
                if i == len(headers) - 1:
                    sql_statement = sql_statement + f"{headers[i]} TEXT"
                else:
                    sql_statement = sql_statement + f"{headers[i]} TEXT, "

            sql_statement = sql_statement + ")"
            logger.info(sql_statement)
            cursor.execute(sql_statement)
            # comitting the table creation sql statemnt against the database
            connection.commit()

            sql_store_statment = f"INSERT INTO {self._table_name} VALUES("
            for i in range(len(headers)):
                if i ==len(headers) - 1:
                    sql_store_statment = sql_store_statment + "?)"
                else:
                    sql_store_statment = sql_store_statment + "?, "
            logger.info(sql_store_statment)
            # going row to row of the csv_file and store the extracted data in db table
            for row in csv_reader:
                logger.info(f"Writing {row}")
                cursor.execute(sql_store_statment, row)
                connection.commit()

        logger.info("Data Migration Successful!")
        logger.info("Clossing the connections")
        cursor.close()
        connection.close()
        logger.info("All connections has been closed")