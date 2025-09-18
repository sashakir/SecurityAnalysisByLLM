import os
import re

def process_java_files(root_dir):
    # Matches comments like: //line 123
    comment_pattern = re.compile(r'//.*$')

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith(".java"):
                java_path = os.path.join(dirpath, filename)
                expected_path = os.path.join(
                    dirpath, filename.replace(".java", "-expected.txt")
                )
                print(f"Processing: {java_path}")

                with open(java_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                line_numbers = []
                cleaned_lines = []

                for i, line in enumerate(lines, start=1):
                    match = comment_pattern.search(line)
                    if match:
                        line_numbers.append(i)
                        # Remove the //line XX comment part only
                        cleaned_line = comment_pattern.sub("", line)
                        cleaned_lines.append(cleaned_line.rstrip() + "\n")
                    else:
                        cleaned_lines.append(line)

                # Write expected file
                with open(expected_path, "w", encoding="utf-8") as f:
                    for num in line_numbers:
                        f.write(f"{filename}:{num}\n")

                # Overwrite cleaned java file
                with open(java_path, "w", encoding="utf-8") as f:
                    f.writelines(cleaned_lines)


target_directory = "tests/fraunhofer-suite"
process_java_files(target_directory)