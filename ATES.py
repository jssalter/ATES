from defusedxml.ElementTree import parse as DETparse
import os
# import sys
import xml.etree.ElementTree as ET

# todo: a lot


class Inputter:
    # todo: placeholder to accept pdf files
    # def pdf_parser(self):
    #     with open(self) as fn:
    #         file_name = pdf.parse(fn.read())
    #     return file_name

    # todo: placeholder to accept txt files
    # def txt_parser(self):
    #     with open(self) as fn:
    #         file_name = txt.parse(fn.read())
    #     return file_name

    # parsing xml files
    def xml_parser(self):
        parsed_file = DETparse(self)
        return parsed_file


class Main:
    @staticmethod
    def main():
        print("--------------------------------------------------------- \n"
              "                AT->ES Conversion Program \n"
              "    Place this script in the same directory as JESS \n"
              " and run it with attack trees in the Attack_Trees folder\n"
              "---------------------------------------------------------")
        data = 'things go here'  # todo: remove this line, but maybe use data variable somewhere
        file_name = 'RFID_Comm_Block.xml'  # todo: remove this entire line, then remove "))  #" on below line.
        try:
            parsed_file = Inputter.xml_parser(os.path.join('Attack_Trees', file_name))  # := input("What is the name of your XML file to be converted? ")))
            split_file, node_list, levels = Splitter.xml_file_splitter(parsed_file)
            # todo: if > then for tree type to make different paths
            tree_type = split_file.tag
            new_file_name, old_ext = os.path.splitext(file_name)
        except FileNotFoundError:
            print("Input error. Please check the file's name and location and try again.")
        except Exception as e:
            print('Coding error. See below for details. \n', e)
        else:
            # Outputter.printer(file_name)
            Outputter.printer(tree_type)
            Outputter.printer(levels)
            # Outputter.node_printer(node_list)
            Outputter.file_writer(node_list, new_file_name)
            Outputter.printer('Conversion successful!')
        finally:
            print('\n======================================='
                  '\n     Thank you for using AT->ES.'
                  '\n    Questions, comments, concerns?'
                  '\n  Jonathan-Steven.Salter@stud.vgtu.lt'
                  '\n=======================================')


# class Node:
#     def __init__(self, name, parent, cost, duration, exploited, countermeasure, siblings, children):
#         self.name = name
#         self.parent = parent
#         self.cost = cost
#         self.duration = duration
#         self.exploited = exploited
#         self.countermeasure = countermeasure
#         self.siblings = siblings
#         self.children = children
#
#     @property
#     def __str__(self):
#         return str(self)


class Outputter:
    def file_writer(self, new_file_name):
        try:
            os.makedirs('Attack_Trees/JESS')
        except FileExistsError:
            pass
        finally:
            with open('Attack_Trees/JESS/' + new_file_name + '.clp', 'w') as f:
                f.write(';;;====================================================== \n'
                        ';;;   Self Learning Decision Tree Program\n'
                        ';;;\n'
                        ';;;   This program tries to determine the animal you are \n'
                        ';;;   thinking of by asking questions. \n'
                        ';;; \n'
                        ';;;   Jess Version 4.2 Example \n'
                        ';;; \n'
                        ';;;   To execute, merely load the file with the command\n'
                        f';;;   (batch "Attack_Trees/JESS/{new_file_name}.clp")\n'
                        ';;;======================================================\n'
                        '\n'
                        '(clear)\n'
                        '(reset)\n'
                        ';;;;;;;;;;;;;;;;;;;;\n'
                        ';template for nodes:\n'
                        '(deftemplate node "Data about nodes"\n'
                        '(slot name)\n'
                        '(slot parent)\n'
                        '(slot cost (default 0))\n'
                        '(slot duration (default 0))\n'
                        '(slot exploited (default FALSE))\n'
                        '(slot countermeasure (default FALSE))\n'
                        '(multislot siblings (default nil)) ;for "and" nodes of same level\n'
                        '(multislot children (default nil)))\n'
                        '\n'
                        ';;;;;;;;;;;;;;;;;;;;\n'
                        ';template for trees:\n'
                        '(deftemplate tree "Data about ATs"\n'
                        '(slot name)\n'
                        '(slot rootnode))\n'
                        '\n'
                        ';;;;;;;;;;;;;;;;;;;;;;;;;\n'
                        ';planned space for rules:\n'
                        ';(defrule tree-has-root\n'
                        ';	"Make sure a tree has a root node."\n'
                        ';\n'
                        ';(defrule node-exploited\n'
                        ';something like "if node exploited = true and node has no siblings then progress up"??\n'
                        ';	"If a node is exploited, then move up the tree"\n'
                        ';	(node (exploited ?x))\n'
                        ';	(test (?x))\n'
                        ';	=>\n'
                        ';	(printout t "A node is exploited!" crlf)\n'
                        ';	($activenode <- (node (parent))))\n'
                        ';\n'
                        '\n'
                        ';;;;;;;;;;;;\n'
                        ';Query? Something like "if node has parent then parent\'s child is node"??\n'
                        ';(defrule anc (or (parent ?a ?b) (and (parent ?a ?c)(ancestor ?c ?b)) )\n'
                        ';=> (assert(ancestor ?a ?b)))\n'
                        ';\n'
                        ';(bind ?it (run-query search <string>))\n'
                        ';(while (?it hasNext)\n'
                        ';	(bind ?token (call ?it next))\n'
                        ';	(bind ?fact (call ?token fact 1))\n'
                        ';	(bind ?slot (fact-slot-value ?fact __data))\n'
                        ';	(bind ?datum (nth$ 2 ?slot))\n'
                        ';	(printout t ?datum crlf))\n'
                        ';\n'
                        ';\n'
                        ';something like "if node has no parent then assert rootnode"??\n'
                        ';\n'
                        ';\n'
                        ';\n'
                        ';\n'
                        ';\n\n')
                for i in self:
                    f.write(f'(assert (node (name "{i}")))\n')
                f.write("\n(run)\n\n")


    def jess_printer(self):
        # for i in self:
        #     print("(assert (node (name \"" + str(i) + "\")))")
        pass

    def node_printer(self):
        for i in self:
            fact = f'(assert (node (name "{i}")))'
            print(fact)

    def printer(self):
        print(self)


class JESS_Rules:
    @staticmethod
    def initilizer():
        # todo: add more (rules and queries and such) to this and make it work
        print(";;;====================================================== \n;;;   Self Learning Decision Tree Program"
              "\n;;;\n;;;   This program tries to determine the animal you are \n;;;   thinking of by asking "
              "questions. \n;;; \n;;;   Jess Version 4.2 Example \n;;; \n;;;   To execute, merely load the file"
              ".\n;;;======================================================\n\n(clear)\n(reset)\n;;;;;;;;;;;;;;;;;;;;\n"
              ";template for nodes:\n(deftemplate node \"Data about nodes\"\n(slot name)\n(slot parent)\n(slot cost "
              "(default 0))\n(slot duration (default 0))\n(slot exploited (default FALSE))\n(slot countermeasure "
              "(default FALSE))\n(multislot siblings (default nil)) ;for \"and\" nodes of same level\n(multislot "
              "children (default nil)))\n\n;;;;;;;;;;;;;;;;;;;;\n;template for trees:\n(deftemplate tree \"Data about "
              "ATs\"\n(slot name)\n(slot rootnode))\n\n;;;;;;;;;;;;;;;;;;;;;;;;;\n;planned space for rules:\n;(defrule "
              "tree-has-root\n;	\"Make sure a tree has a root node.\"\n;\n;(defrule node-exploited\n"
              ";something like \"if node exploited = true and node has no siblings then progress up\"??\n"
              ";	\"If a node is exploited, then move up the tree\"\n;	(node (exploited ?x))\n;	(test (?x))\n"
              ";	=>\n;	(printout t \"A node is exploited!\" crlf)\n;	($activenode <- (node (parent))))\n;\n\n"
              ";;;;;;;;;;;;\n;Query? Something like \"if node has parent then parent's child is node\"??\n"
              ";(defrule anc (or (parent ?a ?b) (and (parent ?a ?c)(ancestor ?c ?b)) )\n;=> (assert(ancestor ?a ?b)))\n"
              ";\n;(bind ?it (run-query search <string>))\n;(while (?it hasNext)\n;	(bind ?token (call ?it next))\n"
              ";	(bind ?fact (call ?token fact 1))\n;	(bind ?slot (fact-slot-value ?fact __data))\n"
              ";	(bind ?datum (nth$ 2 ?slot))\n;	(printout t ?datum crlf))\n;\n;\n"
              ";something like \"if node has no parent then assert rootnode\"??\n;\n;\n;\n;\n\n")

    @staticmethod
    def finalizer():
        print("\n(run)\n\n")


class Splitter:
    def xml_file_splitter(self):
        # todo: fix split_file being a memory object value
        # split_file = []
        # todo: for getroot look at tool name and process differently based upon that tool's name - move to main
        split_file = self.getroot()
        # node_list = {'name': '', 'parent': '', 'cost': '', 'duration': '', 'exploited': '', 'countermeasure': '', 'siblings': '', 'children': ''}
        node_list = []
        level = []
        levels = []
        # below prints out refinements. Todo: split text to get dis/conjunctive and switchroles then pipe that into "if"
        '''for child in split_file.iter('node'):
            node_list.append(child.attrib)
        return split_file, node_list'''
        # below prints out node names
        for node in split_file.iter('label'):
            # print(node.text + "\"\n", end="\"")
            node_list.append(node.text)
        for l in split_file.iter('node'):
            level.append(l.text)
            mylst = [s.replace('\n\t', '') for s in level]
            levels = [len(i) for i in mylst]
        print(pair := {k: v for k, v in zip(node_list, levels)})
        return split_file, node_list, levels


if __name__ == '__main__':
    Main.main()
