import os
import sys
import traceback
LOG_FLAG = True

msgStr = ""


def d(msg):
    global msgStr
    if (LOG_FLAG):
        if type(msg) == str:
            msgStr += (msg + '\n')
        else:
            msgStr += str(msg)
            msgStr += '\n'
        print(msg)


def e(error):
    errorStr = "\nERROR: " + str(error)
    global msgStr
    if (LOG_FLAG):
        msgStr += (errorStr + '\n')
        print(errorStr)
        msgStr += traceback.format_exc()
        print(traceback.format_exc())


def save():
    with open(getSavePath('LOG'), 'w') as f:
        f.write(msgStr)


def getSavePath(name):
    return os.path.join(sys.path[0], name)
