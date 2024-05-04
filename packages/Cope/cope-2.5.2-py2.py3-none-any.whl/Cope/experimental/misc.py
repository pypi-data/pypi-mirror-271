# from .decorators import todo, confidence
from .imports import dependsOnPackage
from ..debugging import get_varname, called_as_decorator, debug, get_metadata
# from .colors import ERROR
import re
import subprocess
from os.path import join
from random import randint
import sys
# from math import floor

# TODO: I think this broke
def replace_line(line, offset=0, keepTabs=True, convertTabs=True, calls=0):
    """ Replaces the line of code this is called from with the give line parameter.
        This is a very bad idea and you should not use it
        Automatically adds a newline to the end, but does not automatically add tabs.
    """
    meta = get_metadata(calls=calls+2)

    with open(meta.filename, 'r') as f:
        file = f.readlines()

    # Not really sure of the reason for the -1.
    if file[meta.lineno-1] == meta.code_context[0]:
        if keepTabs:
            tabs = re.match(r'([\t ]+)', file[meta.lineno-1 + offset])
            if tabs:
                line = tabs.group(1) + line

        if convertTabs:
            line = line.replace('\t', '    ')

        file[meta.lineno-1 + offset] = line + '\n'

    else:
        debug(f"Error: lines don't match, not replacing line.\n\tMetadata: \"{meta.code_context}\"\n\tFile: \"{file[meta.lineno-1]}\"", clr=-1)
        return

    with open(meta.filename, 'w') as f:
        f.writelines(file)

# TODO Unfinished
def comment(comment='', line_limit=80, char='=', start='', end='#', capitalize=False):
    """ Replaces the call with a nicely formatted comment line next time the line is run
        NOTE: This is a terrible, terrible function that you should NOT use.
                I'm pretty confident it won't overwrite your source code.
                And it's surprisingly useful.
                But still, use at your own risk.
    """
    if capitalize:
        comment = comment.upper()

    meta = get_metadata(calls=2)

    with open(meta.filename, 'r') as f:
        file = f.readlines()

    # Not really sure of the reason for the -1.
    if file[meta.lineno-1] == meta.code_context[0]:
        tabs = re.match(r'([\t ]+)', file[meta.lineno-1])
        if tabs is None:
            tabs = ''
        else:
            tabs = tabs.group(1)

        if not len(char):
            replace_line('# ' + comment, calls=1)
            return
        if not len(start):
            start = char
        if not len(end):
            end = char

        # Calculate half the distance - comment
        half = (((line_limit // len(char)) - len(comment) - (len(tabs) // 2) - 1 - (2 if len(comment) else 0) - len(end)) // 2) - 1
        # We want the comment to be nicely seperated
        seperateChar = ' ' if len(comment) else ''
        # Add them all together
        c = '#' + start + (char * half) + seperateChar + comment + seperateChar + (char * half)
        # If it doesn't quite reach the max number of characters, make sure it does
        c += ((line_limit - len(c) - len(end)) // len(char)) * char
        c = tabs + c + end
        file[meta.lineno-1] = c + '\n'

    else:
        debug(f"Error: lines don't match, not replacing line.\n\tMetadata: \"{meta.code_context}\"\n\tFile: \"{file[meta.lineno-1]}\"", clr=-1)
        return

    with open(meta.filename, 'w') as f:
        f.writelines(file)


# @todo('Make this use piping and return the command output', False)
def runCmd(args):
    """ Run a command and terminate if it fails. """
    try:
        ec = subprocess.call(' '.join(args), shell=True)
    except OSError as e:
        print("Execution failed:", e, file=sys.stderr)
        ec = 1
    if ec:
        sys.exit(ec)

def center(string):
    """ Centers a string for printing in the terminal """
    from os import get_terminal_size
    for _ in range(int((get_terminal_size().columns - len(string)) / 2)): string = ' ' + string
    return string


# TODO: Failing
def insert_newlines(string:str, max_line_length:int) -> str:
    """ Inserts newline characters into `string` in order to keep `string` under `max_line_length`
        characters long, while not inserting a newline in the middle of a word
    """
    # split the string into a list of words
    words = string.split()
    # initialize the result as an empty string
    result = ""
    # initialize the current line as an empty string
    current_line = words[0]
    # iterate over the words in the list
    for word in words[1:]:
        # if the current line plus the next word would exceed the maximum line length,
        # add a newline character to the result and reset the current line
        if len(current_line) + 1 + len(word) > max_line_length:
            result += current_line + "\n"
            current_line = word
        else:
            # add the word to the current line and a space character after it
            current_line += " " + word
    return result

def assertValue(param, *values, blocking=True):
    paramName = get_varname(param)
    if not called_as_decorator('assertValue'):
        if param not in values:
            err = ValueError(f"Invalid value for {paramName}, must be one of: {values}")
            if blocking:
                raise err
            else:
                debug(err)
    else:
        print('TODO: AssertValue usage as a decorator')
