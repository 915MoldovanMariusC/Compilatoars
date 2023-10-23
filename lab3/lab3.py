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


sym_table = SymbolTable(100)
sym_table.insert("x", 42)
sym_table.insert("y", 30)
sym_table.insert("z", 15)

print(sym_table.lookup("x")) 
print(sym_table.lookup("y"))  
print(sym_table.lookup("z"))  

sym_table.delete("y")
print(sym_table.lookup("y"))  
