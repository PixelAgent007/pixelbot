CREATE TABLE IF NOT EXISTS exp (GuildID BIGINT PRIMARY KEY, UserID BIGINT, CurXP integer DEFAULT 0, XP integer DEFAULT 0, Level integer DEFAULT 1);
CREATE TABLE IF NOT EXISTS mutes (GuildID BIGINT PRIMARY KEY, UserID BIGINT, EndTime text);
CREATE TABLE IF NOT EXISTS suggestionSettings (GuildID BIGINT PRIMARY KEY, isEnabled text, outputChannel BIGINT, tmpID int);
CREATE TABLE IF NOT EXISTS levelingSettings (GuildID BIGINT PRIMARY KEY, isEnabled text, Lvl5Role BIGINT, Lvl10Role BIGINT, Lvl15Role BIGINT, Lvl20Role BIGINT, Lvl35Role BIGINT, Lvl50Role BIGINT, Lvl75Role BIGINT, Lvl100Role BIGINT);
CREATE TABLE IF NOT EXISTS globalSettings (Prefix text, Token text);