#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
import sys, feedparser, math, re, MySQLdb, types, urllib, urllib2, datetime, random, time, unicodedata, base64, socket
from BeautifulSoup import BeautifulSoup, SoupStrainer, Comment
from urlparse import urljoin
from urllib2 import URLError
# database parameters

hostname = "mysql.abacadaba.com"
username = "abacadaba_sys"
urlsTable = 'young_frankenstein_monster_urls'
urlAuthTable = 'young_frankenstein_monster_urls_auth'
urlsMetaTable = 'young_frankenstein_monster_urls_meta'
urlsSourceTable = 'young_frankenstein_monster_urls_source'
optionsTable = 'young_frankenstein_monster_options'
err=0

# options 
rowLimit=100000 # row_limit
urlExpirationDays=7 # url_expiration_days
timeout=9 # timeout_seconds
scoreThreshold=0.0 # score_threshold
urlExpirationDate=datetime.datetime.now()


# Create a connection object, then use it to create a cursor
con = MySQLdb.connect(host=hostname, port=3306, 
    user=username, passwd=password, db=dbname)
cursor = con.cursor()

# mime types

mime={'rgb':1,'pbm': 1,'ppm': 1,'rast': 1,'xbm': 1,'bmp': 1,'jpg':1,'gif': 1,'png': 1,'swf': 1,'mp3': 1,'zip': 1,'gz': 1,'tar': 1,'pdf': 1,'doc': 1,'jpeg': 1,'tif': 1,'tiff': 1}
  

  
def fetchHTML(url):
  urls = []
  words = ''
  title = ''
  desc = ''
  keywords = ''
  body = ''
  error_code = ''
  error_reason = ''
  content_type = ''
  last_modified = ''
  err=0
  url=re.compile(r"/$").sub('',url)
  url=re.compile(r"^http://").sub('',url)
  url = "http://" + url
  req = urllib2.Request(url)
  try:
    res = urllib2.urlopen(req)
    info = res.info()
    data = res.read()
  except IOError, e:
    if hasattr(e, 'reason'):
      if e.reason[1]:
        error_reason = str(e.reason[1])
      elif e.reason[0]:
        error_reason = str(e.reason[0])
      err=1
      error_code = 2
      return (urls,body,title,desc,keywords,error_code,error_reason,content_type,last_modified,err)
    elif hasattr(e, 'code'):
      if e.code != 401:
        error_code = int(e.code)
        err=1
        return (urls,body,title,desc,keywords,error_code,error_reason,content_type,last_modified,err)
      elif e.code == 401:
      #401 = auth required error
        domain=getDomain(url)
        sql = "SELECT auth_role, auth_user, auth_passwd FROM " + urlAuthTable + " WHERE url_domain = \'" + str(domain) + "\'"
        cursor.execute(sql)
        res = cursor.fetchone()
        if res:
          role = res[0]
          username = res[1]
          password = res[2]
          base64string = base64.encodestring('%s:%s' % (username, password))
          authheader =  "Basic %s" % base64string
          req.add_header("Authorization", authheader)
          try:
            res = urllib2.urlopen(req)
            info = res.info()
            data=res.read()
          except IOError, e:
            error_code = int(e.code)
            err=1
            return (urls,body,title,desc,keywords,error_code,error_reason,content_type,last_modified,err)
  err=0
  if output > 0:
    print info
  if info.has_key("content-type"):
    content_type = str(info["content-type"])
  if info.has_key("last-modified"):
    last_modified = str(info["last-modified"])
  soup=BeautifulSoup(data)
  try:
    title=cleanHTML(soup.html.head.title.string)
    title=convertAccents(title)
  except:
    title = ''
  try:
    for meta in soup.head('meta'):
      ctxt = str(meta)
      pat = re.compile(r"meta[ ]*name[ ]*=[ ]*[\"]*key").findall(ctxt.lower())
      if pat:
        temp=re.compile(r"ontent[ ]*=[ ]*[\"]*").split(ctxt)
        if len(temp) > 1:
          keywords=temp[1]
          keywords=re.compile(r"[ ]*[\"]*[ ]*[/]*[>]").sub(' ',keywords)
          keywords=cleanHTML(keywords)
          keywords=convertAccents(keywords)
          keywords=keywords.strip()
      pat = re.compile(r"meta[ ]*name[ ]*=[ ]*[\"]*descrip").findall(ctxt.lower())
      if pat:
        temp=re.compile(r"ontent[ ]*=[ ]*[\"]*").split(ctxt)
        if len(temp) > 1:
          desc=temp[1]
          desc=re.compile(r"[ ]*[\"]*[ ]*[/]*[>]").sub(' ',desc)
          desc=convertAccents(desc)
          desc=desc.strip()
  except:
    err=1
  for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
    comment.extract()
  for script in soup.findAll('script'):
    script.extract()
  for link in soup.findAll('a', href=True):
    if len(link['href']) > 9:
      pat = re.compile(r'^http').findall(link['href'])
      if pat:
        href=re.compile(r"/$").sub('',link['href'])
        temp=re.compile(r"\.").split( href.lower())
        size = len(temp)
        size = size -1
        ext=temp[size]
        if mime.has_key(ext):
          err=1
        else:
          urls.append(href)
  body = soup.body(text=True)
  body = ' '.join(body)
  body=convertAccents(body)
  body=cleanHTML(body)
  title=convertAccents(title)
  title=cleanHTML(title)
  try:
    body=unicodedata.normalize('NFKD',body).encode('ascii', 'ignore')
  except:
    err=1
  try:
    title=unicodedata.normalize('NFKD',title).encode('ascii', 'ignore')
  except:
    err=1
  body=re.compile(r'\n').sub(' ',body)
  body=re.compile(r'[ ]+').sub(' ',body)
  title=re.compile(r'\n').sub(' ',title)
  title=re.compile(r'[ ]+').sub(' ',title)
  return (urls,body,title,desc,keywords,error_code,error_reason,content_type,last_modified,err)
  

def crawlUrls(numbots):
  cnt=0
  if numbots == 0:
    sql = "SELECT count(id) FROM " + urlsTable + " WHERE (url_visits = 0) AND (url_content_type = 'text/html') AND (url_error_code = 0) ORDER BY url_priority DESC LIMIT " + str(rowLimit)
  else:
    sql = "SELECT count(id) FROM " + urlsTable + " WHERE (url_visits = 0) AND (url_content_type = 'text/html') AND (url_error_code = 0)  AND (numbot = " + str(numbots) + ") ORDER BY url_priority DESC LIMIT " + str(rowLimit)
  cursor.execute(sql)
  row=cursor.fetchone()
  if row:
    cnt=row[0]
  if cnt==0:
    return cnt
  id = ''
  domain = ''
  url = ''
  name = ''
  title = ''
  url_content_type = ''
  url_visits = 0
  score=0
  if numbots == 0:
    sql = "SELECT id, url_domain, url, url_title, url_visits, url_content_type FROM " + urlsTable + " WHERE (url_visits = 0) AND (url_content_type = 'text/html') AND (url_error_code = 0) ORDER BY url_priority DESC LIMIT " + str(rowLimit)
  else:
    sql = "SELECT id, url_domain, url, url_title, url_visits, url_content_type FROM " + urlsTable + " WHERE (url_visits = 0) AND (url_content_type = 'text/html') AND (url_error_code = 0)  AND (numbot = " + str(numbots) + ") ORDER BY url_priority DESC LIMIT " + str(rowLimit)
  cursor.execute(sql)
  if output > 0:
    print sql
  result = cursor.fetchall()
  for row in result:
    id = row[0]
    domain = row[1]
    url = row[2]
    title = row[3]
    url_visits = row[4]
    url_visits = url_visits + 1
    url_content_type = row[5]
    url= re.sub(r"\/$", "", url)
    domain= re.sub(r"\/$", "", domain)
    sql = "UPDATE " + urlsTable + " SET url_checked = 1, url_visits = " + str(url_visits) + ", url=\'" + str(url) + "\', url_domain=\'" + str(domain) +  "\', last_update = NOW() WHERE id = " + str(id)
    score=0
    if output > 0:
      print "processing %s" % url
    try:
      cursor.execute(sql)
    except:
      continue
    pat = re.compile(r"html").findall(url_content_type)
    if pat:
      try:
        (urls,body,title,desc,keywords,error_code,error_reason,content_type,last_modified,err) = fetchHTML(url)
      except:
        err=2
      if err ==2:
        err=2
      elif err ==1:
        addUrlError(url,error_code,error_reason)
      else:
        if content_type:
          pat = re.compile(r"html").findall(content_type.lower())
          if not pat:
            try:
              addContentType(url,content_type)
            except:
              err=1
        if (len(last_modified) > 4):
          try:
            addUrlTime(url,last_modified)
          except:
            err=1
        if len(title) > 2:
          updateUrlInfo(url,title,body,desc,keywords)
          try:
            updateUrlInfo(url,title,body,desc,keywords)
          except:
            erro=1
        if len(urls) > 0:
          for link in urls:
            try:
              addUrl(link,id)
            except:
              erro=1
        if len(body) > 9:
          turls = extractTextUrls(body)
          if len(turls) > 0:
            for link in turls:
              try:
                addUrl(link,id)
              except:
                erro=1 
  return cnt
  
def getDomain(url):
  domain = url
  pat = re.compile(r'^https://').findall(domain.lower())
  if pat:
    domain = re.sub(r'^https://', '', domain.lower())
    temp = domain.split('/')
    if len(temp[0]) < 6:
      domain = url
    else:
      domain = 'https://' + temp[0]
  else:
    patt = re.compile(r'^http://').findall(domain.lower())
    if patt:
      domain = re.sub(r'^http://', '', domain.lower())
      temp = domain.split('/')
      if len(temp[0]) < 6:
        domain = url
      else:
        domain = 'http://' + temp[0]
    else:
      domain = url
  return domain
  
def getSlug(url):
  slug=url.lower()
  slug=re.sub(r'^http://', '', slug)
  slug=re.sub(r'^www.', '', slug)
  slug=re.sub(r"\'", "\\\'", slug)  
  return slug
  
def getOptions():
# get options from database
  cnt=0
  sql = "SELECT id, row_limit, url_expiration_days, timeout_seconds, score_threshold FROM " + optionsTable + " WHERE 1 ORDER BY last_modified DESC"
  cursor.execute(sql)
  row=cursor.fetchone()
  if row:
    id=row[0]
    row_limit=row[1]
    url_expiration_days=row[2]
    timeout_seconds=row[3]
    score_threshold=row[4]
  return (row_limit, url_expiration_days, timeout_seconds, score_threshold)
  
  
def addContentType(url,content_type):
  ctype=re.sub(r'^[ ]+', '', content_type.lower())
  temp=ctype.split(' ')
  if len(temp) > 0:
    ctype=temp[0]
  ctype=re.sub(r';', '', ctype)
  url=re.compile(r"/$").sub('',url)
  url=re.compile(r"^http://").sub('',url)
  url = "http://" + url
  urlslug=getSlug(url)
  sql = "SELECT ID FROM " + urlsTable + " WHERE url_slug = \'" + urlslug + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  if result:
    id = result[0]
    sql = "UPDATE " + urlsTable + " SET url_content_type = \'" + str(ctype) + "\', last_update = NOW() WHERE id = " + str(id)
    try:
      cursor.execute(sql)
    except:
      erro=1
  return
  
def addUrlError(url,error_code,error_reason):
  id = ''
  url=re.compile(r"/$").sub('',url)
  url=re.compile(r"^http://").sub('',url)
  url = "http://" + url
  urlslug=getSlug(url)
  sql = "SELECT ID FROM " + urlsTable + " WHERE url_slug = \'" + urlslug + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  if result:
    id = result[0]
    sql = "UPDATE " + urlsTable + " SET url_checked = 1, url_error_code = " + str(error_code) + ", url_error_reason=\'" + str(error_reason) + "\', last_update = NOW() WHERE id = " + str(id)
    try:
      cursor.execute(sql)
    except:
      sql = "UPDATE " + urlsTable + " SET url_checked = 1, url_error_code = 1, last_update = NOW() WHERE id = " + str(id)
      cursor.execute(sql)
  return
  
def addUrlTime(url,last_modified):
  id = ''
  url=re.compile(r"/$").sub('',url)
  url=re.compile(r"^http://").sub('',url)
  urlslug=getSlug(url)
  sql = "SELECT ID FROM " + urlsTable + " WHERE url_slug = \'" + urlslug + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  if result:
    id = result[0]
    if (len(last_modified) > 4):
      c = time.strptime(last_modified,"%a, %d %b %Y %H:%M:%S %Z")
      stamp = time.strftime("%Y-%m-%d %I:%M:%S",c)
      sql = "UPDATE " + urlsTable + " SET last_modified = \'" + str(stamp) +  "\', last_update = NOW() WHERE id = " + str(id)
      try:
        cursor.execute(sql)
      except:
        err=1
  return
 
def convertAccents(yoiuoi):
  yoiuoi= re.sub(r"^[ ]*\"", "",yoiuoi)
  yoiuoi= re.sub(r"\"[ ]*$", "",yoiuoi)
  yoiuoi= re.sub(r"ê", "e",yoiuoi)
  yoiuoi= re.sub(r"ú", "u",yoiuoi)
  yoiuoi= re.sub(r"è", "e",yoiuoi)
  yoiuoi= re.sub(r"È", "E",yoiuoi)
  yoiuoi= re.sub(r"í", "i",yoiuoi)
  yoiuoi= re.sub(r"Á", "A",yoiuoi)
  yoiuoi= re.sub(r"Ã", "A",yoiuoi)
  yoiuoi= re.sub(r"é", "e",yoiuoi)
  yoiuoi= re.sub(r"à", "a",yoiuoi)
  yoiuoi= re.sub(r"â", "a",yoiuoi)
  yoiuoi= re.sub(r"ô", "o",yoiuoi)
  yoiuoi= re.sub(r"ç", "c",yoiuoi)
  yoiuoi= re.sub(r"ó", "o",yoiuoi)
  yoiuoi= re.sub(r"Ô", "O",yoiuoi)
  yoiuoi= re.sub(r"ã", "a",yoiuoi)
  yoiuoi= re.sub(r"á", "a",yoiuoi)
  yoiuoi= re.sub(r"õ", "o",yoiuoi)
  yoiuoi= re.sub(r"Ê", "E",yoiuoi)
  yoiuoi= re.sub(r"É", "E",yoiuoi)
  yoiuoi= re.sub(r"&quot;", "",yoiuoi)
  yoiuoi= re.sub(r"[ ]+", " ",yoiuoi)
  return yoiuoi
  
def convertAccentsHTML(yoiuoi):
  yoiuoi= re.sub(r"^[ ]*\"", "",yoiuoi)
  yoiuoi= re.sub(r"\"[ ]*$", "",yoiuoi)
  yoiuoi= re.sub(r"ê", "&ecirc;",yoiuoi)
  yoiuoi= re.sub(r"ú", "&uacute;",yoiuoi)
  yoiuoi= re.sub(r"è", "&egrave;",yoiuoi)
  yoiuoi= re.sub(r"È", "&Egrave;",yoiuoi)
  yoiuoi= re.sub(r"í", "&iacute;",yoiuoi)
  yoiuoi= re.sub(r"Á", "&Aacute;",yoiuoi)
  yoiuoi= re.sub(r"é", "&eacute;",yoiuoi)
  yoiuoi= re.sub(r"à", "&agrave;",yoiuoi)
  yoiuoi= re.sub(r"â", "&acirc;",yoiuoi)
  yoiuoi= re.sub(r"ô", "&ocirc;",yoiuoi)
  yoiuoi= re.sub(r"ç", "&ccedil;",yoiuoi)
  yoiuoi= re.sub(r"ó", "&oacute;",yoiuoi)
  yoiuoi= re.sub(r"Ô", "&Ocirc;",yoiuoi)
  yoiuoi= re.sub(r"ã", "&atilde;",yoiuoi)
  yoiuoi= re.sub(r"á", "&aacute;",yoiuoi)
  yoiuoi= re.sub(r"õ", "&otilde;",yoiuoi)
  yoiuoi= re.sub(r"Ê", "&Ecirc;",yoiuoi)
  yoiuoi= re.sub(r"É", "&Eacute;",yoiuoi)
  yoiuoi= re.sub(r"&quot;", "",yoiuoi)
  yoiuoi= re.sub(r"[ ]+", " ",yoiuoi)
  return yoiuoi

def cleanHTML(txt):
  # Remove all the HTML tags
  txt=re.sub(r"\n", ' ', txt)
  txt=re.compile(r'<[^>]+>').sub(' ',txt)
  txt=re.compile(r'&[^>]+;').sub(' ',txt)
  txt=re.compile(r'[ ]+').sub(' ',txt)
  return txt
  

  
def addUrl(url,refid):
  url= re.sub(r"\/$", '', url)
  temp=re.compile(r"\.").split(url.lower())
  size = len(temp)
  size = size -1
  ext=temp[size]
  if mime.has_key(ext):
    erro=1
    return
  urlslug=getSlug(url)
  sql = "SELECT ID FROM " + urlsTable + " WHERE url_slug = \'" + urlslug + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  if result:
    return
  posttime = datetime.datetime.now()
  posttimeStr = posttime.strftime("%Y-%m-%d %I:%M:%S")
  url_content_type = 'text/html'
  domain=getDomain(url)
  url= re.sub(r"\'", "\\\'", url)
  priority=random.random()
  domainslug=getSlug(domain)
  sql = "INSERT INTO " + urlsTable + " (url_domain, url, url_content_type, url_verified, url_visits, url_created, last_update, url_slug, url_domain_slug, url_priority) VALUES (\'" + domain + "\', \'" + url + "\', \'" + url_content_type + "\', 0 , 0 ,\'" + posttimeStr + "\', \'" + posttimeStr + "\', \'"  + urlslug + "\', \'" +  domainslug +  "\', " +  str(priority) + ")"
  try:
    cursor.execute(sql)
  except:
    return
  sql = "SELECT ID FROM " + urlsTable + " WHERE url_slug = \'" + urlslug + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  if result:
    id=result[0]
    sql = "SELECT ID FROM " + urlsSourceTable + " WHERE (url_source_id= " + str(refid) + ") AND (url_link_id = " + str(id) + ")"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
      pas=1
    else:
      sql = "INSERT INTO " + urlsSourceTable + " ( url_source_id, url_link_id, last_update) VALUES ( " + str(refid) + ", " + str(id) + ", NOW())"
      try:
        cursor.execute(sql)
      except:
        erro=1
  return
  
def updateUrlInfo(url,title,body,desc,keywords):
  url= re.sub(r"\/$", '', url)
  temp=re.compile(r"\.").split(url.lower())
  size = len(temp)
  size = size -1
  ext=temp[size]
  if mime.has_key(ext):
    return
  urlslug=getSlug(url)
  sql = "SELECT ID FROM " + urlsTable + " WHERE url_slug = \'" + urlslug + "\'"
  cursor.execute(sql)
  result = cursor.fetchone()
  if not result:
    return
  if result:
    id = result[0]  
    posttime = datetime.datetime.now()
    posttimeStr = posttime.strftime("%Y-%m-%d %I:%M:%S")
    url_content_type = 'html'
    domain=getDomain(url)
    title = re.sub(r"\'", '', title)
    title=title[0:250]
    body = re.sub(r"\'", '', body)
    desc = re.sub(r"\'", '', desc)
    keywords = re.sub(r"\'", '', keywords)
    if len(title) > 9:
      sql = "UPDATE " + urlsTable + " SET url_title=\'" + str(title) + "\', last_update = NOW() WHERE id = " + str(id)
      try:
        cursor.execute(sql)
      except:
        erro=1
    if len(body) > 9:
      sql = "SELECT id FROM " + urlsMetaTable + " WHERE (meta_key = \'body\') AND url_id = " + str(id)
      cursor.execute(sql)
      res = cursor.fetchone()
      if res:
        meta_id=res[0]
        sql = "UPDATE " + urlsMetaTable + " SET last_update = NOW(), meta_value = \'" + str(body) + "\' WHERE id = " + str(meta_id)
      else:
        sql = "INSERT INTO " + urlsMetaTable + " (url_id, meta_key, last_update, meta_value) VALUES (" + str(id) + ", \'body\', NOW(), \'" + str(body) + "\')"
      try:
        cursor.execute(sql)
      except:
        erro=1
    if len(keywords) > 9:
      sql = "SELECT id FROM " + urlsMetaTable + " WHERE (meta_key = \'keywords\') AND url_id = " + str(id)
      cursor.execute(sql)
      res = cursor.fetchone()
      if res:
        meta_id=res[0]
        sql = "UPDATE " + urlsMetaTable + " SET last_update = NOW(), meta_value = \'" + str(keywords) + "\' WHERE id = " + str(meta_id)
      else:
        sql = "INSERT INTO " + urlsMetaTable + " (url_id, meta_key, last_update, meta_value) VALUES (" + str(id) + ", \'keywords\', NOW(), \'" + str(keywords) + "\')"
      try:
        cursor.execute(sql)
      except:
        erro=1
    if len(desc) > 9:
      sql = "SELECT id FROM " + urlsMetaTable + " WHERE (meta_key = \'desc\') AND url_id = " + str(id)
      cursor.execute(sql)
      res = cursor.fetchone()
      if res:
        meta_id=res[0]
        sql = "UPDATE " + urlsMetaTable + " SET last_update = NOW(), meta_value = \'" + str(desc) + "\' WHERE id = " + str(meta_id)
      else:
        sql = "INSERT INTO " + urlsMetaTable + " (url_id, meta_key, last_update, meta_value) VALUES (" + str(id) + ", \'desc\', NOW(), \'" + str(desc) + "\')"
      try:
        cursor.execute(sql)
      except:
        erro=1
  return
  
def extractTextUrls(txt):
  turls = []
  txt=re.compile(r'[;=!$%^&*\(\)\{\}\[\]\"\',\>\<]').sub(' ',txt.lower())
  words=re.compile(r'[ ]+').split(txt)
  for word in words:
    pat = re.compile(r'^http').findall(word.lower())
    if pat:
      turls.append(word.lower())
  return (turls)
  

numbots=0
try:
    numbots=sys.argv[1]
except:
    numbots=0 

output=0
try:
    output=sys.argv[2]
except:
    output=0 

(rowLimit, urlExpirationDays, timeout, scoreThreshold)=getOptions()
 # timeout in seconds
socket.setdefaulttimeout(timeout)
cntr=1
while cntr > 0:
  cntr=crawlUrls(numbots)

con.close()



