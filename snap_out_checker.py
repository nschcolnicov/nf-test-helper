import csv
import re
import os
import argparse

def main(input_file):
    output_file = 'output.csv'
    rows = []

    # Read new rows from the input file
    with open(input_file, 'r') as infile:
        test_name = None

        for line in infile:
            if "Test Workflow main.nf" in line:
                test_name = line.strip()
                print(f'Reading: {test_name}')
            # Check if the line contains ":md5"
            if ':md5' in line:
                # Remove any "|" characters
                line = line.replace('|', '')
                line = line.replace('"', '')
                line = line.replace('\t', '')
                line = line.replace(':md5', '')
                line = line.strip()
                fields = re.split(r'[ ,]', line)
                while '' in fields: fields.remove('')
                fields.append(test_name)

                if fields:
                    if len(fields) == 5: 
                        file1, md5_1, file2, md5_2, test_name = fields
                        # Check if md5_1 and md5_2 match
                        match_status = 'YES' if md5_1 == md5_2 else 'NO'
                        row = [test_name, file1, md5_1, file2, md5_2, match_status]
                        rows.append(row)
                    else:
                        print(fields)
                else:
                    print(f'No match found for line: {line.strip()}')

    # Read existing rows from the output file if it exists
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        with open(output_file, 'r') as outfile:
            reader = csv.reader(outfile)
            existing_rows = list(reader)
            header = existing_rows[0]  # Assumes the first row is the header
            existing_rows = existing_rows[1:]  # Skip header
    else:
        existing_rows = []
        header = ['test_name', 'file1', 'md5_1', 'file2', 'md5_2', 'Match']

    # Combine existing rows with new rows
    all_rows = existing_rows + rows

    # Remove duplicates
    unique_rows = list(map(list, set(map(tuple, all_rows))))

    # Check if there are new rows to append
    if row:
        # Write the unique rows to the output file
        with open(output_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(header)  # Write header
            writer.writerows(unique_rows)
    else:
        print("No new rows to append")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process md5 data and save unique rows to CSV.')
    parser.add_argument('input_file', type=str, help='The input file to process')
    args = parser.parse_args()
    
    main(args.input_file)
