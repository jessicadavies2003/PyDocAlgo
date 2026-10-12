from csv import reader, writer
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer
import time
from random import choice

ps = PorterStemmer()
stop_words = stopwords.words("english")

def sendBotMessage(msg: str, isError: bool = False):
    if isError:
        print(f"['{botName}' ERROR] {msg}")
    else:
        print(f"['{botName}' BOT] {msg}")

class SynonymsClass:
    def __init__(self, cleanedInput: list[str]):
        self.cleanedInput = cleanedInput

    def findAndReplace(self, wordToChange: str):
        """Finds and replaces the string `wordToChange` with a random synonym of `wordToChange`. - IN PLACE"""
        syns = wordnet.synsets(wordToChange)
        try:
            idx = self.cleanedInput.index(wordToChange)
            randSynonym = choice(syns)
            self.cleanedInput.insert(idx, randSynonym)

        except ValueError:
            sendBotMessage(f"{wordToChange} was not found in the input.")

    def getInputAsList(self):
        return self.cleanedInput

def word2SynomymsList(word: str, includeWord: bool = True) -> list[str]:
    """Converts a word to a list of its synonyms. if `includeWord` is True, the given word will be included in the list."""
    result = []
    syns = wordnet.synonyms(word)
    for lst in syns:
        result.extend(lst)

    result = list(set(result))

    if includeWord:
        result.append(word)

    return result

class InputHandler:
    def cleanInput(self, stem_words: bool = False):
        for char in "!\"£$%^&*(){}:@;'<>,._+-=~'0123456789":
            self._input = self._input.replace(char, "")

        if stem_words:
            self.cleanedInput = [ps.stem(word) for word in word_tokenize(self._input) if word not in stop_words]
        else:
            self.cleanedInput = [word for word in word_tokenize(self._input) if word not in stop_words]

    def __init__(self, userInput: str):
        self._input = userInput
        self.cleanInput()

    def cleanInput_Ext(self, userInput: str, stem_words: bool = False) -> list[str]:
        copy = userInput.lower()
        for char in "!\"£$%^&*(){}:@;'<>,._+-=`~'0123456789":
            copy = copy.replace(char, "")

        if stem_words:
            return [ps.stem(word) for word in word_tokenize(copy) if word not in stop_words]
        else:
            return [word for word in word_tokenize(copy) if word not in stop_words]

    def compareInputWithFunc(self, functionData: list[str]) -> bool:
        """Compares the function description to the user's input, and returns a boolean value if they are similar"""
        cleanedFunc = self.cleanInput_Ext(functionData[2])
        syns = self.words2Synonyms_Ext(cleanedFunc)

        self.cleanInput(True)

        requiredCounter = 3
        counter = 0
        for item in syns:
            if (type(item) == str) and (item in self.cleanedInput):
                counter += 1
            elif type(item) == list:
                for word in item:
                    counter += 1 if word in self.cleanedInput else 0

            if counter == requiredCounter:
                # print(f"Cleaned user input: {self.cleanedInput} / Length: {len(self.cleanedInput)}")
                # print(f"Cleaned function input: {cleanedFunc} / Length: {len(cleanedFunc)}")

                return True

            # print(f"Synonyms input: {syns} / Length: {len(syns)}")
        return False

    def words2Synonyms(self):
        result = []
        for word in self.cleanedInput:
            result.append(word2SynomymsList(word))
        self.cleanedInput = result

    def words2Synonyms_Ext(self, cleaned_input: list[str]):
        result = []
        for word in cleaned_input:
            result.append(word2SynomymsList(word))
        return result

botName = "PyDocAlgo"
nickname = "Algo"

funcsFile = [row for row in reader(open("data/functions.csv")) if len(row) > 0]
funcsFile = funcsFile[1:]
headers = funcsFile[0]

def addFunctionProcess(funcName: str = None, desc: str = None):
    if (not funcName) and (not desc):
        sendBotMessage("Enter the name of your function. (including the module it comes from. Example: numpy.ndarray).")
        funcName = input("[YOU] ")
        module = funcName.split(".")[0]
        sendBotMessage("Enter a short description for this function. Example: 'Creates and returns an n-dimensional (nD) array of type `ndarray`. In other words, an array of any size.'")
        desc = input("[YOU] ")
    
    sendBotMessage(f"Adding function {funcName} to database...")
    functionsFile = [row for row in reader(open("data/functions.csv")) if len(row) > 0]
    functionsFile.append([module, funcName, desc])

    moduleWriter = writer(open("data/functions.csv", "w"))
    moduleWriter.writerows(functionsFile)

    sendBotMessage("Success!")

# processes #
def makeComparisons(i: InputHandler, moduleToSearch: str = None, selectMultiple: bool = False):
    global rows
    result = []

    if moduleToSearch:
        moduleToSearch = moduleToSearch.replace(" module", "")
        sendBotMessage(f"Variable 'moduleToSearch' provided: {moduleToSearch}")
        rows = [r for r in funcsFile if r[0] == moduleToSearch]
    else:
        sendBotMessage("Variable 'moduleToSearch' not provided. Defaulting to all rows.")
        rows = funcsFile

    for row in rows:
        if (i.compareInputWithFunc(row) == True) and (not selectMultiple):
            return row
        elif (i.compareInputWithFunc(row) == True) and (selectMultiple):
            result.append(row)

    return result
                
def displayFunctionData(function: list[str]):
    print("="*30)
    print(f"Function Name: {function[1]}")
    print(f"Which Module Holds this Function?: {function[0]}")
    print(f"Function Description: {function[2]}")
    print("="*30)

def displayMultipleFunctionData(functions: list[list[str]]):
    for row in functions:
        displayFunctionData(row)

def getAllModules():
    result = []
    for row in funcsFile:
        result.append(f"{row[0]} module")

    return list(set(result))

def main():
    sendBotMessage(f"Hello! I'm {botName}, but you can call me {nickname}. I'm here to help you find the right Python functions for your project!")
    sendBotMessage("Type a description of a function you're looking for, and I'll search in my database for you!")
    sendBotMessage("You can type 'exit' if you wish to exit this session, and type 'I [wish/want] to add a new function [to your database]' to... well, self-explanatory.")
    sendBotMessage("To search a specific module, type '<nameofmodule> module' in your search query. (example: 'in the random module')")

    print("="*40)
    userInput = input("[YOU] ")
    while (userInput.lower() != 'exit'):
        sendBotMessage("Would you like me to fetch multiple functions that match your query? [Y/N] (If you leave this blank, I will default to 'N'.)")
        selectMultipleInput = input("[YOU] ")

        start = time.time()
        sendBotMessage("Starting search process...")
        selectMultiple = None
        if (selectMultipleInput.lower() == 'y') or (selectMultipleInput.lower() == 'yes'):
            selectMultiple = True
        elif (selectMultipleInput.lower() == 'n') or (selectMultipleInput.lower() == 'no') or (selectMultipleInput.lower() == ''):
            selectMultiple = False

        print(f"selectMultiple: {selectMultiple}")

        if "add a new function" in userInput.lower():
            addFunctionProcess()
            continue

        moduleToSearch = None
        for module in getAllModules():
            if module in userInput.lower():
                moduleToSearch = module

        i = InputHandler(userInput)
        foundFunction = makeComparisons(i, moduleToSearch, selectMultiple)

        if foundFunction == None:
            sendBotMessage("I'm sorry, but I couldn't find the function you were looking for. Please try again.")
            
        else:
            if selectMultiple:
                sendBotMessage("I have several results for you!")
                displayMultipleFunctionData(foundFunction)
                sendBotMessage("If you want, you can describe another function for me to retrieve.")

            else:
                sendBotMessage("I have a result for you!")
                displayFunctionData(foundFunction)
                sendBotMessage("If you want, you can describe another function for me to retrieve.")

        sendBotMessage(f"Process completed in {time.time() - start} seconds.")
        print("="*40)
        userInput = input("[YOU] ")

if __name__ == '__main__':
    main()