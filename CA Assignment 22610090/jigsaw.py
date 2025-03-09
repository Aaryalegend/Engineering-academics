import heapq
from collections import Counter

class HuffmanCoding:
    def __init__(self):  # Corrected __init__ method
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, char, freq):  # Corrected __init__ method
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):  # Corrected __lt__ method
            return self.freq < other.freq

    def make_frequency_dict(self, text):
        return Counter(text)

    def make_heap(self, frequency):
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):
        encoded_text = ""
        for character in text:
            encoded_text += self.codes[character]
        return encoded_text

    def compress(self, text):
        frequency = self.make_frequency_dict(text)
        self.make_heap(frequency)
        self.merge_nodes()
        self.make_codes()

        encoded_text = self.get_encoded_text(text)
        return encoded_text

# Example usage
image_path = r"D:\Programming\Python\Aryan_Image.jpg"
output_path = r"D:\Programming\Python\Aryan_Output_Image.jpg"

resized_image = covert8bit(image_path, output_path)
tiles = dividetiles(resized_image)

angle = int(input("Enter the rotation angle (0, 90, 180, 270): "))
start_row = int(input("Enter the starting row of the tile group: "))
start_col = int(input("Enter the starting column of the tile group: "))
size = int(input("Enter the size of the tile group: "))

tiles = rotate(tiles, start_row, start_col, size, angle)
rotated_image = reconstruct_image(tiles)

rotated_image_output_path = r"D:\Programming\Python\Aryan_Rotated_Image.jpg"
cv2.imwrite(rotated_image_output_path, rotated_image)
print(f"Rotated image saved to {rotated_image_output_path}")

movements = f"tiles:rotate{angle},start_row{start_row},start_col{start_col},size{size}"
huffman = HuffmanCoding()
encoded_movements = huffman.compress(movements)
print(f"Encoded Movements: {encoded_movements}")
