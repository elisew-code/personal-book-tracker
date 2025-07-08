
# (viewed data structure in excel)

import sys
PROJECT_ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(PROJECT_ROOT_DIR)) 

import definitions as d
from pathlib import Path
import os
import pandas

book_directories = Path(d.BOOK_DATA_PATH).iterdir()

for item in book_directories:
    new_name = 'amazon_'

    if item.match('**/Top*.csv'): 
        new_name += 'top-100'
        print(new_name)

    elif item.match('**/customer*.csv'): 
        new_name += item.name.replace('customer ', '')
        print(new_name)

    else:
        new_name += item.name
        print(new_name)

    new_path = item.parent / new_name
    os.rename(item, new_path)

# with open('amazon_top-100', 'r') as f:




