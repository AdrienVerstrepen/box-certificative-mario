CREATE TABLE IF NOT EXISTS AppUser
(
    UserID SERIAL  PRIMARY KEY NOT NULL,
    Username VARCHAR(100) unique,
    Email VARCHAR(255) unique,
	UserPassword VARCHAR(255),
	UserRoles VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Tour
(
    TourID SERIAL  PRIMARY KEY NOT NULL  ,
    TourName VARCHAR(100),
    Visibility bool,
	UserID int, 
	TourLenght float,
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
INSERT INTO AppUser (UserID, Username, Email, UserPassword, UserRoles)
VALUES
(1, 'adrien', 'adrien@mail.com', 'scrypt:32768:8:1$lEFfO0NfW3ZCJgtH$5f8d1e8b515935ef2f10cbf455446b9dbae775d1691f1fe337335370a6b409bacaeb9b97371a88e1248e5ebd6ac40f77ace42f2e699ec91ddcd1c20cf4827382', 'USER'),
(2, 'athene', 'athene@mail.com', 'scrypt:32768:8:1$iDeQyzerXMPBIwHC$35913694a1678bdeb03a3323b9a6e6ba2ad52f963362ebb257033b6b37247abc76e49e2dd7657ef96fb8a099ef2b1c228843200fedf9ba67f8a56459f312ef50', 'USER'),
(3, 'mathys', 'mathys@mail.com', 'scrypt:32768:8:1$bV1JUHqL7ksVV4RT$d4659ffd26c50e4c64a0b221ced18360b57e0213c9c1cd23adfd1d3cd5a4b185a70acec1120e6b49d10bddb4ad69e73efc0b10061c48e199d7017553e1d9755e', 'ADMIN');

-- PLACES
INSERT INTO Place (PlaceID, PlaceName, latitude, longitude, country)
VALUES
(1, 'Paris', 48.8566, 2.3522, 'France'),
(2, 'Berlin', 52.5200, 13.4050, 'Germany'),
(3, 'Rome', 41.9028, 12.4964, 'Italy'),
(4, 'Madrid', 40.4168, -3.7038, 'Spain'),
(5, 'Lisbon', 38.7223, -9.1393, 'Portugal'),
(6, 'Amsterdam', 52.3676, 4.9041, 'Netherlands'),
(7, 'Vienna', 48.2082, 16.3738, 'Austria'),
(8, 'Prague', 50.0755, 14.4378, 'Czech Republic'),
(9, 'Budapest', 47.4979, 19.0402, 'Hungary');

-- TOURS
INSERT INTO Tour (TourID, TourName, Visibility, UserID, TourLenght)
VALUES
(1, 'adrien 1', true, 1, 1250.5),
(2, 'adrien 2', false, 1, 540.2),

(3, 'athene 1', true, 2, 3200.8),
(4, 'athene 2', false, 2, 890.4),

(5, 'mathys 1', true, 3, 1780.0),
(6, 'mathys 2', false, 3, 760.6);

-- STAGES
INSERT INTO Stage (PlaceID, TourID, StepNumber, ClusterNumber, HotelNumber)
VALUES

-- TOUR 1
(1, 1, 1, 1, 2),
(2, 1, 2, 1, 2),
(3, 1, 3, 2, 4),
(4, 1, 4, 2, 4),

-- TOUR 2
(5, 2, 1, 1, 6),
(6, 2, 2, 1, 6),
(7, 2, 3, 2, 8),
(8, 2, 4, 2, 8),

-- TOUR 3
(2, 3, 1, 1, 3),
(3, 3, 2, 1, 3),
(4, 3, 3, 2, 5),
(5, 3, 4, 2, 5),

-- TOUR 4
(6, 4, 1, 1, 7),
(7, 4, 2, 1, 7),
(8, 4, 3, 2, 9),
(9, 4, 4, 2, 9),

-- TOUR 5
(1, 5, 1, 1, 3),
(3, 5, 2, 1, 3),
(5, 5, 3, 2, 7),
(7, 5, 4, 2, 7),

-- TOUR 6
(2, 6, 1, 1, 4),
(4, 6, 2, 1, 4),
(6, 6, 3, 2, 8),
(8, 6, 4, 2, 8);