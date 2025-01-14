import argparse
from collections import defaultdict

def main():

    # Define the argument parser
    parser = argparse.ArgumentParser(description="Group URLs by title from an input file.")
    parser.add_argument("input_file", help="Path to the input file containing URLs.")
    parser.add_argument(
        "--output", "-o", 
        help="Path to the output file to save the results. If not provided, results are printed to stdout."
    )

    args = parser.parse_args()

    # Dictionary to group URLs by title
    grouped_urls = defaultdict(list)

    # Read the file line by line
    try:
        with open(args.input_file, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                # Split the line into URL and title
                if " => " in line:
                    url, title = line.split(" => ", 1)
                    grouped_urls[title].append(url)
                else:
                    # URLs without a title go into a special "No Title" group
                    grouped_urls["No Title"].append(line)

    except FileNotFoundError:
        print(f"Error: The file '{args.input_file}' does not exist.")
        exit(1)

    # Format the grouped URLs
    output_lines = []
    for title, urls in grouped_urls.items():
        output_lines.append(f"{title}:\n")
        output_lines.append("-----\n")
        output_lines.extend(f"{url}\n" for url in urls)
        output_lines.append("\n")  # Add a blank line between groups

    # Output to file or stdout
    if args.output:
        try:
            with open(args.output, "w") as output_file:
                output_file.writelines(output_lines)
            print(f"Grouped URLs have been written to '{args.output}'.")
        except Exception as e:
            print(f"Error writing to file '{args.output}': {e}")
    else:
        # Print to stdout
        print("".join(output_lines))
