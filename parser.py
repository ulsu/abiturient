# -*- coding: utf-8 -*-
import MySQLdb

db = MySQLdb.Connect(host='localhost', user='abitur', passwd='b33ac24a', db='abiturient')
c = db.cursor()
c.execute('SET NAMES utf8')
c.execute('SELECT * FROM `temp_all`')
rows = c.fetchall()
for r in rows:
	c.execute('SELECT `id` FROM `temp_spec` WHERE `name`="'+str(r[2])+'"')
	spec = c.fetchall()
	if spec:
		spec_id = spec[0][0]
		print spec_id
	else:
		c.execute('INSERT INTO `temp_spec`(`name`) VALUES ("'+str(r[2])+'")')
		db.commit()
		c.execute('SELECT `id` FROM `temp_spec` WHERE `name`="'+str(r[2])+'"')
		spec = c.fetchall()
		spec_id = spec[0][0]
		print spec_id



	print 'SELECT `id` FROM `temp_fac` WHERE `name`="'+str(r[3])+'"'
	c.execute('SELECT `id` FROM `temp_fac` WHERE `name`="'+str(r[3])+'"')
	fac = c.fetchall()
	if fac:
		fac_id = fac[0][0]
		print fac_id
	else:
		c.execute('INSERT INTO `temp_fac`(`name`) VALUES ("'+str(r[3])+'")')
		db.commit()
		c.execute('SELECT `id` FROM `temp_fac` WHERE `name`="'+str(r[3])+'"')
		fac = c.fetchall()
		fac_id = fac[0][0]
		print fac_id



	c.execute('SELECT `id` FROM `temp_ef` WHERE `name`="'+str(r[4])+'"')
	ef = c.fetchall()
	if ef:
		ef_id = ef[0][0]
		print ef_id
	else:
		c.execute('INSERT INTO `temp_ef`(`name`) VALUES ("'+str(r[4])+'")')
		db.commit()
		c.execute('SELECT `id` FROM `temp_ef` WHERE `name`="'+str(r[4])+'"')
		ef = c.fetchall()
		ef_id = ef[0][0]
		print ef_id


	c.execute('SELECT `id` FROM `temp_exam` WHERE `name`="'+r[5]+'"')
	exam = c.fetchall()
	if exam:
		exam_id = exam[0][0]
	else:
		c.execute('INSERT INTO `temp_exam`(`name`) VALUES ("'+r[5]+'")')
		db.commit()
		c.execute('SELECT `id` FROM `temp_exam` WHERE `name`="'+r[5]+'"')
		exam = c.fetchall()
		exam_id = exam[0][0]


	print 'INSERT INTO `temp_all_num`(`s_id`, `spec_id`, `fac_id`, `ef_id`, `exam_id`) VALUES ("%s", "%s", "%s", "%s", "%s")' % (r[1], spec_id, fac_id, ef_id, exam_id)
	c.execute('INSERT INTO `temp_all_num`(`s_id`, `spec_id`, `fac_id`, `ef_id`, `exam_id`) VALUES ("%s", "%s", "%s", "%s", "%s")' % (r[1], spec_id, fac_id, ef_id, exam_id))
	db.commit()

