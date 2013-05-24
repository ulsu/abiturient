# -*- coding: utf-8 -*-
import MySQLdb
db = MySQLdb.Connect(host='localhost', user='abitur', passwd='b33ac24a', db='abiturient')
c = db.cursor()
c.execute('SET NAMES utf8')
c.execute('SELECT * FROM `temp_mm_exam`')
rows = c.fetchall()


for r in rows:
 	print 'SELECT `id` FROM `temp_spec_fac` WHERE `spec_id`="'+str(r[2])+'" AND `fac_id`="'+str(r[3])+'"'
	c.execute('SELECT `id` FROM `temp_spec_fac` WHERE `spec_id`="'+str(r[2])+'" AND `fac_id`="'+str(r[3])+'"')
	spec_fac = c.fetchall()
	if spec_fac:
		spec_fac_id = spec_fac[0][0]
	else:
		c.execute('INSERT INTO `temp_spec_fac`(`spec_id`, `fac_id`) VALUES ("%s", "%s")' % (r[2], r[3]))
		db.commit()
		c.execute('SELECT `id` FROM `temp_spec_fac` WHERE `spec_id`="'+str(r[2])+'" AND `fac_id`="'+str(r[3])+'"')
		spec_fac = c.fetchall()
		spec_fac_id = spec_fac[0][0]



	c.execute('INSERT INTO `temp_mainspec`(`id`, `mainspec_id`, `eduform_id`, `spec_fac_id`) VALUES ("%s", "%s", "%s", "%s")' % (r[0], r[1], r[4], spec_fac_id)) 
