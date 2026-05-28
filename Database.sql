CREATE TABLE IF NOT EXISTS AppUser
(
    UserID INT PRIMARY KEY NOT NULL,
    Username VARCHAR(100) unique,
    Email VARCHAR(255),
	UserPassword VARCHAR(100),
	UserRoles VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Tour
(
    TourID INT PRIMARY KEY NOT NULL,
    TourName VARCHAR(100),
    Visibility bool,
	UserID int, 
	FOREIGN KEY (UserID) REFERENCES AppUser(UserID)
);

CREATE TABLE IF NOT EXISTS Place
(
    PlaceID INT PRIMARY KEY NOT NULL,
    PlaceName VARCHAR(100),
    latitude float,
	longitude float,
	country Varchar(100)
);

CREATE TABLE IF NOT EXISTS Stage
(
    PlaceID INT,
    TourID Int,
    StepNumber Int,
	primary key (PlaceID, TourID),
	foreign key (PlaceID) references Place(PlaceId),
	foreign key (TourID) references Tour(TourId)
);

-- USERS
INSERT INTO AppUser (UserID, Username, Email, UserPassword, UserRoles)
VALUES
(1, 'alice', 'alice@mail.com', 'pass123', 'USER'),
(2, 'bob', 'bob@mail.com', 'secret456', 'ADMIN'),
(3, 'charlie', 'charlie@mail.com', 'qwerty', 'USER');

-- TOURS
INSERT INTO Tour (TourID, TourName, Visibility, UserID)
VALUES
(1, 'European Capitals', true, 1),
(2, 'French Castles', false, 2),
(3, 'Asian Adventure', true, 1);

-- PLACES
INSERT INTO Place (PlaceID, PlaceName, latitude, longitude, country)
VALUES
(1, 'Paris', 48.8566, 2.3522, 'France'),
(2, 'Berlin', 52.5200, 13.4050, 'Germany'),
(3, 'Tokyo', 35.6762, 139.6503, 'Japan'),
(4, 'Versailles', 48.8049, 2.1204, 'France'),
(5, 'Kyoto', 35.0116, 135.7681, 'Japan');

-- STAGES
INSERT INTO Stage (PlaceID, TourID, StepNumber)
VALUES
(1, 1, 1),
(2, 1, 2),

(4, 2, 1),

(3, 3, 1),
(5, 3, 2);