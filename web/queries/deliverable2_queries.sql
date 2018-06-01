-- Print the name and length of the 10 longest clips that were released in France
SELECT
  C.CLIP_ID,
  C.CLIP_TITLE,
  max(R.RUNNING_TIME) AS runtime
FROM CLIP c
  JOIN RUNS R ON c.CLIP_ID = R.CLIP_ID
  JOIN COUNTRY C2 ON r.COUNTRY_ID = C2.COUNTRY_ID
WHERE C2.COUNTRYNAME = 'France'
GROUP BY c.CLIP_ID, c.CLIP_TITLE
ORDER BY runtime DESC, c.CLIP_ID, C.CLIP_TITLE
FETCH FIRST 10 ROWS ONLY;

-- Compute the number of clips released per country in 2001
SELECT
  c2.COUNTRYNAME,
  count(*) AS nb_of_clips
FROM CLIP c
  JOIN RELEASED R ON c.CLIP_ID = R.CLIP_ID
  JOIN COUNTRY C2 ON R.COUNTRY_ID = C2.COUNTRY_ID
WHERE extract(YEAR FROM r.RELEASE_DATE) = 2001
GROUP BY c2.COUNTRYNAME
ORDER BY c2.COUNTRYNAME;
-- Compute the numbers of clips per genre released in the USA after 2013.

SELECT
  G.GENRE,
  count(*) AS nb_of_clips
FROM CLIP c
  JOIN CLIP_GENRE CG ON CG.CLIP_ID = C.CLIP_ID
  JOIN RELEASED R ON c.CLIP_ID = R.CLIP_ID
  JOIN COUNTRY C2 ON R.COUNTRY_ID = C2.COUNTRY_ID
  JOIN GENRE G ON CG.GENRE_ID = G.GENRE_ID
WHERE extract(YEAR FROM r.RELEASE_DATE) > 2013
      AND C2.COUNTRYNAME = 'USA'
GROUP BY G.GENRE
ORDER BY g.GENRE;

-- Print the name of actor/actress who has acted in more clips than anyone else


SELECT d.FULLNAME
FROM
  (SELECT
     P.FULLNAME,
     count(*) AS nb_acts
   FROM PERSON P
     JOIN ACTS A2 ON P.PERSON_ID = A2.PERSON_ID
   GROUP BY P.person_id
   ORDER BY nb_acts DESC
   FETCH FIRST 1 ROW ONLY
  ) d;

-- Print the maximum number of clips any director has directed.

  SELECT
    P.FULLNAME,
    count(*) AS nb_acts
  FROM PERSON P
    JOIN DIRECTS D2 ON P.PERSON_ID = D2.PERSON_ID
    JOIN CLIP C2 ON D2.CLIP_ID = C2.CLIP_ID
  GROUP BY P.FULLNAME
  ORDER BY nb_acts DESC
  FETCH FIRST 1 ROWS ONLY;

-- Print the names of people that had at least 2 different jobs in a single clip. For example, if X has both
-- acted, directed and written movie Y, his/her name should be printed out. On the other hand, if X has
-- acted as 4 different personas in the same clip, but done nothing else, he/she should not be printed.
;
SELECT d.FULLNAME
FROM (
       SELECT
         c.CLIP_ID,
         P.PERSON_ID,
         p.fullname,
         count(a.CLIP_ID) AS acts,
         count(d.CLIP_ID) AS directs,
         count(w.CLIP_ID) AS writes,
         count(pr.CLIP_ID) as produces
       FROM CLIP C, PERSON P
         LEFT JOIN ACTS a ON a.PERSON_ID = p.PERSON_ID
         LEFT JOIN DIRECTS d ON d.PERSON_ID = p.PERSON_ID
         LEFT JOIN WRITES w ON w.PERSON_ID = p.PERSON_ID
         LEFT JOIN produces pr ON pr.person_id = P.person_id
       WHERE
         a.CLIP_ID = c.CLIP_ID AND
         d.CLIP_ID = c.CLIP_ID AND
         w.CLIP_ID = c.CLIP_ID AND
          pr.clip_id = c.clip_id
       GROUP BY C.CLIP_ID, P.PERSON_ID
       HAVING ((count(a.CLIP_ID) > 0 AND count(d.CLIP_ID) > 0) OR
              (count(d.CLIP_ID) > 0 AND count(w.CLIP_ID) > 0) OR
              (count(a.CLIP_ID) > 0 AND count(w.CLIP_ID) > 0) OR
              (count(a.clip_id) > 0 and count(pr.clip_id) > 0) OR
              (count(d.clip_id) > 0 and count(pr.clip_id) > 0) OR
              (count(w.clip_id) > 0 and count(pr.clip_id) > 0)
     ) )d;

-- Print the 10 most common clip languages

SELECT L.LANGUAGE
FROM CLIP_LANGUAGE
  JOIN LANGUAGE L ON CLIP_LANGUAGE.LANGUAGE_ID = L.LANGUAGE_ID
GROUP BY L.LANGUAGE
ORDER BY count(*) DESC
FETCH FIRST 10 ROWS ONLY;
-- Print the full name of the actor who has performed in the highest number of clips with a user-specified type.
SELECT p.FULLNAME
FROM (
       SELECT
         a.PERSON_ID,
         count(*) AS count
       FROM ACTS A
         JOIN CLIP C2 ON A.CLIP_ID = C2.CLIP_ID
       WHERE C2.CLIP_TYPE = 'V'
       GROUP BY a.PERSON_ID
     ) b
  JOIN PERSON p ON p.PERSON_ID = b.PERSON_ID
ORDER BY b.count DESC
FETCH FIRST 1 ROWS ONLY;

SELECT *
FROM COUNTRY;
