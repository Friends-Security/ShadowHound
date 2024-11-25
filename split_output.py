import os
import math
import argparse


def split_large_file_into_chunks(input_file, base_output_name, num_chunks):
    object_delimiter = "--------------------"

    # Step 1: Count total objects
    total_objects = 0
    with open(input_file, "r", encoding="utf-8-sig") as infile:
        for line in infile:
            if line.strip() == object_delimiter:
                total_objects += 1
                if total_objects % 100000 == 0:
                    print(f"[*] Objects counted: {total_objects}")

    if total_objects == 0:
        print("[-] No objects found in the file.")
        return

    objects_per_chunk = math.ceil(total_objects / num_chunks)
    print(f"[+] Total objects: {total_objects}")
    print(f"[*] Objects per chunk: {objects_per_chunk}")

    # Step 2: Split objects into chunks
    current_chunk_index = 0
    current_object_count = 1
    current_chunk_lines = []

    with open(input_file, "r", encoding="utf-8-sig") as infile:
        for line in infile:
            if line.strip() == object_delimiter and current_object_count > 0:
                # Start a new object
                current_object_count += 1

                # Write the current chunk if it is full
                if current_object_count > objects_per_chunk:
                    write_chunk_to_file(
                        current_chunk_lines, base_output_name, current_chunk_index
                    )
                    current_chunk_index += 1
                    current_chunk_lines = []
                    current_object_count = 1  # Reset for the new object

            # Append the line to the current chunk
            current_chunk_lines.append(line)

        # Write any remaining lines to the last chunk
        if current_chunk_lines:
            write_chunk_to_file(
                current_chunk_lines, base_output_name, current_chunk_index
            )


def write_chunk_to_file(chunk_lines, base_output_name, chunk_index):
    output_file = f"{base_output_name}_chunk_{chunk_index}.txt"
    with open(output_file, "w", encoding="utf-8-sig") as outfile:
        outfile.writelines(chunk_lines)
    print(f"[+] Chunk {chunk_index} written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large ShadowHound file into chunks.")
    parser.add_argument(
        "-i",
        "--input_file",
        type=str,
        required=True,
        help="Path to the input text file.",
    )
    parser.add_argument(
        "-o",
        "--base_output_name",
        type=str,
        required=True,
        help="Base name for the output files.",
    )
    parser.add_argument(
        "-n",
        "--num_chunks",
        type=int,
        required=True,
        help="Number of chunks to split the file into.",
    )

    args = parser.parse_args()

    split_large_file_into_chunks(
        args.input_file, args.base_output_name, args.num_chunks
    )
