import argparse
import inspect
import json
import os
import site

from jinja2 import Environment
from jinja2 import FileSystemLoader
from seoanalyzer import analyze


module_path = os.path.dirname(inspect.getfile(analyze))

arg_parser = argparse.ArgumentParser()

arg_parser.add_argument('site', help='http://ananas.rs/')
arg_parser.add_argument('-s', '--sitemap', help='http://ananas.rs/robots/txt')
arg_parser.add_argument('-f', '--output-format', help='json', choices=['json', 'html', ],
                        default='json')
arg_parser.add_argument('-d', '--disk', help='save to disk', choices=['y', 'n', ], default='y')

args = arg_parser.parse_args()
print("Echo:", args.echo)

output = analyze(args.site, args.sitemap)

if args.output_format == 'html':
    from jinja2 import Environment
    from jinja2 import FileSystemLoader

    env = Environment(loader=FileSystemLoader(os.path.join(module_path, 'templates')))
    template = env.get_template('index.html')
    output_from_parsed_template = template.render(result=output)
    if args.disk == 'y':
        with open("test.html", "w", encoding='utf-8') as text_file:
            text_file.write(output_from_parsed_template)
    else:
        print(output_from_parsed_template)
elif args.output_format == 'json':
    if args.disk == 'y':
        with open("test.json", "w", encoding='utf-8') as text_file:
            text_file.write(json.dumps(output, indent=4, separators=(',', ': ')))
    else:
        print(json.dumps(output, indent=4, separators=(',', ': ')))
