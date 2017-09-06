# python-filemon

Description
-------------------
This is a simple filesystem monitor program that logs all the files in your chosen path along with their last access
times, sizes and permissions. When you next run the program, it will compare the previous state with the current state
and send you an email with any changes.

Installation
-------------------
* Edit efw.ini with your path to watch and the location you want the temp files and log file saved
* If you don't have ssmtp on your system, change check.sh to use your chosen command line mail client
* Run check.sh to make sure it's working for you
* Add or change a file in your watched path to make sure you get an email alert
* Add check.sh to your crontab on whatever frequency you prefer

License
-------------------
This program is open source software licensed under the [MIT license](http://opensource.org/licenses/MIT)
