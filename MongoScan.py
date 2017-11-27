#!/usr/bin/python

import pymongo, json, os, string
from pymongo import MongoClient
from pprint import pprint

file1 = open("mongoIPs.txt","r")
ip = file1.readlines()
counter = 0

while counter < len(ip):
	counter += 1
	print "------------------------------------------------------------------------------------"
	
	try:
		print "\nTesting " + ip[counter]
		port = 27017
		web = 8080
		mgmt = 28017
		addr = str(ip[counter]).strip('\r\n')
		
		conn = pymongo.MongoClient(ip[counter],port,connectTimeoutMS=4000,socketTimeoutMS=4000)

		print "Unauthenticated Login to " + ip[counter]

		print "MongoDB Version: " +  conn.server_info()['version']

		print "Debugs enabled : " + str(conn.server_info()['debug'])

		print "Platform: " + str(conn.server_info()['bits']) + " bit"

		print "SysInfo: " + conn.server_info()['sysInfo']


		#print "Commandline switches: " + conn.admin.command('getcmdlineopts')
		print "\r\n -************************************- \r\n"

		dbs = conn.database_names()

		db = conn.admin


		d = dict((db, [collection for collection in conn[db].collection_names()])
			for db in conn.database_names())
		
		print "Show cluster info: \r\n"
		isMaster = db.command('ismaster')
		pprint(isMaster)

		print "\r\n -************************************- \r\n"

		cmdLineOpt = db.command('getCmdLineOpts')
		print "cmdLineOpts: " 
		pprint(cmdLineOpt)

		print "\r\n -************************************- \r\n"

		print "Is mongoDB Ops Manager running? \r\n"
		fetch = "wget -T 1 -O indexes/%s.index.html -S %s:%s" % (addr, addr, web)
		os.system(fetch)
		print "\r\n -************************************- \r\n"

		print "Is mongoDB Web Status page running? \r\n"
		fetch = "wget -T 1 -O indexes/mgmt.%s.index.html -S %s:%s" % (addr, addr, mgmt)
		os.system(fetch)
		print "\r\n -************************************- \r\n"

		listing = db.command('usersInfo')
		print "\nUsers / role:"
		for document in listing['users']:
			pprint(document['user'] +" "+ document['roles'][0]['role'])
		print "\r\n -************************************- \r\n"
		print "\nDatabase: / Collections"
		for dbItem in conn.database_names():
		            db = conn[dbItem]
		            print dbItem + ":"
		            print "\n".join(db.collection_names())
		            print "\n"
		            users = list(db.system.users.find())
		            pprint(users)
		            print "\r\n"

	
		conn.close()

	except Exception, e:
                if str(e).find('need to login') != -1:
                	print "Need to login."
