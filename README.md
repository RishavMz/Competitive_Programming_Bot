# Competitive_Programming_Bot

A discord bot to get information about upcoming contests and view rating changes along with custom ranklists in competitive programming websites(codeforces and codechef only as of now)
#
# 
Test the bot here:

https://discord.gg/K7Tz6QYgkH

###

How this bot is made:

Codeforces data : Codeforces API
Codeforces data : Web scrapping using beautifulsoup
Discord         : Discord.py module
Database        : sqlite3

###
    COMMAND LIST:
    
    $ccdbusers 
    Displays a ranklist from users whose handles are stored in database(for codechef)
    
    $ccdbadd [userhandle]  
    Adds the user with given handle(username) to the database(for codechef)
    
    $cfdbusers 
    Displays a ranklist from users whose handles are stored in database(for codeforces)
    
    $cfdbadd [userhandle]  
    Adds the user with given handle(username) to the database (for codeforces)      
    
    $cfcontests             
    Displays a list of upcoming contests on codeforces
    
    $cfrating [userhandle]  
    Displays rating change for the last round of the given user on codeforces
    
    $cfuser [userhandle1] [userhandle2] [userhandle3]......
    Displays user details(rank , rating , maxrating etc of the given users) on codeforces
    
    $cfranklist [contestid] [userhandle1] [userhandle2] [userhandle3].....
    Displays a custom ranklist using the given users on codeforces
    
    $cccontests             
    Displays a list of upcoming rated contests on codechef
    
    $ccuser [userhandle] 
    Displays user details(star , rating , maxrating etc of the given user) on codechef
    
    $startbotnotifier
    The bot would check for present and upcoming contests (in both codeforces and codechef) every 24 hours and notify the server membe  (starting from the moment this command is given)
    
    $stopbotnotifier
    Turn off the timed message feature which repeats every 24 hours.
    
    $help
    Get command list
    
