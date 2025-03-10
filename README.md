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

**2. Get the average rating given by a specific user.**
```
cqlsh:movielens_userratings> SELECT AVG(rating) FROM ratings WHERE user_id = 1200;

 system.avg(rating)
--------------------
                  3

(1 rows)
```

**3. Get the number of ratings made by a specific user**
```
cqlsh:movielens_userratings> SELECT COUNT(*) FROM ratings WHERE user_id = 12;

 count
-------
    23

(1 rows)
```

### Complex Queries
**1. Get every movie a specific user has given a rating of 5.**
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
**2. Get users between 18 and 26 of age**
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
**3. Get the movie_id and the average rating of a specific movie**
```
cqlsh:movielens_userratings> SELECT movie_id, AVG(rating) FROM ratings WHERE movie_id = 20 ALLOW FILTERING;

 movie_id | system.avg(rating)
----------+--------------------
       20 |                  2

(1 rows)

Warnings :
Aggregation query used without partition key
```
**4. Get all unemployed users**
```
cqlsh:movielens_userratings> SELECT * FROM user WHERE occupation = 'unemployed' LIMIT 15 ALLOW FILTERING;

 user_id | age | gender | name            | occupation
---------+-----+--------+-----------------+------------
    1584 |  25 |      M |     Bud Shannon | unemployed
    1902 |  31 |      M |  Carlton Delmar | unemployed
    5420 |   2 |      F |    Yaeko Brooks | unemployed
    1303 |  28 |      M |     Leland Glen | unemployed
    1933 |  23 |      M |    Major Jordon | unemployed
    2160 |  20 |      F |  Tania Porfirio | unemployed
     465 |  24 |      M |      Jim Hassan | unemployed
    3328 |  70 |      M |        Jeff Pat | unemployed
    1699 |  34 |      F | Celinda Stanton | unemployed
    4227 |  28 |      M |     Ahmad Homer | unemployed
    2712 |  21 |      F |   Jestine Isaac | unemployed
    1636 |  31 |      F |   Karrie Vernon | unemployed
    2993 |  18 |      M |    Josef Jeramy | unemployed
    2805 |  62 |      M |    Reuben Tyron | unemployed
      46 |  19 |      M |  Rosendo Jayson | unemployed

(15 rows)
```


### Hard queries

**1. Get the number of users for each occupation**
```
cqlsh:movielens_userratings> SELECT COUNT(*), occupation FROM user GROUP BY occupation;
InvalidRequest: Error from server: code=2200 [Invalid query] message="Group by is currently only supported on the columns of the PRIMARY KEY, got occupation"
```
To use GROUP BY on ``occupation``, it needs to be a PRIMARY KEY, so let's create another table with ``occupation`` as a PRIMARY KEY :
```
cqlsh:movielens_userratings> CREATE TABLE users_occupation (
                         ... user_id int,
                         ... name text,
                         ... gender text,
                         ... age int,
                         ... occupation text,
                         ... PRIMARY KEY ((occupation),user_id)
                         ... );
cqlsh:movielens_userratings> ALTER TABLE users_occupation WITH GC_GRACE_SECONDS = 0;
cqlsh:movielens_userratings> COPY users_occupation(user_id,name,gender,age,occupation) FROM './users.csv' WITH HEADER = TRUE AND DELIMITER = ',';
Using 7 child processes

Starting copy of movielens_userratings.users_occupation with columns [user_id, name, gender, age, occupation].
Processed: 6040 rows; Rate:    5328 rows/s; Avg. rate:    8717 rows/s
6040 rows imported from 1 files in 0.693 seconds (0 skipped).
```
Now let's use this table for our query :
```
cqlsh:movielens_userratings> SELECT COUNT(*), occupation FROM users_occupation GROUP BY occupation;

 count | occupation
-------+----------------------
   502 |  technician/engineer
   142 |              retired
    70 |  tradesman/craftsman
    92 |            homemaker
   679 | executive/managerial
   759 | college/grad student
   302 |      sales/marketing
   528 |    academic/educator
   112 |     customer service
   711 |                other
   144 |            scientist
   388 |           programmer
   129 |               lawyer
    72 |           unemployed
   281 |               writer
   236 |   doctor/health care
   173 |        clerical/admi
   241 |        self-employed
    17 |               farmer
   267 |               artist
   195 |         K-12 student

(21 rows)

Warnings :
Aggregation query used without partition key
