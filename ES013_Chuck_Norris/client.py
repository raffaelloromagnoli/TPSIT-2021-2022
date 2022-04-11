import requests

while True:
    choice=input('\nPress C to get the categories\n'
                 'Press R to get a random quote\n'
                 'Press S to search quote by keyword\n')

    if(choice=='c' or choice=='C'):
        categories=eval(requests.get('https://api.chucknorris.io/jokes/categories').text)
        print(categories)
        category=input('Type the category you want: ')
        quote=eval(requests.get(f'https://api.chucknorris.io/jokes/random?category={category}').text)['value']
        print(quote)
    elif(choice=='r' or choice=='R'):
        quote=eval(requests.get(f'https://api.chucknorris.io/jokes/random').text)['value']
        print(quote)
    elif(choice=='s' or choice=='S'):
        query=input('Type the keyword to search for: ')
        quotes=eval(requests.get(f'https://api.chucknorris.io/jokes/search?query={query}').text)
        print(f'Results: {quotes["total"]}\n')
        for quote in quotes['result']:
            print(f'{quote["value"]}\n')

