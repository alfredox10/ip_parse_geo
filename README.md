1. Install Python dependencies:
```
sudo apt-get install python2.7-mysqldb
sudo pip install https://pypi.python.org/packages/source/P/PrettyTable/prettytable-0.7.2.tar.bz2
```


2. Create a MySQL db and user:
db name: ip2location
user: client
password: simple
access rights: SELECT for SCHEMA ip2location


3. Create db table:
```
CREATE TABLE `ip2location_db5`(
	`ip_from` INT(10) UNSIGNED,
	`ip_to` INT(10) UNSIGNED,
	`country_code` CHAR(2),
	`country_name` VARCHAR(64),
	`region_name` VARCHAR(128),
	`city_name` VARCHAR(128),
	`latitude` DOUBLE,
	`longitude` DOUBLE,
	INDEX `idx_ip_from` (`ip_from`),
	INDEX `idx_ip_to` (`ip_to`),
	INDEX `idx_ip_from_to` (`ip_from`, `ip_to`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
```


4. Download CSV file:
https://www.dropbox.com/s/icfzo14t8baq7gb/IP2LOCATION-LITE-DB5.CSV.ZIP?dl=0


5. Load data to db table:
```
LOAD DATA LOCAL
	INFILE 'FULL/PATH/TO/FILE/IP2LOCATION-LITE-DB5.CSV'
INTO TABLE
	`ip2location_db5`
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 0 LINES;
```

6. Run main.py
