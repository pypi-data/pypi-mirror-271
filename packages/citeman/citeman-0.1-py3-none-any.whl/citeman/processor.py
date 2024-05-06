from bibtexparser.model import DuplicateBlockKeyBlock
from .query import CrossRef, Query
from .bibliography import write
from .utils import removeBraces

class Processor():
    """
    A class that represents a processor for handling queries and managing a library.
    All interactions between the user and the Library/.bib file are handled by the Processor.

    Attributes:
        library (Library): The library object that stores the blocks.
        queryHistory (TypedList): A typed list that stores the query history.

    Methods:
        __init__(self, library): Initializes a Processor object with a library.
        processQuery(self, input): Processes a query and adds it to the query history.
        add(self, block): Adds a block to the library and writes the library to .bib file.
        remove(self, block): Removes a block from the library and writes the library .bib file.
        write(self): Writes the library to .bib file.
        getQuery(self, index): Retrieves a query from the query history based on the index.
        getLastQuery(self): Retrieves the last query from the query history.
    """

    def __init__(self, library):
        """
        Initializes a Processor object with a library.

        Args:
            library (Library): The library object that stores the blocks.
        """
        self.library = library
        self.queryHistory = TypedList(Query) 

    def processQuery(self, input):
        """
        Processes a query and adds it to the query history.

        Args:
            input (str): The article ID to query.

        Raises:
            Exception: If an error occurs while processing the query.
            Should only be raising unanticipated exceptions as most have been
            handled in the Query class.
        """
        try:
            query = CrossRef(input)
            self.queryHistory.append(query)
        except:
            raise
    
    def add(self, block) -> None:
        """
        Adds a block to the library and writes the library to .bib file.

        Args:
            block (Block): The block to be added to the library.
        """
        try:
            self.library.add(block, fail_on_duplicate_key=True)
        except:
            raise

        self.write()

    def remove(self, block) -> None:
        """
        Removes a block from the library and writes the library to .bib file.

        Args:
            block (Block): The block to be removed from the library.
        """
        self.library.remove(block)
        self.write()

    def write(self) -> None:
        """
        Writes the library to .bib file.
        """
        write(self.library)

    def compare(self, query):
        """
        Compares a given article ID with the library.

        Args:
            id (str): The article ID to compare.

        Returns:
            bool: True if the article ID is in the library, False otherwise.
        """
        entries = self.library.entries
        type = query.type
        for entry in entries:
            id = removeBraces(entry.get(type).value)
            if id is not None and id == query.id:
                    return True
            else:
                return False
            
    def incrementKey(self, block):
        """
        Increments the key of a block in the library to avoid duplicates.

        Args:
            key (str): The new key to assign to the block.
        """
        key_v = 1
        new_key = block.key + f"_{key_v}"
        while self._keyExists(new_key):
            key_v += 1
            new_key = block.key + f"_{key_v}"
        block.key = new_key

    def _keyExists(self, key):
        """
        Checks if a key already exists in the library.

        Args:
            key (str): The key to check.

        Returns:
            bool: True if the key exists in the library, False otherwise.
        """
        entries = self.library.entries
        for entry in entries:
            if entry.key == key:
                return True
            else:
                return False
            
    def removeDuplicateBlocks(self):
        """
        Removes duplicate blocks from the library.
        """
        duplicates = [block for block in self.library.blocks if isinstance(block, DuplicateBlockKeyBlock)]
        self.library.remove(duplicates)

    def getQuery(self, index) -> Query:
        """
        Retrieves a query from the query history based on the index.

        Args:
            index (int): The index of the query in the query history.

        Returns:
            Query: The query object.
        """
        return self.queryHistory[index]

    def getLastQuery(self) -> Query:
        """
        Retrieves the last query from the query history.

        Returns:
            Query: The last query object in the query history.
        """
        return self.getQuery(-1)
    
class TypedList(list):
    """
    A typed list that enforces a specific element type.

    Attributes:
        element_type (type): The type of elements allowed in the list.

    Methods:
        __init__(self, element_type, initial_list): Initializes a TypedList object with an element type and an initial list.
        _validate(self, element): Validates if an element is of the correct type.
        append(self, element): Appends an element to the list after validating its type.
        insert(self, index, element): Inserts an element into the list at a specific index after validating its type.
        extend(self, iterable): Extends the list with elements from an iterable after validating their types.
    """

    def __init__(self, element_type, initial_list=None):
        """
        Initializes a TypedList object with an element type and an initial list.

        Args:
            element_type (type): The type of elements allowed in the list.
            initial_list (list, optional): An initial list to populate the TypedList with. Defaults to None.
        """
        self.element_type = element_type
        if initial_list:
            for element in initial_list:
                self._validate(element)
                super().append(element)

    def _validate(self, element):
        """
        Validates if an element is of the correct type.

        Args:
            element: The element to be validated.

        Raises:
            TypeError: If the element is not of the correct type.
        """
        if not isinstance(element, self.element_type):
            raise TypeError(f"Only {self.element_type.__name__} elements are allowed")

    def append(self, element):
        """
        Appends an element to the list after validating its type.

        Args:
            element: The element to be appended.
        """
        self._validate(element)
        super().append(element)

    def insert(self, index, element):
        """
        Inserts an element into the list at a specific index after validating its type.

        Args:
            index (int): The index at which to insert the element.
            element: The element to be inserted.
        """
        self._validate(element)
        super().insert(index, element)

    def extend(self, iterable):
        """
        Extends the list with elements from an iterable after validating their types.

        Args:
            iterable (iterable): The iterable containing elements to be added to the list.
        """
        for element in iterable:
            self._validate(element)
        super().extend(iterable)