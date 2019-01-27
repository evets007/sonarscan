# coding: utf-8
import urllib2
from bs4 import BeautifulSoup
import requests
import gzip
from hurry.filesize import size
import os
import json

#################################### TEST Data
test = "2018-12-29-1546111673-fdns_cname.json.gz"
url1 = "https://opendata.rapid7.com/sonar.fdns_v2/2018-12-29-1546111673-fdns_cname.json.gz"
query = "tesla.com"
##############################################

#Realtime data source URL
url = 'https://opendata.rapid7.com/sonar.fdns_v2'
host_url = 'https://opendata.rapid7.com'
param = 'cname'
#Finds the URL to required fdns file
def get_data(url,param):
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
        else: exit("Exiting, Thank you")
    print "Database already found... %s" % (file_name)


def open_file(filename,query):
    with gzip.open(filename, 'r') as g:
        print "Searching %s records, Please wait ..." % (param)
        print "Hostname ------------------------------------ Address "
        for line in g:
            if query in line:
                data = json.loads(line)
                print "%s \t %s" %  (data['name'],data['value'])
    g.close()
    print "Search complete"

def stream_gzip_decompress(stream):
    dec = zlib.decompressobj(zlib.MAX_WBITS | 16 )  # offset 32 to skip the header
    for chunk in stream:
        rv = dec.decompress(chunk)
        if rv:
            yield rv

print "Reading Settings..."
url1 = get_data(url,param);
print "\nSource URL -> %s" % (url1)
local_filename = downloader(url1);
query = raw_input("Please enter host name to search -> ")
open_file(test,query);
