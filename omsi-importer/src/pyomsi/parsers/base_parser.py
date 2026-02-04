import os
from typing import Generator, List, Tuple

class OmsiBaseParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.lines = []

    def _read_file_safe(self) -> List[str]:
        """Tries to read from a file with different encodign."""
        encodings = ['cp1252', 'latin1', 'utf-8']
        
        for enc in encodings:
            try:
                with open(self.filepath, 'r', encoding=enc) as f:
                    return f.readlines()
            except UnicodeDecodeError:
                continue
        raise ValueError(f"Failed to read file {self.filepath} in defined encodings.")

    def parse_blocks(self) -> Generator[Tuple[str, List[str]], None, None]:
        """
        Reads a file and returs pairs: (KeyWord, ListOfLinesBelow).
        For example: returns ('spline', ['data_line_1', 'data_line_2'])
        """
        lines = self._read_file_safe()
        current_keyword = None
        buffer = []

        for line in lines:
            stripped = line.strip()
            # TODO Do we want to skip empty lines?
            # Skip empty lines
            if not stripped:
                continue

            # Detection of keyword [keyword] for example spline, object, etc
            if stripped.startswith('[') and stripped.endswith(']'):
                # If we have loaded anything before, return it
                if current_keyword:
                    yield current_keyword, buffer
                
                # Reset for a new block
                current_keyword = stripped[1:-1]
                buffer = []
            else:
                # Basic line with data
                if current_keyword:
                    buffer.append(stripped)
        
        # Returns last block and the end of file
        if current_keyword:
            yield current_keyword, buffer