import heapq
import numpy as np

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        # defining comparators less_than and equals
        def __lt__(self, other):
            return self.freq < other.freq

        def __eq__(self, other):
            if(other == None):
                return False
            if(not isinstance(other, HeapNode)):
                return False
            return self.freq == other.freq


    def make_frequency_dict(self, stream):
        frequency = {}
        for pixex in stream:
            if not int(pixex) in frequency:
                frequency[int(pixex)] = 0
            frequency[int(pixex)] += 1
        return frequency

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while(len(self.heap)>1):
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)


    def make_codes_helper(self, root, current_code):
        if(root == None):
            return

        if(root.char != None):
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")


    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_stream(self, stream):
        encoded_stream = ""
        print(self.codes)
        for pixel in stream:
            encoded_stream += self.codes[pixel]
        return encoded_stream

    def encode(self, stream):
        frequency = self.make_frequency_dict(stream)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_stream = self.get_encoded_stream(stream)

        return encoded_stream

    def decode_stream(self, encoded_stream):
        current_code = ""
        decoded_stream = np.array([])

        for bit in encoded_stream:
            current_code += bit
            if(current_code in self.reverse_mapping):
                pixel = self.reverse_mapping[current_code]
                decoded_stream = np.append(decoded_stream, pixel)
                current_code = ""
        return decoded_stream

    def decode(self, encoded_stream, ):
        return self.decode_stream(encoded_stream)