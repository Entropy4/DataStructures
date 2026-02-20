import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Needed for heap comparison
    def __lt__(self, other):
        return self.freq < other.freq


class HuffmanCoding:
    def __init__(self, text: str):
        if not text:
            raise ValueError("Input text cannot be empty")
        
        self.text = text
        self.freq_map = Counter(text)
        self.root = self._build_tree()
        self.codes = {}
        self._generate_codes(self.root, "")

    # --------------------------
    # Build Huffman Tree
    # --------------------------
    def _build_tree(self):
        heap = [HuffmanNode(ch, freq) for ch, freq in self.freq_map.items()]
        heapq.heapify(heap)

        while len(heap) > 1:
            left = heapq.heappop(heap)
            right = heapq.heappop(heap)

            merged = HuffmanNode(freq=left.freq + right.freq)
            merged.left = left
            merged.right = right

            heapq.heappush(heap, merged)

        return heap[0]

    # --------------------------
    # Generate Codes
    # --------------------------
    def _generate_codes(self, node, current_code):
        if node is None:
            return
        
        if node.char is not None:  # leaf
            self.codes[node.char] = current_code or "0"
            return
        
        self._generate_codes(node.left, current_code + "0")
        self._generate_codes(node.right, current_code + "1")

    # --------------------------
    # Encode
    # --------------------------
    def encode(self, text=None):
        if text is None:
            text = self.text
        return "".join(self.codes[ch] for ch in text)

    # --------------------------
    # Decode
    # --------------------------
    def decode(self, encoded_text: str):
        result = []
        node = self.root

        for bit in encoded_text:
            node = node.left if bit == "0" else node.right

            if node.char is not None:
                result.append(node.char)
                node = self.root

        return "".join(result)

    # --------------------------
    # Utility
    # --------------------------
    def get_codes(self):
        return dict(self.codes)
    

# Testing
def main():
    text = """Jugemu jugemu gokou no surikire
Kaija risuigyo no suigyou matsu
Unrai matsu fuurai matsu
Kuuneru tokoro ni sumu tokoro
Yabura kouji no bura kouji
Paipo paipo paipo no shuuringan
Shuuringan no guurindai
Guurindai no ponpokopii no
Ponpokonaa no choukyuumei no
Chousuke""".lower()

    huff = HuffmanCoding(text)

    print("Character Codes:")
    for ch, code in huff.get_codes().items():
        print(f"{repr(ch)} : {code}")

    encoded = huff.encode()
    print("\nEncoded:", encoded)

    decoded = huff.decode(encoded)
    print("Decoded:", decoded)

    print("\nCorrect:", decoded == text)

if __name__ == "__main__":
    main()