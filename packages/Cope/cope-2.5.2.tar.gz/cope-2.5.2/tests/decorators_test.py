from os.path import join, dirname; import sys; sys.path.append(join(dirname( __file__ ), '..'))
from Cope import *

def test_todo():
    assert False, 'TODO: toto tests'

    todo('testing todo')
    out, err = capfd.readouterr()
    assert out == "Hello World!"

    return

    todo('testing todo 2', False)

    @todo
    def unfinishedFunc():
        print("this func is unfin")

    try:
        unfinishedFunc()
    except NotImplementedError:
        print("func decorator test worked!")
    else:
        print("func decorator test failed.")

    @todo(blocking=False)
    def unfinishedFunc2():
        print("this non Blocking func is unfin")

    unfinishedFunc2()

    @todo
    class unfinishedClass:
        def __init__(self):
            print('this class is unfin')

    try:
        x = unfinishedClass()
    except NotImplementedError:
        print("class decorator test worked!")
    else:
        print("class decorator test failed.")

def test_confidence():
    assert False, 'TODO: confidence tests'

    @confidence(29)
    def testFunc(funcArg1, funcArg2, funcKwArg='funcKwArg'):
        debug(funcArg1)
        debug(funcArg2)
        debug(funcKwArg)

    @confident(102)
    def testFunc2(funcArg1, funcArg2, funcKwArg='funcKwArg'):
        debug(funcArg1)
        debug(funcArg2)
        debug(funcKwArg)

    @confident(16)
    def testFunc3(funcArg1, funcArg2, funcKwArg='funcKwArg'):
        debug(funcArg1)
        debug(funcArg2)
        debug(funcKwArg)

    @confidence('super')
    def testFunc4(): pass

    @confidence('not very')
    def testFunc5(): pass

    @confidence('none')
    def testFunc6(): pass

    @confidence('low')
    def testFunc7(): pass

    @confidence('Sorta')
    def testFunc8(): pass

    @confidence('asfgs')
    def testFunc9(): pass

    @confidence('confident', 100)
    def testFunc10(): pass

    @confidence('not confident', 0)
    def testFunc11(): pass

    try:
        testFunc2("calledArg1", 'calledArg2', funcKwArg='calledKwArg')
    except TypeError:
        print('testFunc2 worked')

    testFunc( "calledArg1", 'calledArg2', funcKwArg='calledKwArg')
    testFunc3("calledArg1", 'calledArg2', funcKwArg='calledKwArg')
    testFunc4()
    testFunc5()
    testFunc6()
    testFunc7()
    testFunc8()
    testFunc10()
    testFunc11()
    try:
        testFunc9()
    except TypeError:
        print('testFunc9 worked')

todo
confidence
def test_depricated():
    assert False, 'TODO: @depricated tests'

def test_reprise():
    assert False, 'TODO: @reprise tests'
