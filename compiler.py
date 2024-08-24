class Token:
    """Base class for all tokens."""
    pass

class OriginalLineToken(Token):
    def __init__(self, line):
        self.line = line

class StartMarkerToken(Token):
    def __init__(self):
        self.marker = "# >>> DOCKER_XHOST_WATCHER"

class EndMarkerToken(Token):
    def __init__(self):
        self.marker = "# <<< DOCKER_XHOST_WATCHER"

class HostEntryToken(Token):
    def __init__(self, entry):
        self.entry = entry

class HostsFileCompiler:
    def __init__(self, hosts_file_path="/etc/hosts"):
        self.hosts_file_path = hosts_file_path
        self.tokens = []
        self.new_hosts_data = []

    def tokenize(self, lines):
        """Converts the lines from the hosts file into tokens."""
        inside_markers = False

        for line in lines:
            stripped_line = line.strip()
            if stripped_line == "# >>> DOCKER_XHOST_WATCHER":
                self.tokens.append(StartMarkerToken())
                inside_markers = True
            elif stripped_line == "# <<< DOCKER_XHOST_WATCHER":
                self.tokens.append(EndMarkerToken())
                inside_markers = False
            elif inside_markers:
                # Skip lines inside markers
                continue
            else:
                self.tokens.append(OriginalLineToken(line))

    def parse(self):
        """Parses the tokens and inserts the new host data."""
        parsed_lines = []

        for token in self.tokens:
            if isinstance(token, OriginalLineToken):
                parsed_lines.append(token.line)
            elif isinstance(token, StartMarkerToken):
                parsed_lines.append(token.marker + "\n")
                for entry in self.new_hosts_data:
                    parsed_lines.append(entry + "\n")
                parsed_lines.append("# <<< DOCKER_XHOST_WATCHER\n")

        # If the markers were not found, append the new data at the end
        if not any(isinstance(token, StartMarkerToken) for token in self.tokens):
            parsed_lines.append("# >>> DOCKER_XHOST_WATCHER\n")
            for entry in self.new_hosts_data:
                parsed_lines.append(entry + "\n")
            parsed_lines.append("# <<< DOCKER_XHOST_WATCHER\n")

        return parsed_lines


    def update_hosts_data(self, new_hosts_data):
        """Updates the new hosts data that will be added between markers."""
        self.new_hosts_data = new_hosts_data
        print("Updated new hosts data to be added.")


    def read_hosts_file(self):
        """Reads the /etc/hosts file and tokenizes it."""
        with open(self.hosts_file_path, 'r') as f:
            lines = f.readlines()
        self.tokenize(lines)
        print("Read and tokenized the /etc/hosts file.")

    def write_hosts_file(self, parsed_lines):
        """Writes the parsed lines back to the /etc/hosts file."""
        with open(self.hosts_file_path, 'w') as f:
            f.writelines(parsed_lines)
        print("Wrote the updated /etc/hosts file.")


    def get_hosts_file_string(self):
        """Returns the updated hosts file content as a string."""
        parsed_lines = self.parse()
        return ''.join(parsed_lines)

    def compile(self):
        """Runs the full compilation process: read, parse, and write."""
        self.read_hosts_file()
        parsed_lines = self.parse()
        self.write_hosts_file(parsed_lines)
        print("Compilation process completed.")
