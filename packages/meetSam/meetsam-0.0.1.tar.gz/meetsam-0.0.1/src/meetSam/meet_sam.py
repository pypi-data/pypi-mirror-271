#!/usr/bin/env python3

def name():
    """
    Provides my full name.
    
    :return: My full name 
    :rtype: str
    """
    return("Samuel Mehalko")

def title():
    """
    Provides my title at the company that I am employeed.
    
    :return: My title
    :rtype: str
    """
    return("Principle Embedded Software Engineer")

def company():
    """
    Provides the name of the company that I am employeed.
    
    :return: My company
    :rtype: str
    """
    return("Northrop Grumman Corporation")

def email():
    """
    Provides my office email address.
    
    :return: My email address 
    :rtype: str
    """
    return("samuel.mehalko@ngc.com")

def site():
    """
    Provides the url of readthedocs website for this repo.
    
    :return: The readthedocs url
    :rtype: str
    """
    return("https://meetsam.readthedocs.io/en/latest/")

def source():
    """
    Provides the url of the this package's source github url.
    
    :return: This source code's github url.
    :rtype: str
    """
    return("https://github.com/SamuelDonovan/meetSam")

def main():
    """
    Provides a short blurb of of my contact information as well as some fun links.
    
    :return: My contact information as well as some fun links.
    :rtype: str
    """
    print(f"""
    Hi, my name is {name()}!
    I am an {title()}
    working for {company()}.
    I can be reached via email (preferred) at {email()}

    The python package used to generate this text can be found at {site()}
    and the source can be found at {source()}
    """)

if __name__ == "__main__":
    main()
