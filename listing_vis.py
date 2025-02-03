
import pandas as pd

df = pd.read_csv('la_listings_vis.csv')

def get_columns():
    print(df.columns)

def view_listings():
    print(df.head(5))

def df_names():
    # Play around with the dataframe
    new_df = df[['name', 'host_name']]

    # Get all the locations with a price that's less than a certain number
    play_df = df[df['price'] < 5]

    print(play_df)

if __name__ == '__main__':

    choices = [get_columns, view_listings, df_names]

    menu = int(input('''
    1. See Column Headings 
    2. See Listings Head
    3. See chosen DF 
    
'''))

    func_call = choices[menu-1]()
    #view_listings(df)