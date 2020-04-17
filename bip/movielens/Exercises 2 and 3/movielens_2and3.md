# Exercise 2
If you had to design a relational database schema (SQL) to store your results, what would it be?

## Answer to Exercise 2
Using the README.txt available in the 'ml-25m.zip' archive, it possible to extract the following details about the data file structure:
* `genome-scores.csv`: contains the tag relevance scores of movies
    * `movieId`: represents the movie id
    * `tagId`: represents the tag id
    * `relevance`: represents the tag relevance score
* `genome-tags.csv`: contains the tag descriptions for the tag ids
    * `tagId`: represents the tag id
    * `tag`: represents the tag description
* `links.csv`: contains the links to other sources of movie data
    * `movieId`: represents the movie id used on MovieLens.org (can be used to generate URL)
    * `imdbId`: represents the movie id used on IMDb.org (can be used to generate URL)
    * `tmdbId`: represents the movie id used on TheMovieDB.org (can be used to generate URL)
* `movies.csv`: contains the movies information
    * 'movieId': represents the movie id
    * 'title': represents the full movie title and may include the year of release in parenthesis
    * 'genres': a pipe-separated list of genres associated with the movie
* `ratings.csv`: movies ratings
    * `userId`: represents the user id
    * `movieId`: represents the movie id
    * `rating`: a 5-star scale rating of the movie, with 0.5 star increments (0.5 stars - 5.0 stars)
    * `timestamp`: time of rating in the seconds since midnight of January 1, 1970 on UTC time zone
* `tags.csv`: movies tags
    * `userId`: represents the user id
    * `movieId`: represents the movie id
    * `tag`: represents the user-generated textual metadata about the movie
    * `timestamp`: time of tag in the seconds since midnight of January 1, 1970 on UTC time zone

Also, pleas note that:
* only movies with at least one rating or tag are included in the dataset
* `movieId` is consistent with the ones used on the MovieLens web site
* `movieId` is a key field between `ratings.csv`, `tags.csv`, `movies.csv`, and `links.csv`
* `userId` is consistent between `ratings.csv` and `tags.csv `
* genres are a pipe-separated list, and are selected from the following list:
    * Action
    * Adventure
    * Animation
    * Children's
    * Comedy
    * Crime
    * Documentary
    * Drama
    * Fantasy
    * Film-Noir
    * Horror
    * Musical
    * Mystery
    * Romance
    * Sci-Fi
    * Thriller
    * War
    * Western
    * (no genres listed)

Due to the pipe-separated list of genres, we need to transform the `movies` table so that it contains one separate column for each genre.
In other words, for each movie, we are going to find either 1 or 0 in each genre column whether it is associated with the movie or not, respectively.
This will make it easy to answer questions such as "What are the most/least frequent genres?".

I would suggest to use the following schema in SQL.

~~~sql
-- #################################### SCHEMA CREATION & CONNECTION TO DB ###################################
CREATE SCHEMA `movielens`;
USE `movielens`;

-- #################################### START OF TABLES CREATION #############################################
DROP TABLE IF EXISTS `movies`;
CREATE TABLE `movies` (
   `movieId` INT NOT NULL, 
   `title` VARCHAR (255) NOT NULL, 
   `genres` TEXT,
   PRIMARY KEY (`movieId`)
);

DROP TABLE IF EXISTS `genome_scores`;
CREATE TABLE `genome_scores` (
   `genome_scores_id` INT AUTO_INCREMENT,
   `movieId` INT NOT NULL,
   `tagId` INT NOT NULL,
   `relevance` DECIMAL (22,21) NOT NULL,
   INDEX (`tagId`),
   PRIMARY KEY (`genome_scores_id`),
   UNIQUE (`movieId`, `tagId`),
   FOREIGN KEY (`movieId`) REFERENCES `movies`(`movieId`)
);

DROP TABLE IF EXISTS `genome_tags`;
CREATE TABLE `genome_tags` (
   `tagId` INT NOT NULL,
   `tag` VARCHAR(100) NOT NULL,
   INDEX (`tagId`),
   PRIMARY KEY (`tagId`),
   FOREIGN KEY (`tagId`) REFERENCES `genome_scores`(`tagId`)
);

DROP TABLE IF EXISTS `links`;
CREATE TABLE `links` (
   `movieId` INT NOT NULL,
   `imdbId` INT NULL,
   `tmdbId` INT NULL,
   FOREIGN KEY (`movieId`) REFERENCES `movies`(`movieId`)
);

DROP TABLE IF EXISTS `ratings`;
CREATE TABLE `ratings` (
   `userId` INT NOT NULL,
   `movieId` INT NOT NULL,
   `rating` DECIMAL(2,1) NOT NULL,
   `epoch` INT NOT NULL,
   FOREIGN KEY (`movieId`) REFERENCES `movies`(`movieId`)
);

DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
   `userId` INT NOT NULL,
   `movieId` INT NOT NULL,
   `tag` VARCHAR(255) NOT NULL,
   `epoch` INT (10) NOT NULL,
   FOREIGN KEY (`movieId`) REFERENCES `movies`(`movieId`)
);
-- #################################### END OF TABLES CREATION ###############################################
~~~

In particular, here is how I would insert the data into the `movies` table: I am going to add and to update 19 columns, one for each genre, and finally dropping the `genres` column.

~~~sql
-- #################################### START OF DATA LOADING INTO TABLES ####################################
-- Load data into `movies` table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ml-25m/movies.csv" INTO TABLE `movies` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' IGNORE 1 LINES; 
-- Add genre columns to `movies` table
ALTER TABLE `movies` ADD COLUMN `action` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `adventure` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `animation` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `children` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `comedy` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `crime` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `documentary` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `drama` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `fantasy` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `noir` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `horror` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `musical` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `mystery` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `romance` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `scifi` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `thriller` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `war` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `western` INT DEFAULT 0;
ALTER TABLE `movies` ADD COLUMN `no_genre` INT DEFAULT 0;
-- Update `movies` table by filling in genre tables
UPDATE `movies` SET `action` = 1 		WHERE `genres` LIKE '%Action%';
UPDATE `movies` SET `adventure` = 1		WHERE `genres` LIKE '%Adventure%';
UPDATE `movies` SET `animation` = 1 	WHERE `genres` LIKE '%Animation%';
UPDATE `movies` SET `children` = 1		WHERE `genres` LIKE '%Children%';
UPDATE `movies` SET `comedy` = 1 		WHERE `genres` LIKE '%Comedy%';
UPDATE `movies` SET `crime` = 1 		WHERE `genres` LIKE '%Crime%';
UPDATE `movies` SET `documentary` = 1 	WHERE `genres` LIKE '%Documentary%';
UPDATE `movies` SET `drama` = 1 		WHERE `genres` LIKE '%Drama%';
UPDATE `movies` SET `fantasy` = 1 		WHERE `genres` LIKE '%Fantasy%';
UPDATE `movies` SET `noir` = 1 			WHERE `genres` LIKE '%Noir%';
UPDATE `movies` SET `horror` = 1 		WHERE `genres` LIKE '%Horror%';
UPDATE `movies` SET `musical` = 1 		WHERE `genres` LIKE '%Musical%';
UPDATE `movies` SET `mystery` = 1 		WHERE `genres` LIKE '%Mystery%';
UPDATE `movies` SET `romance` = 1 		WHERE `genres` LIKE '%Romance%';
UPDATE `movies` SET `scifi` = 1 		WHERE `genres` LIKE '%Sci-Fi%';
UPDATE `movies` SET `thriller` = 1 		WHERE `genres` LIKE '%Thriller%';
UPDATE `movies` SET `war` = 1 			WHERE `genres` LIKE '%War%';
UPDATE `movies` SET `western` = 1 		WHERE `genres` LIKE '%Western%';
UPDATE `movies` SET `no_genre` = 1 		WHERE `genres` LIKE '%(no genres listed)%';
-- Dropping `genres` column from `movies` table (we do not need it any longer)
ALTER TABLE `movies` DROP `genres`;
~~~

And here is how I would insert the data into the remaining tables.

~~~sql
-- Load data into `tags` table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ml-25m/tags.csv" INTO TABLE `tags` FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' IGNORE 1 LINES; 
-- Add `timestamp` column to `tags` table, fill it from `epoch` column into timestamp and drop `epoch` column
ALTER TABLE `tags` ADD COLUMN `timestamp` TIMESTAMP;
UPDATE `tags` SET `timestamp` = FROM_UNIXTIME(`epoch`);
ALTER TABLE `tags` DROP `epoch`;

-- Load data into `ratings` table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ml-25m/ratings.csv" INTO TABLE `ratings` FIELDS TERMINATED BY ',' IGNORE 1 LINES; 
-- Add `timestamp` column to `ratings` table, fill it from `epoch` column into timestamp and drop `epoch` column
ALTER TABLE `ratings` ADD COLUMN `timestamp` TIMESTAMP;
UPDATE `ratings` SET `timestamp` = FROM_UNIXTIME(`epoch`);
ALTER TABLE `ratings` DROP `epoch`;

-- Load data into `links` table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ml-25m/links.csv" INTO TABLE `links` FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n' IGNORE 1 LINES
(`movieId`, @vimdbId, @vtmdbId)
SET
`imdbId` = IF(CHAR_LENGTH(TRIM(@vimdbId)) = 0, NULL, @vimdbId),
`tmdbId` = IF(CHAR_LENGTH(TRIM(@vtmdbId)) = 0, NULL, @vtmdbId);

-- Load data into `genome_scores` table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ml-25m/genome-scores.csv" INTO TABLE `genome_scores` FIELDS TERMINATED BY ',' IGNORE 1 LINES
(`movieId`, `tagId`, `relevance`);

-- Load data into `genome_tags` table
LOAD DATA INFILE "C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/ml-25m/genome-tags.csv" INTO TABLE `genome_tags` FIELDS TERMINATED BY ',' IGNORE 1 LINES;
-- #################################### END OF DATA LOADING INTO TABLES ######################################
~~~

Eventually, here is how the SQL schema would look like.

![SQL schema of MovieLens database](/bip/movielens/Exercises%202%20and%203/movielens_2and3_sql_schema.PNG)

# Exercise 3
Considering the database schema designed in the previous exercise (Exercise 2), write down a query (in SQL language or pseudo code) which:
1. Returns the frequency of each genres
2. Returns the most frequent tag used for Sci-Fi movies

## Answer to Exercise 3
Here is my SQL code to answer the two questions.
~~~sql
-- #################################### START OF DATA QUERYING FOR EXERCISE 3 ################################

-- 1- Returns the frequency of each genres
SELECT
	 SUM(`action`) AS `action`
	,SUM(`adventure`) AS `adventure`
	,SUM(`animation`) AS `animation`
	,SUM(`children`) AS `children`
	,SUM(`comedy`) AS `comedy`
	,SUM(`crime`) AS `crime`
	,SUM(`documentary`) AS `documentary`
	,SUM(`drama`) AS `drama`
	,SUM(`fantasy`) AS `fantasy`
	,SUM(`noir`) AS `noir`
	,SUM(`horror`) AS `horror`
	,SUM(`musical`) AS `musical`
	,SUM(`mystery`) AS `mystery`
	,SUM(`romance`) AS `romance`
	,SUM(`scifi`) AS `scifi`
	,SUM(`thriller`) AS `thriller`
	,SUM(`war`) AS `war`
	,SUM(`western`) AS `western`
	,SUM(`no_genre`) AS `no_genre`
FROM `movies`;

-- 2- Returns the most frequent tag used for Sci-Fi movies
SELECT
     g.tag
    ,COUNT(m.movieId) AS tag_frequency
FROM movies AS m
LEFT JOIN (
		SELECT
			 gs.movieId
            ,gt.tag
		FROM genome_scores AS gs
		LEFT JOIN genome_tags AS gt
			ON gt.tagId = gs.tagId
		) AS g
	ON g.movieId = m.movieId
WHERE m.scifi = 1
GROUP BY 1
ORDER BY 2 DESC
LIMIT 1;
-- #################################### END OF DATA QUERYING FOR EXERCISE 3 ##################################
~~~