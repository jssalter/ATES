import tkinter as tk
from tkinter import filedialog, DISABLED
from defusedxml.ElementTree import parse as DETparse
import os

IDs = []
names = []
parents = []
costs = []
durations = []
exploiteds = []
countermeasures = []
connectors = []
children = []
files = []
test = []
welcome = '    =======================================' \
          '\n       Thank you for using AT->ES.' \
          '\nThis will convert from UATMM XML format Attack Trees' \
          '\n   and create a JESS program for AT analysis' \
          '\n        This was written in Python 3.8' \
          '\n       Questions, comments, concerns?' \
          '\n     Jonathan-Steven.Salter@stud.vgtu.lt' \
          '\n   ======================================='


def inputter(file_name):
    tree = DETparse(file_name)
    root = tree.getroot()
    # node = tree.getnode()
    # print(node.tag)
    print(f'Tag = {root.tag}. Attribute = {root.attrib}.')
    return root


def lister(root):
    for child in root:
        IDs.append(child.attrib.get('id'))
        names.append(child.attrib.get('label'))
        parents.append(child.attrib.get('parents', 'nil'))
        costs.append(child.attrib.get('cost', 0))
        durations.append(child.attrib.get('duration', 0))
        exploiteds.append(child.attrib.get('exploited', 'FALSE'))
        countermeasures.append(child.attrib.get('role', 'FALSE'))
        children.append(child.attrib.get('children', 'nil').split())
        try:
            umm = child.find('connector').attrib
            connectors.append(umm.get('{http://www.w3.org/2001/XMLSchema-instance}type', 'nil').split(':')[1])
        except AttributeError:
            connectors.append('nil')
    return IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors


def printer(IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors, new_file_name):
    i = 0
    try:
        os.makedirs('Attack_Trees/JESS')
    except FileExistsError:
        pass
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
                    '(clear)\n'
                    '(reset)\n\n'
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
                    '		(default nil))'
                    '	(slot cost \n'
                    '		(type INTEGER)\n'
                    '		(default 0))\n'
                    '	(slot duration \n'
                    '		(type INTEGER)\n'
                    '		(default 0))\n'
                    '	(slot exploited \n'
                    '		(type SYMBOL)\n'
                    '		(default FALSE))\n'
                    '	(slot countermeasure \n'
                    '		(type SYMBOL)\n'
                    '		(default FALSE))\n'
                    '	(multislot children\n'
                    '		(type INTEGER)\n'
                    '		(default nil)))\n'
                    ';;;;;;;;;;;;;;;;;;;;\n'
                    ';template for trees:\n'
                    '(deftemplate tree "Data about ATs"\n'
                    '	(slot name\n'
                    '		(type STRING)\n'
                    '		(default ""))\n'
                    '	(slot rootnode\n'
                    '		(type STRING)\n'
                    '		(default "")))'
                    '\n'
                    ';;;;;;;;;;;;;;;;;;;;;;;;;\n'
                    ';planned space for rules:\n'
                    ';(defrule tree-has-root\n'
                    ';	"Make sure a tree has a root node."\n'
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
                    ';\n\n'
                    f'(assert (tree (name "{new_file_name.split("_UAT")[0]}") (rootnode "{names[0]}")))\n')
            while i < len(IDs):
                f.write(f'(assert (node (ID "{IDs[i]}") (name "{names[i]}") (parent "{parents[i]}") (connector "{connectors[i]}") '
                        f'(cost "{costs[i]}") (duration "{durations[i]}") (exploited "{exploiteds[i]}") '
                        f'(countermeasure "{countermeasures[i]}") (children "{children[i]}")))\n')
                i += 1
            else:
                f.write("\n(run)\n")


def updater(choice, IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors):
    choice_list = ['nothing', 'costs', 'durations', 'exploited', 'countermeasure']
    # todo: find a way to ensure that choice is between 3 and 6. Also exploited/countermeasure is either TRUE or FALSE
    if 0 <= int(choice) <= 5:
        print(f'You have chosen {choice} which relates to {choice_list[int(choice)]}')
        nchoice = input('What is the ID of node you would like to change? ')
        print(f'You have chosen the node "{names[int(nchoice)]}".')
        vchoice = input('What would you like the value to be? ')
        print(f"You have chosen to change node {names[int(nchoice)]} value for {choice} attribute to {vchoice}.")
        costs[int(nchoice)] = vchoice
        return IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors
    else:
        print("I'm sorry, your selection was out of range. Please try again.")


def ATES(file):
    try:
        IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors = lister(root := inputter(file))
        file_path, file_name = os.path.split(file)
        new_file_name, old_ext = os.path.splitext(file_name)
        countermeasures = [w.replace('Counteracting', 'TRUE') for w in countermeasures]
        printer(IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors, new_file_name)
    except:
        message = 'An error has occurred. Please try again.'
    else:
        message = 'Conversion was successful!'
    finally:
        label = tk.Label(frame, text=message)
        label.grid()

#  todo: add in ability to change costs/duration/exploited/whatever values and re-run

    # decision = input('Would you like to change any values (y/n)? ').lower()
    # if decision == 'n':
    #     pass
    #     # filewriter(stuff)
    # elif decision == 'y':
    #     print('------------')
    #     choice = input('Which value would you like to change? 1-4: \n cost (1), duration (2), exploited (3), or '
    #                    'countermeasure (4) ')
    #     updater(choice, IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors)
    #     printer(IDs, names, parents, costs, durations, exploiteds, countermeasures, children, connectors)
    #     pass
    # else:
    #     print("I don't understand your selection. Please try again.")
    #     pass


def addfile():
    for widget in frame.winfo_children():
        widget.destroy()

    # todo: change below command to "filenames" and fix to allow multiple files at once
    file_name = filedialog.askopenfilename(title="Select file",
                                                  filetypes=(("XML files", "*.xml"), ("all files", "*.*")))
    files.append(file_name)
    for file in files:
        label = tk.Label(frame, text=file)
        label.grid()


# todo: add value change abilities to this command
def translate():
    for file in files:
        ATES(file)
    # with open('translated.txt', 'w') as f:
    #     f.write(translation + ',')


def writefile():
    pass
    # for file in files:
    #     printer(ATES(file))


window = tk.Tk()
window.title('AT -> ES Converter')

canvas = tk.Canvas(window, height=500, width=1000)
canvas.grid()

frame = tk.Frame(window)
frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

# todo: use below as input field for changing values in the lists
# textbox = tk.Entry(window)
# textbox.grid(row=1, column=0)
# textbox.insert(0, 'Enter a new value.')

openFile = tk.Button(window, text='Open File', padx=33, command=addfile)
openFile.grid()

translateFiles = tk.Button(window, text='Translate ', padx=33, command=translate)
translateFiles.grid(row=31, column=0)

writefile = tk.Button(window, text='Write translated file', padx=7, command=writefile, state=DISABLED)
writefile.grid(row=32, column=0)

label = tk.Label(frame, text=welcome)
label.pack()


window.mainloop()

# if __name__ == '__main__':
#     main()
