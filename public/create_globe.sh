#!/usr/bin/env bash
lat=144.4951;
lon=50.1391;
lat=151.0098;
lon=48.7847;
proj='JG';
gmt pscoast -Rg -$proj$lat/$lon/6i -Bag -Dc -A5000 -Gforestgreen -Sblue3 -P -K > /home/pi/Desktop/globe.ps;
gmt psxy -R -$proj -O -K -W15/15/255/0  <<END >> /home/pi/Desktop/globe.ps
144.4951 50.1391 
-151.0098 48.7847 
END
gmt psimage /home/pi/Desktop/ISSIcon.png -Dg$lat/$lon+w1i -Rg -$proj -O >> /home/pi/Desktop/globe.ps;
gmt psconvert -A+s4c -Tg /home/pi/Desktop/globe.ps;
