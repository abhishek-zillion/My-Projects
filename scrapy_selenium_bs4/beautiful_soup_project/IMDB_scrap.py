from bs4 import BeautifulSoup
from selenium_ import selenium_config, excel


def imdb_rating_extraction():
    '''
    Script for extracting data of Top 250 movies
    from IMDB website and saving the data in an Excel file.
    '''
    excel_obj, sheet = excel.workbook_creation()
    try:
        selenium_obj = selenium_config.Selenium()
        page_source = selenium_obj.land_page()

        soup = BeautifulSoup(page_source, 'html.parser')
        movies_list = soup.find(
            'ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-a1e81754-0 eBRbsI compact-list-view ipc-metadata-list--base')

        for movie in movies_list.find_all('li'):
            movie: BeautifulSoup
            name_data: str = movie.find('h3').get_text(strip=True)

            first_dot_index = name_data.find('.')
            rank = name_data[0:first_dot_index]

            first_space_index: int = name_data.find(' ')
            name: str = name_data[first_space_index+1:]

            year_and_time = movie.find_all(
                'span', class_='sc-b189961a-8 kLaxqf cli-title-metadata-item')
            year = year_and_time[0].text
            watchtime: str = year_and_time[1].text
            watchtime = ''.join(watchtime.split())

            rating = movie.find('span', class_="ipc-rating-star--rating").text

            voted_users_unformatted: str = movie.find(
                'span', class_="ipc-rating-star--voteCount").text.strip()
            voted_users = voted_users_unformatted[1:-1]
            print(rank, name, year, watchtime, rating, voted_users)
            sheet.append([rank, name, year, watchtime, rating, voted_users])

        excel_obj.save('IMDB_movie_rating.xlsx')
        selenium_obj.quit()

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    imdb_rating_extraction()
