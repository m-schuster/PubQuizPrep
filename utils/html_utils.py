from bs4 import BeautifulSoup

def extract_news(soup):
    events = soup.find(class_="current-events-content description")
    
    titles = []
    contents = []
    
    for child in events.children:
        if child.name == 'p':
            titles.append(child.text.strip())
        elif child.name == 'ul':
            content_list = [li.text.strip() for li in child.find_all('li')]
            contents.append(content_list)
    
    result = []
    for title, content in zip(titles, contents):
        result.append(f"Title: {title}")
        result.append("Contents:")
        for item in content:
            result.append(f"  - {item}")
        result.append("")  # Add a blank line for separation
    
    result_string = "\n".join(result)
    return result_string

def extract_html_section(soup, header1_id, header2_id):
    header1 = soup.find(id=header1_id)
    header2 = soup.find(id=header2_id)

    ul_texts = []

    for element in header1.find_all_next():
        if element == header2:
            break
        if element.name == 'ul':
            ul_texts.append(element.text)

    return "".join(ul_texts)