import csv
import re
import os
import argparse

def main(input_file):
    output_file = 'output.csv'
    rows = []

    # Open the input file and read the data
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

    # Remove duplicate rows
    unique_rows = list(map(list, set(map(tuple, rows))))

    # Open the output file and write the unique data
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)

        # Write header
        writer.writerow(['test_name', 'file1', 'md5_1', 'file2', 'md5_2', 'Match'])

        # Write all unique rows
        writer.writerows(unique_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process md5 data and save unique rows to CSV.')
    parser.add_argument('input_file', type=str, help='The input file to process')
    args = parser.parse_args()
    
    main(args.input_file)
