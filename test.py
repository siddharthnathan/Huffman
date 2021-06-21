# Test functions goes here
import unittest

from huffman import encode, decode

class TestHuffman(unittest.TestCase):
	# write all your tests here
	# function name should be prefixed with 'test'

	def test_encode(self):
		encode("story.txt", "story.huff")
		assert True

	def test_decode(self):
		decode("story.huff", "story_.txt")
		assert True

	def test_encode(self):
		encode("story_1.txt", "story_1.huff")
		assert True

	def test_decode(self):
		decode("story_1.huff", "story_1_.txt")
		assert True

	def test_encode(self):
		encode("story_2.txt", "story_2.huff")
		assert True

	def test_decode(self):
		decode("story_2.huff", "story_2_.txt")
		assert True


if __name__ == '__main__':
	unittest.main()
