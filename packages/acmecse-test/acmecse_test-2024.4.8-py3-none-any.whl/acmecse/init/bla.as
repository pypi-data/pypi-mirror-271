@name scratch
@onKey ü
@tuiTool
@tuiInput Attribute


(while true (
	(print "hallo")
	(sleep 1)))

(clear-console)

(if (!= argc 2)
	((print "[red]Add one identifier without spaces")
	 (quit)))
(dolist (t (cse-attribute-infos (argv 1)))
	(
	 (print "[dodger_blue2]attribute  = " (nth 1 t))
	 (print "[dark_orange]short name = " (nth 0 t))
	 (print "type       = " (nth 2 t) nl)))

(quit)




(print 'test)


(dolist (i '(1 2 3 4 5 6 7 8 9 10))
	(print i))                   ;; print 1..10

(setq result 0)
(dolist (i '(1 2 3 4 5 6 7 8 9 10) result)
	(setq result (+ result i)))  ;; sum 1..10
(print result)                   ;; 55


(defun x ()
	(print "hallo"))

(print (dotimes (var 10)
	(print var)))

(print (dolist (var '(1 2 3 4 5 6 7 8 9 10) result)
	((print var)
	 (setq result var))))
( print result)



(setq result 0)
(dotimes (i 10 result)
	(setq result (+ result i)))  ;; sum 1..10
(print result)


;;(setq result 23)
(print (dotimes (var (+ 1 1) result) ((x) (setq result var))))


(print '(1 2 3 4 5 6 7 8 9 10))

(print nil)

(tui-notify "test" )
(tui-notify "test" "title" )
(tui-notify "test" "title" "default")
(tui-notify "test" "title" "information")
(tui-notify "test" "title" "warning")
(tui-notify "test" "title" "error" )
(tui-notify "test" "title" "error" nil )
(tui-notify "test" "title" "error" 5 )

