import urllib2
import urllib
import re

def URLRequest(url, params, method="GET"):
    if method == "POST":
        return urllib2.Request(url, data=urllib.urlencode(params))
    else:
        return urllib2.Request(url + "?" + urllib.urlencode(params))

images = { 
   "10Guy" : [ "http://memegenerator.net/Really-Stoned-Guy", "4168627"],
   "YUNo" : [ "http://memegenerator.net/Y-U-No", "166088"],
   "FirstWorld" : [ "http://memegenerator.net/First-World-Problems-Ii", "2055789"],
   "OAG" : [ "http://memegenerator.net/Overly-Obsessed-Girlfriend", "5052922"],
}


def makeMeme( imageid, text1, text2 ):
    print "Making request..."

    if not imageid in images:
        return "Id not found!"
    
    request = urllib2.Request( images[ imageid ][0] )
    request.add_header( 'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22')

    for i in range(3):
        try:
            sock = urllib2.urlopen( request )
            break
        except:
            print "1 Fail " + str( i )
            if i == 2:
                return "Request error."
            continue
        
    
        

    content = sock.read()

    genID = re.findall( r'id="generatorID".+?value="(\d+)"', content )

    params = { "generatorID":str(genID[0]), "imageID":images[ imageid ][1], "text0":text1, "text1":text2, "languageCode":"en" } 

    request = URLRequest( "http://memegenerator.net/create/instance", params, "POST" )
    request.add_header( 'User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.22 (KHTML, like Gecko) Chrome/25.0.1364.172 Safari/537.22')
    request.add_header( 'Content-Type', 'application/x-www-form-urlencoded' )
    request.add_header( 'Referer', images[ imageid ][0] )

    for i in range(3):
        try:
            sock = urllib2.urlopen( request )
            break
        except:
            print "2 Fail " + str( i )
            if i == 2:
                return "Request error."
            continue
        

    content = sock.read()

    id = re.findall ( r'name="instanceID".+?value="(\d+)"', content )

    memeurl = r'http://cdn.memegenerator.net/instances/400x/' + id[0] + ".jpg"
    print "Done...!"
    print memeurl
    return memeurl

if __name__=="__main__":
    makeMeme( "FirstWorld", "prueba1", "prueba2" )
