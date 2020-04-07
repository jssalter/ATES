# Used to create GUI window and import files via GUI.
import tkinter as tk
from tkinter import filedialog
# A secure XML parsing function.
from defusedxml.ElementTree import parse as detparse
# Allows for reading and writing files.
import os

# This version prints two JESS files; one is the program and one is the data file.

# Empty list for collecting file names for translation.
files = []
# Banner message for GUI window.
welcome = '    =======================================' \
          '\n       Thank you for using AT->ES.' \
          '\nThis will convert from UATS XML format Attack Trees' \
          '\n   and create a JESS program for AT analysis' \
          '\n        This was written in Python 3.8' \
          '\n       Questions, comments, concerns?' \
          '\n     Jonathan-Steven.Salter@stud.vgtu.lt' \
          '\n   ======================================='


# Inputs XML files, parses them, and returns the XML data.
def inputter(file_name):
    tree = detparse(file_name)
    root = tree.getroot()
    return root


# Extracts the desired data from the XML data.
def lister(root):
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
    # Fills above lists with data from the XML files.
    for child in root:
        ids.append(child.attrib.get('id'))
        names.append(child.attrib.get('label'))
        parents.append(child.attrib.get('parents', 'nil'))
        costs.append(child.attrib.get('cost', 0))
        probabilities.append(child.attrib.get('probability', 0.0))
        difficulties.append((child.attrib.get('difficulty', 0)))
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
def printer(ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties, new_file_name):
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
            f.write(';;;====================================================== \n'
                    ';;;   This was created with the ATES Conversion program \n'
                    ';;;   Place this file in a subdirectory from your JESS \n'
                    ';;;   program named /Attack_Trees/JESS \n'
                    ';;;    \n'
                    ';;;   Created by Jon Salter at VGTU \n'
                    ';;;    \n'
                    ';;;    \n'
                    ';;;   To execute, merely load the file with the command\n'
                    f';;;   (batch "Attack_Trees/JESS/{new_file_name}.clp")\n'
                    ';;;======================================================\n\n'
                    '(clear)\n\n'
                    ';;;;;;;;;;;;;;;;;;;;\n'
                    ';template for nodes:\n'
                    '(deftemplate node "Data about nodes"\n'
                    '	(slot ID\n'
                    '		(type INTEGER))\n'
                    '	(slot name\n'
                    '		(type STRING)\n'
                    '		(default ""))\n'
                    '	(slot parent\n'
                    '		(type STRING)\n'
                    '		(default ""))\n'
                    '	(slot connector \n'
                    '		(type STRING)\n'
                    '		(default nil))\n'
                    '	(slot cost \n'
                    '		(type INTEGER)\n'
                    '		(default 0))\n'
                    '	(slot time \n'
                    '		(type INTEGER)\n'
                    '		(default 0))\n'                    
                    '	(slot difficulty \n'
                    '		(type INTEGER)\n'
                    '		(default 0))\n'
                    '	(slot probability \n'
                    '		(type FLOAT)\n'
                    '		(default 0.0))\n'
                    '	(slot exploited \n'
                    '		(type SYMBOL)\n'
                    '		(default FALSE))\n'
                    '	(slot countermeasure \n'
                    '		(type SYMBOL)\n'
                    '		(default FALSE))\n'
                    '	(multislot children\n'
                    '		(type STRING)\n'
                    '		(default nil)))\n'
                    ';;;;;;;;;;;;;;;;;;;;\n'
                    ';template for trees:\n'
                    '(deftemplate tree "Data about ATs"\n'
                    '	(slot tname\n'
                    '		(type STRING)\n'
                    '		(default ""))\n'
                    '	(slot rootnode\n'
                    '		(type STRING)\n'
                    '		(default "")))'
                    '\n'
                    ';;;;;;;;;;;;;;;;;;;;;;;;;\n'
                    ';planned space for rules:\n'
                    ';(defrule initialize-1\n'
                    ';	(not (node (name root)))\n'
                    ';	=>\n'
                    f';	(load-facts "Attack_Trees/JESS/{new_file_name}.dat")\n'
                    ';	(assert (current-node root)))\n\n'
                    ';;\n'
                    ';(defrule ask-decision-node-question\n'
                    ';	?node <- (current-node ?name)\n'
                    ';	(node (name ?name)\n'
                    ';		(type decision)\n'
                    ';		(question ?question))\n'
                    ';	(not (answer ?))\n'
                    ';	=>\n'
                    ';	(printout t ?question " (yes or no) ")\n'
                    ';	(assert (answer (read))))\n'
                    ';\n'
                    ';(defrule bad-answer\n'
                    ';	?answer <- (answer ~yes&~no)\n'
                    ';	=>\n'
                    ';	(printout t "Answer not understood. Please try again." crlf)\n'
                    ';	(retract ?answer))\n'
                    ';\n'
                    ';(defrule change-value\n'
                    ';	\n'
                    ';\n'
                    ';\n'
                    ';\n'
                    ';\n'
                    ';(defrule node-exploited\n'
                    ';something like "if node exploited = true and node has no ands then progress up"??\n'
                    ';	"If a node is exploited, then move up the tree"\n'
                    ';	(node (exploited ?x))\n'
                    ';	(test (?x))\n'
                    ';	=>\n'
                    ';	(printout t "A node is exploited!" crlf)\n'
                    ';	($activenode <- (node (parent))))\n'
                    ';\n'
                    '\n'
                    ';;;;;;;;;;;;;;;;;;;;;;;;;\n'
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
                    ';;;;;;;;;;;;;;;;;;;;; \n'
                    '\n(reset)\n(run)\n')
            # Writes the data for each node into its own fact in a separate data file.
        with open('Attack_Trees/JESS/' + new_file_name + '.dat', 'w') as f:
            f.write(f'(MAIN::tree (tname "{treename}") (rootnode "{names[0]}")))')
            # Writes the data for each node into its own JESS fact.
            while i < len(ids):
                f.write(f'\n(MAIN::node (ID {ids[i]}) (name "{names[i]}") (parent {parents[i]}) (connector {connectors[i]}) '
                        f'(cost {costs[i]}) (time {times[i]}) (exploited {exploiteds[i]}) (probability {probabilities[i]}) '
                        f'(difficulty {difficulties[i]}) (countermeasure {countermeasures[i]}) (children {children[i]}))')
                i += 1


# Compiles the functions for parsing, formatting, and writing files into one function. Returns a success/fail message.
def ates(file):
    try:
        ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties = lister(root := inputter(file))
        # Gets the file name, extension, and path from the input files.
        file_path, file_name = os.path.split(file)
        new_file_name, old_ext = os.path.splitext(file_name)
        # Changes countermeasures values from UATS format to JESS format.
        countermeasures = [w.replace('Counteracting', 'TRUE') for w in countermeasures]
        printer(ids, names, parents, costs, times, exploiteds, countermeasures, children, connectors, probabilities, difficulties, new_file_name)
    # Returns a message to the window for either success or failure.
    except Exception as e:
        message = f'An error ({e}) has occurred. Please try again.'
    else:
        message = 'Conversion was successful!'
    finally:
        label2 = tk.Label(frame, text=message)
        label2.grid()


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
        label1.grid()


# Translates all files added in the window.
def translate():
    for file in files:
        ates(file)


# Creates and formats a simple GUI window.
window = tk.Tk()
window.title('AT -> ES Converter')

canvas = tk.Canvas(window, height=500, width=1000)
canvas.grid()

frame = tk.Frame(window)
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

openFile = tk.Button(window, text='Select File(s)', padx=6, command=addfile)
openFile.grid()

translateFiles = tk.Button(window, text='Convert File(s)', command=translate)
translateFiles.grid(row=31, column=0)

label = tk.Label(frame, text=welcome)
label.pack()

# Keeps the script running while the window is open.
window.mainloop()
