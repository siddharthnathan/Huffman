#!/usr/bin/env bash

# Encode story.txt
time python3 huffman.py -e story.txt -o story.huff

# Decode story.txt
time python3 huffman.py -d story.huff -o story_.txt

# Find Differences
./diff.sh story.txt story_.txt

#Find Compression Ratio
echo "Compression Ratio"
expr $(ls -l story.txt | awk '{ print $5 }')/$(ls -l story.huff | awk '{ print $5 }') | bc -l


# Encode story_1.txt
time python3 huffman.py -e story_1.txt -o story_1.huff

# Decode story_1.txt
time python3 huffman.py -d story_1.huff -o story_1_.txt

# Find Differences
./diff.sh story_1.txt story_1_.txt

#Find Compression Ratio
echo "Compression Ratio"
expr $(ls -l story_1.txt | awk '{ print $5 }')/$(ls -l story_1.huff | awk '{ print $5 }') | bc -l


# Encode story_2.txt
time python3 huffman.py -e story_2.txt -o story_2.huff

# Decode story_2.txt
time python3 huffman.py -d story_2.huff -o story_2_.txt

# Find Differences
./diff.sh story_2.txt story_2_.txt

#Find Compression Ratio
echo "Compression Ratio"
expr $(ls -l story_2.txt | awk '{ print $5 }')/$(ls -l story_2.huff | awk '{ print $5 }') | bc -l


