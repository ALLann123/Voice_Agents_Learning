#!/usr/bin/python3
import os
from dotenv import load_dotenv
from tavily import TavilyClient

# load our API keys
load_dotenv()

# get the Tavily API key
client=TavilyClient(api_key=os.getenv("TAVILLY_API"))

def web_search(query: str)-> str:
    """
    Search the web using Tavily and return a formatted string
    suitable for an LLM prompt
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    results=response.get("results", [])

    # if results is empty
    if not results:
        return "No relevant search results were found"
    

    #------This is done for Proper formating to the LLM"
    output=f"Search Query: {query}\n\n"
    output+="Search Result:\n\n"

    for i, result in enumerate(results, start=1):
        output+=(
            f"Result {i}\n"
            f"Title: {result.get('content')}\n"
            f"URL: {result.get('url')}\n\n"
            f"Content: {result.get('content')}\n\n"
        )

    return output

# call our function
search_results=web_search("Current Price of USD to CAD?")
print(search_results)





"""
Tavily_web_search>python main.py
Search Query: Current Price of USD to CAD?

Search Result:

Result 1
Title: | Oct 16, 2025 | 1.4046 | 1.4057 | 1.4022 | 1.4046 | 1.4046
| Oct 15, 2025 | 1.4045 | 1.4053 | 1.4027 | 1.4045 | 1.4045
| Oct 14, 2025 | 1.4039 | 1.4079 | 1.4030 | 1.4039 | 1.4039
| Oct 13, 2025 | 1.3999 | 1.4032 | 1.3983 | 1.3999 | 1.3999
| Oct 10, 2025 | 1.4019 | 1.4033 | 1.3976 | 1.4019 | 1.4019
| Oct 9, 2025 | 1.3955 | 1.4020 | 1.3933 | 1.3955 | 1.3955
| Oct 8, 2025 | 1.3953 | 1.3970 | 1.3932 | 1.3953 | 1.3953
| Oct 7, 2025 | 1.3946 | 1.3962 | 1.3940 | 1.3946 | 1.3946
| Oct 6, 2025 | 1.3965 | 1.3967 | 1.3941 | 1.3965 | 1.3965
| Oct 3, 2025 | 1.3961 | 1.3968 | 1.3945 | 1.3961 | 1.3961
| Oct 2, 2025 | 1.3939 | 1.3985 | 1.3932 | 1.3939 | 1.3939
| Oct 1, 2025 | 1.3923 | 1.3955 | 1.3907 | 1.3923 | 1.3923
| Sep 30, 2025 | 1.3916 | 1.3934 | 1.3896 | 1.3916 | 1.3916 [...] | Jul 18, 2025 | 1.3736 | 1.3742 | 1.3696 | 1.3736 | 1.3736
| Jul 17, 2025 | 1.3689 | 1.3773 | 1.3689 | 1.3689 | 1.3689

    ....................


Result 2
Title: ### What is the USD to CAD exchange rate today?

As of 19:43 UTC, the mid-market USD to CAD rate is $1 = $1.4161. The mid-market rate is the midpoint between buy and sell prices in global currency markets. To see how much this transfer would be with Xe, visit our send money page.

### How much is 1 USD in CAD?

1 USD equals 1.41 CAD using the current mid-market exchange rate of $1.4161. If you're looking to send 1 USD to CAD, check if Xe could save you money on your transfer. Get a live quote on our send money page and see the full price upfront.

### How do I convert currencies?

To convert currencies, visit the top our Currency Converter, select your preferred currency pair, enter your amount, and view the live mid-market rate.

### Can I set rate alerts with Xe? [...] 1 USD to CAD

| Metric | Last 7 days | Last 30 days | Last 90 days |
 ---  --- |
| High | 1.4218 | 1.4235 | 1.4235 |
| Low | 1.4190 | 1.3938 | 1.3580 |
| Average | 1.4205 | 1.4110 | 1.3865 |
| Volatility | 0.09% | 0.18% | 0.20% |

### USD to CAD statistics

Over the last 7 days, USD to CAD moved between 1.4190 and 1.4218. The average was 1.4205 with 0.09% volatility.

"""