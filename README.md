# HuffmanEncoder
REST API built using Django that compresses a text message using Huffman Encoding algorithm and extracts the original message from a given compressed message and key

Huffman Encoding is a lossless compression technique that assigns a unique binary code to each distinct character in the message based on the frequency of occurrence of each character. More frequenct characters have shorter codes and less frequent characters haver longer codes. These codes are assigned using a greedy algorithm highlighted below:

<ul>
<li>For each distinct character in the message we create a leaf node with frequency set to the number of occurrence of that character in the original message. All leaf nodes are inserted into a min-heap based priority queue.</li>

<li>While number of elements in the heap is greater than one, we extract two nodes with lowest frequency, create a new internal node with frequency set to the sum of the extracted nodes frequency, make the extracted nodes the left and right child of this new node and insert it back.</li>

<li>The last remaining node is the root of the huffman tree and each leaf represents a unique character in the original message. The path from root to leaf denotes the encoding for that character (left branches representing 0 , right branches representing 1).</li>
</ul>

Once the codes have been assigned, compression and extraction is done as follows:

<ul>
<li>Using the above encoding the original message is converted to a bit string and this is then mapped to a string of characters in groups of 6 bits. The string resulting from this mapping is the compressed message.</li>

<li> Now the huffman tree is necessary to decode the message and so the preorder traversal of the tree is also returned as key_1 to the user. key_1 is later used to re-construct the huffman tree when the user wishes to extract the original message. We also return key_2 to the user which indicates the representation of internal nodes in the huffman tree as well as some padding bits that are added to the encoding.</li>

<li>To extract the original message from the comrpessed message, we first map each character back to 6 bits to get a bit string back and then re-construct the huffman tree using the keys. We then use it to get back the original message.</li>
</ul>

<b><i>
The algorithm performs best when messages consist of only a limited number of distinct characters or when there is a lot of repetition of certain characters than others. Ex. DNA protein sequences, list of phone numbers.
</i></b>

##Encode Message:
  Send a <b>GET</b> request to <b>127.0.0.1:8000/encode/</b> with the following parameters:
  
  <i>'message':</i> Message to be compressed
  
  This returns the following:
  
  <i>'compressedMessage' , 'key_1' , 'key_2' , 'compressionEfficieny'</i>

##Decode Message:
Send a <b>GET</b> request to <b>127.0.0.1:8000/decode/</b> with the following parameters:

<i>'compressedMessage' , 'key_1' , 'key_2'</i>

These you will get when you make a encode request. This returns the following:

<i>'extractedMessage' :</i> Original message


## Issues / Future Improvements
<ul>

<li> While converting the encoded bit string to characters, the current version maps the bits in groups of 6. A more efficient solution would do this in groups of 8 but then certain values in the range (0-255) map to characters that cannot be eaisly passed in URLs, for example '\x15' and so I have used only 64 characters presently that don't cause such a problem.</li>

<li> Reduction in overhead for storing the keys</li>





