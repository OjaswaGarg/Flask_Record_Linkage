# %%
import os
from os import walk
def remove_input():
    for (dirpath, dirnames, filenames) in walk(os.path.abspath('input')):
        for f in filenames:
            f1=os.path.join('input',f)
            os.remove(f1)

def remove_output():
    for (dirpath, dirnames, filenames) in walk(os.path.abspath('output')):
        for f in filenames:
            f1=os.path.join('output',f)
            os.remove(f1)
# %%
