CREATE TABLE IF NOT EXISTS exp (UserID integer PRIMARY KEY, XP integer DEFAULT 0, Level integer DEFAULT 1);
CREATE TABLE IF NOT EXISTS mutes (UserID integer PRIMARY KEY, RoleIDs text, EndTime text);