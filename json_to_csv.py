import json
import csv

def convert_json_to_csv(json_file, csv_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = [json.loads(line) for line in f]  # Read as JSON lines

    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["user_id", "name", "gender", "age", "occupation", "movie_id", "rating", "timestamp"])

        for user in data:
            user_id = user["_id"]
            name = user["name"]
            gender = user["gender"]
            age = user["age"]
            occupation = user["occupation"]

            for movie in user["movies"]:
                movie_id = movie["movieid"]
                rating = movie["rating"]
                timestamp = movie["timestamp"]
                writer.writerow([user_id, name, gender, age, occupation, movie_id, rating, timestamp])

if __name__ == "__main__":
    convert_json_to_csv("../movielens_usersRating.json/movielens_usersRating.json", "../movielens_usersRating.json/movielens_usersRating.csv")
    print("CSV file created successfully!")
