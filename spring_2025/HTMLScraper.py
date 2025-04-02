import requests
from bs4 import BeautifulSoup


def fetch_hours_from_google_doc():
    global url, response, p, file, text
    # URL of the Google Doc published on the VML site
    url = "https://docs.google.com/document/d/e/2PACX-1vQI6sOZt1i9eRKaXa5B3FiLgzjGktt9ymqVpUAswEVlbiNLb4shDFMN82DVsNsDd_6OboApnCzIrwDw/pub"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Info is (currently) in the form of a table; may need to change this code if format is changed in the future
        table = soup.find('table')
        if table:
            rows = table.find_all('tr')  # Extracts table rows (tr)
            table_data = []

            for row in rows:  # parsing table rows
                cells = row.find_all(['td', 'th'])
                cell_texts = []
                for cell in cells:
                    p_tags = cell.find_all(
                        'p')  # If there are multiple <p> tags inside the <td>, join them with \n newline characters
                    if p_tags:
                        cell_text = str.rstrip("\n".join([p.get_text(strip=True) for p in p_tags]))
                    else:
                        cell_text = cell.get_text(strip=True)
                    cell_texts.append(cell_text)
                table_data.append(" ".join(cell_texts))

            with open("/home/vml/eink_data/schedule.txt", "w") as file:
                file.write(repr(table_data))

            # this is an alternate saving scheme, but I think the repr format is the
            # smoothest option for the purpose of the eink display
            # with open("schedule.txt", "w", encoding="utf-8") as file:
            #     for i in range(len(table_data)):
            #         row_text = " ".join(table_data[i])
            #         if i == (len(table_data)-1):
            #             file.write(row_text)
            #         else:
            #             file.write(row_text + "\n")

        # if the format is changed from a table, this is some starting code to parse it.
        # Haven't tested it much though (might need a bit of work if it becomes necessary)
        else:
            doc_body = soup.find('body')
            paragraphs = []  # finding <p> tags
            for paragraph in doc_body.find_all('p'):
                text = paragraph.get_text(strip=True)
                if text:  # Ignore empty paragraphs
                    paragraphs.append(text)
            # Combine the paragraphs with line breaks for separation
            document_text = "\n".join(paragraphs)
            print(document_text)
    else:
        print(f"Failed to retrieve the document. Status code: {response.status_code}")


#fetch_hours_from_google_doc()