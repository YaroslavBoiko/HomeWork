import folium
from geopy.geocoders import Nominatim

def main():
    """

    This function does not return anything
    But it executes the code lines using other functions

    """
    try:
        year = int(input("Enter year "))
        if len(str(year)) == 4 :
            with open('locations.list.txt', 'r',errors='ignore', encoding='UTF-8') as in_file:
                read = in_file.read()
                data = read.split("\n")
                start = 0
                end = 2
                for i in data:
                    if i == "==============":
                        films = find(data[start + 1 : -end], year)
                        info = cleared(films)
                        break
                    start = start + 1
                print(info)
                locations = transformed_geo(info)
                map,fg = creat_map(year)
                map.add_child(draw(info, locations, fg))
                map.save('Map.html')
        else:
            print("Your year nedd be len - 4 ")
            main()
    except ValueError:
        print("Your year is not integer ")
    pass


def find(data, year):
    """
    (file.txt , number ) -> list

    The function returns a list with sorted rows in which there is a year

    """
    nice_film = []
    for row in data:
        if row.split("(")[1][:4] == year:
            nice_film.append(row)
    return nice_film


def cleared(films):
    """
    (list) -> (list)

    This function returns a list of each item containing two subelements
    The title of the movie and the place where the film was shot

    """
    info = []
    for film in films:
        splited = film.split(" (")
        name = splited[0]
        country = splited[-1]
        country = country.split(")")[1].replace('\t', '')
        info.append((name, country))
    return info

def creat_map(year):
    """
    This function creates a map
    """
    maps= folium.Map()
    fg = folium.FeatureGroup(name=year)
    return maps,fg


def transformed_geo(info):
    """

    This function returns a list
    Whose elements are subelements of two elements (latitude and longitude)

    """
    geolocator = Nominatim()
    loc = []
    for i in info:
        location = geolocator.geocode(i[1])
        lt = location.latitude
        ln = location.longitude
        loc.append((lt, ln))
    return loc

def draw(info, locations, fg):
    """

    This function marks the points where movies were shot in a particular year
    """
    for movies, location in zip(info, locations):
        fg.add_child(folium.Marker(location=[location[0], location[1]],popup=movies[0],icon=folium.Icon()))
    return fg
main()
