# -*- coding: utf-8 -*-
import MySQLdb
db = MySQLdb.Connect(host='localhost', user='abitur', passwd='b33ac24a', db='abiturient')
c = db.cursor()
c.execute('SET NAMES utf8')
c.execute('SELECT * FROM `temp_all_num`')
rows = c.fetchall()

for r in rows:
 	print 'SELECT `id` FROM `temp_mm_exam` WHERE `s_id`="'+str(r[1])+'" AND `spec_id`="'+str(r[2])+'" AND `fac_id`="'+str(r[3])+'" AND `ef_id`="'+str(r[4])+'"'
	c.execute('SELECT `id` FROM `temp_mm_exam` WHERE `s_id`="'+str(r[1])+'" AND `spec_id`="'+str(r[2])+'" AND `fac_id`="'+str(r[3])+'" AND `ef_id`="'+str(r[4])+'"')
	mm_exam = c.fetchall()
	if mm_exam:
		mm_exam_id = mm_exam[0][0]
	else:
		c.execute('INSERT INTO `temp_mm_exam`(`s_id`, `spec_id`, `fac_id`, `ef_id`) VALUES ("%s", "%s", "%s", "%s")' % (r[1], r[2], r[3], r[4])) 
		db.commit()
		c.execute('SELECT `id` FROM `temp_mm_exam` WHERE `s_id`="'+str(r[1])+'" AND `spec_id`="'+str(r[2])+'" AND `fac_id`="'+str(r[3])+'" AND `ef_id`="'+str(r[4])+'"')
		mm_exam = c.fetchall()
		mm_exam_id = mm_exam[0][0]



	c.execute('INSERT INTO `temp_mm_exam_linker`(`exam_id`, `mm_exam_id`) VALUES ("%s", "%s")' % (r[5], mm_exam_id)) 


		
	



