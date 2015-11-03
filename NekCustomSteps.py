from buildbot.steps import shell
from buildbot.process.buildstep import LogLineObserver
from buildbot.status.builder import EXCEPTION, FAILURE, SKIPPED, SUCCESS , WARNINGS

############################################
#### NEK Step                           ####
############################################

# This step will run the NekTests.py script
# If all tests are successful then the step will be green (SUCCESS)
# If some tests fail, the step will be orange (WARNINGS)
# If for some reason buildbot cannot run the python command (probably wrong working directory), the step will be red (FAILURE)
# It will automatically create a summarry (on the webpage) of the failing tests if there are any of them


class NekStepP(shell.ShellCommand):
    numPass = 0
    numTotal = 0

    def __init__(self, **kwargs):
        shell.ShellCommand.__init__(self,  **kwargs)
        self.description = ["TopDown", "Testing","Parallel"]
        self.command = ["python", "../Analysis.py","mpi"]
        self.numPass = 0
        self.numTotal = 0
        counter = NekTestCounter()
        self.addLogObserver('stdio', counter)

    def createSummary(self, log) :
        warnings = []
        for line in log.readlines():
            if "Summary" in line :
                warnings.append(line)
            if "F " in line and "successful" not in line :
                warnings.append("Failing benchmark : ")
                warnings.append(line)
        if len(warnings) > 0 :
            self.addCompleteLog('Summary', "".join(warnings))

    def getText(self, cmd, results):
        text = shell.ShellCommand.getText(self, cmd, results)
        if self.numTotal > 0 :
            text.append("tests failed: " + str(self.numTotal - self.numPass))
            text.append("tests passed: " + str(self.numPass))
        return text
        
    def evaluateCommand(self, cmd):
        if self.numPass < self.numTotal :
            return FAILURE
        else :
            return SUCCESS



class NekTestCounter(LogLineObserver) :

    def outLineReceived(self,line):
        if "Test Summary" in line :
            self.step.numPass = int(line.split()[3].split("/")[0])
            self.step.numTotal = int(line.split()[3].split("/")[1])

# serial only logs.
class NekStepS(shell.ShellCommand):
    numPass = 0
    numTotal = 0

    def __init__(self, **kwargs):
        shell.ShellCommand.__init__(self,  **kwargs)
        self.description = ["TopDown", "Testing","Serial"]
        self.command = ["python", "../Analysis.py","serial"]
        self.numPass = 0
        self.numTotal = 0
        counter = NekTestCounter()
        self.addLogObserver('stdio', counter)

    def createSummary(self, log) :
        warnings = []
        for line in log.readlines():
            if "Summary" in line :
                warnings.append(line)
            if "F " in line and "successful" not in line :
                warnings.append("Failing benchmark : ")
                warnings.append(line)
        if len(warnings) > 0 :
            self.addCompleteLog('Summary', "".join(warnings))

    def getText(self, cmd, results):
        text = shell.ShellCommand.getText(self, cmd, results)
        if self.numTotal > 0 :
            text.append("tests failed: " + str(self.numTotal - self.numPass))
            text.append("tests passed: " + str(self.numPass))
        return text
        
    def evaluateCommand(self, cmd):
        if self.numPass < self.numTotal :
            return FAILURE
        else :
            return SUCCESS

