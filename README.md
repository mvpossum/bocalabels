# Boca Labels

This small script generates usernames and password for the Boca system ( https://github.com/cassiopc/boca ).
Also it can generate a pdf, containing the credentials of the teams.
It is useful when holding competition with this system.
You can see an example of the output in example.pdf.

## Generating credentials
1. First, log in to icpc.baylor.edu using the organizer account of the contest.
2. In the Dashboard, select the desired contest. 
3. Click on the Export button, choose PC^2 format.
4. Extract the file PC2_Team.tab
5. This file contains the teams from all sites. If you want the team from all the sites go to step 7. Otherwise open PC2_Team.tab, look for a team registered in your site and copy the number in the second column. This is the site number.
6. Assuming the site number is 12345, run the following command:
    > SITE=12345; sed -i -n '/^[[:digit:]]*\t'$SITE'/p' PC2_Team.tab
   
   Now PC2_Team.tab contains only the teams from the site.
7. Generate the file users.txt with the usernames and passwords running:
    > python2 generate_users.py PC2_Team.tab users.txt
    
    Note that this will by default set all site numbers to 1.
    You can change this by passing --keep-site.
    
## Loading the credential into Boca
1. Log in as admin to the Boca system ( http://localhost/boca )
2. Go to tab Users, section Import and select the users.txt file generated previously. The users should be loaded.

## Generating pdf with labels
1. Run the script to make the labels:
    > python2 make_labels.py contest_name users.txt labels
    
    It will try to compile it into a pdf.
