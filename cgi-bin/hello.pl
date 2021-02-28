#!/usr/bin/perl -w
     # Tell perl to send a html header.
     # So your browser gets the output
     # rather then <stdout>(command line
     # on the server.)
print "Content-type: text/html\n\n";
     # print your basic html tags.
     # and the content of them.
print "<html><head><title>Hello World!! </title><link rel='stylesheet' href='/public/css/bootstrap_v3.3.7.min.css'></head>\n";
print "<body><h1>Hello world this is a perl file</h1></body></html>\n";
