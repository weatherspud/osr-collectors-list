#!/usr/bin/env python3
import csv
import os
import sys

PRODUCT_TYPES = ['rulebook', 'supplement', 'adventure', 'setting', 'periodical']
CATEGORIES = ['reprint', 'proto-osr', 'osr']
HEADER = ['product_type', 'title', 'publisher', 'year', 'product_code', 'category']


def checklist(paths, fout):
    writer = csv.writer(fout)
    writer.writerow(['subcategory'] + HEADER)
    for path in sorted(paths):
        category = os.path.basename(os.path.dirname(path))
        try:
            with open(path) as f:
                header = None
                for row in csv.reader(f):
                    if header:
                        if 'product_type' in header and row[header.index('product_type')]:
                            product_type = row[header.index('product_type')]
                            if product_type not in PRODUCT_TYPES:
                                raise Exception('{}: not a product type {}'.format(path, product_type))
                        if 'category' in header and row[header.index('category')]:
                            category = row[header.index('category')]
                            if category not in CATEGORIES:
                                raise Exception('{}: not a category {}'.format(path, category))
                        outrow = [row[header.index(h)] if h in header else ''
                                  for h
                                  in HEADER]
                        outrow.insert(0, category)
                        writer.writerow(outrow)
                    else:
                        header = [o.lstrip('\ufeff') for o in row]
                        assert('title' in header)
        except FileNotFoundError:
            sys.stderr.write(f'WARNING not found: {path}\n')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception('USAGE: checklist.py PATHS')
    checklist(sys.argv[1:], sys.stdout)
