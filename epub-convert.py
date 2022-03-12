#!/usr/bin/env python3

#Convert EPUB files to either single HTML or text files.
#They can then be read on refreshable Braille displays, such as the Brailliant series from HumanWare or the Braille Edge by Hims.
#Also works with the Victor Reader Trek/Stream by Humanware.
#Requires pypandoc (shoutouts to @TheQuinbox on twitter!)
#Try pip3 install pypandoc


#usage: epub-convert.py [-i input_dir] [-o output_dir] [-T]

import argparse
import functools
import os
from pathlib import Path
import pypandoc
import sys
import time

@functools.total_ordering
class Ebook:
    """Represents a book to be converted.
    
    Rich comparison will order on the file size.
    bool determines whether this book should be converted.
    """
    def __init__(self, book_path: Path, output_ext: str, input_base: Path, output_base: Path):
        self.book_path=book_path.resolve() # basically absolute
        # self.dest_path is the output filename, pathlib makes this elegant.
        self.dest_path=output_base.resolve()/self.book_path.relative_to(input_base.resolve()).with_suffix('.'+output_ext)
        self.in_stat=self.book_path.stat()
        if self.dest_path.exists(): self.out_stat=self.dest_path.stat()
        else: self.out_stat=None
    
    def __eq__(self, other):
        return self.in_stat.st_size==other.in_stat.st_size
    
    def __lt__(self, other):
        return self.in_stat.st_size<other.in_stat.st_size
    
    def __bool__(self):
        """
        Should this book be converted?
        True if destination does not exist or if source modtime is newer.
        """
        if self.out_stat is not None and self.in_stat.st_mtime<self.out_stat.st_mtime: return False
        else: return True
        

# Increment these on successful or failed conversion respectively.
progress=0
errors=0
input_dir=Path('.')
file_format='html'
output_dir=input_dir/'html conversions'
#Since we change directories later, keep track of the current directory now so the output dir is relative to *that* instead of the input directory.
basedir=Path.cwd().resolve()
parser = argparse.ArgumentParser(description='Convert a directory of EPUB files into single HTML or text files')
parser.add_argument('-t', '--text', help='Output text files instead of HTML', action='store_true')
parser.add_argument('-i', '--input', help='Directory to search for epub files (default .)')
parser.add_argument('-o', '--output', help='output directory (default: ./[html|txt] conversions)')
args = parser.parse_args()

if args.input:
    input_dir = Path(args.input)
if args.output:
    output_dir = basedir/args.output
if args.text:
    if not args.output:
        output_dir = basedir/'txt conversions'
    file_format= 'txt'
    print('Converting to text files')
input_dir=input_dir.resolve()
if not output_dir.exists(): output_dir.mkdir(parents=True, exist_ok=True)
output_dir=output_dir.resolve()


def epubs(base: Path, exclude: Path=None):
    """
    Recursively yields all epub files to be converted as Path instances
    
    The only filtering done here is to avoid traversing into the directory given by exclude
    """
    for item in base.iterdir():
        if item.is_dir():
            if exclude is not None and item.is_relative_to(exclude):
                continue
            else:
                yield from epubs(item, exclude)
        elif item.is_file() and item.suffix.lower()=='.epub':
            yield item

epub_files = []
for i in epubs(input_dir, output_dir):
    book=Ebook(i, file_format, input_dir, output_dir)
    if bool(book): epub_files.append(book)
epub_files.sort() # smallest first
file_count=len(epub_files)
if file_count<=0:
    print('All conversions are up to date.')
    sys.exit()

print(f'Have {file_count} to convert')
for book in epub_files:
    file=book.book_path # easier access
    output_file=book.dest_path
    # .parent is used because mkdir needs the path to be a directory
    output_file.parent.mkdir(parents=True, exist_ok=True)
    # some things to print
    pretty_input_file=str(file.relative_to(input_dir))
    pretty_output_file=str(output_dir.parts[-1]/output_file.relative_to(output_dir))
    print(f'{progress+1}/{file_count}: Converting {pretty_input_file} to {pretty_output_file}')
    conversion_result = None
    convert_start = time.perf_counter_ns()
    #If pandoc barfs on conversion, warn the user and skip to the next file.
    try:
        #This next bit of silliness is because pandoc uses 'plain' instead of 'txt' as a format name.
        if args.text:
            conversion_result = pypandoc.convert_file(str(file), 'plain', outputfile=str(output_file), extra_args=['-s'])
        else:
            conversion_result = pypandoc.convert_file(str(file), file_format, outputfile=str(output_file), extra_args=['-s'])
        assert(conversion_result == '')
    except RuntimeError as e:
        print(f'Error converting file {file}; output is likely malformed or corrupt:\n{e.args}', file=sys.stderr)
        errors+=1
    convert_end = time.perf_counter_ns()
    print(f'Conversion took {(convert_end - convert_start)/1000000000} seconds', file=sys.stderr)
    progress+=1

if file_count>0:
    print(f'{progress} converted, {errors} failed.')

