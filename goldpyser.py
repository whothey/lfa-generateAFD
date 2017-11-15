from xml.etree import ElementTree
from html      import unescape
from simbolo   import simbolo
from enum      import Enum

class ActionType(Enum):
    """
    In GoldParser XML, each LALRAction has an attribute "Action" whose means the Transference,
    Reduction, Jump or Acceptance, for convenience and redability this enum was created to map
    each one.
    """
    Transference = 1
    Reduction    = 2
    Jump         = 3
    Accept       = 4


# Text representation of ActionType
ACTIONTEXT = {                     
    ActionType.Transference: 'T',
    ActionType.Reduction:    'R',
    ActionType.Jump:         '',
    ActionType.Accept:       'AC'
}


def read_from_xml(path):
    """
    Read a Gold-Parser XML dump and creates the LALR Parsing Table using a list of `simbolo`
    """
    tree = ElementTree.parse(path)
    root = tree.getroot()
    LALRTable = []

    table_node   = root.find('LALRTable')
    symbols_node = root.find('m_Symbol')

    nstates = int(table_node.attrib['Count'])

    for symbol in symbols_node.findall('Symbol'):
        sym = simbolo()
        # Sometimes in XML the symbols are escaped in HTML format. E.g.: &lt; = <, then we need to
        # undo this convertion
        sym.rotulo = unescape(symbol.attrib['Name'])
        # Initialize a list of `nstates` with -1 in each position
        sym.transicoes = ['-1']*nstates
        LALRTable.append(sym)

    for state in table_node.findall('LALRState'):
        state_number = int(state.attrib['Index'])

        for action in state.findall('LALRAction'):
            symbol_index  = int(action.attrib['SymbolIndex'])
            action_number = int(action.attrib['Action'])
            goto          = action.attrib['Value']

            # Here in parse_action, the attribute 'Action' in XML is 1, 2, 3 or 4. Each one
            # represents an action decribed in ActionType enum.
            parse_action = ActionType(action_number)

            if parse_action == ActionType.Accept:
                transition_str = ACTIONTEXT[parse_action]
            else:
                transition_str = "%s%s" % (ACTIONTEXT[parse_action], goto)

            LALRTable[symbol_index].transicoes[state_number] = transition_str

    return LALRTable

