import os
import sys

def generate_nf_test(output_dir, test_name, num_tasks):
    # Header section of the nf-test
    nf_test_content = f"""
nextflow_pipeline {{

    name "Test Workflow main.nf - {test_name}"
    script "main.nf"
    profile "{test_name}"
    tag "{test_name}"
    tag "pipeline"

    test("{test_name}") {{

        when {{
            params {{
                outdir        = "$outputDir"
            }}
        }}

        then {{
            assertAll(
                {{ assert workflow.success }},
                {{ assert snapshot(UTILS.removeNextflowVersion("$outputDir")).match("software_versions") }},
                {{ assert workflow.trace.succeeded().size() == {num_tasks} }},
"""
    # Loop over first-level directories in outputDir
    for first_level_dir in os.listdir(output_dir):
        first_level_path = os.path.join(output_dir, first_level_dir)

        # Skip the "pipeline_info" directory
        if first_level_dir == "pipeline_info" or not os.path.isdir(first_level_path):
            continue

        # List all files recursively under the first-level directory
        snapshot_files = []
        for root, dirs, files in os.walk(first_level_path):
            # Filter files that should be excluded
            filtered_files = [f for f in files if not (f.endswith(".json") or f.endswith(".html") or f.endswith(".log") or f.endswith(".png") or f.endswith(".svg") or f.endswith(".pdf"))]
            snapshot_files.extend([os.path.relpath(os.path.join(root, f), output_dir) for f in filtered_files])

        # If there are valid files, create a snapshot assertion
        if snapshot_files:
            snapshot_assertion = f"""\
                {{ assert snapshot(
                    {',\n                    '.join([f'path("$outputDir/{f}")' for f in snapshot_files])}
                ).match("{first_level_dir}") }},\n"""
            nf_test_content += snapshot_assertion

    # Close the then block and nf-test format
    nf_test_content += """\
            )
        }

    }

}
"""
    return nf_test_content

def main():
    if len(sys.argv) != 4:
        print("Usage: python generate_nf_test.py <outputDir> <test_name> <number_of_tasks>")
        sys.exit(1)

    output_dir = sys.argv[1]
    test_name = sys.argv[2]
    num_tasks = sys.argv[3]

    nf_test_content = generate_nf_test(output_dir, test_name, num_tasks)

    # Output the generated nf-test to a file
    test_filename = f"{test_name}.nf.test"
    with open(test_filename, 'w') as test_file:
        test_file.write(nf_test_content)

    print(f"nf-test generated: {test_filename}")

if __name__ == "__main__":
    main()
