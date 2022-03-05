#!/usr/bin/env python3

#Convert EPUB files to either single HTML or text files.
#They can then be read on refreshable Braille displays, such as the Brailliant series from HumanWare orr the Braille Edge by Hims.
#Also works with the Victor Reader Trek/Stream by Humanware.
#Requires pypandoc (shoutouts to @TheQuinbox on twitter!)
#Try pip3 install pypandoc


#usage: epub-convert.py [-i input_dir] [-o output_dir] [-T]

import os
import os.path
import argparse
import pathlib
import pypandoc
import time
import sys

# Increment these on successful or failed conversion respectively.
progress=0
errors=0
input_dir='.'
file_format='html'
output_dir = os.path.join('.', 'html conversions')
#Since we change directories later, keep track of the current directory now so the output dir is relative to *that* instead of the input directory.
basedir=os.getcwd()
parser = argparse.ArgumentParser(description='Convert a directory of EPUB files into single HTML or text files')
parser.add_argument('-t', '--text', help='Output text files instead of HTML', action='store_true')
parser.add_argument('-i', '--input', help='Directory to search for epub files (default .)')
parser.add_argument('-o', '--output', help='output directory (default: ./[html|txt] conversions)')
args = parser.parse_args()

if args.input:
    input_dir = args.input
if args.output:
    output_dir = os.path.join(basedir, args.output)
if args.text:
    if not args.output:
        output_dir = os.path.join('.', 'txt conversions')
    file_format= 'txt'
    print('Converting to text files')

os.chdir(input_dir)
epub_files = list(pathlib.Path('.').rglob('*.[eE][pP][uU][bB]'))
file_count=len(epub_files)
print(f'Found {file_count} to convert\n')

#FIXME: Skip files that have already been converted, check file modification times

for file in epub_files:
    output_name = os.path.join(output_dir, file.__str__()[:-4] + file_format)
    os.makedirs(os.path.dirname(output_name), exist_ok=True)
    print(f'{progress+1}/{file_count}: Converting {file} to {output_name}')
    conversion_result = None
    convert_start = time.perf_counter_ns()
    #If pandoc barfs on conversion, warn the user and skip to the next file.
    try:
        #This next bit of silliness is because pandoc uses 'plain' instead of 'txt' as a format name.
        if args.text:
            conversion_result = pypandoc.convert_file(file.__str__(), 'plain', outputfile=output_name, extra_args=['-s'])
        else:
            conversion_result = pypandoc.convert_file(file.__str__(), file_format, outputfile=output_name, extra_args=['-s'])
        assert(conversion_result == '')
    except RuntimeError as e:
        print(f'Error converting file {file}; output is likely malformed or corrupt:\n{e.args}', file=sys.stderr)
        errors+=1
    convert_end = time.perf_counter_ns()
    print(f'Conversion took {(convert_end - convert_start)/1000000000} seconds', file=sys.stderr)
    progress+=1

if file_count>0:
    print(f'{progress} converted, {errors} failed.')

