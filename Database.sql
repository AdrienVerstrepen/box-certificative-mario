CREATE TABLE AppUser
(
    UserID INT PRIMARY KEY NOT NULL,
    Username VARCHAR(100) unique,
    Email VARCHAR(255),
	UserPassword VARCHAR(100),
	UserRoles VARCHAR(100)
);

CREATE TABLE Tour
(
    TourID INT PRIMARY KEY NOT NULL,
    TourName VARCHAR(100),
    Visibility bool,
	UserID int, 
	FOREIGN KEY (UserID) REFERENCES AppUser(UserID)
);

CREATE TABLE Place
(
    PlaceID INT PRIMARY KEY NOT NULL,
    PlaceName VARCHAR(100),
    latitude float,
	longitude float,
	country Varchar(100)
);

CREATE TABLE Stage
(
    PlaceID INT,
    TourID Int,
    StepNumber Int,
	primary key (PlaceID, TourID),
	foreign key (PlaceID) references Place(PlaceId),
	foreign key (TourID) references Tour(TourId)
);