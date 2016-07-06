import graphical
class Storage(graphical.Display):
    def write(self, x, y, thing):
        if self.matrix == []:
            self.matrix = self.gen_matrix(self.matrix, [self.width, self.height])
        self.matrix[x][y] = thing

    def read(self, x, y):
        return self.matrix[x][y]

    def gen_matrix(self, displayMatrix, dims):
        for x in range(0, dims[0]):
            horizontal = []
            for y in range(0, dims[1]):
                horizontal.append("?")
            displayMatrix.append(horizontal)
        return displayMatrix

    def draw_display(self):
        longestLength = 0
        for y in range(0, self.height):
            for x in range(0, self.width):
                if len(str(self.matrix[x][y])) > longestLength:
                    longestLength = len(str(self.matrix[x][y]))

        outputStr = ""
        for y in range(0, self.height):
            horizontal = []
            for x in range(0, self.width):
                output = str(self.matrix[x][y])
                while len(output) < longestLength + 1:
                    output += " "
                horizontal.append(output)
            outputStr += "".join(horizontal) + "\n"
        return outputStr[:-1]

    def evaluate(self):
        blacklist = {}

        for x in range(0, self.width):
            for y in range(0, self.height):
                value = self.matrix[x][y]
                if value != "?":
                    if (x,y) not in blacklist.keys():
                        blacklist[(x,y)] = set()
                    newX1 = (x+1) % self.width
                    valueToRight = self.matrix[newX1][y]
                    if (newX1,y) not in blacklist.keys():
                        blacklist[(newX1, y)] = set()
                    if valueToRight != "?" and (x,y) not in blacklist[(newX1, y)]:
                        newX2 = (x+2) % self.width
                        if (newX2,y) not in blacklist.keys():
                            blacklist[(newX2,y)] = set()
                        blacklist[(newX2, y)].add((x,y))
                        blacklist[(newX2, y)].add((newX1,y))
                        combinedValues = value * valueToRight
                        self.matrix[newX2][y] = combinedValues

                    newY1 = (y+1) % self.height
                    valueToDown = self.matrix[x][newY1]
                    if (x,newY1) not in blacklist.keys():
                        blacklist[(x, newY1)] = set()
                    if valueToDown != "?" and (x,y) not in blacklist[(x,newY1)]:
                        newY2 = (y+2) % self.height
                        if (x,newY2) not in blacklist.keys():
                            blacklist[(x,newY2)] = set()
                        blacklist[(x, newY2)].add((x,y))
                        blacklist[(x, newY2)].add((x,newY1))
                        combinedValues = value + valueToDown
                        self.matrix[x][newY2] = combinedValues