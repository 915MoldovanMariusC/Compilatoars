import re
from lab5 import FiniteAutomata


class SymbolTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash(self, key):
        # Compute the sum of ASCII values of characters in the key then mod length to fit
        hash_value = sum(ord(char) for char in key)
        return hash_value % self.size

    def insert(self, key, value):
        index = self.hash(key)
        if self.table[index] is None:
            self.table[index] = [(key, value)]
        else:
            # Handle collisions by chaining (using a list of key-value pairs)
            for i in range(len(self.table[index])):
                if self.table[index][i][0] == key:
                    # Update the value if the key already exists
                    self.table[index][i] = (key, value)
                    return
            # Append a new key-value pair if no collision resolution was successful
            self.table[index].append((key, value))

    def lookup(self, key):
        index = self.hash(key)
        if self.table[index] is not None:
            for k, v in self.table[index]:
                if k == key:
                    return v
        # Key not found
        return None

    def delete(self, key):
        index = self.hash(key)
        if self.table[index] is not None:
            for i in range(len(self.table[index])):
                if self.table[index][i][0] == key:
                    del self.table[index][i]
                    return

    def __str__(self):
        string = ''
        for l in self.table:
            if l:
                for elem in l:
                    string += "{} -> {}\n".format(elem[0], elem[1])
        return string


class Scanner:
    def __init__(self, tokens):
        self.symtable = SymbolTable(101)
        self.token_file = tokens
        self.tokens = []
        self.read_tokens()
        self.PIF = []
        self.integer = FiniteAutomata("int.in")
        self.identifier = FiniteAutomata("id.in")

    def read_tokens(self):
        token_file = open(self.token_file, "r")
        self.tokens = [line.strip() for line in token_file.readlines()]

    @staticmethod
    def split_line(line):
        separators = r'[;,|(): ]'
        result = re.split(r'({})'.format(separators), line)
        result = [s.strip() for s in result if s and s != ' ']
        try:
            result.remove('')
        except ValueError:
            pass
        return result if result != [''] else []

    @staticmethod
    def print_list(l):
        for e in l:
            print(e)

    def analyze(self, file):
        fin = open(file, "r")
        nr = 1
        for line in fin:
            for token in self.split_line(line):
                if token in self.tokens:
                    self.PIF.append((token, -1))
                elif self.identifier.is_match(token):
                    self.symtable.insert(token, 0)
                    self.PIF.append(('id', token))
                elif self.integer.is_match(token):
                    self.PIF.append(('const', token))
                    self.symtable.insert(token, token)
                else:
                    print("Error at {}, token {}".format(nr, token))
            nr += 1
        print("PIF")
        self.print_list(self.PIF)
        with open("PIF.out", "w") as f:
            f.write("{}".format(self.PIF))
        print("ST")
        print(self.symtable)


def main():
    sc = Scanner("token.in")
    file = input("file:")
    sc.analyze(file)


main()
