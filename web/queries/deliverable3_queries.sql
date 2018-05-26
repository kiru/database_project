--a) Print the names of the top 10 actors ranked by the average rating of their 3 highest-rated clips that where
--voted by at least 100 people. The actors must have had a role in at least 5 clips (not necessarily rated).

-- The actors must have had a role in at least 5 clips
select
  *
FROM (
  SELECT
    d.*,
    (
      SELECT
        avg(f.rank)
      FROM (
        SELECT
          r.rank
        FROM clip_rating r
        JOIN acts a ON a.clip_id = r.clip_id
        WHERE votes >= 100 AND a.person_id = d.person_id AND r.rank IS NOT NULL
        ORDER BY r.rank DESC
        FETCH FIRST 3 ROWS ONLY
      )f
    ) as avg_rating
  FROM (
      SELECT
        person_id,
        count(character)
      FROM acts
      GROUP BY person_id
      HAVING count(character) >= 5
      ) d
) b
where b.avg_rating is not NULL
order by b.avg_rating DESC
fetch first 10 rows ONLY ;

--b) Compute the average rating of the top-100 rated clips per decade in decreasing order.
select
  b.decade,
  (
    select
      avg(d.rank)
    FROM (
      SELECT cr.rank
      FROM clip_rating cr
      JOIN clip c ON c.clip_id = cr.clip_id
      WHERE extract(DECADE FROM c.clip_year) * 10 = b.decade
      ORDER BY cr.rank DESC
      FETCH FIRST 100 ROWS ONLY
    ) d
  ) as avg_rating
from (
    SELECT
      DISTINCT extract(DECADE FROM clip_year) * 10 as decade
    FROM clip
) b
where b.decade is not null
order by avg_rating;

--c) For any video game director, print the first year he/she directed a game, his/her name and all his/her
-- game titles from that year.
select
  *
from (
  select
    p.fullname,
    c.clip_id,
    c.clip_title,
    (
      select
        extract(year from min(r.release_date))
      from released r
      where r.clip_id = d.clip_id
    ) as first_year
  From directs d
    join person p on d.person_id = p.person_id
    join clip c on d.clip_id = c.clip_id
  where d.role like 'game director:%'
) x
-- only keep the one from the same year
where x.first_year in (
  select
    extract(year from r.release_date)
  from released r
  where r.clip_id = x.clip_id
)
;

--d) For each year, print the title, year and rank-in-year of top 3 clips, based on their ranking.
-- TODO

--e) Print the names of all directors who have also written scripts for clips, in all of which they were
--additionally actors (but not necessarily directors) and every clip they directed has at least two more
--points in ranking than any clip they wrote.
-- TODO

--f) Print the names of the actors that are not married and have participated in more than 2 clips that they
--both acted in and co-directed it.
-- TODO

--g) Print the names of screenplay story writers who have worked with more than 2 producers.
-- TODO
select
  distinct role
from writes ;


--h) Compute the average rating of an actor's clips (for each actor) when she/he has a leading role (first 3
-- credits in the clip).
-- TODO: we cannot do this, since we loose the information of the order of the credit.

--i) Compute the average rating for the clips whose genre is the most popular genre.
-- Select g.
select
  round(avg(cr.rank), 2)
from clip_rating  cr
  join clip_genre cg on cg.clip_id = cr.clip_id
where cg.genre_id = (
  select
    cg.genre_id
  from clip_genre cg
  group by cg.genre_id
  order by count(*)  desc
  fetch first 1 rows only
)
;

--j) Print the names of the actors that have participated in more than 100 clips, of which at least 60% where
--short but not comedies nor dramas, and have played in more comedies than double the dramas. Print
--also the number of comedies and dramas each of them participated in.

-- TODO

--k) Print the number of Dutch movies whose genre is the second most popular one.
Select
  cg.genre_id,
  count(cg.genre_id)
from clip_country cc
    join country c on cc.country_id = c.country_id
    join clip_genre cg on cc.clip_id = cg.clip_id
where c.countryname = 'Netherlands'
GROUP BY cg.genre_id
order by count(cg.genre_id) desc
offset 1
fetch first 1 rows only;


--l) Print the name of the producer whose role is coord
select
  distinct p.fullname
From produces
join person p on produces.person_id = p.person_id
where role like 'coordinating producer: %'
order by p.fullname;
