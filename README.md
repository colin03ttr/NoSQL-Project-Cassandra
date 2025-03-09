# NoSQL - Project - Cassandra

Colin TANTER - ESILV - OCC3

[link to my github repository](https://github.com/colin03ttr/NoSQL-Project-Cassandra)

## Create Database on Cassandra

### Files transfer

```
docker cp ../ cassandraServer:/
```

On Docker Desktop, I open the CLI and find the dataset :

```
ls -l
...
-rwxr-xr-x   1 root root  61483877 Mar  7 16:13 movielens_usersRating.json
...
...
```

### Database and Table Creation

Let's create the database using Cassandra with ``cqlsh``, and 2 tables ``user`` and ``ratings`` :
```
cqlsh> CREATE KEYSPACE IF NOT EXISTS MOVIELENS_USERRATINGS
   ... WITH REPLICATION =
   ... { 'class' : 'SimpleStrategy', 'replication_factor': 1 };

cqlsh> USE MOVIELENS_USERRATINGS;
cqlsh:movielens_userratings> CREATE TABLE user ( user_id int, name text, gender text, age int, occupation text, PRIMARY KEY (user_id) );
cqlsh:movielens_userratings> CREATE TABLE ratings ( user_id int, movie_id int, rating int, timestamp bigint, PRIMARY KEY (user_id,movie_id) );
```

### Import data
I chose to convert the json file into a csv to populate the database, I did it using [this python script](./json_to_csv.py).

Then I chose to split the csv into 2 different csv, to fit each table using [this python script](./split_csv_tables.py).

I moved the files into the container files :
```
 docker cp .\users.csv cassandraServer:/
Successfully copied 238kB to cassandraServer:/
 docker cp .\ratings.csv cassandraServer:/
Successfully copied 22.6MB to cassandraServer:/
```


Then I populated the tables :

```
COPY user(user_id,name,gender,age,occupation) FROM './users.csv' WITH HEADER = TRUE AND DELIMITER = ',';
Using 7 child processes

Starting copy of movielens_userratings.user with columns [user_id, name, gender, age, occupation].
Processed: 6040 rows; Rate:    4745 rows/s; Avg. rate:    7507 rows/s
6040 rows imported from 1 files in 0.805 seconds (0 skipped).
COPY ratings(user_id,movie_id,rating,timestamp) FROM './ratings.csv' WITH HEADER = TRUE AND DELIMITER = ',';
Using 7 child processes

Starting copy of movielens_userratings.ratings with columns [user_id, movie_id, rating, timestamp].
Processed: 1000209 rows; Rate:   26431 rows/s; Avg. rate:   53223 rows/s
1000209 rows imported from 1 files in 0 day, 0 hour, 0 minute, and 18.793 seconds (0 skipped).
```

I can now perform the queries

## Queries
### Simple Queries

**1. Get 5 users infos.**
```
cqlsh:movielens_userratings> SELECT * FROM user LIMIT 5;

 user_id | age | gender | name           | occupation
---------+-----+--------+----------------+----------------------
    4317 |  44 |      F |   Ceola Quincy |      sales/marketing
    3372 |  60 |      M |   Cecil Edmund |              retired
    1584 |  25 |      M |    Bud Shannon |           unemployed
    4830 |   9 |      M |    Jeromy Huey |         K-12 student
    2731 |  38 |      M | Orville Gerald | executive/managerial

(5 rows)
```
**2. Get users between 18 and 26**
```
cqlsh:movielens_userratings> SELECT user_id, name, age FROM user WHERE age >= 18 AND age <= 26 LIMIT 20 ALLOW FILTERING;

 user_id | name             | age
---------+------------------+-----
    1584 |      Bud Shannon |  25
    1863 |        Irwin Ali |  19
    2453 |     Lonny Armand |  25
    5801 |        Ty Tommie |  25
    3733 |         Man Evan |  21
    1765 |     Irvin Kareem |  21
    1580 |    Tania Donnell |  22
    2062 | Franklin Darnell |  18
    2744 |          Ty Hank |  20
    2747 |   Aileen Cordell |  19
     878 |      Danial Bret |  18
    2850 |     Levi Clifton |  24
     363 |   Jordon Alfonso |  20
    3315 |   Danny Santiago |  25
     778 |    Tyrell Russel |  18
    2074 | Leonel Sebastian |  21
    5585 |       Herb Davis |  25
     310 |    Emilia Bobbie |  22
    4635 |   Dwayne Timothy |  18
    5546 |     Jeromy Jared |  23

(20 rows)
```
**3. Get the average rating given by a specific user.**
```
cqlsh:movielens_userratings> SELECT AVG(rating) FROM ratings WHERE user_id = 1200;

 system.avg(rating)
--------------------
                  3

(1 rows)
```
**4. Get every movie a specific user has given a rating of 5.**
```
cqlsh:movielens_userratings> SELECT movie_id, rating FROM ratings WHERE user_id = 1 AND rating = 5 ALLOW FILTERING;

 movie_id | rating
----------+--------
        1 |      5
       48 |      5
      150 |      5
      527 |      5
      595 |      5
     1022 |      5
     1028 |      5
     1029 |      5
     1035 |      5
     1193 |      5
     1270 |      5
     1287 |      5
     1836 |      5
     1961 |      5
     2028 |      5
     2355 |      5
     2804 |      5
     3105 |      5

(18 rows) 
```
**6. Get the number of ratings made by a specific user**
```
cqlsh:movielens_userratings> SELECT COUNT(*) FROM ratings WHERE user_id = 12;

 count
-------
    23

(1 rows)
```
