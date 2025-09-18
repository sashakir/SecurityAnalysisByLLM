import os


def prepend_line_numbers_to_java_files(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".java"):
                file_path = os.path.join(dirpath, filename)
                print(f"Processing: {file_path}")

                # Read file content
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                # Prepend line numbers
                modified_lines = [
                    f"/*line {i + 1}*/ {line}" if line.strip() != "" else f"/*line {i + 1}*/\n"
                    for i, line in enumerate(lines)
                ]

                # Write back
                with open(file_path, "w", encoding="utf-8") as f:
                    f.writelines(modified_lines)


target_directory = "tests/fraunhofer-suite"  # Change this to your directory path
prepend_line_numbers_to_java_files(target_directory)