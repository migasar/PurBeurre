-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema purbeurre
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `purbeurre` ;

-- -----------------------------------------------------
-- Schema purbeurre
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `purbeurre` DEFAULT CHARACTER SET utf8 ;
USE `purbeurre` ;

-- -----------------------------------------------------
-- Table `purbeurre`.`product`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `purbeurre`.`product` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`product` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `product_name` VARCHAR(250) NULL,
  `description` LONGTEXT NULL,
  `nutriscore` INT NULL,
  `off_url` VARCHAR(500) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre`.`category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `purbeurre`.`category` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `category_name` VARCHAR(250) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre`.`store`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `purbeurre`.`store` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`store` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `store_name` VARCHAR(250) NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre`.`favorite`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `purbeurre`.`favorite` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`favorite` (
  `old_product_id` INT NOT NULL,
  `substitute_product_id` INT NOT NULL,
  INDEX `fk_favorite_product1_idx` (`old_product_id` ASC),
  INDEX `fk_favorite_product2_idx` (`substitute_product_id` ASC),
  PRIMARY KEY (`old_product_id`, `substitute_product_id`),
  CONSTRAINT `fk_favorite_product1`
    FOREIGN KEY (`old_product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_favorite_product2`
    FOREIGN KEY (`substitute_product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre`.`product_category`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `purbeurre`.`product_category` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`product_category` (
  `product_id` INT NOT NULL,
  `category_id` INT NOT NULL,
  INDEX `fk_product_category_category_idx` (`category_id` ASC),
  INDEX `fk_product_category_product1_idx` (`product_id` ASC),
  PRIMARY KEY (`product_id`, `category_id`),
  CONSTRAINT `fk_product_category_category`
    FOREIGN KEY (`category_id`)
    REFERENCES `purbeurre`.`category` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_category_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `purbeurre`.`product_store`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `purbeurre`.`product_store` ;

CREATE TABLE IF NOT EXISTS `purbeurre`.`product_store` (
  `product_id` INT NOT NULL,
  `store_id` INT NOT NULL,
  INDEX `fk_product_store_store1_idx` (`store_id` ASC),
  INDEX `fk_product_store_product1_idx` (`product_id` ASC),
  PRIMARY KEY (`product_id`, `store_id`),
  CONSTRAINT `fk_product_store_store1`
    FOREIGN KEY (`store_id`)
    REFERENCES `purbeurre`.`store` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_product_store_product1`
    FOREIGN KEY (`product_id`)
    REFERENCES `purbeurre`.`product` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
