import requests
from bs4 import BeautifulSoup
import json
import argparse

def extract_modules(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    modules = []

    for h2 in soup.find_all("h2"):
        module_name = h2.get_text(strip=True)
        module_desc = "This module contains documentation related to " + module_name.lower()

        submodules = {}
        sibling = h2.find_next_sibling()

        while sibling and sibling.name != "h2":
            if sibling.name == "h3":
                title = sibling.get_text(strip=True)
                submodules[title] = "Details about " + title.lower()
            sibling = sibling.find_next_sibling()

        modules.append({
            "module": module_name,
            "Description": module_desc,
            "Submodules": submodules
        })

    return modules


    soup = BeautifulSoup(response.text, "html.parser")

    modules = []

    # h2 = Module, h3 = Submodule
    for h2 in soup.find_all("h2"):
        module_name = h2.get_text(strip=True)
        module_desc = "This module contains documentation related to " + module_name.lower()

        submodules = {}
        sibling = h2.find_next_sibling()

        while sibling and sibling.name != "h2":
            if sibling.name == "h3":
                title = sibling.get_text(strip=True)
                submodules[title] = "Details about " + title.lower()
            sibling = sibling.find_next_sibling()

        modules.append({
            "module": module_name,
            "Description": module_desc,
            "Submodules": submodules
        })

    return modules


def main():
    parser = argparse.ArgumentParser(description="Module Extraction AI Agent")
    parser.add_argument("--url", required=True, help="Documentation URL")
    args = parser.parse_args()

    result = extract_modules(args.url)
    print(json.dumps(result, indent=4))


if __name__ == "__main__":
    main()
