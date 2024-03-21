1. To use the client you have the following command options:
        (login, logout, post, delete <key>, news, list)
    
    login - Asks for a url host to connect to and username/password.
            The url host can be without https://
    logout - Lets you logout
    post - Asks for:
                A story headline
                A category (art, tech, pol, trivia)
                A region (uk, eu, w)
                Details to describe the story
    delete <key> - Lets an authorised used to delete their own news story of X key
    news - Lets you view 20 random news agencies and all stories that match flags:
                Flags include: -id, -cat, -reg, -date
                e.g. -id=RRB03
    list - Lists 20 random active news agencies

2. https://ed20rb5.pythonanywhere.com/

3.  Ammar's secure account details are:
    Username = ammar
    Password = securepassword123

    This can be used to log into the service and act as an author.

4.  Your machine must have these python libraries: requests, getpass, random.
    No other special information regarding client, you can call a hidden 'register' command, but this will do nothing without manual configuration.
