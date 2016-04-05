##Description
#####Program that will read a given set of IPs and perform Geo IP look ups by accepting a query to filter results in python.
### Objectives
##### * Create a language and algorithm for filtering
##### * Reading, parsing, and extracting IP addresses from unstructured text in an efficient manner
### Technical
##### * The filter should implement a generic query language that can be passed abstract parameters
##### * The main function should read the attached file with 5k IP addresses with words mixed in and parse out ips
  
.  

####1 - Install Python dependencies:
```
sudo apt-get install python2.7-mysqldb
sudo pip install https://pypi.python.org/packages/source/P/PrettyTable/prettytable-0.7.2.tar.bz2
```


####2 - Create a MySQL db and user:
```
db name: ip2location
user: client
password: simple
access rights: SELECT for SCHEMA ip2location
```


####3 - Create db table:
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


####4 - Download CSV file:
>https://www.dropbox.com/s/icfzo14t8baq7gb/IP2LOCATION-LITE-DB5.CSV.ZIP?dl=0


####5 - Load data to db table:
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

####6 - Run main.py
