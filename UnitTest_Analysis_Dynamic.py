#! /usr/bin/python
# Python module to run top-down tests for Nek

import unittest
import re

###############################################################################

# class BaseTestCase(unittest.TestCase):
#     """
#         name (string): name of the test
#         logfile (string): path of the log file
#         dictOfValue (dict): dict of different
#             {valName: {'target':val, 'tolerance':val, 'col':val}}
#             we want to check (where 'col' is the column)
#     """
#
#     testName = ""
#     logfile = ""
#     foundVals = {}
#     missingVals = {}
#
#     @classmethod
#     def setUpClass(cls):
#         with open(cls.logfile, 'r') as fd:
#             for line in fd:
#                 for valName in cls.missingVals:
#                     if valName in line:
#                         try:
#                             col = cls.missingVals[valName]['col']
#                             testVal = float(line.split()[col])
#                         except (ValueError,IndexError) :
#                             pass
#                         else:
#                             cls.foundVals[valName] = cls.missingVals.pop(valName)
#                             cls.foundVals[valName]['test'] = testVal

def testCaseFactory(exampleName, logfile, listOfVals):

    # Convenient data structure
    dictOfVals = {testName: {'target': target, 'tolerance': tolerance, 'col': col}
         for [testName, target, tolerance, col] in listOfVals }

    # dictOfVals = collections.OrderedDict(
    #     [(testName, {'target': target, 'tolerance': tolerance, 'col': col})
    #      for (testName, target, tolerance, col) in listOfVals ] )

    # Get a new subclass of TestCase
    validName = re.sub(r'[_\W]+', '_', 'NekTest_%s' % exampleName)
    cls = type(validName, (unittest.TestCase,), {})

    # Add a test function for each test
    for (i, testName) in enumerate(dictOfVals):

        def testFunc(self, testName=testName):
            self.assertIn(testName, cls.foundTests)
            self.assertLess(abs(cls.foundTests[testName]['testVal'] - cls.foundTests[testName]['target']),
                            cls.foundTests[testName]['tolerance'])

        validName = re.sub(r'[_\W]+', '_', 'test_%s_%02d' % (testName, i))
        setattr(cls, validName, testFunc)

    # Find each test in the logfile
    cls.missingTests = dictOfVals
    cls.foundTests = {}

    with open(logfile, 'r') as fd:
        for line in fd:
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

    return cls

if __name__ == '__main__':

    suite = unittest.TestSuite()

    # 2d_eig Example
    log = "./srlLog/eig1.err"
    value = [[' 2   ',0,21,6],
             [' 3   ',0,39,6],
             [' 6  ' ,0,128,6],
             [' 10  ',0,402,6]]
    newTests = testCaseFactory("Example 2d_eig/SRL: Serial-iter/err",log,value)
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase(newTests))

    #axi Example
    log = "./srlLog/axi.log.1"
    value = [['total solver time',0.1,2,2],
             ['PRES: ',0,76,4]]
    newTests = testCaseFactory("Example axi/SRL: Serial-time/iter",log,value)
    suite.addTest( unittest.TestLoader().loadTestsFromTestCase(newTests))

    unittest.TextTestRunner(verbosity=2).run(suite)


