;;;====================================================== 
;;;   This was created with the ATES Conversion program 
;;;   Place this file in a subdirectory from your JESS 
;;;   program named /Attack_Trees/JESS 
;;;    
;;;   Created by Jon Salter at VGTU 
;;;    
;;;    
;;;   To execute, merely load the file with the command
;;;   (batch "Attack_Trees/JESS/RFID_Comm_Block_UATS.clp")
;;;======================================================

(clear)

;;;;;;;;;;;;;;;;;;;;
;template for nodes:
(deftemplate node "Data about nodes"
	(slot ID
		(type INTEGER))
	(slot name
		(type STRING)
		(default ""))
	(slot parent
		(type STRING)
		(default ""))
	(slot connector 
		(type STRING)
		(default nil))
	(slot cost 
		(type INTEGER)
		(default 0))
	(slot time 
		(type INTEGER)
		(default 0))
	(slot difficulty 
		(type INTEGER)
		(default 0))
	(slot probability 
		(type FLOAT)
		(default 0.0))
	(slot exploited 
		(type SYMBOL)
		(default FALSE))
	(slot countermeasure 
		(type SYMBOL)
		(default FALSE))
	(multislot children
		(type STRING)
		(default nil)))
;;;;;;;;;;;;;;;;;;;;
;template for trees:
(deftemplate tree "Data about ATs"
	(slot tname
		(type STRING)
		(default ""))
	(slot rootnode
		(type STRING)
		(default "")))
;;;;;;;;;;;;;;;;;;;;;;;;;
;planned space for rules:
;(defrule initialize-1
;	(not (node (name root)))
;	=>
;	(load-facts "Attack_Trees/JESS/RFID_Comm_Block_UATS.dat")
;	(assert (current-node root)))

;;
;(defrule ask-decision-node-question
;	?node <- (current-node ?name)
;	(node (name ?name)
;		(type decision)
;		(question ?question))
;	(not (answer ?))
;	=>
;	(printout t ?question " (yes or no) ")
;	(assert (answer (read))))
;
;(defrule bad-answer
;	?answer <- (answer ~yes&~no)
;	=>
;	(printout t "Answer not understood. Please try again." crlf)
;	(retract ?answer))
;
;(defrule change-value
;	
;
;
;
;
;(defrule node-exploited
;something like "if node exploited = true and node has no ands then progress up"??
;	"If a node is exploited, then move up the tree"
;	(node (exploited ?x))
;	(test (?x))
;	=>
;	(printout t "A node is exploited!" crlf)
;	($activenode <- (node (parent))))
;

;;;;;;;;;;;;;;;;;;;;;;;;;
;Query? Something like "if node has parent then parent's child is node"??
;(defrule anc (or (parent ?a ?b) (and (parent ?a ?c)(ancestor ?c ?b)) )
;=> (assert(ancestor ?a ?b)))
;
;(bind ?it (run-query search <string>))
;(while (?it hasNext)
;	(bind ?token (call ?it next))
;	(bind ?fact (call ?token fact 1))
;	(bind ?slot (fact-slot-value ?fact __data))
;	(bind ?datum (nth$ 2 ?slot))
;	(printout t ?datum crlf))
;
;
;something like "if node has no parent then assert rootnode"??
;
;
;
;
;;;;;;;;;;;;;;;;;;;;; 
; inputting tree and nodes to working memory: 
(deffacts AttackTree "RFID Comm Block UATS"
(tree (tname "RFID Comm Block UATS") (rootnode "Block Communication"))
(node (ID 0) (name "Block Communication") (parent nil) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 1 14))
(node (ID 1) (name "Block Tag Reader") (parent 0) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 2 8 9 10))
(node (ID 2) (name "Shield Tag") (parent 1) (connector AND) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 3 5))
(node (ID 3) (name "Be in Vicinity of Tag") (parent 2) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 4))
(node (ID 4) (name "Secure Warehouse") (parent 3) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children nil))
(node (ID 5) (name "Faraday Cage") (parent 2) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 6 7))
(node (ID 6) (name "Cage Around Reader") (parent 5) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (ID 7) (name "Cage Around Tag") (parent 5) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (ID 8) (name "Blocker Reader") (parent 1) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (ID 9) (name "Blocker Tag") (parent 1) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (ID 10) (name "Jam Signal") (parent 1) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 11))
(node (ID 11) (name "Isolate Network") (parent 10) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children 12 13))
(node (ID 12) (name "Secure Warehouse") (parent 11) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children nil))
(node (ID 13) (name "Faraday Around Tag and Reader") (parent 11) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children nil))
(node (ID 14) (name "Block Reader Backend") (parent 0) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 15))
(node (ID 15) (name "Dos in Network") (parent 14) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil)))

(reset)
(run)
