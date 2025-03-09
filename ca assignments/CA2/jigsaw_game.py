import pygame
import numpy as np
import random
import heapq
from collections import defaultdict

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = (208, 208)
TILE_SIZE = 8
GRID_SIZE = 26
BACKGROUND_COLOR = (0, 0, 0)
TILE_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 0, 0)

# Pygame setup
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Jigsaw Puzzle Game")

# Huffman Node Class
class Node:
    def __init__(self, character, frequency):
        self.character = character
        self.frequency = frequency
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.frequency < other.frequency

# Huffman Tree Builder
def huffman_tree_builder(text):
    frequency_dict = defaultdict(int)
    for char in text:
        frequency_dict[char] += 1
    priority_queue = [Node(char, freq) for char, freq in frequency_dict.items()]
    heapq.heapify(priority_queue)
    while len(priority_queue) > 1:
        left_node = heapq.heappop(priority_queue)
        right_node = heapq.heappop(priority_queue)
        merged_node = Node(None, left_node.frequency + right_node.frequency)
        merged_node.left = left_node
        merged_node.right = right_node
        heapq.heappush(priority_queue, merged_node)
    return priority_queue[0]

# Code Mapping for Huffman Encoding
def code_mapping(root, prefix="", code_dict=None):
    if code_dict is None:
        code_dict = {}
    if root is None:
        return
    if root.character is not None:
        code_dict[root.character] = prefix
    code_mapping(root.left, prefix + "0", code_dict)
    code_mapping(root.right, prefix + "1", code_dict)
    return code_dict

# Compressing the moves
def compress_moves(moves_list):
    move_string = "".join(str(move) for move in moves_list)
    huffman_tree = huffman_tree_builder(move_string)
    encoding_map = code_mapping(huffman_tree)
    encoded_data = "".join(encoding_map[char] for char in move_string)
    return encoded_data, encoding_map

# Decompressing the moves
def decompress_moves(encoded_data, code_map):
    reverse_map = {code: char for char, code in code_map.items()}
    current_code = ""
    decoded_string = ""
    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_map:
            decoded_string += reverse_map[current_code]
            current_code = ""
    return decoded_string

# Matrix Chain Multiplication for optimizing rotations
def matrix_chain_mult(matrices):
    n = len(matrices)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            for k in range(i, j):
                cost = dp[i][k] + dp[k+1][j] + matrices[i][0] * matrices[k][1] * matrices[j][1]
                dp[i][j] = min(dp[i][j], cost)
    return dp[0][n-1]

# Tile Class
class Tile:
    def __init__(self, id, image):
        self.id = id
        self.image = image
        self.rotation = 0
    
    def rotate(self):
        self.rotation = (self.rotation + 90) % 360
        self.image = pygame.transform.rotate(self.image, 90)

# JigsawRecorder Class to record and compress moves
class JigsawRecorder:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.moves = []
        self.huffman_codes = None
    
    def record_move(self, tile_id, old_x, old_y, new_x, new_y, rotation):
        move = (tile_id, old_x, old_y, new_x, new_y, rotation)
        self.moves.append(move)
    
    def compress_moves(self):
        move_data = "".join(str(m) for m in self.moves)
        huffman_tree = huffman_tree_builder(move_data)
        self.huffman_codes = code_mapping(huffman_tree)
        compressed_data = "".join(self.huffman_codes[char] for char in move_data)
        return compressed_data
    
    def decompress_moves(self, compressed_data):
        return decompress_moves(compressed_data, self.huffman_codes)
    
    def get_moves(self):
        return self.moves

# Create the puzzle from the image
def create_puzzle(image_path):
    original_image = pygame.image.load(image_path)
    original_image = pygame.transform.scale(original_image, WINDOW_SIZE)
    tiles = []
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
            tile_surface.blit(original_image, (0, 0), (j*TILE_SIZE, i*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            tiles.append(Tile(i*GRID_SIZE + j, tile_surface))
    random.shuffle(tiles)
    return tiles

# Draw the puzzle
def draw_puzzle(tiles):
    for i, tile in enumerate(tiles):
        x = (i % GRID_SIZE) * TILE_SIZE
        y = (i // GRID_SIZE) * TILE_SIZE
        window.blit(tile.image, (x, y))
    pygame.display.flip()

# Optimize rotations using Matrix Chain Multiplication
def optimize_rotations(rotations):
    matrices = [(TILE_SIZE, TILE_SIZE) for _ in range(len(rotations))]
    return matrix_chain_mult(matrices)

# Main game loop
def main():
    tiles = create_puzzle("image.jpg")
    recorder = JigsawRecorder(tiles)
    selected_tile = None
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
                    index = tile_y * GRID_SIZE + tile_x
                    if selected_tile is None:
                        selected_tile = (index, tile_x, tile_y)
                    else:
                        old_index, old_x, old_y = selected_tile
                        tiles[old_index], tiles[index] = tiles[index], tiles[old_index]
                        recorder.record_move(tiles[index].id, old_x, old_y, tile_x, tile_y, tiles[index].rotation)
                        selected_tile = None
                elif event.button == 3:
                    x, y = event.pos
                    tile_x, tile_y = x // TILE_SIZE, y // TILE_SIZE
                    index = tile_y * GRID_SIZE + tile_x
                    tiles[index].rotate()
                    recorder.record_move(tiles[index].id, tile_x, tile_y, tile_x, tile_y, tiles[index].rotation)
        
        window.fill(BACKGROUND_COLOR)
        draw_puzzle(tiles)
        if selected_tile:
            x, y = selected_tile[1] * TILE_SIZE, selected_tile[2] * TILE_SIZE
            pygame.draw.rect(window, HIGHLIGHT_COLOR, (x, y, TILE_SIZE, TILE_SIZE), 2)
        pygame.display.flip()
    
    pygame.quit()

    # Output the recorded moves and compressed data
    print("Recorded moves:")
    for move in recorder.get_moves():
        print(move)
    
    compressed_data = recorder.compress_moves()
    print("Compressed moves:", compressed_data)
    
    decompressed_data = recorder.decompress_moves(compressed_data)
    print("Decompressed moves:", decompressed_data)
    
    # Optimize rotation calculations
    rotations = [move[5] for move in recorder.get_moves() if move[2] == move[4] and move[3] == move[5]]  # Only rotation moves
    min_operations = optimize_rotations(rotations)
    print("Minimum operations for rotation calculations:", min_operations)

# Run the game
if __name__ == "__main__":
    main()
