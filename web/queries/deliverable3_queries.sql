--a) Print the names of the top 10 actors ranked by the average rating of their 3 highest-rated clips that where
--voted by at least 100 people. The actors must have had a role in at least 5 clips (not necessarily rated).
with actors_with_more_than_five_roles as (
    SELECT
      person_id as person_id,
      count(character) as number_of_clips_he_played
    FROM acts
    GROUP BY person_id
    HAVING count(character) >= 5
),
actor_with_avg_rating as (
  SELECT
  actor.*,
  (
    -- gives the average of the top rated clips
    SELECT
      avg(f.rank)
    FROM (
      -- find 3 highest-rated clips
      SELECT
        r.rank
      FROM clip_rating r
      JOIN acts a ON a.clip_id = r.clip_id
      WHERE votes >= 100 AND a.person_id = actor.person_id AND r.rank IS NOT NULL
      ORDER BY r.rank DESC
      FETCH FIRST 3 ROWS ONLY
    )f
  ) as avg_rating
  FROM actors_with_more_than_five_roles actor
)
select
  p.fullname,
  b.number_of_clips_he_played,
  b.avg_rating
FROM actor_with_avg_rating b
  join person p on p.person_id = b.person_id
  where b.avg_rating is not NULL
order by b.avg_rating DESC
fetch first 10 rows ONLY;
;

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
order by b.decade desc;

--c) For any video game director, print the first year he/she directed a game, his/her name and all his/her
-- game titles from that year.
with director_first_year_he_directed as (
  select
    d.person_id as person_id,
    min(extract(year from clip_year)) as first_year
  from directs d
    join clip c on c.clip_id = d.clip_id
  where d.role like '%game%'
  group by d.person_id
)
select
  distinct p.fullname,
  df.first_year,
  c.clip_title
from director_first_year_he_directed df
  join directs d on d.person_id = df.person_id
  join person p on p.person_id = d.person_id
  join clip c on c.clip_id = d.clip_id
where extract(year from c.clip_year ) = df.first_year;
;

--d) For each year, print the title, year and rank-in-year of top 3 clips, based on their ranking.
WITH clip_year_rank_in_year AS (
  select
    C.CLIP_YEAR,
    C.clip_title,
    CR.RANK,
    ROW_NUMBER() OVER(PARTITION BY C.CLIP_YEAR ORDER BY CR.RANK DESC, CR.VOTES DESC) AS rowind
  FROM CLIP C
  JOIN CLIP_RATING CR ON C.CLIP_ID = CR.CLIP_ID
)
SELECT
  extract(YEAR FROM s.CLIP_YEAR) as year,
  s.CLIP_TITLE,
  s.RANK
FROM clip_year_rank_in_year s
WHERE s.rowind <=3 and s.CLIP_YEAR IS NOT NULL
ORDER BY s.clip_year desc;


--e) Print the names of all directors who have also written scripts for clips, in all of which they were
--additionally actors (but not necessarily directors)
-- and every clip they directed has at least two more points in ranking than any clip they wrote.

--join to get directors with their clip_ratings
with directed as (
  select
    distinct p.person_id,
    cr.rank
  from person p
    join directs d on p.person_id = d.person_id
    join clip c on d.clip_id = c.clip_id
    join clip_rating cr on c.clip_id = cr.clip_id
),
wrote as (
  select distinct --join to get writers with their clip_ratings
    p.person_id,
    cr.rank
from person p
  join writes w on p.person_id = w.person_id
  join clip c on w.clip_id = c.clip_id
  join clip_rating cr on c.clip_id = cr.clip_id
)
select
 aw.fullname,
 min(d.rank) as minpoints_directed,
 max(w.rank) as minpoints_written
from (
  select
      distinct --join to get writers who acted in their written clips
      p.person_id,
      p.fullname
  from person p
    join writes w on p.person_id = w.person_id
    join acts a on p.person_id = a.person_id
    join clip c on w.clip_id = c.clip_id and a.clip_id = c.clip_id
  ) as aw
join directed d on d.person_id=aw.person_id --final join of above tables
join wrote w on w.person_id=aw.person_id
group by aw.fullname
having( min(d.rank) >= max(w.rank) +2) --data selection criterion on ranking
order by aw.fullname
;

--f) Print the names of the actors that are not married and have participated in more than 2 clips that they
--both acted in and co-directed it.
with unmarried_person as (
    select
      p.person_id
    from person p
      left join married_to m on m.person_id = p.person_id
    where m.person_id is null
),
acting_codirectors as (
  select
    p.person_id
  from person p
    join acts a on p.person_id = a.person_id
    join directs d on p.person_id = d.person_id
    join clip c on d.clip_id = c.clip_id and a.clip_id = c.clip_id
  where d.role like 'co-director%'
  group by p.person_id
  having count(p.person_id)>2
)
select
  p.fullname
from person p
  join unmarried_person a on a.person_id = p.person_id
  join acting_codirectors d on d.person_id = p.person_id
order by p.fullname;

create index ix_role on directs(role);
create index ix_person_fullname on person(person_id, fullname);
create index ix_married on married_to(person_id);
;
drop index ix_role;
drop index ix_person_fullname;
drop index ix_married;
;

--g) Print the names of screenplay story writers who have worked with more than 2 producers.
with screenplay_writer as (
  select
    distinct w.person_id
  from writes w
 where work_type like '%screenplay story%'
)
select
  person.fullname
from clip c
  join produces p on c.clip_id = p.clip_id
  join writes w on c.clip_id = w.clip_id
  join person person on person.person_id = w.person_id
where w.person_id in ( select * from screenplay_writer )
group by w.person_id, person.fullname
having count(distinct p.person_id) > 2
;

--h) Compute the average rating of an actor's clips (for each actor) when she/he has a leading role (first 3
-- credits in the clip).
with person_leading as (
    select
      DISTINCT aa.person_id,
      fullname,
      orders_credit
    from acts aa
      join clip_rating cr on aa.clip_id = cr.clip_id
      join person p on aa.person_id = p.person_id
      where orders_credit <= 3
)
select
  b.person_id,
  b.fullname,
  (
    Select round(avg(cr.rank), 2)
    from acts a
      join clip_rating cr on a.clip_id = cr.clip_id
      where orders_credit <= 3
            AND b.person_id = a.person_id
  ) as avg_rating
from person_leading b
  order by b.person_id DESC
;

--i) Compute the average rating for the clips whose genre is the most popular genre.
with most_popular_genre as (
  select
    cg.genre_id
  from clip_genre cg
  group by cg.genre_id
  order by count(*)  desc
  fetch first 1 rows only
)
select
  round(avg(cr.rank), 2)
from clip_rating  cr
  join clip_genre cg on cg.clip_id = cr.clip_id
where cg.genre_id = ( select * from most_popular_genre )
;

--j) Print the names of the actors that have participated in more than 100 clips, of which at least 60% where
--short but not comedies nor dramas, and have played in more comedies than double the dramas. Print
--also the number of comedies and dramas each of them participated in.
with actor_more_than_100_clips as (
    select
      a.person_id               as person_id,
      count(distinct a.clip_id) as number_of_clips
    from acts a
    group by a.person_id
    having count(distinct a.clip_id) > 100
),
short_not_comedy_nor_drama as (
    -- clips which are not short but not comedies nor dramas
      select c.clip_id
      from clip c
        join clip_genre cg on c.clip_id = cg.clip_id
        join genre g on cg.genre_id = g.genre_id
      group by c.clip_id
      -- is short but not comedy nor drama
      having array_agg(g.genre) && ARRAY ['Short' :: varchar]
             and not (array_agg(g.genre) && ARRAY ['Comedy' :: varchar])
             and not (array_agg(g.genre) && ARRAY ['Drama' :: varchar])
),
actor_of_interest as (
  select
    a.person_id,
    aiq.number_of_clips,
    count(distinct a.clip_id) as short_not_comedies
  from acts a
    join actor_more_than_100_clips aiq on aiq.person_id = a.person_id
    join short_not_comedy_nor_drama s on a.clip_id = s.clip_id
    join person p on a.person_id = p.person_id
  group by a.person_id, aiq.number_of_clips
  having count(distinct a.clip_id) >= 0.6 * aiq.number_of_clips
)
select
  p.fullname,
  (
    select
      count(*)
    from acts a
      join clip c on a.clip_id = c.clip_id
      join clip_genre cg on c.clip_id = cg.clip_id
      join genre g on cg.genre_id = g.genre_id
    where g.genre = 'Drama' and a.person_id = p.person_id
  ) as nr_drama,
  (
    select
      count(*)
    from acts a
      join clip c on a.clip_id = c.clip_id
      join clip_genre cg on c.clip_id = cg.clip_id
      join genre g on cg.genre_id = g.genre_id
    where g.genre = 'Comedy' and a.person_id = p.person_id
  ) as nr_comedy
from actor_of_interest aoi
  join person p on p.person_id = aoi.person_id
;

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
;

