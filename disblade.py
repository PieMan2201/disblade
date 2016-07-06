#TODO: Optimize this stuff!
#Performance is fairly awful
#Current high score: 256329

from graphical import Display
from execution import Storage
from time import sleep, time
from sys import argv

def clear():
    print(clrfile, end="")

def creation(codefile):
    #set params for display and storage
    display = 0
    storage = 0

    for line in codefile[:2]:
        if "DISPLAY" in line:
            size = line.split(" ")[-1]
            dims = size.split(",")
            display = Display([int(dims[0]), int(dims[1])])
        elif "STORAGE" in line:
            size = line.split(" ")[-1]
            dims = size.split(",")
            storage = Storage([int(dims[0]), int(dims[1])])
    
    return display, storage

def eval_type(thing):
    if '"' in thing:
        return str(thing[1:-1])
    elif "STORAGE" in thing:
        crds = eval_locn(thing)
        return storage.read(int(crds[0]), int(crds[1]))
    else:
        return float(thing)

def eval_locn(loc):
    #returns tuple of coords from input of "x,y"
    str_crds = loc[8:-1].split(",")
    if "STORAGE" in str_crds[0] or "DISPLAY" in str_crds[0]:
        str_crds = ",".join(str_crds)
        str_crds = str_crds.split("),")
        str_crds[0] += ")"
        crdx = eval_locn(str_crds[0])
        crdy = eval_locn(str_crds[1])
        crdx = storage.read(crdx[0], crdx[1])
        crdy = storage.read(crdy[0], crdy[1])
    else:
        crdx = int(str_crds[0])
        crdy = int(str_crds[1])
    return crdx, crdy

def eval_from(src, drn):
    #evaluate the "from" statement, setting source equal to drain
    if "DISPLAY" in src:
        src = 0
    elif "STORAGE" in src:
        crds = eval_locn(src)
        src = storage.read(int(crds[0]), int(crds[1]))
    elif "INPUT" in src:
        inputParams = src[6:-1].split(",")
        crdx = inputParams[0]
        crdy = inputParams[1]
        inputStr = inputParams[2]
        inputStr = eval_type(inputStr)
        inputDone = False
        response = ""
        display.write(int(crdx), int(crdy), inputStr)

        while not inputDone:
            clear()
            print(display.draw_display())
            response, pressed = display.user_input(int(crdx), int(crdy), inputStr, response)
            print(display.draw_display())
            if pressed == "\n":
                inputDone = True
        src = response[:-1]
    elif "KYPRS" in src:
        pressed = display.get_key()
        src = pressed
    elif "TIME" in src:
        src = time() * 10 #deciseconds, remember?
    else: #some kind of data type
        src = eval_type(src)

    if "DLY" in drn:
        sleep(src * 0.1)
    else:
        drnCrds = eval_locn(drn)
        if "DISPLAY" in drn:
            display.write(int(drnCrds[0]), int(drnCrds[1]), src)
        elif "STORAGE" in drn:
            storage.write(int(drnCrds[0]), int(drnCrds[1]), src)

def eval_cond(cnd):
    #takes condition of form "x{cmp}y" and returns appropriate bool
    compares = [
        "=",
        "<",
        ">"
    ]
    cndCompare = " "
    for compare in compares:
        if compare in cnd:
            cndCompare = compare
            x,y = cnd.split(cndCompare)
            break
    if "STORAGE" in x:
        crds = eval_locn(x)
        x = storage.read(int(crds[0]), int(crds[1]))
    else:
        x = eval_type(x)
    if "STORAGE" in y:
        crds = eval_locn(y)
        y = storage.read(int(crds[0]), int(crds[1]))
    else:
        y = eval_type(y)
    if cndCompare == "=":
        if x == y:
            return True
        else:
            return False
    elif cndCompare == "<":
        if x < y:
            return True
        else:
            return False
    elif cndCompare == ">":
        if x > y:
            return True
        else:
            return False
    else:
        return False


def eval_whle(line):
    global lineNum
    condition = line[4:-2]

    newLineNum = lineNum + 1
    startOfWhile = newLineNum
    starts = 1
    while newLineNum < len(codefile):
        newCodeLine = codefile[newLineNum]
        if "{" in newCodeLine:
            starts += 1
        if "}" in newCodeLine:
            starts -= 1
        if starts == 0:
            endOfWhile = newLineNum
            break
        newLineNum += 1
    lineNum = startOfWhile
    while eval_cond(condition):
        while lineNum < endOfWhile:
            interpret(codefile[lineNum])
            lineNum += 1
        lineNum = startOfWhile
    else:
        lineNum = endOfWhile

def eval_ifst(line):
    global lineNum
    condition = line[3:-2]

    newLineNum = lineNum + 1
    startOfIf = newLineNum
    starts = 1
    while newLineNum < len(codefile):
        newCodeLine = codefile[newLineNum]
        if "{" in newCodeLine:
            starts += 1
        if "}" in newCodeLine:
            starts -= 1
        if starts == 0:
            endOfIf = newLineNum
            break
        newLineNum += 1
    lineNum = startOfIf
    if eval_cond(condition):
        interpret(codefile[lineNum])
    else:
        lineNum = endOfIf

def halt():
    global startExecutionTime
    print(time() - startExecutionTime)
    raise SystemExit

def interpret(line):
    global lineNum
    #commands are redirected to their appropriate functions from here
    if " from " in line:
        drn, src = line.split(" from ")
        eval_from(src, drn)
    elif "EVALUATE" in line:
        #evaluate whatever (default=storage)
        if "DISPLAY" in line:
            clear()
            print(display.draw_display())
        else: 
            storage.evaluate()
    elif "CLEAR" in line:
        if "STORAGE" in line:
            storage.clear()
        else:
            display.clear()
    elif "WHL(" in line:
        eval_whle(line)
    elif "IF(" in line:
        eval_ifst(line)
    elif "HALTCODE" in line:
        halt()


if __name__ == "__main__":
    startExecutionTime = time()
    clrfile = open("clear").read()
    lineNum = 0
    oldcodefile = open(argv[1]).read().split("\n")
    codefile = []
    for line in oldcodefile:
        if len(line) > 0:
            if line == " ":
                continue
            elif line[0] == "~":
                continue
            while " " == line[0]:
                line = line[1:]
            codefile.append(line)
    display, storage = creation(codefile)
    lineNum += 2
    while lineNum < len(codefile):
        interpret(codefile[lineNum])
        lineNum += 1
    halt()
