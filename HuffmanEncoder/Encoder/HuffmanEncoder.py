from .models import Encoding,ExtractedMessage
from .Heap import Heap
from .CompressionMap import CompressionMap


class Node:

    # Node of the huffman tree
    def __init__(self,character,freq):
        self.left = None
        self.right = None
        self.character = character
        self.freq = freq


class HuffmanTree:

    # Character to denote internal (non-leaf) nodes
    internalNodeMarker = '0'

    # Set value of internal node marker
    @classmethod
    def setInternalNodeMarker(cls,internalNodeMarker):
        cls.internalNodeMarker = internalNodeMarker

    # Find suitable internal node marker or return None
    @staticmethod
    def getInternalNodeMarker(message):
        options = '*_()<>ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        for option in options:
            if not option in message:
                return option
        return None

    # Returns pre-order traversal of huffman tree
    @staticmethod
    def getPreorder(root):
        if root is None:
            return ''
        return root.character + HuffmanTree.getPreorder(root.left) + HuffmanTree.getPreorder(root.right)

    # Construct the huffman tree from the given preorder traversal
    @staticmethod
    def reconstructHuffmanTree(preorder,index):
        if preorder[index[0]] != HuffmanTree.internalNodeMarker:
            index[0] = index[0] + 1
            return Node(preorder[index[0]-1],0)
        node = Node(HuffmanTree.internalNodeMarker,0)
        index[0] = index[0] + 1
        node.left = HuffmanTree.reconstructHuffmanTree(preorder,index)
        node.right = HuffmanTree.reconstructHuffmanTree(preorder,index)
        return node

    # Decode bit string using huffman tree
    @staticmethod
    def decodeMessage(root,bitEncoding):
        temp = root
        l = len(bitEncoding)
        message = ''
        i = 0
        while i < l:
            if temp.left is None and temp.right is None:
                message += temp.character
                temp = root
            else:
                if bitEncoding[i] == '0':
                    temp = temp.left
                else: temp = temp.right
                i = i + 1
        message += temp.character
        return message

    # Construct the huffman tree
    @staticmethod
    def getHuffmanTreeRoot(characterHeap):
        while characterHeap.heapSize > 1:
            n1 = characterHeap.extractMin()
            n2 = characterHeap.extractMin()
            n3 = Node(HuffmanTree.internalNodeMarker, n1.freq + n2.freq)
            n3.left = n1
            n3.right = n2
            characterHeap.insertHeap(n3)
        return characterHeap.heapArray[0]

    # Generate encodings for each character
    @staticmethod
    def getEncodings(huffmanTree, code, encodings):
        if (huffmanTree.left is None) and (huffmanTree.right is None):
            print(huffmanTree.character + ' - ' + code)
            encodings[huffmanTree.character] = code
        else:
            HuffmanTree.getEncodings(huffmanTree.left, code + '0', encodings)
            HuffmanTree.getEncodings(huffmanTree.right, code + '1', encodings)


class HuffmanEncoder:

    # Returns single character encoding
    @staticmethod
    def singleCharacterEncoding(message):
        compressionEfficiency = len(str(len(message)) + '   ') / len(message)
        return Encoding(compressedMessage=message[0],key_1=str(len(message)),key_2='ss',compressionEfficiency=compressionEfficiency)

    # Get count of all unique characters
    @staticmethod
    def getCharacterMap(message):
        characterMap = {}
        for char in message:
            if characterMap.get(char) is None:
                characterMap[char] = 1
            else:
                characterMap[char] += 1
        return characterMap

    @staticmethod
    def getCharacterHeap(characterMap):
        characterHeap = Heap()
        for character in characterMap:
            characterHeap.insertHeap(Node(character, characterMap[character]))
        return characterHeap

    @staticmethod
    def getPaddingSize(bitEncoding):
        l = (6 - (len(bitEncoding)%6))%6
        return l

    # Takes input message and returns an Encoding object
    @staticmethod
    def compressMessage(message):

        # Decide internal node marker
        internalNodeMarker = HuffmanTree.getInternalNodeMarker(message)
        if internalNodeMarker is None:
            return None

        HuffmanTree.setInternalNodeMarker(internalNodeMarker)

        # Generate character map
        characterMap = HuffmanEncoder.getCharacterMap(message)

        # Handle case of single unique character
        if len(characterMap) == 1:
            return HuffmanEncoder.singleCharacterEncoding(message)

        # Generate character heap
        characterHeap = HuffmanEncoder.getCharacterHeap(characterMap)

        # Construct the huffman tree and get its root node
        huffmanTreeRoot = HuffmanTree.getHuffmanTreeRoot(characterHeap)

        # Generate huffman tree encodings for each character
        encodings = {}
        HuffmanTree.getEncodings(huffmanTreeRoot,'',encodings)

        # Translate message to bit encodings using the huffman codes
        bitEncoding = ''
        for c in message:
            bitEncoding += encodings[c]

        # Add 0 padding to make number of bits divisible by 6
        padding = HuffmanEncoder.getPaddingSize(bitEncoding)
        for i in range(0,padding):
            bitEncoding += '0'

        # Generate compressed message
        compressedMessage = ''
        noOfChunks = round(len(bitEncoding)/6)
        CompressionMap.setupMap()
        for i in range(0,noOfChunks):
            compressedMessage += CompressionMap.convertBinaryToCharacter(bitEncoding[(i*6):((i*6)+6)])

        # Generate key
        preorder = HuffmanTree.getPreorder(huffmanTreeRoot)
        key_1 = preorder
        key_2 = str(padding) + internalNodeMarker

        # Generate Compression Efficieny
        compressionEfficiency = len(key_1 + key_2 + compressedMessage)/len(message)
        return Encoding(compressedMessage=compressedMessage,key_1=key_1,key_2=key_2,compressionEfficiency=compressionEfficiency)

    @staticmethod
    def extractMessage(encoding):

        # Handle single character case
        if encoding.key_2 == 'ss':
            return ExtractedMessage(extractedMessage=(encoding.compressedMessage[0] * int(encoding.key_1)))

        # Get necessary data from the passed encoding
        [preorder,padding,internalNodeMarker] = [encoding.key_1,encoding.key_2[0],encoding.key_2[1]]
        HuffmanTree.setInternalNodeMarker(internalNodeMarker)
        huffmanTreeRoot = HuffmanTree.reconstructHuffmanTree(preorder,[0])

        # Transalte message to a bit string
        CompressionMap.setupMap()
        bitEncoding = ''
        for m in encoding.compressedMessage:
            bitEncoding += CompressionMap.convertCharacterToBinary(m)
        bitEncoding = bitEncoding[0:(len(bitEncoding)-int(padding))]

        # Decode the bit string
        message = HuffmanTree.decodeMessage(huffmanTreeRoot,bitEncoding)

        return ExtractedMessage(message)

