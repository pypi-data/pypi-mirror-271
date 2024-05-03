def armenian_latin_to_armenian_hy(input_string):

    word_chars = list(input_string)

    # exception
    if word_chars[0] == "o" and word_chars[1] == "d" and len(word_chars) == 2:
        word_chars = ["օդ"]

    for index, _ in enumerate(word_chars):

        if (
            index < len(word_chars) - 1
            and word_chars[index] == "T"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Թ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "T"
            and word_chars[index + 1] == "s"
        ):
            word_chars[index] = "Ծ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "Z"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ծ"
            word_chars[index + 1] = ""

        elif index < len(word_chars) - 1 and (
            word_chars[index] == "t" and word_chars[index + 1] == "z"
        ):
            word_chars[index] = "ծ"
            word_chars[index + 1] = ""

        elif index < len(word_chars) - 1 and (
            word_chars[index] == "g" and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "ծ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "T"
            and word_chars[index + 1] == "z"
        ):
            word_chars[index] = "Ծ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "G"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ծ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "R"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ր"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "O"
            and word_chars[index + 1] == "o"
        ):
            word_chars[index] = "Ու"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "O"
            and word_chars[index + 1] == "w"
        ):
            word_chars[index] = "Ու"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "o"
            and word_chars[index + 1] == "o"
        ):
            word_chars[index] = "ու"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "O"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "O"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "o"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "o"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "G"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Ղ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "g"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "ղ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "K"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Խ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "D"
            and word_chars[index + 1] == "z"
        ):
            word_chars[index] = "Ձ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "S"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Շ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "C"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Ճ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "Z"
            and word_chars[index + 1] == "H"
        ):
            word_chars[index] = "Ժ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "Z"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Ժ"
            word_chars[index + 1] = ""

        elif word_chars[index] == "@":
            word_chars[index] = "ը"

        # lower case chars
        elif index < len(word_chars) - 1 and (
            word_chars[index] == "t"
            and word_chars[index + 1] == "z"
            and word_chars[index + 2] == "’"
        ):
            word_chars[index] = "ծ"
            word_chars[index + 1] = ""
            word_chars[index + 2] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "z"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "ծ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "o"
            and word_chars[index + 1] == "o"
        ):
            word_chars[index] = "ու"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "t"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "թ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "t"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "թ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "T"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Թ"
            word_chars[index + 1] = ""

        elif index < len(word_chars) - 1 and (
            word_chars[index] == "t" and word_chars[index + 1] == "s"
        ):
            word_chars[index] = "ծ"
            word_chars[index + 1] = ""

        elif index < len(word_chars) - 1 and (
            word_chars[index] == "c" and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "ծ"
            word_chars[index + 1] = ""

        elif index < len(word_chars) - 1 and (
            word_chars[index] == "C" and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ծ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "r"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "ռ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "z"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "ժ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "k"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "խ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "d"
            and word_chars[index + 1] == "z"
        ):
            word_chars[index] = "ձ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "g"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "ղ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "s"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "շ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "c"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "չ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "e"
            and word_chars[index + 1] == "v"
        ):
            word_chars[index] = "և"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "v"
            and word_chars[index + 1] == "o"
        ):
            word_chars[index] = "ո"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "e"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "է"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "e"
            and word_chars[index + 1] != "’"
        ):
            word_chars[index] = "ե"

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "u"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "ը"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "y"
            and word_chars[index + 1] == "a"
        ):
            word_chars[index] = "ը"

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "U"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ը"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "U"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ը"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "t"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "թ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "j"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "ճ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "p"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "փ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "E"
            and word_chars[index + 1] != "’"
        ):
            word_chars[index] = "Ե"

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "E"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Է"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "J"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ճ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars)
            and word_chars[index] == "R"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Ռ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "P"
            and word_chars[index + 1] == "’"
        ):
            word_chars[index] = "Փ"
            word_chars[index + 1] = ""

        elif (
            index < len(word_chars) - 1
            and word_chars[index] == "P"
            and word_chars[index + 1] == "h"
        ):
            word_chars[index] = "Փ"
            word_chars[index + 1] = ""

        elif word_chars[index] == "r":
            word_chars[index] = "ր"

        elif word_chars[index] == "L":
            word_chars[index] = "Լ"

        elif word_chars[index] == "x":
            word_chars[index] = "խ"

        elif word_chars[index] == "X":
            word_chars[index] = "Խ"

        # ??????
        elif word_chars[index] == "y":
            word_chars[index] = "ը"

        elif word_chars[index] == "z":
            word_chars[index] = "զ"

        elif word_chars[index] == "a":
            word_chars[index] = "ա"

        elif word_chars[index] == "b":
            word_chars[index] = "բ"

        elif word_chars[index] == "g":
            word_chars[index] = "գ"

        elif word_chars[index] == "d":
            word_chars[index] = "դ"

        elif word_chars[index] == "o":
            word_chars[index] = "ո"

        elif word_chars[index] == "U":
            word_chars[index] = "Ու"

        elif word_chars[index] == "u":
            word_chars[index] = "ու"

        elif word_chars[index] == "Z":
            word_chars[index] = "Զ"

        elif word_chars[index] == "i":
            word_chars[index] = "ի"

        elif word_chars[index] == "l":
            word_chars[index] = "լ"

        elif word_chars[index] == "k":
            word_chars[index] = "կ"

        elif word_chars[index] == "h":
            word_chars[index] = "հ"

        elif word_chars[index] == "m":
            word_chars[index] = "մ"

        #!!!!
        elif word_chars[index] == "y":
            word_chars[index] = "յ"

        elif word_chars[index] == "n":
            word_chars[index] = "ն"

        elif word_chars[index] == "u":
            word_chars[index] = "ո"

        elif word_chars[index] == "p":
            word_chars[index] = "պ"

        elif word_chars[index] == "W":
            word_chars[index] = "Ւ"

        elif word_chars[index] == "w":
            word_chars[index] = "ւ"

        elif word_chars[index] == "R":
            word_chars[index] = "Ռ"

        elif word_chars[index] == "j":
            word_chars[index] = "ջ"

        elif word_chars[index] == "v":
            word_chars[index] = "վ"

        elif word_chars[index] == "t":
            word_chars[index] = "տ"

        elif word_chars[index] == "c":
            word_chars[index] = "ց"

        elif word_chars[index] == "q":
            word_chars[index] = "ք"

        elif word_chars[index] == "f":
            word_chars[index] = "ֆ"

        # Higher case letters here.

        elif word_chars[index] == "A":
            word_chars[index] = "Ա"

        elif word_chars[index] == "B":
            word_chars[index] = "Բ"

        elif word_chars[index] == "G":
            word_chars[index] = "Գ"

        elif word_chars[index] == "D":
            word_chars[index] = "Դ"

        elif word_chars[index] == "J":
            word_chars[index] = "Ջ"

        elif word_chars[index] == "I":
            word_chars[index] = "Ի"

        elif word_chars[index] == "K":
            word_chars[index] = "Կ"

        elif word_chars[index] == "H":
            word_chars[index] = "Հ"

        elif word_chars[index] == "M":
            word_chars[index] = "Մ"

        # !!!
        elif word_chars[index] == "Y":
            word_chars[index] = "Ը"  # Ը

        elif word_chars[index] == "N":
            word_chars[index] = "Ն"

        elif word_chars[index] == "P":
            word_chars[index] = "Պ"

        elif word_chars[index] == "V":
            word_chars[index] = "Վ"

        elif word_chars[index] == "T":
            word_chars[index] = "Տ"

        elif word_chars[index] == "C":
            word_chars[index] = "Ց"

        elif word_chars[index] == "Q":
            word_chars[index] = "Ք"

        elif word_chars[index] == "O":
            word_chars[index] = "Ո"

        elif word_chars[index] == "F":
            word_chars[index] = "Ֆ"

        elif word_chars[index] == "S":
            word_chars[index] = "Ս"

        elif word_chars[index] == "s":
            word_chars[index] = "ս"

        elif word_chars[index] == "T":
            word_chars[index] = "Տ"

        elif word_chars[index] == "t":
            word_chars[index] = "տ"

    word_chars = [i for i in word_chars if i]

    return "".join(word_chars)
