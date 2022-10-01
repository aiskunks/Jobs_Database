#!/usr/bin/env python
 # -*- coding: iso-8859-1 -*-
import sys, feedparser, math, re, MySQLdb, types, urllib2, datetime, random, time, unicodedata

# database parameters
hostname = 'localhost'
username = 'nbrown'
dbname = 'discrim_terms'
password = 'Temp12345'
urlsTable = 'pmt_urls'
urlDomainsTable = 'pmt_domains'


# Create a connection object, then use it to create a cursor
con = MySQLdb.connect(host=hostname, port=3306, 
    user=username, passwd=password, db=dbname)
cursor = con.cursor()

def getAvgScores(url_domain_slug):
  score=0
  score_num=0
  sql = "SELECT id, url_score FROM " + urlsTable + " WHERE (url_domain_slug = \'" + url_domain_slug + "\') AND (url_error_code = 0) AND (url_score > 0)"
  cursor.execute(sql)
  result = cursor.fetchall()
  for row in result:
    id=row[0]
    url_score=row[1]
    if output > 0:
      print url_score
    score_num=score_num+1
    score=score+url_score
  if score_num > 0:
    score=(score/score_num)
  return score

def updateScores():
  sql = "SELECT id, url_domain_slug FROM " + urlDomainsTable + " WHERE 1"
  cursor.execute(sql)
  result = cursor.fetchall()
  for row in result:
    id = row[0]
    url_domain_slug = row[1]
    score=getAvgScores(url_domain_slug)
    if output > 0:
      print "%s score %s" % (url_domain_slug,str(score))
    sql = "UPDATE " + urlDomainsTable + " SET domain_empirical_score = " + str(score) + " WHERE id = " + str(id)
    cursor.execute(sql)
  return 
  



output=0
try:
  output=sys.argv[1]
except:
  output=0 


updateScores()

con.close()






