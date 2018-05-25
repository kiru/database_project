--a) Print the names of the top 10 actors ranked by the average rating of their 3 highest-rated clips that where
--voted by at least 100 people. The actors must have had a role in at least 5 clips (not necessarily rated).



--avg top 3 ratings where voted by at least 100
select avg(d.rank)
from
(
select r.rank
from clip_rating r
  join acts a on a.clip_id = r.clip_id
where a.person_id = 28
order by r.rank desc
fetch first 3 rows only
) d;

-- The actors must have had a role in at least 5 clips
select *
FROM (
  SELECT
    d.*,
    (SELECT avg(f.rank)
     FROM
       (
         SELECT r.rank
         FROM clip_rating r
           JOIN acts a ON a.clip_id = r.clip_id
         WHERE votes >= 100 AND a.person_id = d.person_id AND r.rank IS NOT NULL
         ORDER BY r.rank DESC
         FETCH FIRST 3 ROWS ONLY
       )
       f) as avg_rating
  FROM (
         SELECT
           person_id,
           count(character)
         FROM acts
         GROUP BY person_id
         HAVING count(character) > 4
       ) d
) b where b.avg_rating is not NULL
order by b.avg_rating DESC
fetch first 10 rows ONLY ;

--b) Compute the average rating of the top-100 rated clips per decade in decreasing order.
select avg(d.rank)
FROM (
  SELECT cr.rank
  FROM clip_rating cr
    JOIN clip c ON c.clip_id = cr.clip_id
  WHERE extract(DECADE FROM c.clip_year) * 10 = 2000
  ORDER BY cr.rank DESC
  FETCH FIRST 100 ROWS ONLY
) d;
select
  b.decade,
  (
  select avg(d.rank)
FROM (
  SELECT cr.rank
  FROM clip_rating cr
    JOIN clip c ON c.clip_id = cr.clip_id
  WHERE extract(DECADE FROM c.clip_year) * 10 = b.decade
  ORDER BY cr.rank DESC
  FETCH FIRST 100 ROWS ONLY
) d

  ) as avg_rating
from
  (
    SELECT DISTINCT extract(DECADE FROM clip_year) * 10 as decade
    FROM clip
  ) b

where b.decade is not null
order by avg_rating;



--c) For any video game director, print the first year he/she directed a game, his/her name and all his/her
--game titles from that year.



--d) For each year, print the title, year and rank-in-year of top 3 clips, based on their ranking.
Select
  extract(year from c.clip_year), min(r.rank) as rank
from clip c, clip_rating r
where c.clip_id = r.clip_id
GROUP BY extract(year from c.clip_year)
;

select
  *
from
  ( select distinct extract(year from c.clip_year) as y from clip c ) y,
  (
    select *
    from clip c
    join clip_rating rating on c.clip_id = rating.clip_id
    order by rating.rank desc
    -- FETCH FIRST 3 ROWS ONLY
  ) b
where extract(year from b.clip_year) = y.y
order by y.y desc, b.rank desc
;

    select *
    from clip c
    join clip_rating rating on c.clip_id = rating.clip_id
    ;


-- ORDER BY c.clip_year, rank ASC

--e) Print the names of all directors who have also written scripts for clips, in all of which they were
--additionally actors (but not necessarily directors) and every clip they directed has at least two more
--points in ranking than any clip they wrote.



--f) Print the names of the actors that are not married and have participated in more than 2 clips that they
--both acted in and co-directed it.



--g) Print the names of screenplay story writers who have worked with more than 2 producers.



--h) Compute the average rating of an actor's clips (for each actor) when she/he has a leading role (first 3
--credits in the clip).



--i) Compute the average rating for the clips whose genre is the most popular genre.
-- Select g.


--j) Print the names of the actors that have participated in more than 100 clips, of which at least 60% where
--short but not comedies nor dramas, and have played in more comedies than double the dramas. Print
--also the number of comedies and dramas each of them participated in.



--k) Print the number of Dutch movies whose genre is the second most popular one.
Select cg.genre_id, count(cg.genre_id)
  from clip_country cc
    join country c on cc.country_id = c.country_id
    join clip_genre cg on cc.clip_id = cg.clip_id
  where c.countryname = 'Netherlands'
GROUP BY cg.genre_id
order by count(cg.genre_id) desc
offset 1
fetch first 1 rows only;



--l) Print the name of the producer whose role is coord