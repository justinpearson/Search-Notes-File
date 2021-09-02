# dodo.py: A generalized makefile-like python script used by 
# the doit tool (pip3 install doit).

# Goal: monitor my test files and re-run the tests whenever
# I save the file. Make a success or failure noise.

# Usage: $ doit auto
# (then edit & save any of the files to watch)
# doit should re-run the tests with pytest, and make a happy/sad noise.

# One-time run: $ doit forget test; doit run test (bc of def task_test())

# Notes:
# 

from subprocess import call
import os, sys, pathlib

IGNORE_FILES = ['dodo.py','__init__.py']
FILES_TO_WATCH = [ p for p in pathlib.Path('.').glob('*.py') if p.name not in IGNORE_FILES ]
base = pathlib.Path.home().joinpath('Utilities','doit')
sounds = { k: base / v for k,v in { 'yay': 'Tink-trim.m4a', 'no': 'Sosumi-trim.m4a' }.items() }

# Check that the happy/sad sound files exist.
for f in sounds.values():
    if not f.is_file():
        print(f'Sound file not found: {f}')
        exit()

def task_test():
    'Monitor my test files and re-run the tests whenever I save the file. Make a success or failure noise.'

    def f():
        print(f'Running pytest! pwd: {os.getcwd()}')
        r = call(['pytest'])
        call([
            'afplay',
            sounds['yay'] if r==0 else sounds['no']
            ])

    return { 
        'file_dep': FILES_TO_WATCH,
        'actions': [f],
        'verbosity': 2
    }
