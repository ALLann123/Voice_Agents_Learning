#!/usr/bin/python3
from firecrawl import FirecrawlApp
import os
from dotenv import load_dotenv

# load environment variables
load_dotenv()

# create an object
app=FirecrawlApp(api_key=os.getenv("FIRECRAWL"))

def scrape_webpage(url: str)-> str:
    """
    Read a webpage and return clean markdown suitable for an LLM
    """
    # send our request and store the markdown data
    response=app.scrape_url(
        url=url,
        formats=["markdown"]
    )
    print(type(response))
    print(response)
    print(dir(response))

    print("\n\n")
    markdown=getattr(response,"markdown","")

    # if it is empty
    if not markdown:
        return "Unable to extract content from the webpage."
    
    return f"""
    Source URL:
    {url}

    Extracted Content:
    {markdown}
"""

target="https://medium.com/@karisallan237/android-tv-pwn-910a26cc35c5"

result=scrape_webpage(target)

print("[+] Starting Scrape....\n")
print(result)

"""
fire_Crawl_Web_scraping>python main.py
[+] Starting Scrape....


    Source URL:
    https://medium.com/@karisallan237/android-tv-pwn-910a26cc35c5

    Extracted Content:
    [Sitemap](https://medium.com/sitemap/sitemap.xml)

    ....
Share

Android TV is essentially built on top of the Linux operating system, meaning the core functionality of Android TV relies on the Linux kernel for basic operations like memory management and threading, making Linux the foundation upon which Android TV is built.

However, most users won’t directly interact with the underlying Linux features as Android TV provides a separate user interface and app ecosystem on top of it.

Key points about the relationship:

· **Base system:** The foundation of Android TV is the Linux kernel.

· **Abstraction layer:** While Android TV runs on Linux, the user interface and most features are designed to hide the complexities of the underlying Linux system.

· **App ecosystem:** Unlike a standard Linux distribution, Android TV primarily uses apps from the Google Play Store, tailored for a TV experience.

**Discovering android TVs on Shodan**
"""

