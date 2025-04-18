import csv
import os
import string
import re
import shutil
import pandas as pd

def main():  # songs.csv is pretty much useless. It has no extra info that I need

    initial_copy()

    remove_columns()

    # renaming some columns
    rename_column("albums", "name", "album_name")
    rename_column("albums", "type", "album_type")
    rename_column("albums", "year", "album_year")
    rename_column("albums", "singer_name", "artist")
    rename_column("albums", "Unnamed: 0", "id")
    rename_column("lyrics", "Unnamed: 0", "id")

    # remove some words from the csv files
    replace_array = ["albums", "lyrics"]
    for i in range(len(replace_array)):
        replace(replace_array[i], "original", "artist", " Lyrics", "")
        
    replace("albums", "original", "album_year", "Not Defined", "-1")

    # copy the clean files before stemming etc
    for name in ["lyrics", "albums"]:
        copy_file(name)

    # lowering the case of the files in the modified folder
    for name in ["lyrics", "albums"]:
        to_lower_case(name)

def initial_copy():  # copies tha data from the "back-up" folder to the "data/original"
    for name in ["albums", "lyrics"]:
        src = f"./back-up/{name}.csv"
        dst = f"./data/original/{name}.csv"
        shutil.copy2(src, dst)

def remove_columns():
    cols_to_remove = {
        "albums": ["id"],  # "Unnamed: 0"
        "lyrics": ["link"],  # "Unnamed: 0"
        # "songs": ["", "song_id", "song_href"],  # song_href was added later on
    }

    for key, values in cols_to_remove.items():
        for value in values:
            pass
            delete_column("original", key, value)
        
def rename_column_old(filename, column, col_new_name):
    file_1 = f"./data/original/{filename}.csv"
    file_2 = f"./data/original/{filename}_renamed_column.csv"

    if not os.path.exists(file_1):
        print(f"rename_column: problem while locating the '{file_1}' file")
        return

    with open(file_1, 'r') as input_csv, open(file_2, 'w', newline='') as output_csv:
        reader = csv.DictReader(input_csv)

        new_fieldnames = [col_new_name if field == column else field for field in reader.fieldnames]

        writer = csv.DictWriter(output_csv, fieldnames=new_fieldnames)
        writer.writeheader()

        for row in reader:
            row[col_new_name] = row.pop(column)
            writer.writerow(row)

    print(f"The '{column}' column was renamed to '{col_new_name}' in the '{filename}.csv'")
    os.remove(file_1)
    os.rename(file_2, file_1)
    
def rename_column(filename, column, col_new_name):
    file_1 = f"./data/original/{filename}.csv"
    file_2 = f"./data/original/{filename}_renamed_column.csv"

    if not os.path.exists(file_1):
        print(f"rename_column: problem while locating the '{file_1}' file")
        return

    try:
        df = pd.read_csv(file_1)

        if column not in df.columns:
            print(f"rename_column: '{column}' column not found in the CSV file")
            return

        df.rename(columns={column: col_new_name}, inplace=True)

        df.to_csv(file_2, index=False)

        print(f"The '{column}' column was renamed to '{col_new_name}' in the '{filename}.csv'")
        os.remove(file_1)
        os.rename(file_2, file_1)

    except Exception as e:
        print(f"An error occurred: {e}")

def replace(filename, case, column, old_value, new_value):  # "\n", "\'", "Lyrics"
    file_1 = f"./data/{case}/{filename}.csv"
    file_2 = f"./data/{case}/{filename}_modified.csv"

    if not os.path.exists(file_1):  # if file doesn't exist
        print(f"replace: problem while locating the '{file_1}' file")
        return
        
    with open(file_1, 'r') as input_csv, open(file_2, 'w', newline='') as output_csv:
        reader = csv.DictReader(input_csv)
        
        fieldnames = [field for field in reader.fieldnames]  # gets all the column names

        writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if column in row:
                row[column] = row[column].replace(old_value, new_value)
                writer.writerow(row)

    print(f"'{old_value}' got replaced with '{new_value}' for the '{column}' column in the '{filename}.csv'")
    os.remove(file_1)
    os.rename(file_2, file_1)  # to rename the output file to the input file name

def copy_file(filename):
    input = f"./data/original/{filename}.csv"
    output = f"./data/modified/{filename}.csv"

    shutil.copy2(input, output)

def to_lower_case_old(filename):
    file_1 = f"./data/modified/{filename}.csv"
    file_2 = f"./data/modified/{filename}_lower.csv"

    with open(file_1, 'r') as input_csv, open(file_2, 'w') as output_csv:

        reader = csv.reader(input_csv)
        writer = csv.writer(output_csv)

        header = next(reader, None)
        if header:
            writer.writerow([col.lower() for col in header])

        for row in reader:
            writer.writerow([col.lower() if isinstance(col, str) else col for col in row])

    print(f"Text converted to lowercase for '{filename}.csv'")
    os.remove(file_1)
    os.rename(file_2, file_1)

def to_lower_case(filename):
    file_1 = f"./data/modified/{filename}.csv"
    
    # if file doesn't exist
    if not os.path.exists(file_1):
        print(f"to_lower_case: problem while locating the '{file_1}' file")
        return
    
    try:
        df = pd.read_csv(file_1)

        # Convert column names to lowercase
        df.columns = map(str.lower, df.columns)

        # Convert all text in the DataFrame to lowercase
        df = df.apply(lambda x: x.map(lambda y: y.lower() if isinstance(y, str) else y))

        df.to_csv(file_1, index=False)
        
        print(f"Text converted to lowercase for '{filename}.csv'")

    except Exception as e:
        print(f"An error occurred: {e}")

def delete_column(folder, filename, column):
    file_1 = f"./data/{folder}/{filename}.csv"

    # if file doesn't exist
    if not os.path.exists(file_1):
        print(f"delete_column: problem while locating the '{file_1}' file")
        return
    
    try:
        df = pd.read_csv(file_1)

        if column not in df.columns:  # checks if the column exists
            print(f"delete_column: '{column}' column can't be found in the '{filename}.csv' file")
            return

        df.drop(column, axis=1, inplace=True)

        df.to_csv(file_1, index=False)
        
        print(f"The '{column}' column from the '{filename}.csv' was deleted")

    except Exception as e:
        print(f"An error occurred: {e}")

def append_to_file(folder, filename, string):  # boolean, if the data are raw
    file_1 = f"./data/{folder}/{filename}.csv"

    with open(file_1, 'a') as target_file:
        target_file.write(f"{string}\n")

def check_if_exists(filename, array):
    target_file = f"./data/modified/{filename}.csv"

    with open(target_file, 'r') as target_file:
        reader = csv.DictReader(target_file)

        for row in reader:
            if row and row["artist"].lower() == array[0].lower():
                if row["song_name"].lower() == array[1].lower():
                    # print(f"The song {array[1]} by {array[0]} already exists")
                    return True

        return False

def remove_entry(folder, filename, array):
    target_file = f"./data/{folder}/{filename}.csv"
    temp_file_name = "temp.csv"

    with open(target_file, 'r') as source_file, open(temp_file_name, 'w', newline='') as temp_file:
        reader = csv.DictReader(source_file)
        fieldnames = reader.fieldnames
        decrement_id = False

        writer = csv.DictWriter(temp_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            if row and row["artist"].lower() == array[0].lower():
                if row["song_name"].lower() == array[1].lower():
                    print(f"Removed the song '{array[1]}' by '{array[0]}' from the '{target_file}' file")
                    decrement_id = True
                else:
                    if decrement_id:
                        row["id"] = str(int(row["id"]) - 1)
                    writer.writerow(row)
            else:
                if decrement_id:
                    row["id"] = str(int(row["id"]) - 1)
                writer.writerow(row)

    os.remove(target_file)
    os.rename(temp_file_name, target_file)

def check_csv_length(filename):
    file_1 = f"./data/modified/{filename}.csv"
    df = pd.read_csv(file_1)
    return len(df)
