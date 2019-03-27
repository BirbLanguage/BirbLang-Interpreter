import re
import ast


class BirbLang:
    def __init__(self, program):
        self.program = program

    def removeAll(self, array, character):
        return [x for x in array if x != character]

    def evaluate(self):
        variables = {}
        data_types = ("string", "int", "float", "boolean", "complex", "list")
        code = self.program.split("\n")  # Splits code into each individual line

        # Checks to see if program can be executed and stopped successfully
        if "hatch egg" in code and "slep" in code:

            # Starts program at wherever the "break egg" line occurs
            line = code.index("hatch egg") + 1

            while code[line] != "slep":

                # Removes all comments and whitespace at the start and end of the line (easier to read that way)
                linesplit = list(code[line])

                if "#" in linesplit:
                    del linesplit[linesplit.index("#"):]

                if not linesplit or not self.removeAll(linesplit, " "):
                    line += 1
                    continue

                while linesplit[0] == " ":
                    del linesplit[0]

                while linesplit[-1] == " ":
                    del linesplit[-1]

                code[line] = "".join(linesplit)

                linesplit = code[line].split(" ")

                # Outputs element at specific index of array (if possible)
                if re.match("^chirp\s.+\sat\s[0-9]+$", code[line]):
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
                elif re.match("^chirp\s.+$", code[line]):

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

                # Runs if the line is meant to declare a new variable (new birb variable_name is value)
                elif re.match("^new\sbirb\s[^\s]+\sis\s[^\s]+$", code[line]):
                    try:
                        # Converts string to its appropriate data type
                        variables[linesplit[2]] = ast.literal_eval(linesplit[4])
                    except ValueError:
                        if linesplit[4] == "mimic":  # Handles case where the line asks for user input
                            variables[linesplit[2]] = input(">>> ")
                        else:
                            raise ValueError(f"{variables[linesplit[2]]} is not a valid data type")

                # Checks if the line is "floof (variable)," and will increment it if possible
                elif re.match("^floof\s[^\s]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is int or type(variables[linesplit[1]]) is float:
                            variables[linesplit[1]] += 1
                        else:
                            raise ValueError(f"{variables[linesplit[1]]} cannot be incremented")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                elif re.match("^unfloof\s[^\s]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is int or type(variables[linesplit[1]]) is float:
                            variables[linesplit[1]] -= 1
                        else:
                            raise ValueError(f"{variables[linesplit[1]]} cannot be incremented")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Changes data type of variable if the line matches "(variable) is now (data_type)"
                elif re.match("^breed\sof\s[^\s]+\sis\snow\s[^\s]+$", code[line]):
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
                                variables[linesplit[2]] = list(variables[linesplit[2]])
                            elif linesplit[5] == "complex":
                                variables[linesplit[2]] = complex(variables[linesplit[2]])
                            elif linesplit[5] == "boolean":
                                variables[linesplit[2]] = bool(variables[linesplit[2]])
                        else:
                            raise ValueError(f"{linesplit[5]} is not a valid data type")
                    else:
                        raise NameError(f"{linesplit[2]} is not defined")

                # Outputs the data type of a variables/value if the line matches "breed of (variable/value)"
                elif re.match("^breed\sof\s[^\s]+$", code[line]):
                    try:
                        print(type(ast.literal_eval(linesplit[2])))

                    except ValueError:
                        if linesplit[2] in variables:
                            print(type(variables[linesplit[2]]))
                        else:
                            raise NameError(f"{linesplit[2]} is not defined")

                elif re.match("^[^\s]+\sat\s[0-9]+\sis\snow\s[^\s]+$", code[line]):
                    if linesplit[0] in variables:
                        if type(ast.literal_eval(linesplit[5])) is type(variables[linesplit[0]][int(linesplit[2])]):
                            variables[linesplit[0]][int(linesplit[2])] = ast.literal_eval(linesplit[5])
                        else:
                            raise ValueError(
                                f"{type(variables[linesplit[0]])} cannot be given value of type {type(ast.literal_eval(linesplit[3]))}")
                    else:
                        raise NameError(f"{linesplit[0]} is not defined")

                # Changes value of variable (if possible) if the line matches "(variable) is now (value)"
                elif re.match("^[^\s]+\sis\snow\s[^\s]+$", code[line]):
                    if linesplit[0] in variables:
                        if type(ast.literal_eval(linesplit[3])) is type(variables[linesplit[0]]):
                            variables[linesplit[0]] = ast.literal_eval(linesplit[3])
                        else:
                            raise ValueError(
                                f"{type(variables[linesplit[0]])} cannot be given value of type {type(ast.literal_eval(linesplit[3]))}")
                    else:
                        raise NameError(f"{linesplit[0]} is not defined")

                elif re.match("^peck\s[^\s]+\sat\s[0-9]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            del variables[linesplit[1]][int(linesplit[3])]
                        else:
                            raise AttributeError(f"peck is not defined for type {type(variables[linesplit[1]])}")
                    else:
                        raise NameError(f"{variables[linesplit[1]]} is not defined")

                # Removes the last element of an array if the line matches "peck (variable)"
                elif re.match("^peck\s[^\s]+$", code[line]):
                    if linesplit[1] in variables:
                        try:
                            variables[linesplit[1]].pop()
                        except AttributeError:
                            raise AttributeError(f"peck for type {type(variables[linesplit[1]])} is not defined")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Inserts value into specific index of array
                elif re.match("^feed\s[^\s]+\s.+\sat\s[0-9]+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            variables[linesplit[1]].insert(int(linesplit[-1]), ast.literal_eval(
                                " ".join(linesplit[2:linesplit.index("at")])))
                        else:
                            raise AttributeError(f"feed is not defined for type {type(variables[linesplit[1]])}")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Appends a value to an array
                elif re.match("^feed\s[^\s]+\s.+$", code[line]):
                    if linesplit[1] in variables:
                        if type(variables[linesplit[1]]) is list:
                            variables[linesplit[1]].append(ast.literal_eval("".join(linesplit[2:])))
                        else:
                            raise AttributeError(f"peck for type {type(variables[linesplit[1]])} is not defined")
                    else:
                        raise NameError(f"{linesplit[1]} is not defined")

                # Raises an error if the line doesn't match any of the above cases
                else:
                    raise SyntaxError(f"{code[line]} is not defined")

                line += 1
        return 0


BirbLang_Program = BirbLang("""
hatch egg
new birb borb is [5,4,2]
feed borb 3 at 1
chirp borb at 1
borb at 1 is now 7
chirp borb at 1
chirp "hello world"
slep
""")
BirbLang_Program.evaluate()
