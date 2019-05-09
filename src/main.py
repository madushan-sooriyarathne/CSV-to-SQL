
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
    args = docopt(USAGE)
    
    if args['<csv_file_path>'] is None or args['<database_file_path>'] is None:
        print(USAGE)
    else:
        converter_obj = csvconverter.CSVConverter(args['<csv_file_path>'], args['<database_file_path>'])
        converter_obj.convert()
    
if __name__ == "__main__":
    main()
