;;;====================================================== 
;;;   This was created with the ATES Conversion program 
;;;   Place this file in a subdirectory from your JESS  
;;;   program named /Attack_Trees/JESS 
;;;    
;;;   Created by Jon Salter at VGTU 
;;;    
;;;    
;;;   To execute, load the file with the below command
;;;   (batch "Attack_Trees/JESS/RFID_Comm_Block_UATS.clp")
;;;======================================================

(clear)

;;;;;;;;;;;;;;;;;;;;
; Node Template:
(deftemplate node "Data about nodes"
	(slot id
		(type INTEGER))
	(slot name
		(type STRING)
		(default ""))
	(slot parent
		(type STRING)
		(default ""))
	(slot connector
		(type STRING)
		(default nil)
		(allowed-values nil AND OR XOR SAND))
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
		(default FALSE)
		(allowed-values TRUE FALSE))
	(slot countermeasure 
		(type SYMBOL)
		(default FALSE)
		(allowed-values TRUE FALSE))
	(multislot children
		(type INTEGER)
		(default nil)))

;;;;;;;;;;;;;;;;;;;;
; Tree Template:
(deftemplate tree "Data about ATs"
	(slot tname
		(type STRING)
		(default ""))
	(slot rootnode
		(type STRING)
		(default "")))

;;;;;;;;;;;;;;;;;;;;;
; Inputting tree and nodes to working memory:
(deffacts AttackTree "RFID Comm Block UATS"
(tree (tname "RFID Comm Block UATS") (rootnode "Block Communication"))
(node (id 0) (name "Block Communication") (parent nil) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 1 14))
(node (id 1) (name "Block Tag Reader") (parent 0) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 2 8 9 10))
(node (id 2) (name "Shield Tag") (parent 1) (connector AND) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 3 5))
(node (id 3) (name "Be in Vicinity of Tag") (parent 2) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 4))
(node (id 4) (name "Secure Warehouse") (parent 3) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children nil))
(node (id 5) (name "Faraday Cage") (parent 2) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 6 7))
(node (id 6) (name "Cage Around Reader") (parent 5) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (id 7) (name "Cage Around Tag") (parent 5) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (id 8) (name "Blocker Reader") (parent 1) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (id 9) (name "Blocker Tag") (parent 1) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil))
(node (id 10) (name "Jam Signal") (parent 1) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 11))
(node (id 11) (name "Isolate Network") (parent 10) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children 12 13))
(node (id 12) (name "Secure Warehouse") (parent 11) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children nil))
(node (id 13) (name "Faraday Around Tag and Reader") (parent 11) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure TRUE) (children nil))
(node (id 14) (name "Block Reader Backend") (parent 0) (connector OR) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children 15))
(node (id 15) (name "Dos in Network") (parent 14) (connector nil) (cost 0) (time 0) (exploited FALSE) (probability 0.0) (difficulty 0) (countermeasure FALSE) (children nil)))

(reset)
(run)
