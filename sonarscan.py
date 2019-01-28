# coding: utf-8
import urllib2
from bs4 import BeautifulSoup
import requests
import gzip
from hurry.filesize import size
import os
import json
import io

#################################### TEST Data
test = "2018-12-29-1546111673-fdns_cname.json.gz"
url1 = "https://opendata.rapid7.com/sonar.fdns_v2/2018-12-29-1546111673-fdns_cname.json.gz"
query = "tesla.com"
##############################################

#Global Realtime data source URL
url = 'https://opendata.rapid7.com/sonar.fdns_v2'
host_url = 'https://opendata.rapid7.com'
param = 'cname'
hlist = ['']

def get_data(url,param):                    #Finds the URL to required fdns file
    page_data = urllib2.urlopen(url)
    soup = BeautifulSoup(page_data,"html.parser")
    databuf = soup.find('div',attrs={"class":"table-scroll"})
    databuf = databuf.findAll('td')
    for i in databuf:
        link = i.findAll('a')
        for x in link:
            x = x.get('href')
            if "cname" in str(x):
                u = x;
    return(host_url + u)

def downloader(url):

    file_name = url.split('/')[-1]
    if not os.path.isfile('./' + file_name):
        if 'y' == raw_input("\nDatabase needs to be downloaded from Project Sonar URL, type 'y' to proceed! "):
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, size(file_size))

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

            f.close()
            return(file_name)
        else: exit("\nExiting, Thank you")
    print "\nDatabase already found... %s" % (file_name)


def open_file(filename,query):
    with gzip.open(filename, 'r') as f:
        g = io.BufferedReader(f)
        hlist.insert(1,query)                       # Initiaing List
        print "\nSearching %s records, Please wait ..." % (param)
        print "\n\n####################################### Results ############################################"
        print "------ URL ------------------------------------------------- Record Address ----------------"
        print "####################################### ####### ############################################ \n\n "
        for line in g:
            if query in line:
                data = json.loads(line)
                hlist.append(str(data['name']))     # Adding http to all hosts and send to list
#                print "%s \t %s" %  (data['name'],data['value'])
                print '{:<60}{:<40}'.format(' '.join(data['name'].split()[-1:]), ' '.join(data['value'].split()[-1:]))
    g.close()
    print "\n\nSearch complete..."

def ping(list):
    for item in list:
        try:
            r = requests.get("http://" + item, timeout=3)
            print '{:<60}{:<10}'.format(' '.join(item.split()[-1:]), ' '.join(str(r.status_code).split()[-1:]))
        except requests.exceptions.RequestException as e:
            if e:
                print '{:<60}{:<20}'.format(' '.join(item.split()[-1:]), ' '.join('Timeout'.split()[-1:]))
    print "\n\n\n\t\t\tExiting..."
    exit()

def pingy(h):  #Testfunction
    try:
        r = requests.get("http://" + h, timeout=3)
        stat = r.status_code
    except requests.exceptions.RequestException as e:
        if e:
            stat = 'No Response'
    return(stat)


print "\n##################################### SONARSCAN v1.0 ###################################"
print "################################## post2steve@live.in ##################################"
print "\nReading Settings..."
url1 = get_data(url,param);
print "\nSource URL -> %s" % (url1)
local_filename = downloader(url1);
query = raw_input("\nPlease enter hostname to search -> ")
open_file(test,query);
print "\n Sending GET requests all the URLs "
print "\n##################################### Status codes #####################################"
ping(hlist);
