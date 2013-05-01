# -*- coding: utf-8 -*-
import xml.dom.minidom as minidom
from primo.core import BayesNet
from primo.core import Node
from primo.reasoning import DiscreteNode
import re


class XMLBIF(object):
    '''
    This class represents the Interchange Format for Bayesian Networks (XMLBIF).
    It helps you to convert a BayesNet to a XMLBIF and a XMLBIF to a BayesNet.

    See: http://www.cs.cmu.edu/~fgcozman/Research/InterchangeFormat/
    '''
    def __init__(self, network, network_name = "Unnamed network",
                 encoding = "UTF-8", ndent = "    ", newl = "\n",
                 addindent = "    "):
        '''
        Create a new XMLBIF instance.

        Keyword arguments:
        network -- is a valid BayesNet that must only contain DicreteNodes.
        network_name -- is some name that will be mentioned in the XMLBIF.
        encoding -- encoding of the XMLBIF. Encoding other than UTF-8 is
        likely incorrect, since UTF-8 is the default encoding of XML.
        ndent -- specifies the indentation string and defaults to a tabulator.
        newl -- specifies the string emitted at the end of each line.
        addindent -- is the incremental indentation to use for subnodes of the current one
        '''
        self.network = network
        self.network_name = network_name
        self.encoding = encoding
        self.ndent = ndent
        self.newl = newl
        self.addindent = addindent
        self.root = minidom.Document()
        if isinstance(network, BayesNet):
            self.network = network
        else:
            raise Exception("Given network is not a BayesNet.")
        # Create inital XMLBIF
        self.generate_XMLBIF()

    def __str__(self):
        '''
        Returns a pretty string representation of the XMLBIF.
        '''
        return self.root.toprettyxml(self.ndent, self.newl, self.encoding);

    def write(self, filename):
        '''
        Write this XMLBIF instance to disk.

        Keyword arguments:
        filename -- is a string containing the filename.
        '''
        f = open(filename, "w")
        self.root.writexml(f, self.ndent, self.addindent, self.newl, self.encoding)



    def generate_XMLBIF(self):
        '''
        Generate the XMLBIF document.

        This method is used internally. Do not call it outside this class.
        '''
        self.calculate_positions()
        root_node = minidom.Document()
        tag_bif = root_node.createElement("BIF")
        tag_net = root_node.createElement("NETWORK")
        tag_bif.setAttribute("VERSION","0.3")
        root_node.appendChild(tag_bif)
        tag_bif.appendChild(tag_net)

        tag_name = minidom.Element("NAME")
        text = minidom.Text()
        text.data = str(self.network_name)
        tag_name.appendChild(text)
        tag_net.appendChild(tag_name)

        for node_name in self.network.node_lookup:
            current_node = self.network.node_lookup[node_name]
            if not isinstance(current_node, DiscreteNode):
                raise Exception("Node " + str(current_node) + " is not a DiscreteNode.")
            node_tag = self.create_node_tag(current_node)
            tag_net.appendChild(node_tag)

        #Generate CPTs
        for node_name in self.network.node_lookup:
            current_node = self.network.node_lookup[node_name]
            tag_def = minidom.Element("DEFINITION")
            tag_for = minidom.Element("FOR")
            txt_for = minidom.Text()
            txt_for.data = node_name
            tag_for.appendChild(txt_for)
            tag_def.appendChild(tag_for)

            # It's not guaranteed that the own node is at dimension zero in 
            # the probability table.But for the function the order of the 
            # variables is important
            for parent in reversed(current_node.get_cpd().get_variables()):
                tag_par = minidom.Element("GIVEN")
                txt_par = minidom.Text()
                txt_par.data = str(parent.name)
                tag_par.appendChild(txt_par)
                tag_def.appendChild(tag_par)

            tag_cpt = minidom.Element("TABLE")
            txt_cpt = minidom.Text()
            txt = ""
            for elem in current_node.get_cpd().get_table().T.flat:
                txt += str(elem) + " "

            txt_cpt.data = txt
            tag_cpt.appendChild(txt_cpt)
            tag_def.appendChild(tag_cpt)

            tag_net.appendChild(tag_def)

        self.root = root_node
        return self



    def create_node_tag(self, node):
        '''
        Create a node tag that will look like:
        <VARIABLE TYPE="nature">
            <NAME>node_name</NAME>
            <OUTCOME>...</OUTCOME>
            <OUTCOME>...</OUTCOME>
            <PROPERTY>position = (x, y)</PROPERTY>
        </VARIABLE>

        Keyword arguments:
        node -- a Node with valid name and position

        Returns a XMLBIF conform "variable" tag
        '''
        if not isinstance(node, Node):
            raise Exception("Node " + str(node) + " is not a Node.")
        tag_var = minidom.Element("VARIABLE")
        tag_own = minidom.Element("NAME")
        tag_pos = minidom.Element("PROPERTY")
        tag_var.setAttribute("TYPE", "nature")

        # set node name
        txt_name = minidom.Text()
        txt_name.data = node.name
        tag_var.appendChild(tag_own)
        tag_own.appendChild(txt_name)

        # set outcomes
        for value in node.value_range:
            tag_outcome = minidom.Element("OUTCOME")
            txt_outcome = minidom.Text()
            txt_outcome.data = value
            tag_outcome.appendChild(txt_outcome)
            tag_var.appendChild(tag_outcome)

        # set position
        txt_pos = minidom.Text()
        x, y = node.position
        txt_pos.data = "position = (" + str(x) + ", " + str(y) + ")"
        tag_pos.appendChild(txt_pos)
        tag_var.appendChild(tag_pos)

        return tag_var


    def calculate_positions(self):
        '''
        Calculate the visual position for each node.

        This method is used internally. Do not call it outside this class.
        '''
        q = []
        p = []
        already_seen = []
        x_step = 150
        y_step = 100
        x_pos = 0
        y_pos = 0
        for node_name in self.network.node_lookup:
            node = self.network.node_lookup[node_name]
            if len(self.network.graph.predecessors(node)) == 0:
                q.append(node)
                already_seen.append(node)
        while q:
            p = q
            q = []
            y_pos += y_step
            x_pos = x_step
            while p:
                node = p.pop()
                node.position = (x_pos, y_pos)
                x_pos += x_step

                for child in self.network.graph.successors(node):
                    if not child in already_seen:
                        q.append(child)
                        already_seen.append(child)

    @staticmethod
    def read(filename_or_file, is_string = False):
        '''
        Reads a XMLBIF and returns a BayesNet.

        Keyword arguments:
        filename_or_file -- may be either a file name, or a file-like object.
        is_string -- is True if filename_or_file is a XML in a string

        Returns a BayesNet.
        '''
        if is_string:
            root = minidom.parseString(filename_or_file)
        else:
            root = minidom.parse(filename_or_file)

        return XMLBIF.generate_BayesNet(root)

    @staticmethod
    def generate_BayesNet(root):
        '''
        Generate a BayesNet from a XMLBIF.

        This method is used internally. Do not call it outside this class.
        '''
        network = BayesNet()
        bif_nodes = root.getElementsByTagName("BIF")
        if len(bif_nodes) != 1:
            raise Exception("More than one or none <BIF>-tag in document.")
        network_nodes = bif_nodes[0].getElementsByTagName("NETWORK")
        if len(network_nodes) != 1:
            raise Exception("More than one or none <NETWORK>-tag in document.")
        variable_nodes = network_nodes[0].getElementsByTagName("VARIABLE")
        for variable_node in variable_nodes:
            name = "Unnamed node"
            value_range = []
            position = (0, 0)
            for name_node in variable_node.getElementsByTagName("NAME"):
                name = XMLBIF.get_node_text(name_node.childNodes)
                break
            for output_node in variable_node.getElementsByTagName("OUTCOME"):
                value_range.append(XMLBIF.get_node_text(output_node.childNodes))
            for position_node in variable_node.getElementsByTagName("PROPERTY"):
                position = XMLBIF.get_node_position_from_text(position_node.childNodes)
                break
            new_node = DiscreteNode(name, value_range)
            new_node.position = position
            network.add_node(new_node)
        definition_nodes = network_nodes[0].getElementsByTagName("DEFINITION")
        for definition_node in definition_nodes:
            node = None
            for for_node in definition_node.getElementsByTagName("FOR"):
                name = XMLBIF.get_node_text(for_node.childNodes)
                node = network.get_node(name)
                break
            if node == None:
                continue
            for given_node in definition_node.getElementsByTagName("GIVEN"):
                parent_name = XMLBIF.get_node_text(given_node.childNodes)
                parent_node = network.get_node(parent_name)
                node.announce_parent(parent_node)
            for table_node in definition_node.getElementsByTagName("TABLE"):
                table = XMLBIF.get_node_table_from_text(table_node.childNodes)
                node.get_cpd().get_table().T.flat = table
                break

        return network

    @staticmethod
    def get_node_text(nodelist):
        '''
        Keyword arguments:
        nodelist -- is a list of nodes (xml.dom.minidom.Node).

        Returns the text of the given nodelist or a empty string.
        '''
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    @staticmethod
    def get_node_position_from_text(nodelist):
        '''
        Keyword arguments:
        nodelist -- is a list of nodes (xml.dom.minidom.Node).

        Returns the position of the given nodelist as pair (x, y).
        '''
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        text = ''.join(rc)
        number_list = re.findall(r"\d+", text)
        if len(number_list) != 2:
            raise Exception("Ambiguous node position in XMLBIF.")
        return (number_list[0], number_list[1])

    @staticmethod
    def get_node_table_from_text(nodelist):
        '''
        Keyword arguments:
        nodelist -- is a list of nodes (xml.dom.minidom.Node).

        Returns the probability table of the given nodelist as pair numpy.array.
        '''
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        text = ''.join(rc)
        number_list = re.findall(r"[0-9]*\.*[0-9]+", text)
        return number_list