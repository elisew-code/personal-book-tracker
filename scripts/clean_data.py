
# (viewed data structure in excel - manual inspection)

import sys
from pathlib import Path
PROJECT_ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT_DIR)) 

import definitions as d
import pandas as pd
import re

ENCODING = 'latin-1'

# cleaning filenames
def clean_filenames(book_directories):    
    unclean_directories = [
        item for item in book_directories 
        if not (item.name.startswith('.') or item.name.startswith('renamed_'))
    ]
    
    for item in unclean_directories:
        new_name = 'renamed_'

        if item.match('**/Top*.csv'): 
            new_name += 'top-100_books.csv'

        elif item.match('**/customer*.csv'): 
            new_name += item.name.replace('customer ', '')

        else:
            new_name += item.name

        p = Path(item)
        p.rename(Path(item.parent, new_name)) 

# create genre column using genre table? like genre match or something? a function?

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

def clean_data():
    for file in file_paths:
        with open(file, 'r', encoding=ENCODING) as f:
            firstline = f.readline()
            f.close()

        delim = find_delimiter(firstline)
        df = pd.read_csv(file, delimiter=delim, encoding=ENCODING, on_bad_lines='skip') # skip malformed lines - check
        df = clean_columns(df) 

        # clean the data types here (df has all potential columns, so can clean as one df)

def clean_columns(original_df): 
    filtered_df = pd.DataFrame() # empty df

    for original_header in original_df.columns:
        sanitised_header = re.sub(r'[-_]', ' ', original_header).strip().lower()
        if 'book' in sanitised_header.split(' ') and len(sanitised_header.split(' ')) > 1:
            sanitised_header = sanitised_header.replace('book', '').strip()

        # flags
        is_review = 'review' in sanitised_header.split(' ') # exact match to avoid 'reviewer', etc.
        is_title_like = any(re.search(p, sanitised_header, re.IGNORECASE) for p in ['name', 'book', 'title'])             
        is_synopsis = any(re.search(p, sanitised_header, re.IGNORECASE) for p in ['synopsis', 'summary', 'description']) 
        is_rating = any(re.search(p, sanitised_header, re.IGNORECASE) for p in ['rating'])
        is_publication_year = any(re.search(p, sanitised_header, re.IGNORECASE) for p in ['year'])

        if is_synopsis:
            filtered_df['synopsis'] = original_df[original_header]

        elif is_review and not is_title_like:
            filtered_df['review'] = original_df[original_header]
            
        elif is_rating:
            filtered_df['rating'] = original_df[original_header]

        elif is_publication_year:
            filtered_df['publication_year'] = pd.to_numeric(original_df[original_header], errors="coerce") # mixed data types detected in the column
            # do coerce for other columns? appropriate cleaning?

        elif is_title_like: 
            filtered_df['title'] = original_df[original_header]

        elif sanitised_header in d.VALID_SCHEMA_COLUMNS: 
            filtered_df[sanitised_header] = original_df[original_header]

    print(f'{filtered_df.columns} extracted from {original_df.columns}')
    return filtered_df

book_directories = list(Path(d.BOOK_DATA_PATH).iterdir())
clean_filenames(book_directories) 

file_paths = [str(Path(d.BOOK_DATA_PATH) / item.name) for item in book_directories if not item.name.startswith('.')]

clean_data() # cleaning the data, quality and header checks - check cleaning choices

#def sort_data(): # putting info into relevant place in db -> make insert_data(); reuse this function for later inserts
    # for file in file_paths

# change to: clean all then sort all at once
#for file in file_paths:
    #clean_data(file) # cleaning the data, quality and header checks - check cleaning choices
    #sort_data(file) # putting info into relevant place in db -> make insert_data(); reuse this function for later inserts