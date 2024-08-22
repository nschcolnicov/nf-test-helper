
# TODO for nf-test-helper Development

## Next steps
- [ ] Generate beautify script to sort lines by snapshot group, separating the ones with .exist() from the other ones
- [ ] Update test generation script to split by first subdirectory as well
- [ ] Update usage readme so that it says to run nf-test 10 times twice and then run script for correcting nf-test file.

# Ideas
- Goal: Have everything run within a tool that should be able to run nextflow and nf-test and iterate so that it generates the nf-test fully automatically.

## 1. Initial Setup and Execution
- [ ] Implement a feature to allow the tool to run the Nextflow pipeline using `-profile "$profile_name"` and `--outdir "$outputdir"`.
- [ ] Update the `nf-test-gen.py` script to automatically read the number of tasks from the Nextflow execution or the trace file.

## 2. Automated Testing Workflow
- [ ] Ensure the `nf-test-gen.py` script runs on the specified output directory.
- [ ] Modify the workflow to:
  - [ ] Run the `nf-test test` command on the generated .nf.test file twice (once for generating the test and another for validating it).
  - [ ] Store the stdout and stderr output into a text file.

## 3. Handling Test Failures
- [ ] Implement logic to:
  - [ ] If the test fails on the second execution, run the `snap_out_checker.py` script on the generated stdout/stderr file to identify undeterministic files and generate an `output.csv`.
  - [ ] Run the `test_updater.py` script using `output.csv` and `.nf.test` files as input.
  - [ ] Automatically update the `.nf.test` file with the updated version from `test_updater.py`.

## 4. Iterative Testing
- [ ] Develop a loop to:
  - [ ] Run the `nf-test test` command again twice (first with the `--updateSnapshot` argument and then without it).
  - [ ] Store the stdout and stderr output into a text file.
  - [ ] If the test fails on the second execution, repeat steps 5-9 until successful execution on both `nf-test test` runs.

## 5. Workflow and User Options
- [ ] Implement the entire process as an automated workflow that loops through the steps until successful.
- [ ] Add an option for users to specify which arguments to run in `nf-test`.
- [ ] By default, exclude certain file extensions; add an argument allowing users to modify which extensions to exclude.
- [ ] Implement a feature to delete the `.nf-test` folder between runs to prevent running out of disk space.

## 6. Managing Multiple Tests
- [ ] When running multiple tests simultaneously:
  - [ ] Ensure the `test_updater.py` script updates only the lines related to the respective tests based on the `test_name` column in `output.csv`.
  - [ ] Provide an option to update all lines for a particular file if it fails in any of the tests (as per the current implementation).
