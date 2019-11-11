CREATE DATABASE `botlpf` /*!40100 COLLATE 'utf8mb4_general_ci' */
;
USE botlpf
;
CREATE TABLE `posts_full` (
	`titulo` VARCHAR(280) NULL DEFAULT NULL COLLATE 'utf8mb4_spanish_ci',
	`autor` VARCHAR(10) NOT NULL,
	`timestamp` CHAR(25) NOT NULL,
	`url` VARCHAR(280) NOT NULL COLLATE 'utf8mb4_spanish_ci',
	`post` TEXT NOT NULL,
	`etiquetas` VARCHAR(280) NULL DEFAULT NULL COLLATE 'utf8mb4_spanish_ci',
	`comentarios` INT(11) NULL DEFAULT 0,
	`fecha` CHAR(5) NOT NULL,
	`hora` CHAR(5) NOT NULL,
	`ano` CHAR(4) NOT NULL,
	`tags` VARCHAR(280) NULL DEFAULT NULL COLLATE 'utf8mb4_spanish_ci',
	`twitter` VARCHAR(12) NOT NULL COLLATE 'latin1_spanish_ci',
	PRIMARY KEY (`url`)
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
CREATE TABLE `posts_min` (
	`titulo` VARCHAR(280) NULL DEFAULT NULL COLLATE 'utf8mb4_spanish_ci',
	`url` VARCHAR(280) NOT NULL COLLATE 'utf8mb4_spanish_ci',
	`ano` CHAR(4) NOT NULL DEFAULT '',
	`fecha` CHAR(5) NOT NULL DEFAULT '',
	`hora` CHAR(5) NOT NULL DEFAULT '',
	`twitter` VARCHAR(12) NOT NULL DEFAULT '' COLLATE 'latin1_spanish_ci',
	`tags` VARCHAR(280) NULL DEFAULT NULL COLLATE 'utf8mb4_spanish_ci',
	PRIMARY KEY (`url`)
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;
CREATE TABLE `log` (
	`timestamp` CHAR(19) NOT NULL,
	`tweet` VARCHAR(280) NOT NULL DEFAULT 'False'
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;