#!/usr/local/bin/python3
import sys
import argparse
import shutil
import ast
import os

    
# Create an Empty Dictionary to store the Huffman Codes for all Characters
huffman_codes = dict()

# Create an Empty List to store Pre-Order Traversal of Binary Search Tree
pre_order_list = []


# Definea Function to Convert Decimal to Binary
def decimalToBinary(n):
    return bin(n).replace("0b", "")

    
# Class for Node in Binary Tree
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.huff_code = ''
        

# Define a Function to Create & Return Pre-Order Traversal of BST as a List
def pre_order(root):

    if root:
        pre_order_list.append([root.key, root.value])
        pre_order(root.left)
        pre_order(root.right)

    return pre_order_list


# Define Function to Form Huffman Codes for the Node from BST
def form_huff_code(node, code, parent_node):

    if parent_node == None:

        if node.left == None and node.right == None:
            huffman_codes[node.key] = node.huff_code
        else:
            if node.left:
                form_huff_code(node.left, '0', node)
            if node.right:
                form_huff_code(node.right, '1', node)
    else:

        node.huff_code = parent_node.huff_code + str(code)

        if node.left == None and node.right == None:
            huffman_codes[node.key] = node.huff_code
        else:
            if node.left:
                form_huff_code(node.left, '0', node)
            if node.right:
                form_huff_code(node.right, '1', node)
                
    return huffman_codes


# Define Function to Convert Bit String to Characters
def contents_to_chars(data):
    characters = ''
    for i in range(0, len(data), 8):
        char_int = int(data[i:i+8], 2)
        characters += chr(char_int)
    return characters



# Define Function for Huffman Encoding
def encode(input_file, output_file):

    print("encoding ", input_file, output_file)

    ##### STEP 1: COUNTING FREQUENCIES #####
    
    # Create an Empty Dictionary to Store the Frequency of Occurring Characters in Input Text file
    char_freq_dict = dict()

    # Open Input Text File in Read mode
    input_txt_file = open(input_file, 'r')

    # Read Character by Character, Update the Dictionary & Close the Text file
    while True:

        char = input_txt_file.read(1)
        
        if not char:
            break
        else:

            if char not in char_freq_dict:
                char_freq_dict[char] = 1
            else:
                char_freq_dict[char] += 1

    input_txt_file.close()

    # Add EOF (~) key and value as 1
    char_freq_dict['~'] = 1
    

    ##### STEP 2: BUILDING ENCODING TREE #####

    # Sort the Dictionary using Keys
    char_freq_dict = dict(sorted(char_freq_dict.items()))
        
    # Sort the Dictionary using Values
    char_freq_sorted_list = sorted(char_freq_dict.items(), key = lambda x:x[1])
    char_freq_sorted_dict = dict(char_freq_sorted_list)

    # Find Left and Right Child for Root of Binary Tree
    left_child_key = char_freq_sorted_list[0][0]
    right_child_key = char_freq_sorted_list[1][0]
    left_child_value = char_freq_sorted_list[0][1]
    right_child_value = char_freq_sorted_list[1][1]

    # Create Root Node and Children of Binary Tree
    root = Node('~~', left_child_value + right_child_value)
    root.left = Node(left_child_key, left_child_value)
    root.right = Node(right_child_key, right_child_value)

    # Pop First 2 Elements from Dictionary
    char_freq_sorted_dict.pop(left_child_key)
    char_freq_sorted_dict.pop(right_child_key)

    # Modify the First Element of Dictionary
    char_freq_sorted_dict[root.key] = root.value
    

    # Until there is One Node in Encoding Tree
    ## Sort the Dictionary in Ascending order according to their Values
    ## Merge the First 2 Nodes in Dictionary, make Merged Node as Parent node with Combined Nodes as Children
    while(len(char_freq_sorted_dict) > 1):

        # Sort the Dictionary using Keys
        char_freq_sorted_dict = dict(sorted(char_freq_sorted_dict.items()))
        
        # Sort the Dictionary using Values
        char_freq_sorted_list = sorted(char_freq_sorted_dict.items(), key = lambda x:x[1])
        char_freq_sorted_dict = dict(char_freq_sorted_list)

        # Find Left and Right Child for Root of Binary Tree
        left_child_key = char_freq_sorted_list[0][0]
        right_child_key = char_freq_sorted_list[1][0]
        left_child_value = char_freq_sorted_list[0][1]
        right_child_value = char_freq_sorted_list[1][1]

        # Update Binary Tree
        if root.key == right_child_key and root.value == right_child_value:
        
            temp_node = Node('~~', left_child_value + right_child_value)
            temp_node.left = Node(left_child_key, left_child_value)
            temp_node.right = root
            root = temp_node

        elif root.key == left_child_key and root.value == left_child_value:
        
            temp_node = Node('~~', left_child_value + right_child_value)
            temp_node.right = Node(right_child_key, right_child_value)
            temp_node.left = root
            root = temp_node

        else:

            temp_node = Node('~~', left_child_value + right_child_value)
            temp_node.left = Node(left_child_key, left_child_value)
            temp_node.right = Node(right_child_key, right_child_value)
            temp_node_1 = Node('~~', root.value + temp_node.value)

            if temp_node.value > root.value:

                temp_node_1.left = root
                temp_node_1.right = temp_node

            else:

                temp_node_1.right = root
                temp_node_1.left = temp_node

            root = temp_node_1
            

        # Pop First 2 Elements from Dictionary
        char_freq_sorted_dict.pop(left_child_key)
        char_freq_sorted_dict.pop(right_child_key)

        # Modify the First Element of Dictionary
        char_freq_sorted_dict[root.key] = root.value

    # Open BST Text File in Write mode
    BST_txt_file = open('BST.txt', 'w')

    # Store the Pre-Order Traversal of Binary Search Tree in a Text file
    pre_order_list = pre_order(root)

    # Write the List into Text File & Close it
    BST_txt_file.write(str(pre_order_list))
    BST_txt_file.close()


    ##### STEP 3: BUILDING ENCODING MAP #####
    huffman_codes = form_huff_code(root, '', None)
    
    ##### STEP 4: ENCODING THE TEXTUAL DATA #####

    # Open Input Text File in Read mode
    input_txt_file = open(input_file, 'r')

    # Open Output Text File in Write mode
    with open(output_file, 'w') as output_txt_file:

        # Read Character by Character, Encode Character into Huff file & Close the Text Files
        encoded_char = ''
        while True:

            char = input_txt_file.read(1)
            
            if not char:
                break
            else:
                encoded_char = encoded_char + str(huffman_codes[char])

        # Add Encoded Symbol for EOF
        encoded_char = encoded_char + str(huffman_codes['~'])

        # Append Additional 0s to make Length of Bit String a Multiple of 8
        len_bit_string = len(encoded_char)
        num_of_zeros = 8 - (len_bit_string % 8)
        for i in range(num_of_zeros):
            encoded_char += str('0')

        # Find the Encoded Message 
        encoded_message = contents_to_chars(encoded_char)

        # Convert the Encoded Result into Bytes and write into HUFF file
        output_txt_file.write(encoded_message)
    
    # Close the Files
    input_txt_file.close()
    output_txt_file.close()



# Define Function for Huffman Decoding
def decode(input_file, output_file):

    print("decoding ", input_file, output_file)

    # Open BST Text File & Read Contents
    BST_text_file = open('BST.txt', 'r')
    pre_order_str = BST_text_file.read()

    # Convert the String of Nested List to a List & Close the BST File
    pre_order_list = ast.literal_eval(pre_order_str)
    BST_text_file.close()

    # Open the HUFF File and Read Contents & Close it
    input_huff_file = open(input_file, 'r')
    contents = input_huff_file.read()
    input_huff_file.close()

    # Initialise an Empty Bit String
    bit_string = ''

    # Convert the Contents into Bit String
    for i in range(len(contents)):

        # Read the Character and find its Corresponding Integer value
        char = contents[i]
        char_int = ord(char)

        # Find its Binary value
        char_bin = decimalToBinary(char_int)

        # Append 0s to make it 8 bits
        char_bin_rev = char_bin[::-1] 
        while len(char_bin_rev) < 8:
            char_bin_rev += '0'
        char_bin = char_bin_rev[::-1]

        # Append to Bit String
        bit_string += str(char_bin)

    # Open the Output File in Append Mode & Clear Previous Contents
    output_txt_file = open(output_file, 'a')
    output_txt_file.seek(0)
    output_txt_file.truncate()

    # Initialise Root Index
    root_index = 0

    # Until the end bit of Bit String is Encountered
    ## Decode the Encoded Bit Message
    for i in range(len(bit_string)):

        # Find the Character and Value of the Node and its Children
        node_index = root_index
        node_char = pre_order_list[node_index][0]
        node_value = pre_order_list[node_index][1]
        
        left_child_index = node_index + 1
        left_child_char = pre_order_list[left_child_index][0]
        left_child_value = pre_order_list[left_child_index][1]

        right_child_value = node_value - left_child_value
        for index in range(left_child_index + 1, len(pre_order_list)):
            if pre_order_list[index][1] == right_child_value:
                right_child_index = index
                break

        # Get the Bit from the Bit String
        bit = bit_string[i]

        # Decode the Bit Message
        if bit == '0':
            
            if pre_order_list[left_child_index][0] != '~~':
                char = pre_order_list[left_child_index][0]
                root_index = 0
                if char == '~':
                    output_txt_file.close()
                    break
                else:
                    output_txt_file.write(char)
                
            else:
                root_index = left_child_index

        else:

            if pre_order_list[right_child_index][0] != '~~':
                char = pre_order_list[right_child_index][0]
                root_index = 0
                if char == '~':
                    output_txt_file.close()
                    break
                else:
                    output_txt_file.write(char)
                
            else:
                root_index = right_child_index
        


def get_options(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Huffman compression.")
    groups = parser.add_mutually_exclusive_group(required=True)
    groups.add_argument("-e", type=str, help="Encode files")
    groups.add_argument("-d", type=str, help="Decode files")
    parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
    options = parser.parse_args()
    return options


if __name__ == "__main__":
    options = get_options()
    if options.e is not None:
        encode(options.e, options.o)
    if options.d is not None:
        decode(options.d, options.o)
