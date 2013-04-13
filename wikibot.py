import urllib
import sys
import re

class myOpener( urllib.FancyURLopener ):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def getURLContent( url ):
    opener = myOpener()
    reader = opener.open( url )
    content = reader.read()
    return content.decode( 'utf-8', 'replace' )

def stripTags( raw_data ):
    result = ""
    ignore = False
    
    for i in raw_data:
        if i == '<':
            ignore = True
        elif i == '>':
            ignore = False
            continue

        if not ignore:
            result += i

    return result

def wikiSearch( query ):

    query = urllib.quote( query )
    wikiprefix = "http://en.wikipedia.org/w/index.php?search="
    fullurl = wikiprefix + query

    content = getURLContent( fullurl )

    title = re.findall( r'<title>(.+?) - Wiki.+?</title>', content )[0]

    mayReferToIndex = content.find("<b>" + title + "</b> may refer to:")

    if mayReferToIndex > -1:
        found = re.findall( r'href="(.*?)"', content[mayReferToIndex:] )
        content = getURLContent( "http://en.wikipedia.org" + found[1] )

    title = re.findall( r'<title>(.+?) - Wiki.+?</title>', content )[0]
    paragraphs = re.findall( r'<p>(.+?)</p>', content )
    
    result = "Not found!"

    for p in paragraphs:
        if p.find( title ) > -1:
            result = p
            break

    result = stripTags( result )
    
    if isinstance( result, str ):
        result = result.decode( 'UTF-8','replace' )
        result = result.encode()

    return result

    


if __name__=="__main__":
    while 1:
        print "Enter your search: "
        searchquery = raw_input()
        print wikiSearch( searchquery )
   
    
    
            
            

        
    
    
