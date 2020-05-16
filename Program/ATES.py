# Used to create GUI window and import files via GUI.
import tkinter as tk
from tkinter import filedialog
# A secure XML parsing function.
from defusedxml.ElementTree import parse as detparse
# Allows for reading and writing files.
import os


# Empty list for collecting file names for translation.
files = []
# Banner message for GUI window.
welcome = '    =======================================' \
          '\n       Thank you for using AT->ES.' \
          '\nThis will convert from UATS XML format Attack Trees' \
          '\n   and create a JESS program for AT analysis' \
          '\n        This was written in Python 3.8' \
          '\n\n   v1 is a simple conversion without JESS program' \
          '\n   v2 includes a functional JESS program' \
          '\n\n       Questions, comments, concerns?' \
          '\n     Jonathan-Steven.Salter@stud.vgtu.lt' \
          '\n   ======================================='


# Inputs XML files, parses them, and returns the XML data.
def inputter(file_name):
    tree = detparse(file_name)
    root = tree.getroot()
    return root


# Extracts the desired data from the UATS format XML data.
def lister_uats(root):
    # Creates lists for Node attributes.
    ids = []
    names = []
    parents = []
    costs = []
    probabilities = []
    difficulties = []
    times = []
    exploiteds = []
    countermeasures = []
    connectors = []
    children = []
    # Fills above lists with data from the XML files. Alter the attribute within the get to change formats.
    for child in root:
        ids.append(child.attrib.get('id'))
        names.append(child.attrib.get('label'))
        parents.append(child.attrib.get('parents', 'nil'))
        costs.append(child.attrib.get('cost', 0))
        probabilities.append(child.attrib.get('probability', 0.0))
        difficulties.append(child.attrib.get('difficulty', 0))
        times.append(child.attrib.get('time', 0))
        exploiteds.append(child.attrib.get('exploited', 'FALSE'))
        countermeasures.append(child.attrib.get('role', 'FALSE'))
        children.append(child.attrib.get('children', 'nil'))
        # Transforms the complex "connector" attribute in the XML file into "AND", "OR", or "nil".
        try:
            cnct = child.find('connector').attrib
            connectors.append(cnct.get('{http://www.w3.org/2001/XMLSchema-instance}type', 'nil').split(':')[1])
        except AttributeError:
            connectors.append('nil')
    return ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties


# Writes the XML data into the JESS format.
def printerv1(ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties, new_file_name):
    # Used for writing the information for each node.
    i = 0
    # Used for the tree name in the "facts" portion of the JESS file.
    treename = new_file_name.replace('_', ' ')
    # Creates the directory for the translated files to go in to, then writes the file.
    try:
        os.makedirs('Attack_Trees/JESS')
    except FileExistsError:
        pass
    # Writes the JESS program into its own file.
    finally:
        with open('Attack_Trees/JESS/' + new_file_name + '.clp', 'w') as f:
            f.write(';;;====================================================== '
                    '\n;;;   This was created with the ATES Conversion program '
                    '\n;;;   Place this file in a subdirectory from your JESS  '
                    '\n;;;   program named /Attack_Trees/JESS '
                    '\n;;;    '
                    '\n;;;   Created by Jon Salter at VGTU '
                    '\n;;;    '
                    '\n;;;    '
                    '\n;;;   To execute, load the file with the below command'
                    f'\n;;;   (batch "Attack_Trees/JESS/{new_file_name}.clp")'
                    '\n;;;======================================================'
                    '\n\n(clear)'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Node Template:'
                    '\n(deftemplate node "Data about nodes"'
                    '\n	(slot id'
                    '\n		(type INTEGER))'
                    '\n	(slot name'
                    '\n		(type STRING)'
                    '\n		(default ""))'
                    '\n	(slot parent'
                    '\n		(type STRING)'
                    '\n		(default ""))'
                    '\n	(slot connector'
                    '\n		(type STRING)'
                    '\n		(default nil)'
                    '\n		(allowed-values nil AND OR XOR SAND))'
                    '\n	(slot cost'
                    '\n		(type INTEGER)'
                    '\n		(default 0))'
                    '\n	(slot time'
                    '\n		(type INTEGER)'
                    '\n		(default 0))'                    
                    '\n	(slot difficulty'
                    '\n		(type INTEGER)'
                    '\n		(default 0))'
                    '\n	(slot probability'
                    '\n		(type FLOAT)'
                    '\n		(default 0.0))'
                    '\n	(slot exploited'
                    '\n		(type SYMBOL)'
                    '\n		(default FALSE)'
                    '\n		(allowed-values TRUE FALSE))'
                    '\n	(slot countermeasure '
                    '\n		(type SYMBOL)'
                    '\n		(default FALSE)'
                    '\n		(allowed-values TRUE FALSE))'
                    '\n	(multislot children'
                    '\n		(type INTEGER)'
                    '\n		(default nil)))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Tree Template:'
                    '\n(deftemplate tree "Data about ATs"'
                    '\n	(slot tname'
                    '\n		(type STRING)'
                    '\n		(default ""))'
                    '\n	(slot rootnode'
                    '\n		(type STRING)'
                    '\n		(default "")))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;;'
                    '\n; Inputting tree and nodes to working memory:'
                    f'\n(deffacts AttackTree "{treename}"'
                    f'\n(tree (tname "{treename}") (rootnode "{names[0]}"))')
            # Writes the data for each node into its own JESS fact.
            while i < len(ids):
                f.write(f'\n(node (id {ids[i]}) (name "{names[i]}") (parent {parents[i]}) (connector {connectors[i]}) '
                        f'(cost {costs[i]}) (time {times[i]}) (exploited {exploiteds[i]}) (probability {probabilities[i]}) '
                        f'(difficulty {difficulties[i]}) (countermeasure {countermeasures[i]}) (children {children[i]}))')
                i += 1
            else:
                # Finishes the data file.
                f.write(')\n\n(reset)\n(run)\n')


def printerv2(ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties, new_file_name):
    # Used for writing the information for each node.
    i = 0
    # Used for the tree name in the "facts" portion of the JESS file.
    treename = new_file_name.replace('_', ' ')
    # Creates the directory for the translated files to go in to, then writes the file.
    try:
        os.makedirs('Attack_Trees/JESS')
    except FileExistsError:
        pass
    # Writes the JESS program into its own file.
    finally:
        with open('Attack_Trees/JESS/' + new_file_name + 'v2.clp', 'w') as f:
            # Writes the data for each node into its own fact in a separate data file.
            f.write(';;;====================================================== '
                    '\n;;;   This was created with the ATES Conversion program '
                    '\n;;;   Place this file in a subdirectory from your JESS  '
                    '\n;;;   program named /Attack_Trees/JESS '
                    '\n;;;    '
                    '\n;;;   Created by Jon Salter at VGTU '
                    '\n;;;    '
                    '\n;;;    '
                    '\n;;;   To execute, load the file with the below command'
                    f'\n;;;   (batch "Attack_Trees/JESS/{new_file_name}v2.clp")'
                    '\n;;;======================================================'
                    '\n\n(clear)'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Node Template:'
                    '\n(deftemplate node "Data about nodes"'
                    '\n	(slot id'
                    '\n		(type INTEGER))'
                    '\n	(slot name'
                    '\n		(type STRING)'
                    '\n		(default ""))'
                    '\n	(slot parent'
                    '\n		(type STRING)'
                    '\n		(default ""))'
                    '\n	(slot connector'
                    '\n		(type STRING)'
                    '\n		(default nil)'
                    '\n		(allowed-values nil AND OR XOR SAND))'
                    '\n	(slot cost'
                    '\n		(type INTEGER)'
                    '\n		(default 0))'
                    '\n	(slot time'
                    '\n		(type INTEGER)'
                    '\n		(default 0))'
                    '\n	(slot difficulty'
                    '\n		(type INTEGER)'
                    '\n		(default 0))'
                    '\n	(slot probability'
                    '\n		(type FLOAT)'
                    '\n		(default 0.0))'
                    '\n	(slot exploited'
                    '\n		(type SYMBOL)'
                    '\n		(default FALSE)'
                    '\n		(allowed-values TRUE FALSE))'
                    '\n	(slot countermeasure '
                    '\n		(type SYMBOL)'
                    '\n		(default FALSE)'
                    '\n		(allowed-values TRUE FALSE))'
                    '\n	(multislot children'
                    '\n		(type INTEGER)'
                    '\n		(default nil)))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Tree Template:'
                    '\n(deftemplate tree "Data about ATs"'
                    '\n	(slot tname'
                    '\n		(type STRING)'
                    '\n		(default ""))'
                    '\n	(slot rootnode'
                    '\n		(type STRING)'
                    '\n		(default "")))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Fact template for JESS program:'
                    '\n(deftemplate program "Program default facts"'
                    '\n	(slot phase'
                    '\n		(type STRING)'
                    '\n		(default initialization)))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Fact template for questions:'
                    '\n(deftemplate question'
                    '\n	(slot ident)'
                    '\n	(slot text)'
                    '\n	(slot answer'
                    '\n		(default nil)))'
                    '\n\n; Default fact for the program:'
                    '\n(deffacts Program "ATES"'
                    '\n	(program))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Require statement for fact file:'
                    f'\n(require* "Attack_Trees/JESS/{new_file_name}v2.dat")'
                    '\n\n;;;;;;;;;;;;;;;;;;;;'
                    '\n; Question bank for the program:'
                    '\n(deffacts question-data'
                    '\n	"Questions for the ATs."'
                    '\n	(question (ident node-select) (answer nil)'
                    '\n		(text "Which node ID would you like to select? "))'
                    '\n	(question (ident slot-select) (answer nil)'
                    '\n		(text "Which slot would you like to modify? "))'
                    '\n	(question (ident modify-value) (answer nil)'
                    '\n		(text "What should the value be? "))'
                    '\n	(question (ident main-menu) (answer nil)'
                    '\n		(text "What would you like to do? (l)ookup name, (m)odify data, (v)iew AT, (q)uit: "))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;;;;;;'
                    '\n;Rule Space:'
                    '\n		'
                    '\n(defrule start'
                    '\n	?p <- (program (phase initialization))'
                    '\n	=>'
                    f'\n	(load-facts "Attack_Trees/JESS/{new_file_name}v2.dat")'
                    '\n	(facts)'
                    '\n	(modify ?p (phase main-menu)))'
                    '\n'
                    '\n(defrule name-lookup1'
                    '\n	?p <- (program (phase main-menu))'
                    '\n	?q1 <- (question (ident main-menu) (answer l))'
                    '\n	?q2 <- (question (ident node-select) (text ?t))'
                    '\n	=>'
                    '\n	(printout t ?t)'
                    '\n	(modify ?q1 (answer nil))'
                    '\n	(modify ?q2 (answer (read)))'
                    '\n	(modify ?p (phase name-lookup2)))'
                    '\n'
                    '\n(defrule bad-answer-name-lookup'
                    '\n	?p <- (program (phase name-lookup2))'
                    '\n	?q <- (question (ident node-select) (answer ?x))'
                    '\n	(not (node (id ?x)))'
                    '\n	=>'
                    '\n	(printout t "Node not found. Please try again." crlf)'
                    '\n	(modify ?q (answer nil))'
                    '\n	(modify ?p (phase main-menu)))'
                    '\n'
                    '\n(defrule name-lookup2'
                    '\n	?p <- (program (phase name-lookup2))'
                    '\n	?q <- (question (ident node-select) (answer ?x))'
                    '\n	(node (id ?x) (name ?name))'
                    '\n	=>'
                    '\n	(printout t "Node " ?x "\'s name is " ?name "." crlf)'
                    '\n	(modify ?q (answer nil))'
                    '\n	(modify ?p (phase main-menu)))'
                    '\n'
                    '\n(defrule phase-quit'
                    '\n	(program)'
                    '\n	(question (ident main-menu) (answer q))'
                    '\n	=>'
                    '\n	(remove program)'
                    '\n	(remove question)'
                    f'\n	(save-facts "Attack_Trees/JESS/{new_file_name}v2.dat")'
                    '\n	(exit))'
                    '\n'
                    '\n(defrule view-at'
                    '\n	(program)'
                    '\n	?q <- (question (ident main-menu) (answer v))'
                    '\n	=>'
                    '\n	(facts)'
                    '\n	(modify ?q (answer nil)))'
                    '\n'
                    '\n(defrule pose-question'
                    '\n	(program (phase ?y))'
                    '\n	?q <- (question (ident ?y) (text ?x))'
                    '\n	=>'
                    '\n	(printout t ?x)'
                    '\n	(modify ?q (answer (read))))'
                    '\n'
                    '\n(defrule bad-answer-main-menu'
                    '\n	(program)'
                    '\n	?q <- (question (ident main-menu) (answer ~l&~m&~q&~v&~nil))'
                    '\n	=>'
                    '\n	(printout t "Answer not understood. Please try again." crlf)'
                    '\n	(modify ?q (answer nil)))'
                    '\n'
                    '\n(defrule modify-value1'
                    '\n	?p <- (program (phase main-menu))'
                    '\n	?m <- (question (ident main-menu) (answer m))'
                    '\n	?q1 <- (question (ident node-select) (text ?t1))'
                    '\n	?q2 <- (question (ident slot-select) (text ?t2))'
                    '\n	?q3 <- (question (ident modify-value) (text ?t3))'
                    '\n	=>'
                    '\n	(printout t ?t1)'
                    '\n	(modify ?q1 (answer (read)))'
                    '\n	(printout t ?t2)'
                    '\n	(modify ?q2 (answer (read)))'
                    '\n	(printout t ?t3)'
                    '\n	(modify ?q3 (answer (read)))'
                    '\n	(modify ?m (answer nil))'
                    '\n	(modify ?p (phase modify2)))'
                    '\n'
                    '\n(defrule modify-value2'
                    '\n	?p <- (program (phase modify2))'
                    '\n	?q1 <- (question (ident node-select) (answer ?x))'
                    '\n	?q2 <- (question (ident slot-select) (answer ?y))'
                    '\n	?q3 <- (question (ident modify-value) (answer ?z))'
                    '\n	?n <- (node (id ?x))'
                    '\n	=>'
                    '\n	(try'
                    '\n		(modify ?n (?y ?z))'
                    '\n	catch'
                    '\n		(printout t "Something went wrong. Please try again." crlf)'
                    '\n	finally'
                    '\n		(modify ?q1 (answer nil))'
                    '\n		(modify ?q2 (answer nil))'
                    '\n		(modify ?q3 (answer nil))'
                    '\n		(modify ?p (phase main-menu))))'
                    '\n'
                    '\n(defrule bad-answer-modify-value'
                    '\n	?p <- (program (phase modify2))'
                    '\n	?q1 <- (question (ident node-select) (answer ?x))'
                    '\n	?q2 <- (question (ident slot-select) (answer ?y))'
                    '\n	?q3 <- (question (ident modify-value) (answer ?z))'
                    '\n	(not (node (id ?x)))'
                    '\n	=>'
                    '\n	(printout t "Node not found. Please try again." crlf)'
                    '\n	(modify ?q1 (answer nil))'
                    '\n	(modify ?q2 (answer nil))'
                    '\n	(modify ?q3 (answer nil))'
                    '\n	(modify ?p (phase main-menu)))'
                    '\n'
                    '\n(defrule probability-exploited'
                    '\n	(program)'
                    '\n	?n <- (node {probability >= 1})'
                    '\n	=>'
                    '\n	(modify ?n (exploited TRUE)))'
                    '\n'
                    '\n(defrule countermeasure-protect'
                    '\n	(declare (salience 10))'
                    '\n	?p <- (program)'
                    '\n	?n <- (node (countermeasure TRUE) (exploited TRUE))'
                    '\n	=>'
                    '\n	(printout t "Countermeasure nodes cannot be exploited!" crlf)'
                    '\n	(modify ?n (exploited FALSE) (probability 0.0))'
                    '\n	(modify ?p (phase main-menu)))'
                    '\n'
                    '\n(defrule node-exploited'
                    '\n	(program)'
                    '\n	(node (id ?id ) (name ?name) (exploited TRUE) (countermeasure FALSE))'
                    '\n	=>'
                    '\n	(printout t "Node " ?id ", " ?name ", is exploited!" crlf))'
                    '\n'
                    '\n(defrule exploit-and-climb1'
                    '\n	(program)'
                    '\n	(node (exploited TRUE) (parent ?x))'
                    '\n	?p <- (node (id ?x) (connector OR) (countermeasure FALSE))'
                    '\n	=>'
                    '\n	(modify ?p (exploited TRUE)))'
                    '\n'
                    '\n(defrule exploit-and-climb2'
                    '\n	(declare (salience 5))'
                    '\n	(program)'
                    '\n	(node (exploited FALSE) (parent ?x))'
                    '\n	?p <- (node (id ?x) (connector AND) (countermeasure FALSE))'
                    '\n	=>'
                    '\n	(modify ?p (exploited FALSE)))'
                    '\n\n;;;;;;;;;;;;;;;;;;;;;'
                    '\n\n(reset)\n(run)\n')
        with open('Attack_Trees/JESS/' + new_file_name + 'v2.dat', 'w') as f:
            f.write(f'(MAIN::tree (tname "{treename}") (rootnode "{names[0]}"))')
            # Writes the data for each node into its own JESS fact.
            while i < len(ids):
                f.write(f'\n(MAIN::node (id {ids[i]}) (name "{names[i]}") (parent {parents[i]}) (connector {connectors[i]}) '
                        f'(cost {costs[i]}) (time {times[i]}) (exploited {exploiteds[i]}) (probability {probabilities[i]}) '
                        f'(difficulty {difficulties[i]}) (countermeasure {countermeasures[i]}) (children {children[i]}))')
                i += 1


# Compiles the functions for parsing, formatting, and writing files into one function. Returns a success/fail message.
def ates(file, pvalue):
    try:
        # Gets the file name, extension, and path from the input files.
        file_path, file_name = os.path.split(file)
        new_file_name, old_ext = os.path.splitext(file_name)
        # Parses the XML file.
        root = inputter(file)
        # Places the node data into lists.
        ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties = lister_uats(root)
        # Changes countermeasures values from UATS format to JESS format.
        countermeasures = [w.replace('Counteracting', 'TRUE') for w in countermeasures]
        # Writes the new file in JESS format.
        if pvalue == 1:
            printerv1(ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties, new_file_name)
        elif pvalue == 2:
            printerv2(ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties, new_file_name)
    # Returns a message to the window for either success or failure.
    except Exception as e:
        message = f'An error ({e}) has occurred. Please try again.'
    else:
        message = 'Conversion was successful!'
    finally:
        label2 = tk.Label(frame, text=message)
        label2.pack()


# Select and add files to the list for translating.
def addfile():
    # Clear the frame to keep from adding multiple entries of the files.
    for widget in frame.winfo_children():
        widget.destroy()
    # Select files one at a time.
    file_name = filedialog.askopenfilename(title="Select file", filetypes=(("XML files", "*.xml"), ("all files", "*.*")))
    files.append(file_name)
    # Show selected file names on the window.
    for file in files:
        label1 = tk.Label(frame, text=file)
        label1.pack()


# Translates all files added in the window.
def translatev1():
    for file in files:
        ates(file, 1)


def translatev2():
    for file in files:
        ates(file, 2)


# Creates and formats a simple GUI window.
window = tk.Tk()
window.title('AT -> ES Converter')

canvas = tk.Canvas(window, height=500, width=1000)
canvas.pack()

frame = tk.Frame(window)
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

openFile = tk.Button(window, text='Select File(s)', padx=14, command=addfile)
openFile.pack()

translateFiles = tk.Button(window, text='Convert File(s) v1', command=translatev1)
translateFiles.pack()

translateFiles = tk.Button(window, text='Convert File(s) v2', command=translatev2)
translateFiles.pack()

# Displays welcome message when the program is loaded.
label = tk.Label(frame, text=welcome)
label.pack()

# Keeps the script running while the window is open.
window.mainloop()
