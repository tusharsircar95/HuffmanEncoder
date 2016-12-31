class Heap:

    def __init__(self):
        self.heapArray = []
        self.heapSize = 0

    @staticmethod
    def getLeft(x):
        return (2*x) + 1

    @staticmethod
    def getRight(x):
        return (2*x) + 2
    @staticmethod
    def getParent(x):
        return round((x-1)/2)


    def minHeapify(self,pos):
        minPos = pos
        left = Heap.getLeft(pos)
        right = Heap.getRight(pos)
        if left < self.heapSize and self.heapArray[minPos].freq > self.heapArray[left].freq:
            minPos = left
        if right < self.heapSize and self.heapArray[minPos].freq > self.heapArray[right].freq:
            minPos = right
        if pos != minPos:
            temp = self.heapArray[pos]
            self.heapArray[pos] = self.heapArray[minPos]
            self.heapArray[minPos] = temp
            self.minHeapify(minPos)

    def insertHeap(self,node):
        if len(self.heapArray) <= self.heapSize:
            self.heapArray.append(node)
        else:
            self.heapArray[self.heapSize] = node
        self.heapSize = self.heapSize + 1
        current = self.heapSize - 1
        while (current != 0) and self.heapArray[current].freq < self.heapArray[Heap.getParent(current)].freq:
            temp = self.heapArray[current]
            self.heapArray[current] = self.heapArray[Heap.getParent(current)]
            self.heapArray[Heap.getParent(current)] = temp
            current = Heap.getParent(current)

    def extractMin(self):
        temp = self.heapArray[0]
        self.heapArray[0] = self.heapArray[self.heapSize-1]
        self.heapSize = self.heapSize - 1
        if self.heapSize != 0:
            self.minHeapify(0)
        return temp




