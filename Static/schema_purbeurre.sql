SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


DROP DATABASE IF EXISTS `purbeurre` ;
CREATE DATABASE IF NOT EXISTS `purbeurre` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `purbeurre`;


DROP TABLE IF EXISTS `product` ;
CREATE TABLE IF NOT EXISTS `product` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `category` ;
CREATE TABLE IF NOT EXISTS `category` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `store` ;
CREATE TABLE IF NOT EXISTS `store` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `favorite` ;
CREATE TABLE IF NOT EXISTS `favorite` (
  `base_product_id` int(11) NOT NULL,
  `substitute_product_id` int(11) NOT NULL,
  PRIMARY KEY (`base_product_id`,`substitute_product_id`),
  KEY `fk_favorite_product1_idx` (`base_product_id`),
  KEY `fk_favorite_product2_idx` (`substitute_product_id`),
  CONSTRAINT `fk_favorite_product1` FOREIGN KEY (`base_product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_favorite_product2` FOREIGN KEY (`substitute_product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `product_category` ;
CREATE TABLE IF NOT EXISTS `product_category` (
  `product_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`product_id`,`category_id`),
  KEY `fk_product_category_product1_idx` (`product_id`),
  KEY `fk_product_category_category_idx` (`category_id`),
  CONSTRAINT `fk_product_category_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_category_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `product_store` ;
CREATE TABLE IF NOT EXISTS `product_store` (
  `product_id` int(11) NOT NULL,
  `store_id` int(11) NOT NULL,
  PRIMARY KEY (`product_id`,`store_id`),
  KEY `fk_product_store_product1_idx` (`product_id`),
  KEY `fk_product_store_store1_idx` (`store_id`),
  CONSTRAINT `fk_product_store_product1` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_store_store1` FOREIGN KEY (`store_id`) REFERENCES `store` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
