from main import *

class PyDocAlgoFoundFunc:
    """A custom `PyDocAlgo` class to store information about a function returned from a "Find that Function" unit test."""
    def __init__(self, func):
        if func == []:
            raise ValueError("Param 'func' should not be empty.")

        self.found = func
        self.formatted = {
            'modulename': func[0],
            'funcname': func[1],
            'desc': func[2]
        }

    def getModuleName(self):
        """Getter for retrieving the module name."""
        return self.formatted['modulename']

    def getFuncName(self):
        """Getter for retrieving the function name."""
        return self.formatted['funcname']

    def getDescription(self):
        """Getter for retrieving the function's description."""
        return self.formatted['desc']

    def __str__(self):
        return f"PyDocAlgoFoundFunc({self.formatted})"

class PyDocAlgoTests:
    """A custom `PyDocAlgo` class for unit testing."""
    def findFunctTest(query: str, selectMultipleInput: str = 'n'):
        """A function for 'Find This Function' unit tests.\n
        Returns a `PyDocAlgoFoundFunc` object if a function was found.\n
        Returns `-1` if no function was found."""
        sendBotMessage("Starting search process...")
        selectMultiple = None
        if (selectMultipleInput.lower() == 'y') or (selectMultipleInput.lower() == 'yes'):
            selectMultiple = True
        elif (selectMultipleInput.lower() == 'n') or (selectMultipleInput.lower() == 'no') or (selectMultipleInput.lower() == ''):
            selectMultiple = False

        print(f"selectMultiple: {selectMultiple}")

        moduleToSearch = None
        for module in getAllModules():
            if module in query.lower():
                moduleToSearch = module

        i = InputHandler(query)
        foundFunction = makeComparisons(i, moduleToSearch, selectMultiple)

        if foundFunction == None:
            sendBotMessage("I'm sorry, but I couldn't find the function you were looking for. Please try again.")
            return -1
            
        else:
            if selectMultiple:
                result = []
                for func in foundFunction:
                    r = PyDocAlgoFoundFunc(func)
                    result.append(r)
                return result

            else:
                return PyDocAlgoFoundFunc(foundFunction)

    def addFunctTest(funcName: str, desc: str):
        """A function for 'Add This Function' unit tests."""
        addFunctionProcess(funcName, desc)

    def batchAddFunctTest(functionInfo: list[list[str]]):
        """A function for adding multiple functions to the `functions.csv` file. Good for unit testing and appending batches of functions.\n
Example Usage:\n
```
functionInfo = [
    ["numpy.concat", "Joins, or concatenates, a sequence of arrays along the given axis."],
    ["scipy.stats.shapiro", "Perform the Shapiro-Wilk test for normality."]
]
PyDocAlgoTests.batchAddFunctTest(funcInformation)
```
"""

        for row in functionInfo:
            addFunctionProcess(row[0], row[1])
            print(f"[SYSTEM] Function {row[0]} with description {row[1]} added.")
            time.sleep(2)

findFuncTests = {
    1: ["Find me a function that selects a random element from a list.", 'y'],
    2: ["Get me a function that does a shapiro-wilks test to test for normality.", 'n'],
    3: ["Find a function that performs the mann-whitney u rank test", 'n'],
    4: ["Find me a function in the random module that shuffles a python list", 'n']
}

addFuncTests = {
    1: ["", ""],
    2: ["", ""]
}

def performFindFuncTests(seconds: int = 5):
    for testNum in findFuncTests:
        print("="*40)
        print(f"'Find This Function' Test #{testNum}")
        query = findFuncTests[testNum][0]
        selectMultipleInput = findFuncTests[testNum][1]
        print("Parameters")
        print(f"query: '{query}'")
        print(f"selectMultipleInput: {selectMultipleInput}")

        print(f"Test begins in {seconds} seconds...")
        time.sleep(seconds)

        print("-"*30)
        print("Test Outputs")
        print("-"*30)
        try:
            result = PyDocAlgoTests.findFunctTest(query, selectMultipleInput)
            if result == []:
                print("No functions matches your query.")
            else:
                print(result)

        except ValueError:
            print("No functions matches your query.")

        print(f"Review test output for 10 seconds.")
        print("-"*30)
        time.sleep(10)

def performAddFuncTests(seconds: int = 5):
    for testNum in addFuncTests:
        print("-"*40)
        print(f"'Add This Function' Test #{testNum}")
        funcName = addFuncTests[testNum][0]
        desc = addFuncTests[testNum][1]
        print("Parameters")
        print(f"funcName: {funcName}")
        print(f"desc: {desc}")

        print(f"Test begins in {seconds} seconds...")
        time.sleep(seconds)

        PyDocAlgoTests.addFunctTest(funcName, desc)
        print("Note: be sure to check `functions.csv` before continuing. Press CTRL + C if any errors occur.")
        input("Press <ENTER> to continue...")

userInput = input("Which tests would you like to execute? [Find/Add]: ")
seconds = int(input("How many seconds between tests? (int): "))

if userInput.lower() == 'find':
    performFindFuncTests(seconds)
elif userInput.lower() == 'add':
    performFindFuncTests(seconds)

print("All tests complete. Exiting...")
quit()