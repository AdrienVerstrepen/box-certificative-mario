CREATE TABLE IF NOT EXISTS AppUser
(
    UserID SERIAL  PRIMARY KEY NOT NULL,
    Username VARCHAR(100) unique,
    Email VARCHAR(255) unique,
	UserPassword VARCHAR(100),
	UserRoles VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Tour
(
    TourID SERIAL  PRIMARY KEY NOT NULL  ,
    TourName VARCHAR(100),
    Visibility bool,
	UserID int, 
	FOREIGN KEY (UserID) REFERENCES AppUser(UserID)
);

CREATE TABLE IF NOT EXISTS Place
(
    PlaceID SERIAL  PRIMARY KEY NOT NULL,
    PlaceName VARCHAR(100),
    latitude float,
	longitude float,
	country Varchar(100)
);

create TABLE IF NOT EXISTS Stage
(
    PlaceID INT,
    TourID Int,
    StepNumber Int,
	ClusterNumber Int,
	HotelNumber Int,
	primary key (PlaceID, TourID),
	foreign key (PlaceID) references Place(PlaceId),
	foreign key (TourID) references Tour(TourId),
	foreign key (HotelNumber) references Place(PlaceId)
);

-- USERS
INSERT INTO AppUser (Username, Email, UserPassword, UserRoles)
VALUES
('alice', 'alice@mail.com', 'pass123', 'USER'),
('bob', 'bob@mail.com', 'secret456', 'ADMIN'),
('charlie', 'charlie@mail.com', 'qwerty', 'USER');

-- TOURS
INSERT INTO Tour (TourName, Visibility, UserID)
VALUES
('European Capitals', true, 1),
('French Castles', false, 2),
('Asian Adventure', true, 1);

-- PLACES
INSERT INTO Place (PlaceName, latitude, longitude, country)
VALUES
('Paris', 48.8566, 2.3522, 'France'),
('Berlin', 52.5200, 13.4050, 'Germany'),
('Tokyo', 35.6762, 139.6503, 'Japan'),
('Versailles', 48.8049, 2.1204, 'France'),
('Kyoto', 35.0116, 135.7681, 'Japan');

-- STAGES
INSERT INTO Stage (PlaceID, TourID, StepNumber)
VALUES
(1, 1, 1),
(2, 1, 2),

(4, 2, 1),

(3, 3, 1),
(5, 3, 2);
