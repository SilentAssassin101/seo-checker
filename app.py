import customtkinter as tk
import requests
from bs4 import BeautifulSoup

keywords = []

def fetchPage(url):
    """fetchPage fetches the page from the given URL

    Args:
        url (_type_): url of the page to fetch

    Returns:
        page object
    """
    try:
        page = requests.get(url)
        page.raise_for_status()
        return page
    except requests.HTTPError as e:
        print(f"HTTP Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    
def analyzePage(url, keywords, resultLabel):
    """analyzePage analyzes the page

    Args:
        string: page url

    Returns:
        seo check results
    """
    html = fetchPage(url)
    if html:
        soup = BeautifulSoup(html.text, 'html.parser')
        # SEO checks
        titleCheckResult = checkTitle(soup, keywords)
        metaCheckResult = checkMetaDescription(soup, keywords)
        headingCheckResult = checkHeadings(soup, keywords)
        # print the results
        print(titleCheckResult)
        print(metaCheckResult)
        print(headingCheckResult)
        #show the results in the GUI
        resultLabel.configure(text=f"{titleCheckResult}\n{metaCheckResult}\n{headingCheckResult}")

def checkTitle(soup, keywords):
    """checkTitle checks the title of the page

    Args:
        soup (soup object): soup object of the page
        keywords (list): list of keywords to check for in the title (from the user input)

    Returns:
        string: is title too short? too long? or just right?
    """
    title = soup.find('title')
    titleLength = len(title.string) if title else 0
    output = "Title:"
    if titleLength < 40:
        output += " Too Short"
    elif titleLength > 60:
        output += " Too Long"
    titleWords = title.string.upper().split()
    includedKeywords = 0
    for keyword in keywords:
        if keyword in titleWords:
            includedKeywords += 1
    if includedKeywords < len(keywords) // 2:
        output += " Doesn't include enough keywords"
    return output
    
def checkMetaDescription(soup, keywords):
    """checkMetaDescription checks the meta description of the page

    Args:
        soup (soup object): soup object of the page

    Returns:
        string: is meta description too short? too long? or just right?
    """
    metaDescription = soup.find('meta', attrs={'name': 'description'})
    if metaDescription is None:
        return "Meta Description: Not Found"
    metaDescriptionLength = len(metaDescription['content'])
    metaDescriptionWords = metaDescription['content'].upper().split()
    output = "Meta Description:"
    if metaDescriptionLength < 70:
        output += " Too Short"
    elif metaDescriptionLength > 160:
        output += " Too Long"
    for keyword in keywords:
        if keyword not in metaDescriptionWords:
            output += " Doesn't include all keywords"
            return output
    return output

def checkHeadings(soup, keywords):
    """checkHeadings checks the headings of the page

    Args:
        soup (soup object): soup object of the page
        keywords (list): list of keywords to check for in the headings (from the user input)

    Returns:
        string: do headings contain keywords?
    """
    f_keywords = keywords
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for heading in headings:
        if heading.string is not None:
            for keyword in f_keywords:
                if keyword in heading.string.upper():
                    keywords.remove(keyword)
        if not f_keywords:
            return "Headings: Contain all keywords"
    return "Headings: Do not contain all keywords"
def main():
    # GUI
    tk.set_appearance_mode("system")
    tk.set_default_color_theme("dark-blue")

    root = tk.CTk()
    root.title("SEO Analyzer")
    root.geometry("500x600")

    frame = tk.CTkFrame(master=root)
    frame.pack(pady=20, padx=60, fill="both", expand=True)

    mainLabel = tk.CTkLabel(master=frame, text="SEO Analyzer", font=("Roboto", 20))
    mainLabel.pack(pady=12, padx=10)

    urlBox = tk.CTkEntry(master=frame, placeholder_text="Enter URL", font=("Roboto", 12))
    urlBox.pack(pady=12, padx=10)

    #CoPilot & GPT4 Assisted Start
    keywordBox = tk.CTkTextbox(master=frame, height=5, font=("Roboto", 12))
    keywordBox.pack(pady=12, padx=10, fill="both", expand=True)

    analyzeButton = tk.CTkButton(master=frame, text="Analyze", font=("Roboto", 12), command=lambda: \
        analyzePage("https://" + urlBox.get(), keywordBox.get("1.0", "end-1c").upper().split("\n"), resultLabel))
    analyzeButton.pack(pady=12, padx=10)
    #CoPilot & GPT4 Assisted End

    resultLabel = tk.CTkLabel(master=frame, text="", font=("Roboto", 12))
    resultLabel.pack(pady=12, padx=10)

    root.mainloop()
    
if __name__ == "__main__":
    main()