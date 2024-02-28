import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

def get_career_info(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        # Extracting the text from each paragraph
        paragraph_texts = [p.get_text() for p in paragraphs]
        text = f""
        for i in range(len(paragraph_texts)):
            text += paragraph_texts[i]
        print(text)
        return text

    return "Career information not found"

def main():
    url = "https://en.wikipedia.org/wiki/List_of_Hindi_film_actors"
    response = requests.get(url)
    actors_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        hrefs = [a['href'] for a in soup.find_all('a', href=True)]
        flag = 0
        actors_data = []
        for i in range(len(hrefs)):
            if hrefs[i] == '/wiki/A._K._Hangal':
                flag = 1
            if flag == 1:
                actors_data.append([hrefs[i].split('/')[-1], get_career_info("https://en.wikipedia.org/" + hrefs[i])])
            if hrefs[i] == '/wiki/Zulfi_Syed':
                flag = 0
                break


        # Save to CSV
        df = pd.DataFrame(actors_data, columns=['Name', 'Career'])
        csv_file_path = os.path.join(os.path.dirname(__file__), "../static/hindi_films_actors.csv")
        df.to_csv(csv_file_path, index=False)
        print(f"CSV file saved at {csv_file_path}")
    else:
        print("Failed to fetch the main page.")

if __name__ == "__main__":
    main()
