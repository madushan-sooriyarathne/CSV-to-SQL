
from pyfiglet import Figlet
from docopt import docopt
import csvconverter


USAGE = '''

CSV to SQL(Sqlite3)

Usage:
    __init__.py <csv_file_path> <database_file_path>


'''

def main():

    figlet = Figlet()
    print(figlet.renderText("CSV TO SQL"))
    print("by Madushan Sooriyarathne")
    args = docopt(USAGE)
    
    if args['<csv_file_path>'] is None or args['<database_file_path>'] is None:
        print(USAGE)
    else:
        converter_obj = csvconverter.CSVConverter(args['<csv_file_path>'], args['<database_file_path>'])
        converter_obj.convert()


    # Printing the program intro :) 
    # ? Just to be cool
    

    # # Getting the input from user (csv file name & db file name)
    # csv_file_name = input("Enter the name of csv file : ")
    # db_name = input("Enter the db file name : ")
    # table_name =csv_file_name.replace('.csv', '').replace('-', '')

    # if len(csv_file_name) == 0 or len(db_name) == 0:
    #     print(f"{'csv file name' if len(csv_file_name) else 'database file name'} can't be empty ")
    #     return None

    
if __name__ == "__main__":
    main()