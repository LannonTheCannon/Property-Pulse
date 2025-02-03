
import pandas as pd

df = pd.read_csv('la_listings_vis.csv')

def get_columns():
    print(df.columns)

def view_listings():
    print(df.head(5))

if __name__ == '__main__':

    choices = [get_columns, view_listings]

    menu = int(input('''
    1. See Column Headings 
    2. See Listings Head
    
'''))

    func_call = choices[menu-1]()


    #view_listings(df)