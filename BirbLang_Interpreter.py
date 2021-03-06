import re
import ast


class BirbLang:
    def __init__(self, program):
        self.program = program

    # Defines a function which returns the number of occurrences of a specific character
    @staticmethod
    def count(arr, character):
        number = 0
        for x in arr:
            if x == character:
                number += 1
            else:
                continue
        return number

    # Defines a function which separates a string while keeping all delimiters
    @staticmethod
    def safesplit(string, character1=None, character2=None, character3=None):
        temp = ""
        arr = []
        for x in string:
            if x != character1 and x != character2 and x != character3:
                temp += x

            else:
                arr.append(temp)
                if x == character1:
                    arr.append(character1)
                elif x == character2:
                    arr.append(character2)
                else:
                    arr.append(character3)
                temp = ""
        arr.append(temp)

        return arr

    # Defines a function which splits up a string using any delimiters included, keeping the delimiter within the list
    @staticmethod
    def safesplit2(string, delimiter=None, delimiter2=None):
        arr = string.split(" ")
        temp = ""
        final = []
        for x in arr:
            if x != delimiter and x != delimiter2:
                temp += x + " "
            else:
                temp = list(temp)
                del temp[-1]
                temp = "".join(temp)
                final.append(temp)
                temp = ""
                if x == delimiter:
                    final.append(delimiter)
                else:
                    final.append(delimiter2)
        temp = list(temp)
        del temp[-1]
        temp = "".join(temp)
        final.append(temp)
        return final

    # Defines a function which removes every occurrence of a string in an array
    @staticmethod
    def removeall(arr, character):
        return [x for x in arr if x != character]

    # Defines a function which returns the nth index of a specific character within an array
    @staticmethod
    def indexofoccurrence(arr, character, occurence):
        return [x for x in range(0, len(arr)) if arr[x] == character][occurence - 1]

    # Calculates a math equation
    @staticmethod
    def calculate(equation):
        # The equation provided will be split with (, ), and a space being the delimiters (without removing them)
        equation = BirbLang.safesplit(equation, "(", ")", " ")
        equation = BirbLang.removeall(equation, " ")
        equation = BirbLang.removeall(equation, "")
        result = 0
        operations = ["floof", "unfloof", "megafloof", "megaunfloof", "ultrafloof", "ultraunfloof"]
        # Changes the data type of any variable to its appropriate type
        for x in equation:
            if re.match("[0-9.]+", x):
                equation[equation.index(x)] = ast.literal_eval(x)

        # Defines lambda functions which actually calculate the equation (based on the operation)
        EXPONENT = lambda x: x[1] ** x[3]
        ROOT = lambda x: x[1] ** (1.0/x[3])
        MULTIPLICATION = lambda x: x[1] * x[3]
        DIVISION = lambda x: x[1] / x[3]
        ADDITION = lambda x: x[1] + x[3] if len(x) > 2 else x[1] + 1
        SUBTRACTION = lambda x: x[1] - x[3] if len(x) > 2 else x[1] - 1
        temp = [equation, []]
        while True:
            # Checks to see if there are any brackets within the equation, and will set temp[1] to the innermost
            # brackets to be evaluated. Otherwise, it will just evaluate the equation as-is
            if "(" in temp[0]:
                evaluate = []
                index = temp[0].index("(")
                idunnoIllRenameLater = index
                evaluate.append(temp[0][index])
                index += 1

                # Sets temp[1] to the first brackets detected within the equation
                while BirbLang.count(evaluate, "(") != BirbLang.count(evaluate, ")"):
                    evaluate.append(temp[0][index])
                    index += 1
                temp[1] += evaluate[1:-1]
                evaluate = []
                occurrence = 2

                # Checks to see if there are any inner brackets, and will continue to shrink the array until it has
                # reached the inner most equation
                while "(" in temp[1]:
                    index = temp[1].index("(") + 1
                    evaluate.append("(")
                    while BirbLang.count(evaluate, "(") != BirbLang.count(evaluate, ")"):
                        evaluate.append(temp[1][index])
                        index += 1
                    temp[1] = evaluate[1:-1]
                    idunnoIllRenameLater = BirbLang.indexofoccurrence(temp[0], "(", occurrence)
                    occurrence += 1

                # Removes the part of the equation that will be evaluated
                del temp[0][idunnoIllRenameLater + 1:idunnoIllRenameLater + 6]
            else:
                # Sets temp[1] to the equation
                idunnoIllRenameLater = 0
                temp[1] += (temp[0])
                del temp[0][1:]

            # Checks if the operator being evaluated is an exponent
            if operations[4] in temp[1] or operations[5] in temp[1]:
                calculation = EXPONENT(temp[1][0:]) if temp[1][0] == operations[4] else ROOT(temp[1][0:]) # Calculates it
                result = calculation  # Sets the result variable to be the calculation (in case it's the final answer)
                temp[1] = []
                temp[0][idunnoIllRenameLater] = calculation  # Places the calculation within the equation
                continue

            # Calculates multiplication and division
            elif operations[2] in temp[1] or operations[3] in temp[1]:
                calculation = MULTIPLICATION(temp[1][0:]) if temp[1][0] == operations[2] else DIVISION(
                    temp[1][0:])
                result = calculation
                temp[1] = []
                temp[0][idunnoIllRenameLater] = calculation
                continue

            # Calculates addition and subtraction
            elif operations[0] in temp[1] or operations[1] in temp[1]:
                calculation = ADDITION(temp[1][0:]) if temp[1][0] == operations[0] else SUBTRACTION(
                    temp[1][0:])
                result = calculation
                temp[1] = []
                temp[0][idunnoIllRenameLater] = calculation
                continue
            break
        return result

    # Defines a function which evaluates a conditional statement to a boolen value (either true of false)
    @staticmethod
    def condition(string):
        # Splits up the condition into each separate conditional to check if multiple exist (eg. if x > 5 and x < 10)
        arr = BirbLang.safesplit2(string, "and", "or")

        # Splits each conditional into separate words in a list
        for x in range(len(arr)):
            arr[x] = arr[x].split(" ")

        # Joins any conditionals that may have the word "or" in them and still need to be evaluated as one
        while True:
            i = 1
            endloop = True
            # If an out of place isolated "or" is found, it's joined with the elements next to it
            while i < len(arr):
                if " ".join(arr[i]) == "or" and arr[i + 1][0] == "just":
                    arr[i - 1] = arr[i - 1] + arr[i]
                    arr[i - 1] = arr[i - 1] + arr[i + 1]
                    del arr[i:i + 2]
                    endloop = False
                    break
                i += 1
            if endloop:
                break

        # Checks each individual condition, evaluating them to either true or false
        for x in range(0, len(arr), 2):
            if re.match("[0-9.]+ is floofier than [0-9.]+$", " ".join(arr[x])):
                if ast.literal_eval(arr[x][0]) > ast.literal_eval(arr[x][4]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match("[0-9.]+ is floofier than or just as floofy as [0-9.]+$", " ".join(arr[x])):
                if ast.literal_eval(arr[x][0]) >= ast.literal_eval(arr[x][9]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match("[0-9.]+ is not as floofy as [0-9.]+$", " ".join(arr[x])):
                if ast.literal_eval(arr[x][0]) < ast.literal_eval(arr[x][6]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match("[0-9.]+ is not as floofy or just as floofy as [0-9.]+$", " ".join(arr[x])):
                if ast.literal_eval(arr[x][0]) <= ast.literal_eval(arr[x][10]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match("[0-9.]+ is as floofy as [0-9.]+$", " ".join(arr[x])):
                if ast.literal_eval(arr[x][0]) == ast.literal_eval(arr[x][5]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match("[0-9.]+ is not as floofy as [0-9.]+$", " ".join(arr[x])):
                if ast.literal_eval(arr[x][0]) == ast.literal_eval(arr[x][6]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match(".+ is as floofy as .+$", " ".join(arr[x])):
                f = 0
                while f in range(len(arr[x]) - 5):
                    if arr[x][f] == "is" and arr[x][f + 1] == "as" and arr[x][f + 2] == "floofy" and arr[x][f + 3] == "as":
                        arr[x][f + 4] = " ".join(arr[x][f + 4:])
                        del arr[x][f + 5:]
                        arr[x][0] = " ".join(arr[x][0:f])
                        del arr[x][1:f]
                        break
                    f += 1
                if "\"" not in arr[x][0]:
                    arr[x][0] = f"\"{arr[x][0]}\""
                if "\"" not in arr[x][5]:
                    arr[x][5] = f"\"{arr[x][5]}\""
                if ast.literal_eval(arr[x][0]) == ast.literal_eval(arr[x][5]):
                    arr[x] = True
                else:
                    arr[x] = False
            elif re.match(".+ is not as floofy as .+$", " ".join(arr[x])):
                f = 0
                while f in range(len(arr[x]) - 5):
                    if arr[x][f] == "is" and arr[x][f + 1] == "as" and arr[x][f + 2] == "floofy" and arr[x][f + 3] == "as":
                        arr[x][f + 5] = " ".join(arr[x][f + 5:])
                        del arr[x][f + 6:]
                        arr[x][0] = " ".join(arr[x][0:f])
                        del arr[x][1:f]
                        break
                    f += 1
                if "\"" not in arr[x][0]:
                    arr[x][0] = f"\"{arr[x][0]}\""
                if "\"" not in arr[x][6]:
                    arr[x][6] = f"\"{arr[x][6]}\""
                if ast.literal_eval(arr[x][0]) == ast.literal_eval(arr[x][5]):
                    arr[x] = True
                else:
                    arr[x] = False
            else:
                return 69

        # Checks whether or not the entire conditional is true (if multiple conditions are found)
        if len(arr) > 2:
            while len(arr) > 1:
                if " ".join(arr[1]) == "and":
                    arr[0] = arr[0] and arr[2]
                    del arr[1:3]
                elif " ".join(arr[1]) == "or":
                    arr[0] = arr[0] or arr[2]
                    del arr[1:3]
        return arr[0]

    def evaluate(self):
        variables = {}
        data_types = ("string", "int", "float", "boolean", "complex", "list")
        code = self.program.split("\n")  # Splits code into each individual line
        operations = ["floof", "unfloof", "megafloof", "megaunfloof", "ultrafloof", "ultraunfloof"]
        inloop = []
        loop_index = []
        in_condition = []

        # Checks to see if program can be executed and stopped successfully
        if "hatch egg" in code and "slep" in code:

            # Starts program at wherever the "break egg" line occurs
            line = code.index("hatch egg") + 1

            while code[line] != "slep":

                # Removes all comments and whitespace at the start and end of the line (easier to read that way)
                linesplit = list(code[line])

                if "#" in linesplit:
                    del linesplit[linesplit.index("#"):]

                if not linesplit or not self.removeall(linesplit, " "):
                    line += 1
                    continue

                while linesplit[0] == " " or linesplit[0] == "\t":
                    del linesplit[0]

                while linesplit[-1] == " " or linesplit[0] == "\t":
                    del linesplit[-1]


                code[line] = "".join(linesplit)

                linesplit = code[line].split(" ")

                for x in range(0, len(linesplit)-2):
                    if linesplit[x] in variables:
                        if type(variables[linesplit[x]]) is list and linesplit[x+1] == "at":
                            if linesplit[x+2] in variables:
                                if type(variables[linesplit[x+2]]) is int:
                                    linesplit[x+2] = variables[linesplit[x+2]]
                                else:
                                    raise ValueError(f"Cannot find element at index {linesplit[x+2]}")
                            try:
                                linesplit[x] = variables[linesplit[x]][int(linesplit[x+2])]
                                del linesplit[x+1:x+3]
                            except IndexError:
                                raise IndexError(f"Index out of range")

                # Outputs element at specific index of array (if possible)
                if re.match("^squawk .+ at [0-9.]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            print(variables[linesplit[1]][int(linesplit[3])])
                        else:
                            raise TypeError(f"type {type(variables[linesplit[1]])} does not support indexing")

                    elif type(ast.literal_eval(linesplit[1])) is list:
                        print(ast.literal_eval(linesplit[1])[int(linesplit[3])])

                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Checks if the line follows the pattern "chirp (some variable)", and will then print out the text
                elif re.match("^squawk .+$", code[line]):

                    if linesplit[1] in operations:
                        linesplit = BirbLang.safesplit(code[line], " ", "(", ")")
                        linesplit = BirbLang.removeall(linesplit, " ")
                        linesplit = BirbLang.removeall(linesplit, "")
                        for x in linesplit[1:]:
                            if x in variables:
                                linesplit[linesplit.index(x)] = str(variables[x])
                        print(str(BirbLang.calculate(" ".join(linesplit[1:]))) + "\n")

                    elif len(linesplit) > 2 and list(linesplit[1])[0] != "\"":
                        for x in range(1, len(linesplit)):
                            if linesplit[x] in variables:
                                linesplit[x] = str(variables[linesplit[x]])
                        print(str(BirbLang.condition(" ".join(linesplit[1:]))) + "\n")
                    else:
                        # Will try printing out the value if it were a valid data type
                        try:
                            print(ast.literal_eval(" ".join(linesplit[1:])))

                        # If it isn't a valid data type, it will try to output it as a variable
                        except ValueError:
                            if linesplit[1] in variables:
                                print(variables[linesplit[1]][1:-1]) if type(
                                    variables[linesplit[1]]) == "str" else print(variables[linesplit[1]])
                            else:
                                raise NameError(
                                    f"{linesplit[1]} is not defined")  # Raises an error if all other cases failed

                # Outputs element at specific index of array (if possible, and without a newline character)
                elif re.match("^chirp .+ at [0-9.]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            print(variables[linesplit[1]][int(linesplit[3])], end="")
                        else:
                            raise TypeError(
                                f"type {type(variables[linesplit[1]])} does not support indexing")

                    elif type(ast.literal_eval(linesplit[1])) is list:
                        print(ast.literal_eval(linesplit[1])[int(linesplit[3])], end="")

                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Will print out text (without an endline) if the pattern matches "chirp (something)"
                elif re.match("^chirp .+$", code[line]):

                    if linesplit[1] in operations:
                        linesplit = BirbLang.safesplit(code[line], " ", "(", ")")
                        linesplit = BirbLang.removeall(linesplit, " ")
                        linesplit = BirbLang.removeall(linesplit, "")
                        for x in linesplit[1:]:
                            if x in variables:
                                linesplit[linesplit.index(x)] = str(variables[x])
                        print(BirbLang.calculate(" ".join(linesplit[1:])), end="")
                    elif len(linesplit) > 2 and list(linesplit[1])[0] != "\"":
                        for x in range(1, len(linesplit)):
                            if linesplit[x] in variables:
                                linesplit[x] = str(variables[linesplit[x]])
                        print(BirbLang.condition(" ".join(linesplit[1:])))
                    else:
                        # Will try printing out the value if it were a valid data type
                        try:
                            print(ast.literal_eval(" ".join(linesplit[1:])), end="")

                        # If it isn't a valid data type, it will try to output it as a variable
                        except ValueError:
                            if linesplit[1] in variables:
                                print(variables[linesplit[1]][1:-1], end="") if type(
                                    variables[linesplit[1]]) == "str" else print(variables[linesplit[1]], end="")
                            else:
                                # Raises an error if everything else failed
                                raise NameError(f"{linesplit[1]} is not defined")

                        # else:
                        #     raise NameError(f"{linesplit[1]} is not defined")

                # Runs if the line is meant to declare a new variable (new birb variable_name is value)
                elif re.match("^new birb [^ ]+ is .+$", code[line]):
                    if linesplit[4] in operations:
                        linesplit = BirbLang.safesplit(code[line], " ", "(", ")")
                        linesplit = BirbLang.removeall(linesplit, " ")
                        linesplit = BirbLang.removeall(linesplit, "")
                        for x in linesplit[4:]:
                            if x in variables:
                                linesplit[linesplit.index(x)] = str(variables[x])
                        variables[linesplit[2]] = BirbLang.calculate(" ".join((linesplit[4:])))

                    else:
                        try:
                            # Converts string to its appropriate data type
                            variables[linesplit[2]] = ast.literal_eval(linesplit[4])
                        except ValueError:
                            if linesplit[4] == "mimic":  # Handles case where the line asks for user input
                                variables[linesplit[2]] = input(">>> ")
                            elif linesplit[4] in variables:
                                variables[linesplit[2]] = variables[linesplit[4]]
                            else:
                                raise ValueError(f"{variables[linesplit[2]]} is not a valid data type")

                # Checks if the line is "floof (variable)," and will increment it if possible
                elif re.match("^floof [^ ]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is int or type(variables[linesplit[1]]) is float:
                            variables[linesplit[1]] += 1
                        else:
                            raise ValueError(f"{variables[linesplit[1]]} cannot be incremented")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                elif re.match("^unfloof [^ ]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is int or type(variables[linesplit[1]]) is float:
                            variables[linesplit[1]] -= 1
                        else:
                            raise ValueError(f"{variables[linesplit[1]]} cannot be incremented")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Changes data type of variable if the line matches "(variable) is now (data_type)"
                elif re.match("^breed of [^ ]+ is now [^ ]+$", code[line]):
                    if linesplit[2] in variables:
                        if linesplit[5] in data_types:
                            if linesplit[5] == "string":
                                if type(variables[linesplit[2]]) is list:
                                    variables[linesplit[2]] = "".join(variables[linesplit[2]])
                                else:
                                    variables[linesplit[2]] = str(variables[linesplit[2]])
                            elif linesplit[5] == "int":
                                try:
                                    variables[linesplit[2]] = int(variables[linesplit[2]])
                                except ValueError:

                                    # Handles case of converting a float in a string to an int
                                    if type(ast.literal_eval(variables[linesplit[2]])) is float:
                                        variables[linesplit[2]] = int(float(variables[linesplit[2]]))

                                    else:
                                        raise ValueError(f"{variables[linesplit[2]]} cannot be converted to type int")
                            elif linesplit[5] == "float":
                                variables[linesplit[2]] = float(variables[linesplit[2]])
                            elif linesplit[5] == "list":
                                variables[linesplit[2]] = list(str(variables[linesplit[2]]))
                            elif linesplit[5] == "complex":
                                variables[linesplit[2]] = complex(variables[linesplit[2]])
                            elif linesplit[5] == "boolean":
                                variables[linesplit[2]] = bool(variables[linesplit[2]])
                        else:
                            raise ValueError(f"{linesplit[5]} is not a valid data type")
                    else:
                        raise NameError(f"{linesplit[2]} is not defined")

                # Outputs the data type of a variables/value if the line matches "breed of (variable/value)"
                elif re.match("^breed of [^ ]+$", code[line]):
                    try:
                        print(type(ast.literal_eval(linesplit[2])))

                    except ValueError:
                        if linesplit[2] in variables:
                            print(type(variables[linesplit[2]]))
                        else:
                            raise NameError(f"{linesplit[2]} is not defined")

                # Sets the value of an element within an array
                elif re.match("^[^ ]+ at [0-9.]+ is now .+$", code[line]):
                    if linesplit[0] in variables:
                        if linesplit[5] in operations:
                            linesplit = BirbLang.safesplit(code[line], " ", "(", ")")
                            linesplit = BirbLang.removeall(linesplit, " ")
                            linesplit = BirbLang.removeall(linesplit, "")
                            for x in linesplit[5:]:
                                if x in variables:
                                    linesplit[linesplit.index(x)] = str(variables[x])
                                elif x == "it":
                                    linesplit[linesplit.index(x)] = str(variables[linesplit[0]][int(linesplit[2])])
                            linesplit[5] = BirbLang.calculate(" ".join((linesplit[5:])))
                            variables[linesplit[0]][int(linesplit[2])] = linesplit[5]
                        else:
                            variables[linesplit[0]][int(linesplit[2])] = ast.literal_eval(linesplit[5])
                    else:
                        raise NameError(f"{linesplit[0]} is not defined")

                # Changes value of variable (if possible) if the line matches "(variable) is now (value)"
                elif re.match("^[^ ]+ is now .+$", code[line]):
                    if linesplit[0] in variables:
                        if linesplit[3] in operations:
                            linesplit = BirbLang.safesplit(code[line], " ", "(", ")")
                            linesplit = BirbLang.removeall(linesplit, " ")
                            linesplit = BirbLang.removeall(linesplit, "")
                            for x in linesplit[3:]:
                                if x in variables:
                                    linesplit[linesplit.index(x)] = str(variables[x])
                                elif x == "it":
                                    linesplit[linesplit.index(x)] = str(variables[linesplit[0]])
                            variables[linesplit[0]] = BirbLang.calculate(" ".join(linesplit[3:]))

                        else:
                            variables[linesplit[0]] = ast.literal_eval(linesplit[3])
                    else:
                        raise NameError(f"{linesplit[0]} is not defined")

                # Removes an element within a list at a specific index
                elif re.match("^peck [^ ]+ at [0-9.]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            del variables[linesplit[1]][int(linesplit[3])]
                        else:
                            raise AttributeError(f"peck is not defined for type {type(variables[linesplit[1]])}")
                    else:
                        raise NameError(f"{variables[linesplit[1]]} is not defined")

                # Removes the last element of an array if the line matches "peck (variable)"
                elif re.match("^peck [^ ]+$", code[line]):
                    if linesplit[1] in variables:
                        try:
                            variables[linesplit[1]].pop()
                        except AttributeError:
                            raise AttributeError(f"peck for type {type(variables[linesplit[1]])} is not defined")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Inserts value into specific index of array
                elif re.match("^feed [^ ]+ .+ at [0-9.]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            variables[linesplit[1]].insert(int(linesplit[-1]), ast.literal_eval(
                                " ".join(linesplit[2:linesplit.index("at")])))
                        else:
                            raise AttributeError(f"feed is not defined for type {type(variables[linesplit[1]])}")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Appends a value to an array
                elif re.match("^feed [^ ]+ .+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            variables[linesplit[1]].append(ast.literal_eval("".join(linesplit[2:])))
                        else:
                            raise AttributeError(f"peck for type {type(variables[linesplit[1]])} is not defined")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Starts or ends a while statement
                elif re.match("^[^ ]+ is flying while .+$", code[line]):
                    if linesplit[0] in variables:
                        # Replaces any instance of "it" with the variable being looped
                        for x in range(4, len(linesplit)):
                            if linesplit[x] == "it":
                                linesplit[x] = str(variables[linesplit[0]])
                            if linesplit[x] in variables:
                                linesplit[x] = str(variables[linesplit[x]])

                        # Checks the condition (to decide whether or not to run)
                        evaluate_condition = self.condition(" ".join(linesplit[4:]))
                        if evaluate_condition and evaluate_condition != 69:
                            if line not in loop_index:
                                loop_index.append(line)
                            line += 1
                            continue

                        # Finds the loop's corresponding "stop flying" line and skips over to that line
                        else:
                            del loop_index[-1]
                            i = 1
                            while i != 0:
                                line += 1
                                linesplit = list(code[line])

                                if "#" in linesplit:
                                    del linesplit[linesplit.index("#"):]

                                if not linesplit or not self.removeall(linesplit, " "):
                                    line += 1
                                    continue

                                while linesplit[0] == " " or linesplit[0] == "\t":
                                    del linesplit[0]

                                while linesplit[-1] == " " or linesplit[0] == "\t":
                                    del linesplit[-1]

                                code[line] = "".join(linesplit)
                                if re.match("^[^ ]+ is flying while .+$", code[line]):
                                    i += 1
                                elif re.match("^stop flying", code[line]):
                                    i -= 1
                            line += 1
                            continue
                    else:
                        raise NameError(f"{linesplit[0]} is not defined")

                # Loops back to the corresponding while loop if the code is still in a loop
                elif code[line] == "stop flying":
                    if loop_index:
                        line = loop_index[-1]
                        continue

                elif re.match("^[^ ]+ desires seed$", code[line]):
                    if linesplit[0] in variables:
                        linesplit[0] = str(variables[linesplit[0]])

                    if "\"" not in linesplit[0]:
                        linesplit[0] = f"\"{linesplit[0]}\""

                    try:
                        in_condition.append(ast.literal_eval(linesplit[0]))

                    except ValueError:
                        raise ValueError(f"{linesplit[0]} is not defined")

                elif re.match("^eat seed if .+$", code[line]):
                    if in_condition:
                        for x in range(3, len(linesplit)):
                            if linesplit[x] == "it":
                                linesplit[x] = str(in_condition[-1])
                            elif linesplit[x] in variables:
                                linesplit[x] = str(variables[linesplit[x]])

                        evaluate_condition = self.condition(" ".join(linesplit[3:]))
                        if evaluate_condition and evaluate_condition != 69:
                            line += 1
                            del in_condition[-1]
                            continue
                        else:
                            while True:
                                line += 1
                                linesplit = list(code[line])

                                if "#" in linesplit:
                                    del linesplit[linesplit.index("#"):]

                                if not linesplit or not self.removeall(linesplit, " "):
                                    line += 1
                                    continue

                                while linesplit[0] == " " or linesplit[0] == "\t":
                                    del linesplit[0]

                                while linesplit[-1] == " " or linesplit[0] == "\t":
                                    del linesplit[-1]

                                code[line] = "".join(linesplit)
                                if re.match("^[^ ]+ no longer desires seed$", code[line]):
                                    line += 1
                                    break
                                elif re.match("^eat seed if .+$", code[line]):
                                    break
                                elif code[line] == "throw seed away":
                                    line += 1
                                    break
                            continue
                    else:
                        while True:
                            line += 1
                            linesplit = list(code[line])

                            if "#" in linesplit:
                                del linesplit[linesplit.index("#"):]

                            if not linesplit or not self.removeall(linesplit, " "):
                                line += 1
                                continue

                            while linesplit[0] == " " or linesplit[0] == "\t":
                                del linesplit[0]

                            while linesplit[-1] == " " or linesplit[0] == "\t":
                                del linesplit[-1]

                            code[line] = "".join(linesplit)
                            if re.match("^[^ ]+ no longer desires seed$", code[line]):
                                break
                        continue

                elif code[line] == "throw seed away":
                    if in_condition:
                        line += 1
                        del in_condition[-1]
                        continue
                    else:
                        while True:
                            line += 1
                            linesplit = list(code[line])

                            if "#" in linesplit:
                                del linesplit[linesplit.index("#"):]

                            if not linesplit or not self.removeall(linesplit, " "):
                                line += 1
                                continue

                            while linesplit[0] == " " or linesplit[0] == "\t":
                                del linesplit[0]

                            while linesplit[-1] == " " or linesplit[0] == "\t":
                                del linesplit[-1]

                            code[line] = "".join(linesplit)
                            if re.match("^[^ ]+ no longer desires seed", code[line]):
                                line += 1
                                break
                        continue

                elif re.match("^[^ ]+ no longer desires seed$", code[line]):
                    line += 1
                    continue

                # Raises an error if the line doesn't match any of the above cases
                else:
                    raise SyntaxError(f"\"{code[line]}\" is not defined")

                line += 1
        return 0


BirbLang_Program = BirbLang("""
hatch egg
new birb input is mimic
input desires seed
eat seed if input is as floofy as "A programming language is a formal language, which comprises a set of instructions that produce various kinds of output."
    squawk "A programming language is a formal language, which comprises a set of instructions that produce various kinds of output."
input no longer desires seed
slep
""")
BirbLang_Program.evaluate()
