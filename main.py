from colorama import Fore, Style, init
import requests
from bs4 import BeautifulSoup
import re
import json
import socket
from ipwhois import IPWhois
import instaloader

import pyfiglet
ascii_art = pyfiglet.figlet_format("OSINT TOOL v2.0")

init()

def aboutthetool():
    print(Fore.RED +"|LAST OF FRn13ds TOOLS | RELEASE DATE : 1/25/2025| ")
    print(Fore.GREEN + ascii_art)
    
    
def show_menu():
    """Display the main menu and handle user input."""
    print(Fore.CYAN + """
    =============================
          OSINT Tool Main Menu
    =============================
    """ + Style.RESET_ALL)
    
    menu_options = [
        "Perform Google Search",
        "Analyze IP Address",
        "Resolve Domain to IP",
        "Social Media Profile Lookup",
        "Instagram Profile Detailed Info",
        "About",
        "Exit"
    ]
    
    for i, option in enumerate(menu_options, start=1):
        print(Fore.YELLOW + f"  [{i}]" + Style.RESET_ALL + f" {option}")

    choice = input(Fore.CYAN + "\n  ➤ Select an option [1-7]: " + Style.RESET_ALL)
    return choice

def google_search(query, num_results=10):
    """Perform a Google search and return results."""
    headers = {"User-Agent": "Mozilla/5.0"}
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [re.search(r'url\?q=(.*?)&', link['href']).group(1)
                 for link in soup.find_all('a', href=True) if 'url?q=' in link['href']]
        return links
    else:
        print(Fore.RED + "Failed to fetch Google search results." + Style.RESET_ALL)
        return []

def ip_analysis(ip_address):
    """Analyze an IP address using ipwhois."""
    try:
        obj = IPWhois(ip_address)
        result = obj.lookup_whois()
        return result
    except Exception as e:
        print(Fore.RED + f"Failed to analyze IP {ip_address}: {e}" + Style.RESET_ALL)
        return {}

def domain_to_ip(domain):
    """Resolve a domain name to an IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print(Fore.RED + f"Failed to resolve domain {domain}" + Style.RESET_ALL)
        return None

def instagram_profile_info(username):
    """Fetch detailed Instagram profile info using Instaloader."""
    loader = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        print(Fore.GREEN + f"Username: {profile.username}" + Style.RESET_ALL)
        print(f"Full Name: {profile.full_name}")
        print(f"Bio: {profile.biography}")
        print(f"Followers: {profile.followers}")
    except instaloader.exceptions.ProfileNotExistsException:
        print(Fore.RED + f"Error: Profile '{username}' does not exist." + Style.RESET_ALL)

def main():
    aboutthetool()
    while True:
        choice = show_menu()

        if choice == "1":
            query = input("Enter search query: ")
            num_results = int(input("Enter number of results to fetch: "))
            search_results = google_search(query, num_results)
            print(Fore.GREEN + "Search Results:" + Style.RESET_ALL)
            for result in search_results:
                print(result)

        elif choice == "2":
            ip = input("Enter IP address to analyze: ")
            ip_info = ip_analysis(ip)
            print(Fore.GREEN + "IP Analysis Results:" + Style.RESET_ALL)
            print(json.dumps(ip_info, indent=4))

        elif choice == "3":
            domain = input("Enter domain to resolve: ")
            ip = domain_to_ip(domain)
            if ip:
                print(Fore.GREEN + f"The IP address for {domain} is {ip}" + Style.RESET_ALL)

        elif choice == "4":
            username = input("Enter username: ")
            platform = input("Enter platform (Twitter, Instagram, Facebook): ")
            print(Fore.GREEN + f"Profile URL: https://www.{platform.lower()}.com/{username}" + Style.RESET_ALL)

        elif choice == "5":
            username = input("Enter Instagram username: ")
            instagram_profile_info(username)

        elif choice == "6":
            print(Fore.CYAN + """
            OSINT Tool v1.0
            Created by: FRn13ds
            Description: A versatile OSINT tool for gathering intelligence from open sources.
            """ + Style.RESET_ALL)

        elif choice == "7":
            print(Fore.RED + "Exiting the tool. Goodbye!" + Style.RESET_ALL)
            break

        else:
            print(Fore.RED + "Invalid option. Please try again." + Style.RESET_ALL)

if __name__ == "__main__":
    main()

