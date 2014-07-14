/* Table USER */
CREATE TABLE IF NOT EXISTS user(
name TEXT PRIMARY KEY,
value TEXT
);

INSERT OR REPLACE INTO user (name, value) VALUES ('aeVersion', '1.1.0');

INSERT OR IGNORE INTO user (name, value) VALUES ('currentGold', '50');
INSERT OR IGNORE INTO user (name, value) VALUES ('totalGold', '50');
INSERT OR IGNORE INTO user (name, value) VALUES ('sqlHash', ' ');
INSERT OR IGNORE INTO user (name, value) VALUES ('installDate', date('now'));

/* Table OPTIONS */
CREATE TABLE IF NOT EXISTS options(
optionID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
deckname TEXT,
option TEXT NOT NULL,
optionDesc TEXT,
value TEXT,
UNIQUE(deckname, option)
);

/* Table CITIES */
CREATE TABLE IF NOT EXISTS cities(
cityID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
city TEXT NOT NULL,
country TEXT NOT NULL,
cityPrice INTEGER,
constructionsNeeded INTEGER,
isCapital INTEGER,
UNIQUE(city, country)
);

/* Table OBJECTS */
CREATE TABLE IF NOT EXISTS objects(
objectID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
name TEXT NOT NULL,
nameOrig TEXT,
cityID INTEGER NOT NULL,
price INTEGER,
rounds INTEGER NOT NULL DEFAULT 0,
state INTEGER,
desc TEXT,
image TEXT,
link TEXT,
FOREIGN KEY(cityID) REFERENCES cities(cityID),
UNIQUE(name, cityID)
);

/* Table RANKS */
CREATE TABLE IF NOT EXISTS ranks(
rankID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
description TEXT NOT NULL,
type INTEGER NOT NULL,
rankLimit INTEGER NOT NULL,
UNIQUE(description, type, rankLimit)
);

/*
 * Insert ranks
 */
DELETE FROM ranks;
 
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Impoverished', 1, 0);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Needy', 1, 1000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Cowardly', 1, 2000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Poor', 1, 3000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Lazy', 1, 5000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Sneaky', 1, 7500);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Hard-working', 1, 10000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Diligent', 1, 12500);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Nifty', 1, 15000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Restless', 1, 20000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Beautiful', 1, 25000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Clever', 1, 30000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Wealthy', 1, 40000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Brave', 1, 50000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Rich', 1, 60000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Great', 1, 70000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Enlightened', 1, 80000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Glorious', 1, 90000);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Magnificent', 1, 100000);

INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Slave', 2, 0);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Thief', 2, 5);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Novice', 2, 10);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Squire', 2, 15);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Scout', 2, 20);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Bureaucrat', 2, 25);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Treasurer', 2, 30);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Explorer', 2, 35);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Monk', 2, 40);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Chieftain', 2, 45);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Baron', 2, 50);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Knight', 2, 55);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Commander', 2, 60);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Sovereign', 2, 65);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Prince', 2, 70);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('General', 2, 75);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Shogun', 2, 80);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Prime minister', 2, 85);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('President', 2, 90);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('King', 2, 95);
INSERT OR IGNORE INTO ranks (description, type, rankLimit) VALUES ('Emperor', 2, 100);


/* Table STATS */
CREATE TABLE IF NOT EXISTS stats(
statsID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
statsDay DATE NOT NULL,
cardsAnswered INTEGER NOT NULL
);