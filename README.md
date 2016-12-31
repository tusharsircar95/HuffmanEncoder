# HuffmanEncoder
REST API built using Django that compresses a text message using Huffman Encoding algorithm and extract the original message from a given compressed message and key

Huffman Encoding is a lossless compression technique that assigns a unique binary code to each distinct character in the message based on the frequency of occurrence of each character. More frequenct characters have shorter codes and less frequently characters haver longer codes. These codes are assigned using a greedy algorithm highlighted below:

<ul>
<li>For each distinct character in the message we create a leaf node with frequency set to the number of occurrence of that character in the original message. All leaf nodes are inserted into a min-heap based priority queue</li>

<li>While number of elements in the heap is greater than one, we extract two nodes with lowest frequency, create a new internal node with frequency set to the sum of the extracted nodes frequency, make the extract nodes the let and right child of this new node and insert it back.</li>

<li>The last remaining node is the root of the huffman tree and each leaf represents a unique character in the original message. The path from root to leaf denotes the encoding for that character (left 0 , right 1).</li>

<li>The entire message is then converted to a bit string and this is then mapped to characters in groups of 6 bits. Also the pre-order traversal of the huffman tree is used while extracting to re-construct the huffman tree.</li>
</ul>

##Encode Message:
  Send a <b>GET</b> request to <b>127.0.0.1:8000/encode/</b> with the following parameters:
  
  <i>'message':</i> Message to be compressed
  
  This returns the following:
  
  <i>'compressedMessage' , 'key_1' , 'key_2' , 'compressionEfficieny'</i>

##Decode Message:
Send a GET request to 127.0.0.1:8000/decode/ with the following parameters:

<i>'compressedMessage' , 'key_1' , 'key_2'</i>

These you will get when you make a encode request. This returns the following:

<i>'extractedMessage' :</i> Original message
