-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: projectdb
-- ------------------------------------------------------
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branches` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `specialisation` varchar(30) NOT NULL,
  `location` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branches`
--

LOCK TABLES `branches` WRITE;
/*!40000 ALTER TABLE `branches` DISABLE KEYS */;
INSERT INTO `branches` VALUES (1,'Frytki Smaczne','Szczawnica'),(2,'Burger Zbujnicki','Tatry'),(3,'Pizza Bieszczadczka','Bieszczady'),(7,'ddd','ddd');
/*!40000 ALTER TABLE `branches` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `directors`
--

DROP TABLE IF EXISTS `directors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL,
  `surname` varchar(30) DEFAULT NULL,
  `pesel` varchar(30) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `nationality` varchar(30) NOT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `address` varchar(30) DEFAULT NULL,
  `salary` int(11) NOT NULL,
  `branch_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `directors_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directors`
--

LOCK TABLES `directors` WRITE;
/*!40000 ALTER TABLE `directors` DISABLE KEYS */;
INSERT INTO `directors` VALUES (1,'Jan','Kowalski','11111111111','1999-11-15','Polska','999999999','Wroclaw',5000,1),(2,'Jan','Kowalski','11111111111','1999-11-15','Polska','999999999','Wroclaw',5000,1),(3,'Tamara','Janic','91092307123','2000-02-03','Serbia','009976235','Nis, Wolnosci 12',2000,1),(4,'Tamara','Janic','91092307123','2000-02-03','Serbia','009976235','Nis, Wolnosci 12',2000,1),(5,'Ivona','Petkovic','91092307123','1991-11-01','Serbia','009976234','Belgrad, Wolnosci 10',2100,1),(6,'Milca','Kalinic','97072307123','1997-01-01','Serbia','009976222','Novi Sad, Wolnosci 12',2100,1),(7,'Stiepan','Pawlak','89092307123','1991-01-01','Serbia','999976235','Nis, Wolnosci 12',2000,1),(8,'Bruno','Silva','91092307123','1999-01-09','Serbia','819476235','Belgrad, Wolnosci 15',2000,1),(9,'Jan','Kowalski','11111111111','1999-06-06','Polska','333333333','Myszkow',3000,1);
/*!40000 ALTER TABLE `directors` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_director` AFTER DELETE ON `directors` FOR EACH ROW BEGIN
DELETE FROM directors_login_data WHERE OLD.id=directors_login_data.director_id;
 END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `directors_login_data`
--

DROP TABLE IF EXISTS `directors_login_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `directors_login_data` (
  `director_id` int(11) NOT NULL,
  `login` varchar(30) NOT NULL,
  `password` varchar(120) NOT NULL,
  PRIMARY KEY (`director_id`),
  CONSTRAINT `directors_login_data_ibfk_1` FOREIGN KEY (`director_id`) REFERENCES `directors` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `directors_login_data`
--

LOCK TABLES `directors_login_data` WRITE;
/*!40000 ALTER TABLE `directors_login_data` DISABLE KEYS */;
INSERT INTO `directors_login_data` VALUES (2,'login','207023ccb44feb4d7dadca005ce29a64'),(3,'janic123','202cb962ac59075b964b07152d234b70'),(4,'janic123','202cb962ac59075b964b07152d234b70'),(5,'ivona123','202cb962ac59075b964b07152d234b70'),(6,'milca123','202cb962ac59075b964b07152d234b70'),(7,'pawlak123','202cb962ac59075b964b07152d234b70'),(8,'silva123','202cb962ac59075b964b07152d234b70'),(9,'aa','4124bc0a9335c27f086f24ba207a4912');
/*!40000 ALTER TABLE `directors_login_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `positions`
--

DROP TABLE IF EXISTS `positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `positions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `min_salary` int(11) NOT NULL,
  `max_salary` int(11) NOT NULL,
  `position_name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `positions`
--

LOCK TABLES `positions` WRITE;
/*!40000 ALTER TABLE `positions` DISABLE KEYS */;
INSERT INTO `positions` VALUES (1,1900,2100,'grill'),(2,1900,2100,'frytownica'),(3,2000,2200,'prezenter'),(4,2000,2200,'barista');
/*!40000 ALTER TABLE `positions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `view_workers`
--

DROP TABLE IF EXISTS `view_workers`;
/*!50001 DROP VIEW IF EXISTS `view_workers`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `view_workers` AS SELECT 
 1 AS `id`,
 1 AS `salary`,
 1 AS `branch_id`,
 1 AS `position_id`,
 1 AS `work_time`,
 1 AS `worker_id`,
 1 AS `name`,
 1 AS `surname`,
 1 AS `pesel`,
 1 AS `date_of_birth`,
 1 AS `nationality`,
 1 AS `phone`,
 1 AS `address`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `workers`
--

DROP TABLE IF EXISTS `workers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `salary` int(11) NOT NULL,
  `branch_id` int(11) NOT NULL,
  `position_id` int(11) NOT NULL,
  `work_time` enum('full','half','quater') DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `index_salary` (`salary`) USING BTREE,
  KEY `index_work_time` (`work_time`) USING BTREE,
  KEY `branch_id` (`branch_id`),
  KEY `position_id` (`position_id`),
  CONSTRAINT `workers_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branches` (`id`),
  CONSTRAINT `workers_ibfk_2` FOREIGN KEY (`position_id`) REFERENCES `positions` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workers`
--

LOCK TABLES `workers` WRITE;
/*!40000 ALTER TABLE `workers` DISABLE KEYS */;
INSERT INTO `workers` VALUES (2,2000,2,1,'full'),(3,2000,3,3,'full'),(4,2081,1,1,'half'),(5,2000,3,3,'full'),(6,2000,2,4,'full'),(7,2081,1,3,'half'),(9,2000,3,4,'quater'),(10,2000,3,1,'full'),(11,2000,3,2,'half'),(12,2000,3,3,'full'),(13,2000,3,3,'full'),(18,2040,1,3,'full');
/*!40000 ALTER TABLE `workers` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `salarycheck` AFTER INSERT ON `workers` FOR EACH ROW BEGIN
IF (NEW.salary>(SELECT max_salary FROM positions WHERE NEW.position_id LIKE positions.id)) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Za wysoka placa";
END IF;
IF (NEW.salary<(SELECT min_salary FROM positions WHERE NEW.position_id LIKE positions.id)) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Za niska placa";
END IF;
 END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `salarycheck_UP` AFTER UPDATE ON `workers` FOR EACH ROW BEGIN
IF (NEW.salary>(SELECT max_salary FROM positions WHERE NEW.position_id LIKE positions.id)) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Za wysoka placa";
END IF;
IF (NEW.salary<(SELECT min_salary FROM positions WHERE NEW.position_id LIKE positions.id)) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Za niska placa";
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `delete_worker` AFTER DELETE ON `workers` FOR EACH ROW BEGIN
DELETE FROM workers_data WHERE OLD.id=workers_data.worker_id;
DELETE FROM workers_login_data WHERE OLD.id=workers_login_data.worker_id;
 END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `workers_data`
--

DROP TABLE IF EXISTS `workers_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workers_data` (
  `worker_id` int(11) NOT NULL,
  `name` varchar(30) NOT NULL,
  `surname` varchar(30) DEFAULT NULL,
  `pesel` varchar(30) DEFAULT NULL,
  `date_of_birth` date DEFAULT NULL,
  `nationality` varchar(30) NOT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `address` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`worker_id`),
  KEY `index_pesel` (`pesel`) USING BTREE,
  CONSTRAINT `workers_data_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`),
  CONSTRAINT `workers_data_ibfk_2` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`),
  CONSTRAINT `workers_data_ibfk_3` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workers_data`
--

LOCK TABLES `workers_data` WRITE;
/*!40000 ALTER TABLE `workers_data` DISABLE KEYS */;
INSERT INTO `workers_data` VALUES (3,'Nuka','Stankovic','11001187632','2000-04-01','Chorwacja','912765123','Osijek, Orla Bialego 1'),(4,'Milan','Radnic','88001187632','2000-07-01','Chorwacja','999712323','Split, Wykletych 9'),(5,'Nikola','Kovacevic','09001187632','1999-12-11','Chorwacja','993455123','Dubrownik, Trzeciego Maja 49'),(6,'Vlado','Kalinic','20001187632','2000-01-01','Serbia','999765123','Nis, Belgradzka 4'),(7,'dd','dd','20001187632','2000-01-01','Serbia','999765123','Novi'),(9,'Marko','Nikic','29901187632','1980-06-01','Serbia','999765113','Belgrad, Belgradzka 9'),(10,'Dragan','Starovic','55001187632','1973-05-01','Czarnogora','999115123','Kotor, Belgradzka 4'),(11,'Ivone','Rosiic','11001187632','1982-01-03','Serbia','999765000','Nis, Belgradzka 1'),(12,'Nuka','Stankovic','11001187632','2000-04-01','Chorwacja','912765123','Osijek, Orla Bialego 1'),(13,'Nuka','Stankovic','11001187632','2000-04-01','Chorwacja','912765123','Osijek, Orla Bialego 1'),(18,'Nuka','Stankovic','11001187632','2000-04-01','Chorwacja','912765123','Orla');
/*!40000 ALTER TABLE `workers_data` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `pesel_age_check` AFTER INSERT ON `workers_data` FOR EACH ROW BEGIN
IF (!(CHAR_LENGTH(NEW.pesel) = 11) AND NEW.pesel IS NOT NULL) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Zly pesel";
END IF;
IF ((NEW.date_of_birth + INTERVAL 18 YEAR) > NOW()) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Nieletni";
END IF;
 END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `pesel_age_check_UP` BEFORE UPDATE ON `workers_data` FOR EACH ROW BEGIN
IF (!(CHAR_LENGTH(NEW.pesel) = 11) AND NEW.pesel IS NOT NULL) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Zly pesel";
END IF;
IF ((NEW.date_of_birth + INTERVAL 18 YEAR) > NOW()) THEN
SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = "Nieletni";
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `workers_login_data`
--

DROP TABLE IF EXISTS `workers_login_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workers_login_data` (
  `worker_id` int(11) NOT NULL,
  `login` varchar(30) NOT NULL,
  `password` varchar(120) NOT NULL,
  PRIMARY KEY (`worker_id`),
  CONSTRAINT `workers_login_data_ibfk_1` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`),
  CONSTRAINT `workers_login_data_ibfk_2` FOREIGN KEY (`worker_id`) REFERENCES `workers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workers_login_data`
--

LOCK TABLES `workers_login_data` WRITE;
/*!40000 ALTER TABLE `workers_login_data` DISABLE KEYS */;
INSERT INTO `workers_login_data` VALUES (3,'stanovic1','202cb962ac59075b964b07152d234b70'),(4,'radnic1','202cb962ac59075b964b07152d234b70'),(5,'kovacevic1','202cb962ac59075b964b07152d234b70'),(6,'kalinic1','202cb962ac59075b964b07152d234b70'),(7,'kalinic2','202cb962ac59075b964b07152d234b70'),(9,'nikic1','202cb962ac59075b964b07152d234b70'),(10,'starovic1','202cb962ac59075b964b07152d234b70'),(11,'rosiic1','202cb962ac59075b964b07152d234b70'),(12,'stanovic1','202cb962ac59075b964b07152d234b70'),(13,'stanovic1','202cb962ac59075b964b07152d234b70'),(18,'stanovic1','202cb962ac59075b964b07152d234b70');
/*!40000 ALTER TABLE `workers_login_data` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `view_workers`
--

/*!50001 DROP VIEW IF EXISTS `view_workers`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `view_workers` AS select `workers`.`id` AS `id`,`workers`.`salary` AS `salary`,`workers`.`branch_id` AS `branch_id`,`workers`.`position_id` AS `position_id`,`workers`.`work_time` AS `work_time`,`workers_data`.`worker_id` AS `worker_id`,`workers_data`.`name` AS `name`,`workers_data`.`surname` AS `surname`,`workers_data`.`pesel` AS `pesel`,`workers_data`.`date_of_birth` AS `date_of_birth`,`workers_data`.`nationality` AS `nationality`,`workers_data`.`phone` AS `phone`,`workers_data`.`address` AS `address` from (`workers` join `workers_data` on((`workers`.`id` = `workers_data`.`worker_id`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-02-06 17:27:10
