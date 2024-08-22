import os
import sys

def generate_nf_test(output_dir, test_name, num_tasks):
    nf_test_content = """
nextflow_pipeline {{

    name "Test Workflow main.nf - {test_name}"
    script "main.nf"
    profile "{test_name}"
    tag "{test_name}"
    tag "pipeline"

    test("{test_name}") {{

        when {{
            params {{
                outdir = "$outputDir"
            }}
        }}

        then {{
            assertAll(
                {{ assert workflow.success }},
                {{ assert snapshot(UTILS.removeNextflowVersion("$outputDir")).match("software_versions") }},
                {{ assert workflow.trace.succeeded().size() == {num_tasks} }},
""".format(test_name=test_name, num_tasks=num_tasks)

    # Snapshot for files directly in the output_dir
    direct_files = []
    for root, dirs, files in os.walk(output_dir):
        if root == output_dir:  # Only consider files directly in output_dir
            direct_files.extend(files)

    if direct_files:
        snapshot_direct_files = """
                {{ assert snapshot(
                    {files}
                ).match("outdir") }},
""".format(
            files=',\n                    '.join(['path("$outputDir/{f}")'.format(f=f) for f in direct_files])
        )
        nf_test_content += snapshot_direct_files

    for first_level_dir in os.listdir(output_dir):
        first_level_path = os.path.join(output_dir, first_level_dir)

        if first_level_dir == "pipeline_info" or not os.path.isdir(first_level_path):
            continue

        # Snapshot for files in the first level directory
        all_subdir_files = set()
        snapshot_files = []
        for root, dirs, files in os.walk(first_level_path):
            filtered_files = [f for f in files if not (f.endswith((".json", ".html", ".log", ".png", ".svg", ".pdf")))]
            for f in filtered_files:
                relative_path = os.path.relpath(os.path.join(root, f), output_dir)
                if os.path.dirname(relative_path).startswith(first_level_dir):
                    all_subdir_files.add(relative_path)

            snapshot_files.extend([os.path.relpath(os.path.join(root, f), output_dir) for f in filtered_files if os.path.dirname(os.path.relpath(os.path.join(root, f), output_dir)) == first_level_dir])

        if snapshot_files:
            snapshot_assertion = """
                {{ assert snapshot(
                    {files}
                ).match("{dir}") }},
""".format(
                files=',\n                    '.join(['path("$outputDir/{f}")'.format(f=f) for f in snapshot_files]),
                dir=first_level_dir
            )
            nf_test_content += snapshot_assertion

        # Snapshot for each subdirectory in the first level directory
        for sub_dir in next(os.walk(first_level_path))[1]:
            sub_dir_path = os.path.join(first_level_path, sub_dir)
            snapshot_subdir_files = []

            for root, dirs, files in os.walk(sub_dir_path):
                filtered_files = [f for f in files if not (f.endswith((".json", ".html", ".log", ".png", ".svg", ".pdf")))]
                snapshot_subdir_files.extend([os.path.relpath(os.path.join(root, f), output_dir) for f in filtered_files])

            if snapshot_subdir_files:
                snapshot_subdir_assertion = """
                {{ assert snapshot(
                    {files}
                ).match("{dir}_{subdir}") }},
""".format(
                    files=',\n                    '.join(['path("$outputDir/{f}")'.format(f=f) for f in snapshot_subdir_files]),
                    dir=first_level_dir,
                    subdir=sub_dir
                )
                nf_test_content += snapshot_subdir_assertion

    nf_test_content += """
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
    
    try:
        num_tasks = int(sys.argv[3])
    except ValueError:
        print("Error: <number_of_tasks> must be an integer.")
        sys.exit(1)

    if not os.path.isdir(output_dir):
        print(f"Error: The directory {output_dir} does not exist.")
        sys.exit(1)

    nf_test_content = generate_nf_test(output_dir, test_name, num_tasks)

    test_filename = f"{test_name}.nf.test"
    try:
        with open(test_filename, 'w') as test_file:
            test_file.write(nf_test_content)
    except IOError as e:
        print(f"Error writing to file {test_filename}: {e}")
        sys.exit(1)

    print(f"nf-test generated: {test_filename}")

if __name__ == "__main__":
    main()
