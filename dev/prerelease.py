import sys
import os
import importlib.util

if sys.version_info.major != 3 and sys.version_info.minor != 10:
	raise ValueError("""This prerelease script will only run on Python 3.10.
Some parts of a library change the last few decimals numbers between releases,
and other parts only have obsolete dependencies i.e. pint on Python 2.
For that reason, while the pytest test suite runs everywhere,
the notebooks and doctests only run on one paltform.""")


from datetime import datetime
import os, sys
def set_file_modification_time(filename, mtime):
    atime = os.stat(filename).st_atime
    os.utime(filename, times=(atime, mtime.timestamp()))
    
now = datetime.now()

paths = ['..']

for p in paths:
    for (dirpath, dirnames, filenames) in os.walk(p):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            set_file_modification_time(full_path, now)


import ht
main_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
test_dir = os.path.join(main_dir, 'tests')
os.chdir(test_dir)

#mod_spec = importlib.util.spec_from_file_location("make_test_stubs", os.path.join(test_dir, "make_test_stubs.py"))
#make_test_stubs = importlib.util.module_from_spec(mod_spec)
#mod_spec.loader.exec_module(make_test_stubs)

import pytest
os.chdir(main_dir)
pytest.main(["--doctest-glob='*.rst'", "--doctest-modules", "--nbval", "-n", "3", "--dist", "loadscope", "-v"])
