use NBA_Stats;

-- Get the specified conference 
select * from Conference; 

-- get all from the specified division
select * from Division where conference_id = 1;

-- Get all the teams from the specified conference
select * from Team t join Conference c on (t.conference_id=c.id) where c.name like '%east%';
select * from Team t join Conference c on (t.conference_id=c.id) where c.name like '%west%'; 

-- Get a team from a specific conference
select * from Team t where t.name like '%team%';

-- Gets the record for the specified team in a specified season 
select * from Team t join Season s on (t.id=s.team_id) join Record r on (s.id=r.record_season_id); 
 
-- Gets the games for the specified team in a specified season 
select * from Team t join Season s on (t.id=s.team_id) join Games g on (s.id=r.games_season_id); 


-- ALTER TABLE Season DROP FOREIGN KEY team_id;
-- ALTER TABLE Record DROP FOREIGN KEY record_ibfk_2;
-- ALTER TABLE Record ADD COLUMN season_id INTEGER;
-- ALTER TABLE Record ADD COLUMN team_id INTEGER;
-- Alter Table Record ADD CONSTRAINT fk_record_season_id FOREIGN KEY (season_id) REFERENCES Season(id);
-- Alter Table Record ADD CONSTRAINT fk_record_team_id FOREIGN KEY (team_id) REFERENCES Team(id);

-- alter table Season drop column team_id;

-- DROP TABLE GAMES;