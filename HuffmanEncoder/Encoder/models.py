from django.db import models

# Create your models here.

class Encoding(models.Model):
    compressedMessage = models.TextField()
    key_1 = models.TextField()
    key_2 = models.TextField(null=True)
    compressionEfficiency = models.FloatField(null=True)

    def __init__(self,compressedMessage,key_1,key_2,compressionEfficiency=None):
        self.compressedMessage = compressedMessage
        self.key_1 = key_1
        self.key_2 = key_2
        if (compressionEfficiency is not None):
            self.compressionEfficiency = compressionEfficiency

    def __str__(self):
        return 'Compressed: ' + self.compressedMessage + ', Key_1: ' + self.key_1 + ', Key_2: ' + self.key_2

    def isValid(self):
        if self.compressedMessage is None or self.key_1 is None or self.key_2 is None:
            return False
        if len(self.key_2) != 2 and (self.key_2 != 'ss'):
            return False
        if len(self.compressedMessage) <= 0:
            return False
        return True


class ExtractedMessage(models.Model):
    extractedMessage = models.TextField()

    def __init__(self,extractedMessage):
        self.extractedMessage = extractedMessage

    def __str__(self):
        return self.extractedMessage