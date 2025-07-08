
# (viewed data structure in excel)

import sys
from pathlib import Path
PROJECT_ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT_DIR)) 

import definitions as d
import os
import shutil
import pandas

ENCODING='latin-1'

def clean_filenames(book_directories):    
    unclean_directories = [
        item for item in book_directories 
        if not (item.name.startswith('.') or item.name.startswith('clean'))
    ]
    
    for item in unclean_directories:
        new_name = 'clean_'

        if item.match('**/Top*.csv'): 
            new_name += 'top-100_books.csv'

        elif item.match('**/customer*.csv'): 
            new_name += item.name.replace('customer ', '')

        else:
            new_name += item.name

        new_path = item.parent / new_name
        shutil.copyfile(item, new_path) # making a copy of the files that will be altered

book_directories = list(Path(d.BOOK_DATA_PATH).iterdir())
clean_filenames(book_directories)

# turn into function or something? OR make it so we search to find relevant columns (i.e., name search)! then insert those
# functionalise as much as possible, like searching headers or something

#print(os.getcwd())

# turn into function that just gets any file, reads headers, then inserts the info where needed based on that?

# clean each file here, using functions to apply to columns as they are found
# rename columns as part of clearning

# create genre column using genre table? like genre match or something?? see notes 
# what headers are we looking for, based on the schema? maybe need a constant list, use that to filter out or rename or something? put in definition file?

for item in book_directories:
    if (item.name.startswith('.') or not item.name.startswith('clean')): continue

    with open(Path(d.BOOK_DATA_PATH) / item.name, 'r', encoding=ENCODING) as f:
        print(f.readline())

        f.close()



# then make a fucntion to extract columns that are the same and put into a table, or join and put into the database etc
#for item in book_directories:





    



