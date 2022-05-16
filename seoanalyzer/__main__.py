#!/usr/bin/env python3

import argparse
import inspect
import json
import os

from jinja2 import Environment
from jinja2 import FileSystemLoader
from seoanalyzer import analyze


def main(args=None):
    if not args:
        module_path = os.path.dirname(inspect.getfile(analyze))

        arg_parser = argparse.ArgumentParser()

        arg_parser.add_argument('site', help='https://ananas.rs/')
        arg_parser.add_argument('-s', '--sitemap', help='https://ananas.rs/robots.txt')
        arg_parser.add_argument('-f', '--output-format', help='json', choices=['json', 'html', ],
                                default='json')

        args = arg_parser.parse_args()

        output = analyze(args.site, args.sitemap)

        if args.output_format == 'html':
            from jinja2 import Environment
            from jinja2 import FileSystemLoader

            env = Environment(loader=FileSystemLoader(os.path.join(module_path, 'templates')))
            template = env.get_template('index.html')
            output_from_parsed_template = template.render(result=output)
            print(output_from_parsed_template)
        elif args.output_format == 'json':
            print(json.dumps(output, indent=4, separators=(',', ': ')))
    else:
        exit(1)

if __name__ == "__main__":
    main()
