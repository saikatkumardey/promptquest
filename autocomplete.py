class Autocomplete:
    def __init__(self, words):
        self.words = words
        self.trie = {}
        for word in words:
            node = self.trie
            for char in word:
                node = node.setdefault(char, {})
            node["$"] = word

    def search(self, prefix):
        node = self.trie
        for char in prefix:
            if char in node:
                node = node[char]
            else:
                return []
        return self._search(node)

    def _search(self, node):
        words = []
        for char, child in node.items():
            if char == "$":
                words.append(child)
            else:
                words.extend(self._search(child))
        return words


words = ["dog", "deer", "deal", "hello", "hello_world"]
autocomplete = Autocomplete(words)

while True:
    prefix = input("Enter a prefix: ")
    if prefix == "exit":
        break
    suggestions = autocomplete.search(prefix)
    print("Suggestions:", suggestions)
