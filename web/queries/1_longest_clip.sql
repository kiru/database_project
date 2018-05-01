-- Name: Longest clip

-- select * from (
  SELECT
    C.CLIP_ID,
    C.CLIP_TITLE as Title,
    sum(R.RUNNING_TIME) as Time
  FROM CLIP c
    JOIN CLIP_COUNTRY cc ON cc.CLIP_ID = c.CLIP_ID
    JOIN COUNTRY C2 ON cc.COUNTRY_ID = C2.COUNTRY_ID
    JOIN RUNS R ON c.CLIP_ID = R.CLIP_ID
  WHERE C2.COUNTRYNAME = 'France'
  GROUP BY c.CLIP_ID, c.CLIP_TITLE
-- ) where ROWNUM  < 10
