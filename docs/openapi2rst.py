# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import os
import codecs
import inspect

from jinja2 import Environment, FileSystemLoader, TemplateError
from swg2rst.utils import rst
from swg2rst.converter_exceptions import ConverterError

# note: look into conf.py to see how this is used!

# we "forked" swagger2rst because we wanted to keep the order of definitions
# from the openapi.rst spec file.
# details: https://github.com/Arello-Mobile/swagger2rst/issues/5


def prepare_template(path, module):
    # helper to load jinja2 templates
    jinja_env = Environment(lstrip_blocks=True, trim_blocks=True)

    for name, function in inspect.getmembers(module, inspect.isfunction):
        jinja_env.filters[name] = function

    jinja_env.loader = FileSystemLoader(os.path.dirname(path))
    template = jinja_env.get_template(os.path.basename(path))

    return template


inline = False
examples = None
template = prepare_template('openapi_templates/main.rst', rst)


def generate_docs(packages):
    for package in packages:
        try:
            pkg = __import__(package)  # dynamically import package
            doc = pkg.read_openapi()
            swagger_doc = rst.SwaggerObject(doc, examples=examples)
            rst_doc = template.render(doc=swagger_doc, inline=inline)
        except (ConverterError, TemplateError, ImportError) as err:
            status = err
            if isinstance(err, TemplateError):
                status = 'Template Error: {}'.format(err)
            print(status)
            #sys.exit(status)
            continue

        output = '%s_config.rst' % package
        with codecs.open(output, mode='w', encoding='utf-8') as f:
            f.write(rst_doc)
