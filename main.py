import requests
from bs4 import BeautifulSoup
import argparse
import re
import json
import socket
from ipwhois import IPWhois
import instaloader
from colorama import init
init()

def google_search(query, num_results=10):
    """Perform a Google search and return results."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'url?q=' in href and not 'webcache' in href:
                url = re.search(r'url\?q=(.*?)&', href)
                if url:
                    links.append(url.group(1))
        return links
    else:
        print("Failed to fetch Google search results.")
        return []

def scrape_website(url):
    """Scrape the content of a given URL."""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.get_text()
    else:
        print(f"Failed to scrape {url}")
        return ""

def ip_analysis(ip_address):
    """Analyze an IP address using ipwhois."""
    try:
        obj = IPWhois(ip_address)
        result = obj.lookup_whois()
        return result
    except Exception as e:
        print(f"Failed to analyze IP {ip_address}: {e}")
        return {}

def domain_to_ip(domain):
    """Resolve a domain name to an IP address."""
    try:
        return socket.gethostbyname(domain)
    except socket.gaierror:
        print(f"Failed to resolve domain {domain}")
        return None

def social_media_profile_lookup(username, platform):
    """Perform a simple social media profile lookup."""
    platforms = {
        "twitter": f"https://twitter.com/{username}",
        "instagram": f"https://www.instagram.com/{username}/",
        "facebook": f"https://www.facebook.com/{username}"
    }
    return platforms.get(platform.lower(), "Platform not supported")

def instagram_profile_info(username):
    """Fetch detailed Instagram profile info using Instaloader."""
    loader = instaloader.Instaloader()
    try:
        profile = instaloader.Profile.from_username(loader.context, username)
        print(f"Username: {profile.username}")
        print(f"Full Name: {profile.full_name}")
        print(f"Bio: {profile.biography}")
        print(f"Followers: {profile.followers}")
        print(f"Following: {profile.followees}")
        print(f"Posts: {profile.mediacount}")
        print(f"Private: {profile.is_private}")
        print(f"Verified: {profile.is_verified}")
        print(f"Profile URL: https://www.instagram.com/{profile.username}/")

        if not profile.is_private:
            print("\nRecent Posts:")
            for post in profile.get_posts():
                print(f"- Post URL: https://www.instagram.com/p/{post.shortcode}/")
                print(f"  Likes: {post.likes}")
                print(f"  Comments: {post.comments}")
                print(f"  Caption: {post.caption}")
                print(f"  Date: {post.date}")
                print()

    except instaloader.exceptions.ProfileNotExistsException:
        print(f"Error: Profile '{username}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

def save_results(data, filename):
    """Save data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def show_menu():
    """Display the main menu and handle user input."""
    print("""
    =============================
    OSINT Tool Main Menu
    =============================
    1. Perform Google Search
    2. Analyze IP Address
    3. Resolve Domain to IP
    4. Social Media Profile Lookup
    5. Instagram Profile Detailed Info
    6. About
    7. Exit
    """)

    choice = input("Select an option (1-7): ")
    return choice

def main():
    while True:
        choice = show_menu()

        if choice == "1":
            query = input("Enter search query: ")
            num_results = int(input("Enter number of results to fetch: "))
            search_results = google_search(query, num_results)
            print("Search Results:")
            for result in search_results:
                print(result)

        elif choice == "2":
            ip = input("Enter IP address to analyze: ")
            ip_info = ip_analysis(ip)
            print("IP Analysis Results:")
            print(json.dumps(ip_info, indent=4))

        elif choice == "3":
            domain = input("Enter domain to resolve: ")
            ip = domain_to_ip(domain)
            if ip:
                print(f"The IP address for {domain} is {ip}")

        elif choice == "4":
            username = input("Enter username: ")
            platform = input("Enter platform (Twitter, Instagram, Facebook): ")
            profile_url = social_media_profile_lookup(username, platform)
            print(f"Profile URL: {profile_url}")

        elif choice == "5":
            username = input("Enter Instagram username: ")
            instagram_profile_info(username)

        elif choice == "6":
            print("""
            OSINT Tool v1.0
            Created by: FRn13ds
            Description: A versatile OSINT tool for gathering intelligence from open sources.
            """)

        elif choice == "7":
            print("Exiting the tool. Goodbye!")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
