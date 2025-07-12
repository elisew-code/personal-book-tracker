
# (viewed data structure in excel)

import sys
from pathlib import Path
PROJECT_ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT_DIR)) 

import definitions as d
#import shutil
import pandas as pd
#import csv
import re

ENCODING = 'latin-1'

# generate new files with cleaned df, not just make copies
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


        #new_path = item.parent / new_name
        p = Path(item)
        p.rename(Path(item.parent, new_name))
        #os.rename(item.name, new_path)
        #Path(item).with_name(new_path) # return something to error check

book_directories = list(Path(d.BOOK_DATA_PATH).iterdir())
#clean_filenames(book_directories) # only make new clean versions after cleaning!

# turn into function or something? OR make it so we search to find relevant columns (i.e., name search)! then insert those
# functionalise as much as possible, like searching headers or something

#print(os.getcwd())

# turn into function that just gets any file, reads headers, then inserts the info where needed based on that?

# clean each file here, using functions to apply to columns as they are found
# rename columns as part of clearning

# create genre column using genre table? like genre match or something?? see notes 
# what headers are we looking for, based on the schema? maybe need a constant list, use that to filter out or rename or something? put in definition file?

# maybe a function, genre match?

#.loc is used to access a row by another index if you've set one, like title
# otherwise they both work the same, the first row (.loc[0]) is the same as accessing the row via index 0, numbered by default

def find_delimiter(firstline):
    delim = ','
    for char in firstline:
        if char == delim:
            break
        elif char == ';':
            delim = char
            break
        continue

    return delim

def clean_data(file):
    with open(file, 'r', encoding=ENCODING) as f:
        firstline = f.readline()
        f.close()

    delim = find_delimiter(firstline)
    df = pd.read_csv(file, delimiter=delim, encoding=ENCODING, on_bad_lines='skip') # skip malformed lines
    df = clean_columns(df) 

    # write the cleaned version to a new file AFTER cleaning

    # put this all into a df by detecting delimiters, 
    # then fix headers + filter the columns needed/not needed at the same time
    # then some cleaning of remaining data

def clean_columns(original_df): # TO FIX
    filtered_df = pd.DataFrame() # empty df
    removed_columns = []
    # do pattern matching to any expected columns, filter those that don't match
    for original_header in original_df.columns:
        sanitised_header = re.sub(r'[-_]', ' ', original_header).strip()
        print(f'original_header sanitised to ')

        for valid_header in d.VALID_SCHEMA_COLUMNS: 
            # boundaries for stricter match
            if sanitised_header == valid_header:
                print(sanitised_header, ", ", valid_header)
                filtered_df[valid_header] = original_df[original_header]

            elif (re.search('name', sanitised_header, re.IGNORECASE) or re.search('book', sanitised_header, re.IGNORECASE)) and not re.search('user', sanitised_header, re.IGNORECASE) and not re.search('review', sanitised_header, re.IGNORECASE):
                print(sanitised_header, ", name")
                filtered_df['title'] = original_df[original_header]

            elif re.search('summary', sanitised_header, re.IGNORECASE) or re.search('description', sanitised_header, re.IGNORECASE):
                print(sanitised_header, ", summary/description")
                filtered_df['synopsis'] = original_df[original_header]
    
    print(f'{filtered_df.columns} extracted from {original_df.columns}')
    return filtered_df
        
    # put a message of 'columns not added' for the user or whatever



    # need a constant thingy to match headers, filter them?
    # return the standardised headers, then filter irrelevant ones?
    return headers


#clean_file_paths = [str(Path(d.BOOK_DATA_PATH) / item.name) for item in book_directories if not item.name.startswith('.') and item.name.startswith('clean')]

file_paths = [str(Path(d.BOOK_DATA_PATH) / item.name) for item in book_directories if not item.name.startswith('.')]

for file in file_paths:
    print(file)
    clean_data(file) # cleaning the data, quality and header checks
    #sort_data(file) # putting info into relevant dfs

# insert_data() # inserting df into the schema ()
# reuse this function for later inserts? like insert into x table functions?
# insert into books, insert into reviews etc. etc. 

# load data into a df, 
# clean headers, then use a list of the schema stuff to drop those not needed

# then make a fucntion to extract columns that are the same and put into a table, or join and put into the database etc
#for item in book_directories:


#clean_ratings()

#clean_reviews()

#clean_top_100()

#clean_books()

#clean_genre_predictions()

    



