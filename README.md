# Boca Labels

This small script generates a pdf ready to print, containing the 
credentials of the teams to log in to the Boca system ( https://github.com/cassiopc/boca ).
It is useful when holding competition with this system.

# Usage
1. First, log in to icpc.baylor.edu using the organizer account of the contest.
2. In the Dashboard, select the desired contest. 
3. Click on the Export button, choose PC^2 format.
4. Extract the file PC2_Team.tab
5. This file contains the teams from all sites. If you want the team from all the sites go to step 8. Otherwise open PC2_Team.tab, look for a team registered in your site and copy the number in the second column. This is the site number.
6. Assuming the site number is 12345, run the following command:
    > grep 12345 PC2_Team.tab > site.tab
   
   Now site.tab contains the desired teams.
7. You probably want to set the site number to 1:
    > set -i -e 's^\([0123456789]*\)\t[0123456789]*/\1\t1/g' site.tab
8. Log in as admin to the Boca system (localhost/boca)
9. Go to Users, Import and select the .tab file.
10. If the import is successful it will list the generated users and password. Copy and paste this table into a new file (password.tab).
11. Finally, run this generator to make the labels, using the following format:
    > python2 makelabels.py contest_name users.tab passwords.tab output[.tex]
    
    It will try to compile it into a pdf.
