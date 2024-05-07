import webbrowser

def owl(url):
    if "." in url:
        if "https" in url:
            webbrowser.open(url)
        webbrowser.open(f"https://{url}")
    else:
        if "https" in url:
            webbrowser.open(url + ".com")
        webbrowser.open(f"https://{url}.com")

def web_search(prompt):
    webbrowser.open(f"https://www.google.com/search?q={prompt}")