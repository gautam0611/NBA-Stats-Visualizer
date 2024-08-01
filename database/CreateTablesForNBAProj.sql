-- create database NBA_Stats;

USE NBA_STATS;

CREATE TABLE Conference (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255)	
);

CREATE TABLE Division (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    FOREIGN KEY (id) references Conference(id)
);

CREATE TABLE Team (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    FOREIGN KEY (id) references Division(id)
);

CREATE TABLE Season (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    FOREIGN KEY (id) references Team(id)
);

CREATE TABLE Roster (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    FOREIGN KEY (id) references Season(id)
);

CREATE TABLE Games (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    FOREIGN KEY (id) references Season(id)
);

CREATE TABLE Record (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    FOREIGN KEY (id) references Season(id)
);

Create Table Player (
	id INTEGER AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    points DECIMAL(10,2),
    assists DECIMAL(10,2),
    rebounds DECIMAL(10,2),
    FOREIGN KEY (id) references Roster(id)
);











