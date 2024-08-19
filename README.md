# Nextflow Test Generator

This script, `generate_nf_test.py`, automates the creation of `nf-test` files for testing Nextflow pipelines. It recursively scans the provided output directory (`$outputDir`) to generate snapshot assertions based on the files found. The script ensures that only relevant files are included in the assertions by excluding specific file types such as `.json`, `.html`, `.log`, `.png`, `.svg`, and `.pdf`.

The generated `nf-test` files can then be used to validate the correctness of your Nextflow pipeline by checking that the expected output files are produced and match the snapshots.

## Usage

To generate an `nf-test` file using the `generate_nf_test.py` script, follow these steps:

### 1. Command-Line Execution

Run the script from the command line with the following syntax:

```bash
python generate_nf_test.py <outputDir> <test_name> <number_of_tasks>
```

### Arguments

- **`<outputDir>`**: The path to the directory containing the output files from your Nextflow pipeline. The script will traverse this directory and generate snapshot assertions based on the files found within the first-level subdirectories. It skips files with the extensions `.json`, `.html`, `.log`, `.png`, `.svg`, and `.pdf`, as well as the `pipeline_info` directory.

- **`<test_name>`**: A string that will be used as the name of the test case in the generated `nf-test` file. This name will also be used for tagging the test and identifying it in the `nf-test` output.

- **`<number_of_tasks>`**: An integer that represents the expected number of successfully completed tasks in the Nextflow workflow. This value will be used to assert that the correct number of tasks succeeded.

