from Cope.debugging import *
# from Cope.debugging import Debug as debug
import sys
from os.path import join, dirname
import sys
sys.path.append(join(dirname( __file__ ), '..'))
from Cope.debugging import *
from Cope.colors import parse_color

def test_debug():
    assert False, 'TODO: debug tests'
    debug('test')


    @debug
    def test():
        print('test called')

    test()

    @debug
    class Test:
        def __init__(self):
            print('Test initialized')

    Test()

    def test2():
        print('test2 called')

    debug(test2)
    debug(1)
    debug()
    var = 6
    debug(var)


def test_printArgs():
    assert False, 'TODO: printArgs tests'

def test_get_metadata():
    assert False, 'TODO: get_metadata tests'

def test_prettify():
    assert False, 'TODO: prettify tests'

def test_get_full_typename():
    assert False, 'TODO: get_full_typename tests'

def test_print_debug_count():
    assert False, 'TODO: print_debug_count tests'

def test_get_varname():
    assert False, 'TODO: get_varname tests'

def test_get_adjusted_filename():
    assert False, 'TODO: get_adjusted_filename tests'

def test_get_context():
    assert False, 'TODO: get_context tests'

def test_print_stack_trace():
    assert False, 'TODO: print_stack_trace tests'

def test_called_as_decorator():
    assert False, 'TODO: called_as_decorator tests'

def test_print_context():
    assert False, 'TODO: print_context tests'

def test_debug():
    assert False, 'TODO: review debug tests'

    #%%
    var = 6
    debug(var)
    #%%

    # def test_getMetaData():
    # print('testing get_metadata')
    # print(get_metadata())

    # def test__debugGetLink():
    # print('testing get_link')
    # print(get_link())

    # def test__debugGetListStr():
    # prettify([1, 2, 3])

    # def test__debugGetTypename():
    # get_full_typename('test string literal')

    # def test__debugPrintLink():
    # print_link('testFile.py', 42)

    # def test__printDebugCount():
    # print_debug_count()

    # def test__debugManualGetVarName():
    # get_varname_manually(var)

    # def test__debugGetVarName():
    # get_varname(var)

    # def test__debugGetAdjustedFilename():
    # get_adjusted_filename('testFile.py')

    # def test__debugGetContext():
    # getContext()

    # def test__debugPrintStackTrace():
    # printStackTrace()

    # def test__debugBeingUsedAsDecorator():
    # called_as_decorator('testFunc')

    # def test_printContext():
    # print_context()

    # def test_debug():
    debug()
    a = 6
    s = 'test'
    j = None
    def testFunc():
        print('testFunc called')

    debug(a)
    debug(a, 'apple')

    debug("test3")
    debug(s)
    debug(6)
    debug(None)

    debug(j)
    debug()

    debug(testFunc)

    foo = debug(a)
    debug(foo)

    debug(parseColorParams((5, 5, 5)))

    debug(SyntaxError('Not an error'))
    try:
        debug(SyntaxError('Not an error'), raiseError=True)
    except SyntaxError:
        print('SyntaxError debug test passed!')
    else:
        print('SyntaxError debug test failed.')

    debug(UserWarning('Not a warning'))
    try:
        debug(UserWarning('Not a warning'), raiseError=True)
    except UserWarning:
        print('UserWarning debug test passed!')
    else:
        print('UserWarning debug test failed.')

    @debug
    def testFunc2():
        print('testFunc2 (decorator test) called')

    debug()

    testFunc2()

    debug(None)

    TUPLE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    LIST  = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    DICT  = {'a':1, 'b':2, 'c': 3}
    TYPE_LIST = ['a', 2, 7.4, 3]
    TYPE_TUPLE = ('a', 2, 7.4, 3)

    debug([0, 1, 2, 3, 4, 5, 6, 7, 8, 9], raiseError=True)
    debug((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), raiseError=True)
    debug({'a':1, 'b':2, 'c': 3}, raiseError=True)
    debug(['a', 2, 7.4, 3], raiseError=True)
    debug(('a', 2, 7.4, 3), raiseError=True)
    debug()
    debug(TUPLE, raiseError=True)
    debug(LIST, raiseError=True)
    debug(DICT, raiseError=True)
    debug(TYPE_LIST, raiseError=True)
    debug(TYPE_TUPLE, raiseError=True)

    debug(())
    debug([])
    debug({})
    debug(set())


    # test()

    # CopeConfig.display_file=False
    CopeConfig.display_func=False
    # CopeConfig.display_path=True
    # CopeConfig.root_dir = './.pytest_cache'

    debug()

    # test()
