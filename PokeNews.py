import random
import click
import requests
import json
import spacy


###### TODO
###### List of organizations to replace with
###### List of Geo-Political Entities to replace with
###### Check for repeated entities in the list of names/orgs/etc we match+replace (linked list duplicate removal)


@click.command()
@click.option('--api-key', '-a', help='your API key for newsapi.org API')
@click.option('--query', '-q', help='your keyword query for newsapi.org API')
def main(query, api_key):

    # form our newsapi.org URL
    API_KEY = '&apiKey=' + str(api_key)
    url = 'https://newsapi.org/v2/everything?q='
    google = url + query + API_KEY
    print("Your request URL is: " + str(google))

    # initialize Spacy for named entity recognition
    nlp = spacy.load("en_core_web_sm")

    # Setup the requests for pokemanes
    pokeapi_baseurl = 'http://pokeapi.co/api/v2/pokemon/'


    def random_pokemane(number_of_pokemon, debug=False):
        pokemon_list = []
        x = 0
        while x < number_of_pokemon:
            number = random.randint(1,500)
            pokeapi = requests.get(pokeapi_baseurl + '{0}/'.format(number))
            json_response = json.loads(pokeapi.content)
            pokemon_list.append(json_response)
            x += 1
            if debug is True:
                print("Request for Pokemon #: " + str(number))
                print("HTTP Status Code: " + str(pokeapi.status_code))
        return pokemon_list

    def get_pokenames(list_of_pokemon):
        pokename_list = []
        x = 0
        for i in list_of_pokemon:
            pokename_list.append(str(i['name']).capitalize())
            x += 1
        return pokename_list

    def check_people(jsondict, keyword, content, tokenstring):
        for k, v in jsondict.items():
            x = 0
            if k == keyword:
                print(jsondict[k])
                datastructure = []
                for key in jsondict[k]:
                    for y, z in key.items():
                        if y == content:
                            doc = nlp(z)
                            tokens = [(ent.text, ent.label_) for ent in doc.ents]
                            for i, e in tokens:
                                if e == tokenstring:
                                    print("Adding #" + str(x) + ": " + z)
                                    datastructure.append([z, tokens])
                                    x += 1
                return datastructure

    def get_names(list_of_dicts, search_term):
        list_of_names = []
        for i in list_of_dicts:
            x = 0
            for k in i:
                if k == str(search_term):
                    list_of_names.append(x)
                x = k
        return list_of_names

    # Match and replace names from a list with pokenames from a list
    def string_replace(fullstring, list_of_str_to_match, list_of_names):
        x = 0
        for i in list_of_str_to_match:
            result = fullstring.find(i)
            if result > 0 :
                print("this is string before: " + fullstring)
                fullstring = fullstring.replace(i, list_of_names[x])
                print("this is string after: " + fullstring)
            x += 1
        return fullstring

    # Get some names of PokeMon
    pokemon_list = random_pokemane(4, True)
    pokenames = get_pokenames(pokemon_list)
    print(pokenames)

    print()

    # get some Google News articles
    gNews = requests.get(google)
    googlejson = json.loads(gNews.content)

    # Make a list of articles and pull a list of people and a story headline from one of those articles
    peoplelist = check_people(googlejson, 'articles', 'description', 'PERSON')
    token_list = peoplelist[0][1]
    story_string = peoplelist[0][0]
    print("All matched Token entities: " + str(token_list))

    # Print the list of names and the chosen story headline as it is having person names replaced with PokeNames
    name_match = list(set(get_names(token_list, 'PERSON')))
    print("this is a list of names: " + str(name_match))
    replaced_string = string_replace(story_string, name_match, pokenames)
    print("Replaced string: " + replaced_string)


# Run all that garbage we defined above
if __name__ == "__main__":
    main()

