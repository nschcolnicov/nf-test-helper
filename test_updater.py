import csv
import sys

def update_nf_test_file(csv_file, nf_test_file):
    # Read the CSV file and filter rows
    files_to_change = set()  # Using a set to automatically handle duplicates
    with open(csv_file, 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        # Ensure the CSV file has 6 columns
        if len(csvreader.fieldnames) != 6:
            print("Error: The CSV file must contain exactly 6 columns.")
            return
        
        # Filter rows where "Match" column has value "NO"
        for row in csvreader:
            if row.get("Match") == "NO":
                files_to_change.add(row.get("file1"))  # Add to set to handle duplicates

    files_to_change = list(files_to_change)  # Convert set back to list

    # Read the .nf.test file and update lines
    output_file = nf_test_file + '.v2'
    with open(nf_test_file, 'r') as nf_file, open(output_file, 'w') as nf_file_v2:
        for line in nf_file:
            stripped_line = line.rstrip()
            if any(file in stripped_line for file in files_to_change):
                # Skip lines already containing ".exists()"
                if ".exists()" in stripped_line:
                    nf_file_v2.write(line)
                    continue
                
                # If line ends with ",", replace it with ".exists(),"
                if stripped_line.endswith(','):
                    updated_line = stripped_line[:-1] + '.exists(),'
                else:
                    updated_line = stripped_line + '.exists()'
                
                nf_file_v2.write(updated_line + '\n')
            else:
                nf_file_v2.write(line)

    print(f"Updated .nf.test file saved as {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <csv_file> <nf_test_file>")
    else:
        csv_file = sys.argv[1]
        nf_test_file = sys.argv[2]
        update_nf_test_file(csv_file, nf_test_file)
