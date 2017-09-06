# python-filemon
Filesystem monitor in python

Installation:

* Edit efw.ini with your path to watch and the location you want the temp files and log file saved
* If you don't have ssmtp on your system, change check.sh to use your chosen command line mail client
* Run check.sh to make sure it's working for you
* Add or change a file in your watched path to make sure you get an email alert
* Add check.sh to your crontab on whatever frequency you prefer
