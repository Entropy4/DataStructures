class suffixArray:
    def __init__(self, text:str):
        if text is None: return ValueError('Input text cannot be None')

        self.N = len(text)
        self.text = text
        # The sorted suffix array values.
        self.sa = []
        # Longest Common Prefix array
        self.lcp = []

        self.constructed_sa = False
        self.constructed_lcp = False

    def getTextLength(self) -> int:
        return len(self.text)
    
    def getSa(self) -> list:
        self.buildSuffixArray()
        return self.sa
    
    def getLcpArray(self) -> list:
        self.buildLcpArray()
        return self.lcp
    
    # Builds the suffix array by calling the construct() method.
    def buildSuffixArray(self):
        if self.constructed_sa: return
        self.construct()
        self.constructed_sa = True
    
    # Builds the LCP array by first creating the SA and then running the kasai algorithm.
    def buildLcpArray(self):
        if self.constructed_lcp: return
        self.buildSuffixArray()
        self.kasai()
        self.constructed_lcp = True

    # def toIntArray(s:str) -> list:
    #     if s is None: return None
    #     return list(s)
    
    # The suffix array construction algorithm: can do it in three ways-
    # slow:     O(n * n      * log(n))
    # med:      O(n * log(n) * log(n))
    # fast:     O(n * log(n))
    def construct(self, type='slow'):      
        self.constructSlow()

    # Use Kasai algorithm to build LCP array
    def kasai(self):
        self.lcp = [0] * self.N
        inv = [0] * self.N
        length = 0
        # construct the Inverse of the suffix array
        for i in range(self.N):
            inv[self.sa[i]] = i

        # construct lcp array with the help of the Inverse
        for i in range(self.N):
            if inv[i] > 0:
                k = self.sa[inv[i] - 1]
                while (i + length < self.N
                       and k + length < self.N
                       and self.text[i + length] == self.text[k + length]
                       ): length += 1
                self.lcp[inv[i]] = length
                if length > 0: length -= 1
    
    def __str__(self):
        if not self.constructed_lcp: self.buildLcpArray()
        s ="-----i-----SA-----LCP---Suffix\n"
        for i in range(self.N):
            suffix = ''
            for j in range(self.sa[i], self.N):     suffix += self.text[j]
            s += f"{i}    {self.sa[i]}    {self.lcp[i]}    {suffix}\n"
        return s

    # Naive suffix array construction. Time Complexity: O(n^2log(n))
    def constructSlow(self):
        # self.sa = [0] * self.N
        suffixes = [(self.text[i:], i) for i in range(self.N)]

        # O(nlog(n)) sorting TIMES String comparison in O(n), thus O(n^2log(n))
        suffixes = sorted(suffixes, key=lambda x: x[0])
        self.sa = [suffix[1] for suffix in suffixes]
    


# testing

import random
import time
from copy import deepcopy


# ---------- Main test suite ----------
def main():

    # ---------- Unique substrings ----------
    def count_unique_substrings(text, sa, lcp):
        n = len(text)
        return n * (n + 1) // 2 - sum(lcp)


    # ---------- Build SA+LCP using slow ----------
    def build_slow(text):
        sa_obj = suffixArray(text)
        sa_obj.construct("slow")
        sa = deepcopy(sa_obj.sa)

        sa_obj.kasai()
        lcp = deepcopy(sa_obj.lcp)

        return sa, lcp


    # ---------- Validate suffix array ----------
    def validate_suffix_array(text, sa):
        suffixes = [text[i:] for i in sa]
        return suffixes == sorted(suffixes)


    # ---------- Single test ----------
    def test_text(text):
        print("\n==============================")
        print("TEXT:", repr(text))
        print("==============================")

        start = time.perf_counter()
        sa, lcp = build_slow(text)
        end = time.perf_counter()

        print(f"Build time (slow): {end-start:.6f}s")

        # correctness checks
        valid_sa = validate_suffix_array(text, sa)
        print("SA lexicographically correct:", valid_sa)

        uniq = count_unique_substrings(text, sa, lcp)
        print("Unique substrings:", uniq)

        # diagnostics if incorrect
        if not valid_sa:
            print("\n--- DIAGNOSTIC ---")
            print("SA:", sa)
            print("LCP:", lcp)
            print("Suffixes in SA order:")
            for i in sa:
                print(text[i:])


    # ---------- Random generator ----------
    def random_string(n, alphabet="abcd"):
        return "".join(random.choice(alphabet) for _ in range(n))


    test_cases = [
        "",
        "a",
        "aaaaa",
        "banana",
        "abracadabra",
        "mississippi",
        "abababab",
        "abcde",
        "zyxwv",
        "panamabananas",
    ]

    # random tests
    for _ in range(5):
        test_cases.append(random_string(20))

    for text in test_cases:
        if len(text) == 0:
            continue
        test_text(text)

    # performance scaling of slow method
    print("\n===== PERFORMANCE SCALING (slow only) =====")
    for n in [10, 20, 40, 80, 120]:
        text = random_string(n)
        start = time.perf_counter()
        build_slow(text)
        end = time.perf_counter()
        print(f"Length {n:>3}: {end-start:.6f}s")


if __name__ == "__main__":
    main()