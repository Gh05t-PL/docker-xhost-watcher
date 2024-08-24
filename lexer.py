import re
from abc import ABC, abstractmethod

# Base Token class
class Token(ABC):
    def __init__(self, value: str):
        self.value = value

    @abstractmethod
    def get_type(self) -> str:
        pass

    def __str__(self) -> str:
        return f"Type: {self.get_type()}, Value: {self.value}"

    def detokenize(self) -> str:
        return self.value

# Specific Token classes
class IpToken(Token):
    def get_type(self) -> str:
        return 'IP'

class HostnameToken(Token):
    def get_type(self) -> str:
        return 'HOSTNAME'

class CommentToken(Token):
    def get_type(self) -> str:
        return 'COMMENT'

class WhitespaceToken(Token):
    def get_type(self) -> str:
        return 'WHITESPACE'

class NewlineToken(Token):
    def get_type(self) -> str:
        return 'NEWLINE'

# Lexer class
class Lexer:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as file:
            self.content = file.read()
        self.tokens = []
        self.current_position = 0
        self.patterns = []

    def tokenize(self):
        while self.current_position < len(self.content):
            matched = False

            for pattern, token_class in self.patterns:
                match = re.match(pattern, self.content[self.current_position:])
                if match:
                    value = match.group(0)
                    self.tokens.append(token_class(value))
                    self.current_position += len(value)
                    matched = True
                    break

            if not matched:
                self.current_position += 1

        return self.tokens

    def detokenize(self) -> str:
        return ''.join(token.detokenize() for token in self.tokens)

# HostsLexer class for /etc/hosts file
class HostsLexer(Lexer):
    def __init__(self, file_path: str):
        super().__init__(file_path)
        self.patterns = [
            (r'^#.*$', CommentToken),               # Match comments
            (r'\s+', WhitespaceToken),              # Match whitespace
            (r'\b\d{1,3}(\.\d{1,3}){3}\b', IpToken), # Match IPv4 addresses
            (r'\b[a-zA-Z0-9\.\-]+\b', HostnameToken), # Match hostnames
            (r'\n', NewlineToken)                   # Match new lines
        ]

# Example usage
file_path = '/etc/hosts'
lexer = HostsLexer(file_path)
tokens = lexer.tokenize()

for token in tokens:
    print(token)

# Detokenize the tokens back into a string
original_content = lexer.detokenize()
print("\nDetokenized content:")
print(original_content)