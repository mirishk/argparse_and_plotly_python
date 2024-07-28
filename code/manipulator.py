class DataManipulator:
    def __init__(self, df):
        self.df = df
    # 1 ==================================================================================
    # generate a Series containing individual names from a {column} values after splitting by ', '
    # Also used in section 3
    @staticmethod
    def _split_column_and_count(df, column):
        df_split = df[column].str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
        
        df_counts = df_split.value_counts().reset_index()
        df_counts.columns = [column, 'Count']

        return df_counts

    # Function that splits the column values and counts occurrences
    def split_and_count(self, column, topN):
        filtered_df = self.df[~self.df[column].str.contains('specified', case=False)] # drop the 'non specified' values
        
        df_counts = self._split_column_and_count(filtered_df, column)
        
        return df_counts.head(topN)

    # 2 ======================================================================================
    # Group by year or month based on 'date_added' and 'type', and count the occurrences
    def group_by_time(self, interval): 
        if interval=='year':
            grouped_data = self.df.groupby([self.df['date_added'].dt.year, 'type']).size().reset_index(name='count')
        else:
            grouped_data = self.df.groupby([self.df['date_added'].dt.month, 'type']).size().reset_index(name='count')
        grouped_data.rename(columns = {'date_added': interval}, inplace=True)

        return grouped_data

    # 3 =================================================================================
    # Filter the dataframe
    # Also used in section 4
    @staticmethod
    def _filter_columns(df, type_of_netflix, column, word):
        if type_of_netflix == 'TV':
            type_of_netflix = 'TV Show'
        filtered_df = df[(~df[column].str.contains(word, case=False)) & (df['type'] == type_of_netflix)] # drop the 'non specified' values
        return filtered_df

    # Group by 'country' and count the number of movies or TV shows
    def group_by_country(self, type_of_netflix):
        filtered_df = self._filter_columns(self.df, type_of_netflix, 'country', 'Unknown')
        
        df_counts = self._split_column_and_count(filtered_df, 'country') # in section 1
        
        return df_counts

    # 4 -===============================================================================
    # Calculate the percentage of each age group from all age groups within each country
    @staticmethod
    def _calculate_percentage(grouped_df):
        grouped_df['percentage'] = grouped_df.groupby('country')['count'].transform(lambda x: round((x / x.sum()) * 100, 2))
        return grouped_df

    # Filter countries based on total_counts parameter
    @staticmethod
    def _filter_by_total_counts(df, total_count):
        country_total_counts = df.groupby('country')['count'].sum().reset_index()
        filtered_countries = country_total_counts[country_total_counts['count'] >= total_count]['country'].tolist()

        # Filter the original DataFrame based on selected countries
        filtered_df = df[df['country'].isin(filtered_countries)]
        return filtered_df

    # Analyzes the ratings by age group in different countries for a given type
    def group_by_country_and_rating_age(self, type_of_netflix, total_count):
        filtered_df = self._filter_columns(self.df, type_of_netflix, 'country', 'Unknown') # in section 3
        
        # Split rows with multiple countries into separate rows
        split_df = filtered_df.assign(country= filtered_df['country'].str.split(', ')).explode('country')
        split_df.head(5)
        
        # Group by country and age_group, count occurrences
        grouped_df = split_df.groupby(['country', 'age_group']).size().reset_index(name='count')

        # Calculate percentage and add as new column
        grouped_df = self._calculate_percentage(grouped_df) #in this section

        # Filter countries based on total_counts parameter
        filtered_df = self._filter_by_total_counts(grouped_df, total_count) #in this section

        return filtered_df
    #==================================================================================
