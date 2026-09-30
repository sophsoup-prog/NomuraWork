.read data.sql

-- Q2
CREATE TABLE obedience as
  SELECT seven, gerald
  FROM students;


-- Q3
CREATE TABLE blue_dog as
  SELECT color, pet
  FROM students
  WHERE color='blue' AND pet='dog';  


-- Q4
CREATE TABLE smallest_int as
  SELECT time,smallest
  FROM students
  WHERE smallest >3
  ORDER BY smallest
  LIMIT 20;


-- Q5
CREATE TABLE sevens as
  SELECT s.seven
  FROM students s
  JOIN checkboxes c ON s.number = c.`7`
  WHERE s.number = '7' AND c.'7' = "True";



-- Q7
CREATE TABLE smallest_int_count as
  SELECT smallest, COUNT(*) as count
  FROM students
  WHERE smallest >=1
  GROUP BY smallest;