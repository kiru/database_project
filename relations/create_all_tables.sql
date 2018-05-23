CREATE TABLE Person
(
  person_id INTEGER,
  fullname  VARCHAR(1024),
  PRIMARY KEY (person_id)
);
create index ix_person on person(fullname);

CREATE TABLE Clip
(
  clip_id    INTEGER,
  clip_type  VARCHAR(20),
  clip_year  DATE,
  clip_title VARCHAR(1024),
  PRIMARY KEY (clip_id)
);

CREATE TABLE Directs
(
  person_id       INTEGER,
  clip_id         INTEGER,
  additional_info VARCHAR(1024),
  role            VARCHAR(1024),
  PRIMARY KEY (person_id, clip_id, role),
  FOREIGN KEY (person_id) REFERENCES Person (person_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id)
);

CREATE TABLE Acts
(
  person_id       INTEGER,
  clip_id         INTEGER,
  additional_info VARCHAR(1024),
  orders_credit   VARCHAR(20),
  character       VARCHAR(1024),
  PRIMARY KEY (person_id, clip_id, character),
  FOREIGN KEY (person_id) REFERENCES Person (person_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id)
);


CREATE TABLE Produces
(
  person_id       INTEGER,
  clip_id         INTEGER,
  additional_info VARCHAR(300),
  role            VARCHAR(200),
  PRIMARY KEY (person_id, clip_id, role),
  FOREIGN KEY (person_id) REFERENCES Person (person_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id)
);

CREATE TABLE Writes
(
  person_id       INTEGER,
  clip_id         INTEGER,
  additional_info VARCHAR(400),
  work_type       VARCHAR(50),
  role            VARCHAR(100),
  PRIMARY KEY (person_id, clip_id, role),
  FOREIGN KEY (person_id) REFERENCES Person (person_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id)
);

CREATE TABLE ClipLinks
(
  -- we cannot use clip_from_id and clip_to_id as PK, since it's not unique
  cliplink_id  INTEGER,
  clip_from_id INTEGER,
  clip_to_id   INTEGER,
  link_type    VARCHAR(255),
  PRIMARY KEY (cliplink_id),
  FOREIGN KEY (clip_from_id) REFERENCES Clip (clip_id),
  FOREIGN KEY (clip_to_id) REFERENCES Clip (clip_id)
);

CREATE TABLE Country
(
  country_id  INTEGER,
  countryname VARCHAR(100),
  PRIMARY KEY (country_id),
  constraint ux_country unique (countryname)
);

CREATE TABLE Genre
(
  genre_id INTEGER,
  genre    VARCHAR(20),
  PRIMARY KEY (genre_id),
  constraint ux_genre unique (genre)
);

CREATE TABLE Language
(
  language_id INTEGER,
  language    VARCHAR(70),
  PRIMARY KEY (language_id),
  constraint ux_language unique (language)
);

CREATE TABLE Clip_country
(
  clip_id    INTEGER,
  country_id INTEGER,
  PRIMARY KEY (clip_id, country_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id),
  FOREIGN KEY (country_id) REFERENCES Country (country_id)
);

CREATE TABLE Clip_genre
(
  clip_id  INTEGER,
  genre_id INTEGER,
  PRIMARY KEY (clip_id, genre_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id),
  FOREIGN KEY (genre_id) REFERENCES Genre (genre_id)
);

CREATE TABLE Clip_language
(
  clip_id     INTEGER,
  language_id INTEGER,
  PRIMARY KEY (clip_id, language_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id),
  FOREIGN KEY (language_id) REFERENCES Language (language_id)
);

CREATE TABLE Clip_rating
(
  clip_id   INTEGER NOT NULL,
  rating_id INTEGER,
  rank      NUMBER(10),
  votes     NUMBER(10),
  PRIMARY KEY (rating_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id)
    ON DELETE CASCADE
);

CREATE TABLE Released
(
  clip_id      INTEGER,
  country_id   INTEGER,
  release_date DATE,
  PRIMARY KEY (clip_id, country_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id),
  FOREIGN KEY (country_id) REFERENCES Country (country_id)
);

CREATE TABLE Runs
(
  clip_id      INTEGER,
  country_id   INTEGER,
  running_time NUMBER(10),
  PRIMARY KEY (clip_id, country_id),
  FOREIGN KEY (clip_id) REFERENCES Clip (clip_id),
  FOREIGN KEY (country_id) REFERENCES Country (country_id)
);

CREATE TABLE Biography
(
  biography_id      INTEGER,
  name              VARCHAR(20),
  realname          VARCHAR(20),
  nickname          VARCHAR(20),
  birth_date        DATE,
  birth_place       VARCHAR(20),
  height            VARCHAR(20),
  biography         VARCHAR(400),
  biographer        VARCHAR(20),
  death_date        DATE,
  death_place       VARCHAR(20),
  trivia            VARCHAR(200),
  biographicalbooks VARCHAR(100),
  personalquotes    VARCHAR(200),
  salary            VARCHAR(20),
  trademark         VARCHAR(20),
  wherenow          VARCHAR(200),
  person_id         INTEGER NOT NULL,
  FOREIGN KEY (person_id) REFERENCES Person (person_id)
    ON DELETE CASCADE,
  PRIMARY KEY (biography_id)
);

CREATE TABLE BiographicalBooks
(
  book_id      INTEGER,
  title        VARCHAR(100),
  biography_id INTEGER NOT NULL,
  FOREIGN KEY (biography_id) REFERENCES Biography (biography_id),
  PRIMARY KEY (book_id)
);

CREATE TABLE Married_to
(
  married_id   INTEGER NOT NULL,
  biography_id INTEGER NOT NULL,
  person_id    INTEGER NOT NULL,
  marrie_date  VARCHAR(50),
  state        VARCHAR(20),
  children     VARCHAR(20),
  PRIMARY KEY (married_id),
  FOREIGN KEY (biography_id) REFERENCES Biography (biography_id),
  FOREIGN KEY (person_id) REFERENCES person (person_id)
);

