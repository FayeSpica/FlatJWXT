/*create database test;*/
use test;
/*用户*/
create table users(
  id INT NOT NULL AUTO_INCREMENT,
  email VARCHAR(100) NOT NULL,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(100) NOT NULL,
  head_img VARCHAR(200),
  reg_date DATETIME NOT NULL,
  latest_time DATETIME,
  type INTEGER NOT NULL,
  state INTEGER NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username)
)engine=innodb default CHARSET=utf8;