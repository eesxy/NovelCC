import argparse
import os
import re
import shutil
import zipfile

import opencc


def extract_zip(zip_file: str, temp_folder: str):
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(temp_folder)


def compress_zip(zip_file: str, temp_folder: str):
    with zipfile.ZipFile(zip_file, 'w') as z:
        for root, dirs, files in os.walk(temp_folder):
            for file in files:
                z.write(os.path.join(root, file),
                        os.path.relpath(os.path.join(root, file), temp_folder))


def convert_t2s(folder: str, converter: opencc.OpenCC):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xhtml'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
                    f.write(converter.convert(content))


def convert_v2h(folder: str):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.xhtml'):
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # convert "vrtl" or "vltr" to "hltr"
                    content = re.sub(r'(vrtl)|(vltr)', 'hltr', content)
                with open(os.path.join(root, file), 'w', encoding='utf-8') as f:
                    f.write(content)


def arg_parser():
    parser = argparse.ArgumentParser(
        description='Convert epub files from traditional to simplified Chinese')
    parser.add_argument('--folder', type=str, default='./novel', help='Folder containing epub files')
    parser.add_argument('--temp_folder', type=str, default='./temp',
                        help='Temp folder for extracting epub files')
    return parser.parse_args()


def main():
    args = arg_parser()
    folder = args.folder
    temp_folder = args.temp_folder
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)
    converter = opencc.OpenCC('t2s.json')
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.epub'):
                extract_zip(os.path.join(root, file), temp_folder)
                convert_t2s(temp_folder, converter)
                convert_v2h(temp_folder)
                compress_zip(os.path.join(root, file), temp_folder)
                print('Converted', file)
                # clean up temp folder
                shutil.rmtree(temp_folder)
    print('All done')


if __name__ == '__main__':
    main()
