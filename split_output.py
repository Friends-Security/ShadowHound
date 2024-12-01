import os
import math
import argparse

object_delimiter = "--------------------"


def split_large_file_into_chunks(input_file, base_output_name, num_chunks):

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
    current_object_count = 0  # Total objects processed so far
    chunk_object_count = 0    # Objects in the current chunk
    current_chunk_lines = []

    with open(input_file, "r", encoding="utf-8-sig") as infile:
        for line in infile:
            current_chunk_lines.append(line)

            if line.strip() == object_delimiter:
                current_object_count += 1
                chunk_object_count += 1

                # If we have reached the number of objects per chunk, write the chunk
                if chunk_object_count >= objects_per_chunk:
                    write_chunk_to_file(
                        current_chunk_lines,
                        base_output_name,
                        current_chunk_index,
                        chunk_object_count,
                    )
                    current_chunk_index += 1
                    current_chunk_lines = []
                    chunk_object_count = 0

        # After finishing reading the file, write any remaining lines
        if current_chunk_lines:
            write_chunk_to_file(
                current_chunk_lines,
                base_output_name,
                current_chunk_index,
                chunk_object_count,
            )


def write_chunk_to_file(chunk_lines, base_output_name, chunk_index, chunk_object_count):
    output_file = f"{base_output_name}_chunk_{chunk_index}.txt"
    with open(output_file, "w", encoding="utf-8-sig") as outfile:
        # Write the starting delimiter
        outfile.write(f"{object_delimiter}\n{object_delimiter}\n")
        # Write the chunk lines
        outfile.writelines(chunk_lines)
        # Write the ending lines
        outfile.write(f"Retrieved {chunk_object_count} results total\n")
    print(f"[+] Chunk {chunk_index} written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a large file into chunks.")
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
