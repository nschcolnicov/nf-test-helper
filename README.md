
# nf-test-helper

**nf-test-helper** is a collection of three Python scripts designed to assist in generating and managing nf-tests for Nextflow pipelines. These scripts streamline the process of creating snapshot assertions for file md5sum checks or file existence checks, making it easier to ensure the reliability of your pipeline.

## Scripts

### 1. nf-test-gen.py
This script is used to initialize an nf-test file based on the output directory of a Nextflow pipeline. It generates an .".nf.test" file that includes detailed snapshot assertions for files both directly in the output_dir and within its subdirectories. It organizes the assertions by first-level directories and their subdirectories

**Usage:**
```bash
python nf-test-gen.py <outputDir> <test_name> <number_of_tasks>
```

- `<outputDir>`: The directory where the output files from the Nextflow pipeline are located.
- `<test_name>`: A name for the test.
- `<number_of_tasks>`: The number of tasks expected to have succeeded in the pipeline.

### 2. snap_out_checker.py
This script processes the output of the `nf-test test` command to generate a table comparing the md5sums of all the files used in the snapshot. The output is saved as a CSV file named `output.csv`.

**Usage:**
```bash
python snap_out_checker.py <input_file>
```

- `<input_file>`: The output file generated by running `nf-test test`, typically redirected from stdout and stderr.

### 3. test_updater.py
This script updates the `.nf.test` file by replacing the md5sum checks with `.exists()` assertions for files that are identified as undeterministic in the snapshot comparison.

**Usage:**
```bash
python test_updater.py <csv_file> <nf_test_file>
```

- `<csv_file>`: The CSV file generated by `snap_out_checker.py`, containing the comparison of md5sums.
- `<nf_test_file>`: The `.nf.test` file generated by `nf-test-gen.py` that needs updating.

## Workflow

1. **Run the Nextflow pipeline** with the test profile for which you want to generate an nf-test.
2. **Generate the nf-test file** using `nf-test-gen.py`.
3. **Run the generated nf-test file** using `nf-test test` and redirect stdout and stderr to a file (e.g., `nf-test.out`).
4. **Check the md5sums** using `snap_out_checker.py`.
5. **Update the nf-test file** using `test_updater.py`.
6. **Repeat steps 3-5** until the `nf-test.out` file contains no mismatching md5sums.

## Example

```bash
# Step 1: Run the Nextflow pipeline
nextflow run main.nf -profile test

# Step 2: Generate the nf-test file
python nf-test-gen.py ./output test_name 5

# Step 3: Run the nf-test n times to see which files are deterministic and which ones aren't and save the output
for i in {1..n}; do
nf-test test tests/test_name.nf.test >> nf-test.out 2>&1 
done

# Step 4: Check the md5sums
python snap_out_checker.py nf-test.out

# Step 5: Update the nf-test file
python test_updater.py output.csv tests/test_name.nf.test

# Repeat steps 3-5 as necessary

## Note: The `output.csv` file generated can then be used as a memory of which files are undeterministic and which files arent't. If the output.csv has been updated with enough nf-test runs, then one can skip the step of running the `nf-test test` command and subsequently the `snap_out_checker.py` script, and just run the `nf-test-gen.py` and `test_updater.py` scripts. This works as long as all of the file names outputted by the new test are already included in the `output.csv` table.
```

