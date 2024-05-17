from PIL import Image
import os


def convert_dds_to_png(input_file: str, output_file: str):
    try:
        with Image.open(input_file) as img:
            img.save(output_file)
    except IOError:
        print("Cannot convert file.")


start_dir = input("Path containing .DDS files")
end_dir = input("Output path")

dds_files = [file for file in os.listdir(start_dir) if file.endswith(".DDS")]

for file in dds_files:
    print(file, end="")
    input_file = os.path.join(start_dir, file)
    output_file = os.path.join(end_dir, file).replace(".DDS", ".png")
    convert_dds_to_png(input_file, output_file)
    print(" - Done")
