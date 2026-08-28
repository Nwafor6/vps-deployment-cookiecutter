import re
import sys


MODULE_REGEX = r'^[_a-zA-Z][_a-zA-Z0-9]+$'

project_slug = '{{ cookiecutter.project_slug }}'

# Ensure project_slug is lowercase
if project_slug != project_slug.lower():
    print('ERROR: The project slug must be all lowercase')
    sys.exit(1)

if not re.match(MODULE_REGEX, project_slug.replace('-', '_')):
    print(f'ERROR: The project slug ({project_slug}) is not a valid Python module name. Please do not use a - and use _ instead')

    #Exit to cancel project
    sys.exit(1)

