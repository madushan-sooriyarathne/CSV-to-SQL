#!/usr/bin/python3

import csv
import sqlite3 as db
from pyfiglet import Figlet

# TODO Make the program take command line argument insted of in-python user inputs
# TODO format the command line usage output


def main():
    # Printing the program intro :) 
    # ? Just to be cool
    figlet = Figlet()
    print(figlet.renderText("CSV TO SQL"))
    print("by Madushan Sooriyarathne")

    # Getting the input from user (csv file name & db file name)
    csv_file_name = input("Enter the name of csv file : ")
    db_name = input("Enter the db file name : ")
    table_name =csv_file_name.replace('.csv', '').replace('-', '')

    if len(csv_file_name) == 0 or len(db_name) == 0:
        print(f"{'csv file name' if len(csv_file_name) else 'database file name'} can't be empty ")
        return None

    # making the db connection
    connection = db.connect(db_name)
    connection.row_factory = db.Row
    cursor = connection.cursor()

    # making the table
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    

    connection.commit()

    # reading the csv file
    try:
        with open(csv_file_name, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            # x = [print(type(x)) for x in next(csv_reader)]
            first_row = next(csv_reader)
            # generating the table createion sql statement
            sql_state = f"CREATE TABLE {table_name}("
            for i in range(len(first_row)):
                if i == len(first_row) - 1:
                    sql_state = sql_state + f"{first_row[i]} TEXT"
                else:
                    sql_state = sql_state + f"{first_row[i]} TEXT, "

            sql_state = sql_state + ")"

            # createing the sql table 
            cursor.execute(sql_state)

            for row in csv_reader:
                # insert the current row to database
                print(f"writeing {row}")
                cursor.execute(f"INSERT INTO {table_name} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
                connection.commit()

            print("Migration successful!")

    except FileNotFoundError as error:
        print("ERROR: csv file can't be found")
        print("Migration unsuccessful!")
    # except:
    #     print("Other Error")
    #     print("ERROR: csv file can't be found")
    #     print("Migration unsuccessful!")

    # closing the database connection
    cursor.close()
    
if __name__ == "__main__":
    main()