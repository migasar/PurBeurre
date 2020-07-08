SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


DROP DATABASE IF EXISTS `purbeurre` ;
CREATE DATABASE IF NOT EXISTS `purbeurre` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `purbeurre`;


DROP TABLE IF EXISTS `product` ;
CREATE TABLE IF NOT EXISTS `product` (
  `prod_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  `nutriscore` int(11) DEFAULT NULL,
  `url` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`prod_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `category` ;
CREATE TABLE IF NOT EXISTS `category` (
  `cat_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `store` ;
CREATE TABLE IF NOT EXISTS `store` (
  `shop_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`shop_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `favorite_product` ;
CREATE TABLE IF NOT EXISTS `favorite_product` (
  `base_product_id` int(11) NOT NULL,
  `substitute_product_id` int(11) NOT NULL,
  PRIMARY KEY (`base_product_id`,`substitute_product_id`),
  KEY `fk_favorite_product1_idx` (`base_product_id`),
  KEY `fk_favorite_product2_idx` (`substitute_product_id`),
  CONSTRAINT `fk_favorite_product1` FOREIGN KEY (`base_product_id`) REFERENCES `product` (`prod_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_favorite_product2` FOREIGN KEY (`substitute_product_id`) REFERENCES `product` (`prod_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `category_product` ;
CREATE TABLE IF NOT EXISTS `category_product` (
  `category_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`category_id`, `product_id`),
  KEY `fk_category_product_category_idx` (`category_id`),
  KEY `fk_category_product_product_idx` (`product_id`),
  CONSTRAINT `fk_category_product_category` FOREIGN KEY (`category_id`) REFERENCES `category` (`cat_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_category_product_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`prod_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


DROP TABLE IF EXISTS `store_product` ;
CREATE TABLE IF NOT EXISTS `store_product` (
  `store_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  PRIMARY KEY (`store_id`, `product_id`),
  KEY `fk_store_product_store_idx` (`store_id`),
  KEY `fk_store_product_product_idx` (`product_id`),
  CONSTRAINT `fk_store_product_store` FOREIGN KEY (`store_id`) REFERENCES `store` (`shop_id`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_store_product_product` FOREIGN KEY (`product_id`) REFERENCES `product` (`prod_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
