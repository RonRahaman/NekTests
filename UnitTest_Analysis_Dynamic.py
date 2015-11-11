#! /usr/bin/python
# Python module to run top-down tests for Nek

import collections
import re
import unittest

###############################################################################

class RunTestBase(unittest.TestCase):

    logfile = ""
    exampleName = ""
    missingTests = {}
    foundTests = {}
    passedTests = {}

    @classmethod
    def setUpClass(cls):
        try:
            # Parse to log file.  If a test is found, pop it off missingTests and push it onto foundTests
            with open(cls.logfile, 'r') as fd:
                for line in fd:
                    # Can't use dictionary iterator, since missingTests can change during loop.
                    # Need to iterate over list returned by missngTests.keys()
                    for testName in cls.missingTests.keys():
                        if testName in line:
                            try:
                                col = -cls.missingTests[testName]['col']
                                testVal = float(line.split()[col])
                            except (ValueError,IndexError) :
                                pass
                            else:
                                cls.foundTests[testName] = cls.missingTests.pop(testName)
                                cls.foundTests[testName]['testVal'] = testVal
        except IOError:
            # If an IOError is caught, all the tests will stay in missingTests
            print("[%s]...Sorry, I must skip this test."%cls.exampleName)
            print("[%s]...The logfile is missing or doesn't have the correct name..."%cls.exampleName)

    @classmethod
    def tearDownClass(cls):
        if len(cls.missingTests) > 0:
            # Print all the tests that were not found
            print("[%s]...I couldn't find all the requested value in the log file..."%cls.exampleName)
            testList = ", ".join(cls.missingTests)
            print("[%s]...%s were not found..."%(cls.exampleName,testList))
        if len(cls.passedTests) < len(cls.foundTests) or len(cls.missingTests) > 0:
            print("%s : F "%cls.exampleName)
        else :
            print("%s : ."%cls.exampleName)


def RunTestFactory(exampleName, logfile, listOfVals):

    # Convenient data structure
    dictOfVals = collections.OrderedDict(
        [(testName, {'target': target, 'tolerance': tolerance, 'col': col})
         for (testName, target, tolerance, col) in listOfVals ] )

    # Class attributes
    attr = dict(logfile=logfile,
                exampleName=exampleName,
                missingTests=dictOfVals,
                foundTests={},
                passedTests={})

    # Add a test function for each test
    for (i, testName) in enumerate(dictOfVals):

        def testFunc(self, testName=testName):
            cls = self.__class__
            self.assertIn(testName, cls.foundTests)
            print("[%s] %s : %s" %
                  (cls.exampleName, testName, cls.foundTests[testName]['testVal']))
            self.assertLess(abs(cls.foundTests[testName]['testVal'] - cls.foundTests[testName]['target']),
                            cls.foundTests[testName]['tolerance'])
            cls.passedTests[testName] = cls.foundTests[testName]

        validName = re.sub(r'[_\W]+', '_', 'test_%s_%02d' % (testName, i))
        attr[validName] = testFunc

    # Get a new subclass of RunTestBase
    validName = re.sub(r'[_\W]+', '_', 'NekTest_%s' % exampleName)
    return type(validName, (RunTestBase,), attr)

def Run(exampleName, logfile, listOfVals):
    global suite
    cls = RunTestFactory(exampleName, logfile, listOfVals)
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase(cls))

class FindPhraseBase(unittest.TestCase):

    exampleName = ""
    logfile = ""
    keyword = ""
    foundPhrases = []
    raisedIOError = False

    @classmethod
    def setUpClass(cls):
        try:
            with open(cls.logfile, 'r') as fd:
                for line in fd:
                    if cls.keyword in line:
                        cls.foundPhrases.append(cls.keyword)
                        break
        except IOError :
            cls.raisedIOError = True


    def test_findPhrase(self):
        cls = self.__class__
        self.assertIn(cls.keyword,cls.foundPhrases)

    @classmethod
    def tearDownClass(cls):
        if cls.raisedIOError:
            print("[%s]...Sorry, I must skip this test."%cls.exampleName)
            print("[%s]...The logfile is missing or doesn't have the correct name..."%cls.exampleName)
            print("%s : F "%cls.exampleName) # not in Analysis.py
        else:
            print("[%s] : %s"%(cls.exampleName, cls.keyword))
            if len(cls.foundPhrases) == 0:
                print("[%s]...I couldn't find '%s' in the logfile..."%(cls.exampleName,cls.keyword))
                print("%s : F "%cls.exampleName)
            else:
                print("%s : ."%cls.exampleName)                 #prints the result

def FindPhraseFactory(exampleName, logfile, keyword) :

    validName = re.sub(r'[_\W]+', '_', 'NekTest_%s' % exampleName)
    attr = dict(exampleName=exampleName,
                logfile=logfile,
                keyword=keyword,
                foundPhrases=[],
                raisedIOError=False)
    return type(validName, (FindPhraseBase,), attr)

def FindPhrase(exampleName, logfile, keyword):
    global suite
    cls = FindPhraseFactory(exampleName, logfile, keyword)
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase(cls))

class DFdPhraseBase(unittest.TestCase):

    exampleName = ""
    logfile = ""
    keyword = ""
    foundPhrases = []
    raisedIOError = False

    @classmethod
    def setUpClass(cls):
        try:
            with open(cls.logfile, 'r') as fd:
                for line in fd:
                    if cls.keyword in line:
                        cls.foundPhrases.append(cls.keyword)
                        break
        except IOError :
            cls.raisedIOError = True


    def test_DFdPhrase(self):
        cls = self.__class__
        self.assertNotIn(cls.keyword,cls.foundPhrases)

    @classmethod
    def tearDownClass(cls):
        if cls.raisedIOError:
            print("[%s]...Sorry, I must skip this test."%cls.exampleName)
            print("[%s]...The logfile is missing or doesn't have the correct name..."%cls.exampleName)
            print("%s : F "%cls.exampleName) # not in Analysis.py
        else:
            if len(cls.foundPhrases) > 0:
                print("[%s] : %s"%(cls.exampleName, cls.keyword))
                print("%s : F"%cls.exampleName)                 #prints the result
            else:
                print("%s : . "%cls.exampleName)


def DFdPhraseFactory(exampleName, logfile, keyword) :

    validName = re.sub(r'[_\W]+', '_', 'NekTest_%s' % exampleName)
    attr = dict(exampleName=exampleName,
                logfile=logfile,
                keyword=keyword,
                foundPhrases=[],
                raisedIOError=False)
    return type(validName, (DFdPhraseBase,), attr)

def DFdPhrase(exampleName, logfile, keyword):
    global suite
    cls = DFdPhraseFactory(exampleName, logfile, keyword)
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase(cls))

if __name__ == '__main__':

    __unittest = True

    global suite
    suite = unittest.TestSuite()

    print("\nBEGIN TESTING TOOLS")
    #SRL Compiler
    log = "./tools.out"
    value = "Error "
    DFdPhrase("Tools",log,value)

    print("\n\n2d_eig Example")
    log = "./srlLog/eig1.err"
    value = [[' 2   ',0,21,6],
             [' 3   ',0,39,6],
             [' 6  ' ,0,128,6],
             [' 10  ',0,402,6]]
    Run("Example 2d_eig/SRL: Serial-iter/err",log,value)

    print("\n\n3Dbox Example")

    #SRL
    log = "./srlLog/b3d.log.1"
    value = "end of time-step loop"
    FindPhrase("Example 3dbox/SRL: Serial",log,value)

    #SRL2
    log = "./srl2Log/b3d.log.1"
    value = "end of time-step loop"
    FindPhrase("Example 3dbox/SRL2: Serial",log,value)


    print("\n\naxi Example")
    log = "./srlLog/axi.log.1"
    value = [['total solver time',0.1,2,2],
             ['PRES: ',0,76,4],
             # ['PRES: ',1000000,0,4]
             ]
    Run("Example axi/SRL: Serial-time/iter",log,value)

    #missing log
    print("\n\RunMissingLog")
    log = "./srlLog/foobar"
    value = [['total solver time',0.1,2,2],
             ['PRES: ',0,76,4]]
    Run("Example Run missingLog",log,value)

    print("\n\FindPhraseMissingLog")
    #missing value
    log = "./srlLog/foobar"
    value = "end of time-step loop"
    FindPhrase("Example FindPhrase missingLog",log,value)

    unittest.TextTestRunner(verbosity=2).run(suite)

