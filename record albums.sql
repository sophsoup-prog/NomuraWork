.read data.sql

-- Question 2
CREATE TABLE pricing AS
  SELECT name,unitPrice
  FROM tracks;


-- Question 3
CREATE TABLE long AS
  SELECT name
  FROM tracks
  WHERE milliseconds > 480000;


-- Question 4
CREATE TABLE largest AS
  SELECT name,milliseconds
  FROM tracks
  ORDER BY milliseconds DESC
  LIMIT 1;


-- Question 5
CREATE TABLE long_album AS
  SELECT a.title
  FROM albums as a
  JOIN tracks as t ON a.albumId = t.albumId
  WHERE t.milliseconds > 480000;

-- Question 6
CREATE TABLE track_count AS
  SELECT albumId, COUNT(*) as count
  FROM tracks
  GROUP BY albumId;


-- Question 7
CREATE TABLE album_count AS
  SELECT a.name, COUNT(DISTINCT b.albumID) as count
  FROM artists as a
  JOIN albums as b ON a.artistID = b.artistID
  GROUP BY a.name,b.artistID;


-- Question 8
CREATE TABLE busiest_artists AS
  SELECT a.name, COUNT(c.trackID) as count
  FROM artists as a
  JOIN albums as b ON a.artistID = b.artistID
  JOIN tracks as c on b.albumId = c.albumId
  GROUP BY a.artistID, a.name;
