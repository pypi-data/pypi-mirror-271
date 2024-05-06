from consolemenu import ConsoleMenu, Screen, SelectionMenu
from consolemenu.items import FunctionItem
from consolemenu.prompt_utils import PromptUtils, UserQuit
from colors import color
from .processor import Processor
from .bibliography import setup
from .utils import removeBraces
import pkg_resources

def queryReport(query):
    if query.success:
        return f"{color('Success:', fg='green')} {query.result}"
    elif not query.success:
        return f"{color('Error:', fg='red')} {query.result}"

def libraryIsEmpty(processor):
    if not processor.library.entries:
        pu = PromptUtils(Screen())
        pu.println(f"Library is {color('empty', fg='red')}.")
        pu.enter_to_continue()
        return True
    return False

def queryHistoryIsEmpty(processor):
    if not processor.queryHistory:
        pu = PromptUtils(Screen())
        pu.println(f"Query history is {color('empty', fg='red')}.")
        pu.enter_to_continue()
        return True
    return False

def prettyPrintQuery(query):
    return f"{query.id} - {queryReport(query)}"

def prettyPrintQueries(queries):
    return [prettyPrintQuery(query) for query in queries]

def prettyKey(key):
    key = f"[@{key}]"
    return f"{color(key, fg='blue')}"

def prettyYear(year):
    year = removeBraces(year)
    return color(year, fg='yellow')

def prettyAuthor(authors):
    authors = removeBraces(authors)
    authors = authors.split(" and ")
    author = authors[0].split(", ")
    if len(author) > 1:
        author = f"{author[0]}, {author[1][:1]}."
    else:
        author = author[0]

    if len(authors) > 1:
        author = f"{author} et al."

    return color(author, fg='blue')

def prettyTitle(title):
    title = removeBraces(title)
    return color(title, fg='green')

def prettyPrintBlock(block):
    return f"\n{prettyKey(block.key)}\n{block.raw}\n"

def prettyPrintBlockShort(block):
        
    author = block.get('author').value
    year = block.get('year').value
    title = block.get('title').value

    string = f"{prettyAuthor(author)}, {prettyYear(year)}, {prettyTitle(title)}\n"
    return string

def prettyPrintBlocks(blocks):
    return [prettyPrintBlockShort(block) for block in blocks]

def QueryInput(processor):
    pu = PromptUtils(Screen())

    while True:
        try:
            input = pu.input(f"Enter {color('DOI', fg='blue')}: ", 
                            enable_quit=True, quit_string="q", 
                            quit_message=f"('{color('q', fg='red')}' to quit)").input_string.strip()
        except UserQuit:
            break
            
        processor.processQuery(input)
        query = processor.getLastQuery()
        if query.success:
            pu.println(queryReport(query))
            block = query.block
            pu.println(prettyPrintBlock(block))
            add = pu.prompt_for_yes_or_no(f"Add {prettyKey(block.key)} to library?")
            pu.println()
            if add: 
                try:
                    processor.add(block)
                    pu.println(prettyKey(block.key), color('added to library.', fg='green'), "\n")
                except ValueError as e:
                    pu.println(prettyKey(block.key), color('appears to be a duplicate key.', fg='red'))
                    processor.removeDuplicateBlocks()
                    if processor.compare(query):
                        pu.println(prettyKey(block.key), color(f"already exists in library with matching {query.type} {query.id}.", fg='red'))
                        pu.println(prettyKey(block.key), color('not added to library.', fg='red'))
                    else:
                        pu.println("The duplicate", prettyKey(block.key), f"does not exist in the library with a matching {query.type}.")
                        alternate = pu.prompt_for_yes_or_no(f"Add {prettyKey(block.key)} to library with an alternate key?")
                        pu.println()
                        if alternate:
                            processor.incrementKey(block)
                            processor.add(block)
                            pu.println(prettyKey(block.key), color('added to library with alternate key.', fg='green'), "\n")
                        else:
                            pu.println(prettyKey(block.key), color('not added to library.', fg='red'))
            else:
                pu.println(prettyKey(block.key), color('not added to library.', fg='red'), "\n")
        else:
            pu.println(queryReport(query))
        
        again = pu.prompt_for_yes_or_no(f"Search {color('again?', fg='blue')}")
        if not again:
            break
        pu.clear()

def showCitations(processor):
    if libraryIsEmpty(processor):
        return
    title = "Select an entry to view detailed information."
    entries = processor.library.entries
    exit = len(entries)
    while True:
        selection = SelectionMenu.get_selection(prettyPrintBlocks(entries), title=title)
        try:
            showCitation(entries[selection])
        except IndexError:
            if selection == exit:
                break
        
def showCitation(selection):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(selection))
    pu.enter_to_continue()
    pu.clear()

def removeCitations(processor):
    while True:
        if libraryIsEmpty(processor):
            return
        title = "Select an entry to remove."
        entries = processor.library.entries
        exit = len(entries)
        selection = SelectionMenu.get_selection(prettyPrintBlocks(entries), title=title)
        try:
            removeCitation(entries[selection], processor)
        except IndexError:
            if selection == exit:
                break

def removeCitation(block, processor):
    pu = PromptUtils(Screen())
    pu.println(prettyPrintBlock(block))
    remove = pu.prompt_for_yes_or_no(f"Remove {prettyKey(block.key)} from library?")
    if remove:
        processor.remove(block)
        pu.println(prettyKey(block.key), color('removed from library.', fg='green'), "\n")
    else:
        pu.println(prettyKey(block.key), color('not removed from library.', fg='red'), "\n")
    pu.enter_to_continue()
    pu.clear()

#def showHistoricalQueries(processor):
#    while True:
#        if queryHistoryIsEmpty(processor):
#            return
#        title = "Select a previous query to view."
#        queries = processor.queryHistory
#        exit = len(queries)
#        selection = SelectionMenu.get_selection(prettyPrintQueries(queries), title=title)
#        try:
#            pass
#        except IndexError:
#            if selection == exit:
#                break

def logo():
    logo_path = pkg_resources.resource_filename(__name__, 'logo')
    with open(logo_path, 'r', encoding="utf-8") as f:
        return ''.join([line for line in f])

def mainMenu():
    library = setup()
    processor = Processor(library)
    subtitle = f"A simple command line citation manager for your academic manuscript."
    menu = ConsoleMenu(logo(), subtitle, show_exit_option=False)
    
    menu.append_item(FunctionItem("Query", QueryInput, [processor]))
    menu.append_item(FunctionItem("Show Citations", showCitations, [processor]))
    menu.append_item(FunctionItem("Remove Citations", removeCitations, [processor]))
    #menu.append_item(FunctionItem("Show Historical Queries", showHistoricalQueries, [processor]))

    menu.show()