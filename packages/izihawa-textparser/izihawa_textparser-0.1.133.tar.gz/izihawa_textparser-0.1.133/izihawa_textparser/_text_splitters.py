import copy
from typing import Any

import langchain
from langchain.text_splitter import HeaderType, LineType
from langchain_core.documents import Document


class MarkdownHeaderTextSplitter(langchain.text_splitter.MarkdownHeaderTextSplitter):

    def split_text(self, text: str) -> list[Document]:
        """Split markdown file
        Args:
            text: Markdown file"""

        # Split the input text by newline character ("\n").
        lines = text.split("\n")
        # Final output
        lines_with_metadata: list[LineType] = []
        # Content and metadata of the chunk currently being processed
        current_content: list[str] = []
        next_start_index = 0
        current_metadata: dict[str, Any] = {'start_index': next_start_index}
        # Keep track of the nested header structure
        # header_stack: List[Dict[str, Union[int, str]]] = []
        header_stack: list[HeaderType] = []
        initial_metadata: dict[str, str] = {}

        in_code_block = False
        opening_fence = ""

        for line in lines:
            next_start_index += (len(line) + 1)
            stripped_line = line.strip()

            if not in_code_block:
                # Exclude inline code spans
                if stripped_line.startswith("```") and stripped_line.count("```") == 1:
                    in_code_block = True
                    opening_fence = "```"
                elif stripped_line.startswith("~~~"):
                    in_code_block = True
                    opening_fence = "~~~"
            else:
                if stripped_line.startswith(opening_fence):
                    in_code_block = False
                    opening_fence = ""

            if in_code_block:
                current_content.append(line)
                continue

            # Check each line against each of the header types (e.g., #, ##)
            for sep, name in self.headers_to_split_on:
                # Check if line starts with a header that we intend to split on
                if stripped_line.startswith(sep) and (
                    # Header with no text OR header is followed by space
                    # Both are valid conditions that sep is being used a header
                    len(stripped_line) == len(sep) or stripped_line[len(sep)] == " "
                ):
                    # Ensure we are tracking the header as metadata
                    if name is not None:
                        # Get the current header level
                        current_header_level = sep.count("#")

                        # Pop out headers of lower or same level from the stack
                        while (
                            header_stack
                            and header_stack[-1]["level"] >= current_header_level
                        ):
                            # We have encountered a new header
                            # at the same or higher level
                            popped_header = header_stack.pop()
                            # Clear the metadata for the
                            # popped header in initial_metadata
                            if popped_header["name"] in initial_metadata:
                                initial_metadata.pop(popped_header["name"])

                        # Push the current header to the stack
                        header: HeaderType = {
                            "level": current_header_level,
                            "name": name,
                            "data": stripped_line[len(sep) :].strip(),
                        }
                        header_stack.append(header)
                        # Update initial_metadata with the current header
                        initial_metadata[name] = header["data"]

                    # Add the previous line to the lines_with_metadata
                    # only if current_content is not empty
                    if current_content:
                        complete_chunk = {
                            "content": "\n".join(current_content),
                            "metadata": current_metadata.copy(),
                        }
                        lines_with_metadata.append(complete_chunk)
                        current_content.clear()

                    current_metadata['start_index'] = next_start_index
                    break
            else:
                current_content.append(line)

            current_metadata = {**initial_metadata.copy(), 'start_index': current_metadata['start_index']}

        if current_content:
            lines_with_metadata.append(
                {"content": "\n".join(current_content), "metadata": current_metadata}
            )

        return [
            Document(page_content=chunk["content"], metadata=chunk["metadata"])
            for chunk in lines_with_metadata
        ]


class RecursiveCharacterTextSplitter(
    langchain.text_splitter.RecursiveCharacterTextSplitter
):
    def create_documents(
        self, texts: list[str], metadatas: list[dict] | None = None
    ) -> list[Document]:
        """Create documents from a list of texts."""
        _metadatas = metadatas or [{}] * len(texts)
        documents = []
        for i, text in enumerate(texts):
            index = -1
            for chunk in self.split_text(text):
                metadata = copy.deepcopy(_metadatas[i])
                start_index = metadata["start_index"]
                index = text.find(chunk, index + 1)
                metadata["start_index"] = start_index + index
                new_doc = Document(page_content=chunk, metadata=metadata)
                documents.append(new_doc)
        return documents
