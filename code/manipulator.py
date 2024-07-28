class DataManipulator:
    def __init__(self, df): 
            
        # Initialize the DataManipulator with a DataFrame.
        self.df = df

    # 1 ==================================================================================
    
    @staticmethod
    def _split_column_and_count(df, column):

        # generate a Series containing individual names from a {column} values after splitting by ', '
        # Returns a DataFrame with the split values and their counts.

        df_split = df[column].str.split(', ', expand=True).stack().reset_index(level=1, drop=True)
        
        df_counts = df_split.value_counts().reset_index()
        df_counts.columns = [column, 'Count']

        return df_counts

    def split_and_count(self, column, topN):

        # Split the column values and count occurrences, returning the top N results.
        # Returns a DataFrame with the top N split values and their counts.

        filtered_df = self.df[~self.df[column].str.contains('specified', case=False)] # drop the 'non specified' values
        
        df_counts = self._split_column_and_count(filtered_df, column)
        
        return df_counts.head(topN)

    # 2 ======================================================================================

    def group_by_time(self, interval): 

        # Group by year or month based on 'date_added' and 'type', and count the occurrences.
        # Returns a DataFrame with the counts grouped by the specified interval and type.

        if interval=='year':
            grouped_data = self.df.groupby([self.df['date_added'].dt.year, 'type']).size().reset_index(name='count')
        else:
            grouped_data = self.df.groupby([self.df['date_added'].dt.month, 'type']).size().reset_index(name='count')
        grouped_data.rename(columns = {'date_added': interval}, inplace=True)

        return grouped_data

    # 3 =================================================================================
    
    @staticmethod
    def _filter_columns(df, type_of_netflix, column, word):

        # Filter the DataFrame based on type and column values.
        # Parameter word (str): The word to exclude from the column.
        # Returns the filtered DataFrame.

        if type_of_netflix == 'TV':
            type_of_netflix = 'TV Show'
        filtered_df = df[(~df[column].str.contains(word, case=False)) & (df['type'] == type_of_netflix)] 
        return filtered_df

    def group_by_country(self, type_of_netflix):

        # Group by 'country' and count the number of movies or TV shows.
        # Returns a DataFrame with the counts grouped by country.

        filtered_df = self._filter_columns(self.df, type_of_netflix, 'country', 'Unknown')
        
        df_counts = self._split_column_and_count(filtered_df, 'country') 
        
        return df_counts

    # 4 -===============================================================================
    
    @staticmethod
    def _calculate_percentage(grouped_df):

        # Calculate the percentage of each age group from all age groups within each country.
        # Returns a DataFrame with percentage values added.

        grouped_df['percentage'] = grouped_df.groupby('country')['count'].transform(lambda x: round((x / x.sum()) * 100, 2))
        return grouped_df

    @staticmethod
    def _filter_by_total_counts(df, total_count):

        # Filter countries based on total_counts parameter.
        # Returns the filtered DataFrame.

        country_total_counts = df.groupby('country')['count'].sum().reset_index()
        filtered_countries = country_total_counts[country_total_counts['count'] >= total_count]['country'].tolist()
        filtered_df = df[df['country'].isin(filtered_countries)]
        return filtered_df

    def group_by_country_and_rating_age(self, type_of_netflix, total_count):

        # Analyze the ratings by age group in different countries for a given type.
        # Returns a DataFrame with the counts and percentages grouped by country and age group.

        filtered_df = self._filter_columns(self.df, type_of_netflix, 'country', 'Unknown') # in section 3
        split_df = filtered_df.assign(country= filtered_df['country'].str.split(', ')).explode('country')
        grouped_df = split_df.groupby(['country', 'age_group']).size().reset_index(name='count')
        grouped_df = self._calculate_percentage(grouped_df) 
        filtered_df = self._filter_by_total_counts(grouped_df, total_count) 

        return filtered_df
