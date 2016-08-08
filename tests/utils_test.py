import os
from StringIO import StringIO

from scaffolder import utils

def test_usage():

    out = StringIO()
    utils.usage(out=out)
    output = out.getvalue().strip()

    assert output == 'Usage: scaffolder SCHEMA_FILE [TARGET]'
    assert type(output) == str

def test_clean():

    lines = [
        '\n',
        '# this is a comment\n',
        '   dir2/\n',
        '       one two three\n',
    ]
    expected_lines = [
        '   dir2/',
        '       one two three',
    ]
    result = utils.clean(lines)

    assert result == expected_lines

def test_is_empty():

    empty = ''
    spaces = '   '
    newline = '\n'
    newlines = '\n\n\n'
    comment = '#comment\n'
    dir_name = 'dir3/'

    assert utils.is_empty(empty) is True
    assert utils.is_empty(spaces) is True
    assert utils.is_empty(newline) is True
    assert utils.is_empty(newlines) is True
    assert utils.is_empty(comment) is False
    assert utils.is_empty(dir_name) is False

def test_is_comment():

    comment = '# this is a comment'
    comment_multiple_pounds = '## this is a comment'
    dir_name = 'dir2/'
    empty_space = ''

    assert utils.is_comment(comment) is True
    assert utils.is_comment(comment_multiple_pounds) is True
    assert utils.is_comment(dir_name) is False
    assert utils.is_comment(empty_space) is False 

def test_is_dir():

    dir_name = 'dir2/'
    not_dir_name = 'dir'
    empty_space = ''

    assert utils.is_dir(dir_name) is True 
    assert utils.is_dir(not_dir_name) is False 
    assert utils.is_dir(empty_space) is False 


def test_is_multiple_of_indent():

    #args: this_indent, global indent
    good_case_a = (0,4)
    good_case_b = (4,4)
    good_case_c = (8,4)
    bad_case_a = (1,3)
    bad_case_b = (4,3)

    assert utils.is_multiple_of_indent(*good_case_a) is True
    assert utils.is_multiple_of_indent(*good_case_b) is True
    assert utils.is_multiple_of_indent(*good_case_c) is True
    assert utils.is_multiple_of_indent(*bad_case_a) is False
    assert utils.is_multiple_of_indent(*bad_case_b) is False

def test_parse_indent():

    indent_a = ''
    indent_b = '  dir1/'
    indent_c = '    dir1/'

    assert utils.parse_indent(indent_a) == 0
    assert utils.parse_indent(indent_b) == 2
    assert utils.parse_indent(indent_c) == 4

def test_get_indent():

    case_a = ('    dir1/', 4)
    case_b = ('        dir1/', 4)
    case_c = ('file1.txt', 4)

    assert utils.get_indent(*case_a) == 1
    assert utils.get_indent(*case_b) == 2
    assert utils.get_indent(*case_c) == 0

def test_get_dirname():

    assert utils.get_dirname('dir2//') == 'dir2'
    assert utils.get_dirname('dir2/') == 'dir2'
    assert utils.get_dirname('dir2') == 'dir2'
    assert utils.get_dirname('') == ''

def test_get_filename():

    assert utils.get_filename('dir2') == 'dir2'
    assert utils.get_filename('  dir2  ') == 'dir2'

def test_handle_args():

    args = ('scaffolder', 'schema.txt')
    schema, output_dir = utils.handle_args(args)

    assert type(schema) == str
    assert output_dir.startswith('SCAFFOLDER_OUTPUT') 

    args = ('scaffolder', 'schema.txt', 'output_dir')
    schema, output_dir = utils.handle_args(args)

    assert type(schema) == str
    assert output_dir.startswith('output_dir') 
