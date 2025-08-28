import numpy as np



def fetch_medal_tally(df, year, country):
    medal_df = df.dropna(subset=['Medal'])
    medal_df = medal_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    flag = 0

    if year == 'Overall' and country == 'Overall':
        temp_df = medal_df
    elif year == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    elif year != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(year)]
    else:
        temp_df = medal_df[(medal_df['Year'] == int(year)) & (medal_df['region'] == country)]

    if flag == 1:
        group = 'Year'
    else:
        group = 'region'

    # ✅ Correct way to count medals
    medal_count = temp_df.groupby([group, 'Medal']).size().unstack(fill_value=0).reset_index()

    # ✅ Ensure all medal columns exist
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in medal_count.columns:
            medal_count[medal] = 0

    medal_count['total'] = medal_count['Gold'] + medal_count['Silver'] + medal_count['Bronze']
    medal_count = medal_count.sort_values('Gold', ascending=False).reset_index(drop=True)

    return medal_count

def medal_tally(df):
    medal_df = df.dropna(subset=['Medal'])
    medal_df = medal_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])

    medal_count = medal_df.groupby(['region', 'Medal']).size().unstack(fill_value=0).reset_index()

    # ✅ Ensure all medal columns exist
    for medal in ['Gold', 'Silver', 'Bronze']:
        if medal not in medal_count.columns:
            medal_count[medal] = 0

    medal_count['total'] = medal_count['Gold'] + medal_count['Silver'] + medal_count['Bronze']
    medal_count = medal_count.sort_values('Gold', ascending=False).reset_index(drop=True)

    return medal_count


def Country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    Country = np.unique(df['region'].dropna().values).tolist()
    Country.sort()
    Country.insert(0, 'Overall')

    return years,Country

def data_over_time(df, col):

    temp_df = df.drop_duplicates(['Year',col])

    data_over_time = temp_df.groupby('Year')[col].count().reset_index()
    data_over_time.rename(columns={'Year': 'Edition',col:'No of' + col.capitalize()}, inplace=True)
    data_over_time.sort_values('Edition',inplace=True)
    return data_over_time

def most_successful(df,sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15)
    x.columns = ['Athlete','Medals']
    return x

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year')['Medal'].count().reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'Sport', 'Event', 'Medal'])

    new_df = temp_df[temp_df['region'] == country]

    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    df = df.dropna(subset=['Medal'])
    temp_df = df[df['Team'] == country]

    x = temp_df['Name'].value_counts().reset_index()
    x.columns = ['Name','Medals']
    x = x.head(10).merge(df,on='Name',how='left')[['Name','Medals','Sport']].drop_duplicates('Name')
    x.rename(columns = {'index':'Name','Name_x':'Medals'},inplace=True)
    return x

def weight_v_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    athlete_df['Medal'].fillna('No Medal', inplace=True)
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        return temp_df
    else:
        return athlete_df

def men_vs_women(df):
     athlete_df = df.drop_duplicates(subset=['Name', 'region'])

     men = athlete_df[athlete_df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
     women = athlete_df[athlete_df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()

     final = men.merge(women, on='Year', how='left')
     final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)

     final.fillna(0, inplace=True)

     return final

def men_vs_women(df):
    men = df[df['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    women = df[df['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    men.rename(columns={'Name': 'Male'}, inplace=True)
    women.rename(columns={'Name': 'Female'}, inplace=True)
    final = men.merge(women, on='Year', how='left')
    return final









