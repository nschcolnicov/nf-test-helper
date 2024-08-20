# Nextflow Test Generator

1. First run the 'nf-test-gen.py' to initialize the nf-test for all of the files found in the output directory. This will output a ".nf.test" file.
2. Then run nf-test test on the generated nf.test file redirecting stdout and stdout to a new file. i.e 'nf-test test tests/test.nf.test > nf-test.out 2>&1'.
3. Then run the 'snap_out_checker.py' to generate a table that will contain a table with the comparsion of the md5sums of all the files used in the snapshot.
4. Finally run 'test_updater.py' to update the generated ".nf.test" file replacing the md5sum check with only a ".exists()" assertion for undeterministic files.
5. Loop around steps 2 to 4 until the nf-test.out file contains no mismatching md5sums.

This script, `nf-test-gen.py`, automates the creation of `nf-test` files for testing Nextflow pipelines. It recursively scans the provided output directory (`$outputDir`) to generate snapshot assertions based on the files found. The script ensures that only relevant files are included in the assertions by excluding specific file types such as `.json`, `.html`, `.log`, `.png`, `.svg`, and `.pdf`.

The generated `nf-test` files can then be used to validate the correctness of your Nextflow pipeline by checking that the expected output files are produced and match the snapshots.

## Usage

To generate an `nf-test` file using the `nf-test-gen.py` script, follow these steps:

### 1. Command-Line Execution

Run the script from the command line with the following syntax:

```bash
python nf-test-gen.py <outputDir> <test_name> <number_of_tasks>
```

### Arguments

- **`<outputDir>`**: The path to the directory containing the output files from your Nextflow pipeline. The script will traverse this directory and generate snapshot assertions based on the files found within the first-level subdirectories. It skips files with the extensions `.json`, `.html`, `.log`, `.png`, `.svg`, and `.pdf`, as well as the `pipeline_info` directory.

- **`<test_name>`**: A string that will be used as the name of the test case in the generated `nf-test` file. This name will also be used for tagging the test and identifying it in the `nf-test` output.

- **`<number_of_tasks>`**: An integer that represents the expected number of successfully completed tasks in the Nextflow workflow. This value will be used to assert that the correct number of tasks succeeded.

