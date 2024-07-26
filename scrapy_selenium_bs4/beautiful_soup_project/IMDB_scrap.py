import shutil
import requests
from bs4 import BeautifulSoup
from selenium_ import selenium_config, excel
import os


def imdb_rating_extraction():
    '''
    Script for extracting data of Top 250 movies
    from IMDB website and saving the data in an Excel file.
    '''
    excel_obj, sheet = excel.workbook_creation()
    selenium_obj = selenium_config.Selenium()
    page_source = selenium_obj.land_page()
    try:
        soup = BeautifulSoup(page_source, 'html.parser')
        movies_list = soup.find(
            'ul', {'class': 'ipc-metadata-list', 'role': 'presentation'})
        movie_posters_dir = os.path.join(os.getcwd(), 'movie_posters')
        os.makedirs(movie_posters_dir, exist_ok=True)
        for movie in movies_list.find_all('li'):
            movie: BeautifulSoup
            name_data: str = movie.find('h3').get_text(strip=True)

            first_dot_index = name_data.find('.')
            rank = name_data[0:first_dot_index]

            first_space_index: int = name_data.find(' ')
            name: str = name_data[first_space_index+1:]
            spans = movie.select(
                '.cli-title-metadata .cli-title-metadata-item')
            year = spans[0].text
            watchtime = spans[1].text
            watchtime = ''.join(watchtime.split())

            rating = movie.find('span', class_="ipc-rating-star--rating").text

            voted_users_unformatted: str = movie.find(
                'span', class_="ipc-rating-star--voteCount").text.strip()
            voted_users = voted_users_unformatted[1:-1]
            print(rank, name, year, watchtime, rating, voted_users)

            img_element = movie.find('img', class_='ipc-image')
            if img_element:
                img_url = img_element['src']
                srcset = img_element.get('srcset')
                if srcset:
                    largest_img = srcset.strip().split(' ')[-2]
                    if largest_img:
                        img_url = largest_img
                img_name = f"{rank}_{name.replace(' ','_')}.jpg"

                img_path = os.path.join(movie_posters_dir, img_name)

                print('->', img_path)

                response = requests.get(img_url)
                if response.status_code == 200:
                    with open(img_path, 'wb') as file:
                        file.write(response.content)
                        print(f'Image saved successfully:{img_name}')
                else:
                    print(f"Failed to download image for {img_name}")
                    img_path = "NA"
                sheet.append([rank, name, year, watchtime,
                              rating, voted_users, img_path])

            else:
                print(f"No image found for {name}")
                sheet.append([rank, name, year, watchtime,
                              rating, voted_users, "NA"])

        excel_obj.save('IMDB_movie_rating.xlsx')
        answer = input('Do you want to delete images folder? (Y/N)')
    except Exception as e:
        print(f"Error occurred: {e}")
    if answer.lower() == 'y':
        shutil.rmtree(movie_posters_dir)
    selenium_obj.quit()


if __name__ == "__main__":
    imdb_rating_extraction()
