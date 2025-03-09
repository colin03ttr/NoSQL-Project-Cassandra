import pandas as pd

# Read the dataset from the CSV file
input_file = '../movielens_usersRating.json/movielens_usersRating.csv'
df = pd.read_csv(input_file)

# Create the first set with the first 5 columns
first_5_columns = df.iloc[:, :5]

# Create the second set with the first and last 3 columns
first_and_last_3_columns = pd.concat([df.iloc[:, :1], df.iloc[:, -3:]], axis=1)

# Remove every duplicate row
first_5_columns = first_5_columns.drop_duplicates()
first_and_last_3_columns = first_and_last_3_columns.drop_duplicates()

# Save the two sets to CSV files
first_5_columns.to_csv('../movielens_usersRating.json/users.csv', index=False)
first_and_last_3_columns.to_csv('../movielens_usersRating.json/ratings.csv', index=False)