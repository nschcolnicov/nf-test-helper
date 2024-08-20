import csv
import re

input_file = '/scratch/schcolni/nfcore_pipelines/smrnaseq/nf-test.out'  # Replace with your actual input file
output_file = 'output.csv'  # Replace with your desired output file


with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['test_name','file1', 'md5_1', 'file2', 'md5_2', 'Match'])  # Header row
    
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

            # print(fields)
            if fields:
                if len(fields) == 5: 
                    file1, md5_1, file2, md5_2,test_name = fields
                    # Check if md5_1 and md5_2 match
                    match_status = 'YES' if md5_1 == md5_2 else 'NO'
                    writer.writerow([test_name, file1, md5_1, file2, md5_2, match_status])
                else:
                    print(fields)

            else:
                print(f'No match found for line: {line.strip()}')
