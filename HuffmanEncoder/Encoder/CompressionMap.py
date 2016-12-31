class CompressionMap:

    # A-Z a-z 0-9 $*
    map = {}
    reverseMap = {}
    # Sets up one-to-one mapping
    @classmethod
    def setupMap(cls):
        for i in range(97,123):
           cls.map[i-97] = chr(i)
           cls.reverseMap[chr(i)] = i-97
        for i in range(65,91):
            cls.map[26 + i - 65] = chr(i)
            cls.reverseMap[chr(i)] = 26+i-65
        for i in range(0,10):
            cls.map[52 + i] = str(i)
            cls.reverseMap[str(i)] = 52+i
        cls.map[62] = '$'
        cls.map[63] = '*'
        cls.reverseMap['$'] = 62
        cls.reverseMap['*'] = 63

    # Convert six bit code to alpha-numeric character
    @classmethod
    def convertBinaryToCharacter(cls,bitString):
        if len(bitString) != 6:
            print('ERROR: Passed bit string is not of length 6! ' + bitString)
        else:
            value = 0
            for i in range(5,-1,-1):
                if bitString[i] == '1':
                    value +=  2 ** (5-i)
            return cls.map[value]

    # Convert character to six bit code
    @classmethod
    def convertCharacterToBinary(cls,character):
        value =  cls.reverseMap[character]
        bitEncoding = ''
        for i in range(5,-1,-1):
            if (2**i) <= value:
                value = value - (2**i)
                bitEncoding += '1'
            else:
                bitEncoding += '0'
        return bitEncoding