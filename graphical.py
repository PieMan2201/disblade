import getch
import signal

class Display(object):
    def __init__(self, dims):
        self.width = dims[0]
        self.height = dims[1]
        self.matrix = []

    def gen_matrix(self, displayMatrix, dims):
        for x in range(0, dims[0]):
            horizontal = []
            for y in range(0, dims[1]):
                horizontal.append(0)
            displayMatrix.append(horizontal)
        return displayMatrix

    def draw_display(self):
        outputStr = ""
        for y in range(0, self.height):
            horizontal = []
            for x in range(0, self.width):
                output = self.matrix[x][y]
                horizontal.append(str(output) if output != 0 else " ")
            outputStr += "".join(horizontal) + "#\n"
        return outputStr + ("#" * (len(horizontal) + 1))

    def write(self, x, y, char):
        if self.matrix == []:
            self.matrix = self.gen_matrix(self.matrix, [self.width, self.height])
        char = str(char)
        for z in range(0, len(char)): # a "char" should really be one character but oh well
            self.matrix[x+z][y] = char[z]

    def clear(self):
        self.matrix = self.gen_matrix([], (self.width, self.height))

    def user_input(self, x, y, startStr, response=""):
        keypressed = getch.getch()
        response += keypressed
        if keypressed != "\n":
            self.write(x, y, str(startStr + response))
        return response, keypressed

    def get_key(self, timeout=0.0001):
        def handler():
            raise Exception("timeout")

        #weird alarm stuff
        signal.signal(signal.SIGALRM, handler)
        key = chr(0)
        try:
            signal.setitimer(signal.ITIMER_REAL, timeout) 
            try:
                key = getch.getch()
                if ord(key) == 27:
                    key = getch.getch()
                    key = getch.getch()
            except OverflowError:
                pass
            signal.setitimer(signal.ITIMER_REAL, 0)
        except Exception:
            pass
        return ord(key)
