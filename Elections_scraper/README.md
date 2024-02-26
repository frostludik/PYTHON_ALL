# Elections_scraper.py


This Python program scraps election results from site VOLBY.CZ.

Main url: https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ

- go to main url, choose district and then click on the cross in "vyber PM" field
- now copy the url of current position
- program is supposed to be run from command prompt with 2 arguments
    - 1st - URL , **in double quotes** , otherwise some shell can misinterpret ? and & characters
    - 2nd - output filename, including **.csv**
- csv file will be saved in relative path
- used encoding when writing to csv is UTF-16 in order to get correct Czech characters


$~$

>## Tested on district **"Okres Brno-venkov"**
>- **https://www.volby.cz/pls/ps2017nss/ps31?xjazyk=CZ&xkraj=11&xnumnuts=6203**
>- sample file name: **output.csv**

