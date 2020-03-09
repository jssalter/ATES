;;;====================================================== 
;;;   Self Learning Decision Tree Program
;;;
;;;   This program tries to determine the animal you are 
;;;   thinking of by asking questions. 
;;; 
;;;   Jess Version 4.2 Example 
;;; 
;;;   To execute, merely load the file with the command
;;;   (batch "Attack_Trees/JESS/RFID_Comm_Block.clp")
;;;======================================================

(clear)
(reset)
;;;;;;;;;;;;;;;;;;;;
;template for nodes:
(deftemplate node "Data about nodes"
(slot name)
(slot parent)
(slot cost (default 0))
(slot duration (default 0))
(slot exploited (default FALSE))
(slot countermeasure (default FALSE))
(multislot siblings (default nil)) ;for "and" nodes of same level
(multislot children (default nil)))

;;;;;;;;;;;;;;;;;;;;
;template for trees:
(deftemplate tree "Data about ATs"
(slot name)
(slot rootnode))

;;;;;;;;;;;;;;;;;;;;;;;;;
;planned space for rules:
;(defrule tree-has-root
;	"Make sure a tree has a root node."
;
;(defrule node-exploited
;something like "if node exploited = true and node has no siblings then progress up"??
;	"If a node is exploited, then move up the tree"
;	(node (exploited ?x))
;	(test (?x))
;	=>
;	(printout t "A node is exploited!" crlf)
;	($activenode <- (node (parent))))
;

;;;;;;;;;;;;
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
;

(assert (node (name "Block Communication")))
(assert (node (name "Block Tag Reader")))
(assert (node (name "Shield Tag")))
(assert (node (name "Be in Vicinity of Tag")))
(assert (node (name "Secure Warehouse")))
(assert (node (name "Faraday Cage")))
(assert (node (name "Cage Around Reader")))
(assert (node (name "Cage Around Tag")))
(assert (node (name "Blocker Reader")))
(assert (node (name "Blocker Tag")))
(assert (node (name "Jam Signal")))
(assert (node (name "Isolate Network")))
(assert (node (name "Secure Warehouse")))
(assert (node (name "Faraday Around Tag and Reader")))
(assert (node (name "Block Reader Backend")))
(assert (node (name "Dos in Network")))

(run)

