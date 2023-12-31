-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: runotion
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add ╨а╨░╤Б╤И╨╕╤А╨╡╨╜╨╜╤Л╨╣ ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М',7,'add_userprofile'),(26,'Can change ╨а╨░╤Б╤И╨╕╤А╨╡╨╜╨╜╤Л╨╣ ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М',7,'change_userprofile'),(27,'Can delete ╨а╨░╤Б╤И╨╕╤А╨╡╨╜╨╜╤Л╨╣ ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М',7,'delete_userprofile'),(28,'Can view ╨а╨░╤Б╤И╨╕╤А╨╡╨╜╨╜╤Л╨╣ ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М',7,'view_userprofile'),(29,'Can add ╨г╤А╨╛╨▓╨╡╨╜╤М ╨▓╨░╨╢╨╜╨╛╤Б╤В╨╕',8,'add_importancelevel'),(30,'Can change ╨г╤А╨╛╨▓╨╡╨╜╤М ╨▓╨░╨╢╨╜╨╛╤Б╤В╨╕',8,'change_importancelevel'),(31,'Can delete ╨г╤А╨╛╨▓╨╡╨╜╤М ╨▓╨░╨╢╨╜╨╛╤Б╤В╨╕',8,'delete_importancelevel'),(32,'Can view ╨г╤А╨╛╨▓╨╡╨╜╤М ╨▓╨░╨╢╨╜╨╛╤Б╤В╨╕',8,'view_importancelevel'),(33,'Can add ╨а╨╛╨╗╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',9,'add_roleproject'),(34,'Can change ╨а╨╛╨╗╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',9,'change_roleproject'),(35,'Can delete ╨а╨╛╨╗╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',9,'delete_roleproject'),(36,'Can view ╨а╨╛╨╗╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',9,'view_roleproject'),(37,'Can add ╨н╤В╨░╨┐ ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',10,'add_sectionproject'),(38,'Can change ╨н╤В╨░╨┐ ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',10,'change_sectionproject'),(39,'Can delete ╨н╤В╨░╨┐ ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',10,'delete_sectionproject'),(40,'Can view ╨н╤В╨░╨┐ ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',10,'view_sectionproject'),(41,'Can add ╨Я╤А╨╛╨╡╨║╤В',11,'add_project'),(42,'Can change ╨Я╤А╨╛╨╡╨║╤В',11,'change_project'),(43,'Can delete ╨Я╤А╨╛╨╡╨║╤В',11,'delete_project'),(44,'Can view ╨Я╤А╨╛╨╡╨║╤В',11,'view_project'),(45,'Can add ╨Р╨║╤В╨╕╨▓╨╜╨╛╤Б╤В╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',12,'add_actionproject'),(46,'Can change ╨Р╨║╤В╨╕╨▓╨╜╨╛╤Б╤В╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',12,'change_actionproject'),(47,'Can delete ╨Р╨║╤В╨╕╨▓╨╜╨╛╤Б╤В╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',12,'delete_actionproject'),(48,'Can view ╨Р╨║╤В╨╕╨▓╨╜╨╛╤Б╤В╤М ╨▓ ╨┐╤А╨╛╨╡╨║╤В╨╡',12,'view_actionproject'),(49,'Can add ╨Ш╤Б╤В╨╛╤А╨╕╤П ╨┐╨╛ ╨┐╤А╨╛╨╡╨║╤В╤Г',13,'add_historyproject'),(50,'Can change ╨Ш╤Б╤В╨╛╤А╨╕╤П ╨┐╨╛ ╨┐╤А╨╛╨╡╨║╤В╤Г',13,'change_historyproject'),(51,'Can delete ╨Ш╤Б╤В╨╛╤А╨╕╤П ╨┐╨╛ ╨┐╤А╨╛╨╡╨║╤В╤Г',13,'delete_historyproject'),(52,'Can view ╨Ш╤Б╤В╨╛╤А╨╕╤П ╨┐╨╛ ╨┐╤А╨╛╨╡╨║╤В╤Г',13,'view_historyproject'),(53,'Can add ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',14,'add_checklisttask'),(54,'Can change ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',14,'change_checklisttask'),(55,'Can delete ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',14,'delete_checklisttask'),(56,'Can view ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',14,'view_checklisttask'),(57,'Can add ╨Ч╨░╨┤╨░╤З╨░',15,'add_task'),(58,'Can change ╨Ч╨░╨┤╨░╤З╨░',15,'change_task'),(59,'Can delete ╨Ч╨░╨┤╨░╤З╨░',15,'delete_task'),(60,'Can view ╨Ч╨░╨┤╨░╤З╨░',15,'view_task'),(61,'Can add ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'add_userpositiontask'),(62,'Can change ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'change_userpositiontask'),(63,'Can delete ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'delete_userpositiontask'),(64,'Can view ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'view_userpositiontask'),(65,'Can add ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'add_userpositiontasktotask'),(66,'Can change ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'change_userpositiontasktotask'),(67,'Can delete ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'delete_userpositiontasktotask'),(68,'Can view ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'view_userpositiontasktotask'),(69,'Can add ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',18,'add_subtaskchecklist'),(70,'Can change ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',18,'change_subtaskchecklist'),(71,'Can delete ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',18,'delete_subtaskchecklist'),(72,'Can view ╨з╨╡╨║╨╗╨╕╤Б╤В ╤Г ╨╖╨░╨┤╨░╤З╨╕',18,'view_subtaskchecklist'),(73,'Can add ╨Ъ╨╛╨╝╨╝╨╡╨╜╤В╨░╤А╨╕╨╣ ╤Г ╨╖╨░╨┤╨░╤З╨╕',19,'add_commenttask'),(74,'Can change ╨Ъ╨╛╨╝╨╝╨╡╨╜╤В╨░╤А╨╕╨╣ ╤Г ╨╖╨░╨┤╨░╤З╨╕',19,'change_commenttask'),(75,'Can delete ╨Ъ╨╛╨╝╨╝╨╡╨╜╤В╨░╤А╨╕╨╣ ╤Г ╨╖╨░╨┤╨░╤З╨╕',19,'delete_commenttask'),(76,'Can view ╨Ъ╨╛╨╝╨╝╨╡╨╜╤В╨░╤А╨╕╨╣ ╤Г ╨╖╨░╨┤╨░╤З╨╕',19,'view_commenttask'),(77,'Can add ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨┐╤А╨╛╨╡╨║╤В╤Г',20,'add_usertoproject'),(78,'Can change ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨┐╤А╨╛╨╡╨║╤В╤Г',20,'change_usertoproject'),(79,'Can delete ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨┐╤А╨╛╨╡╨║╤В╤Г',20,'delete_usertoproject'),(80,'Can view ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨┐╤А╨╛╨╡╨║╤В╤Г',20,'view_usertoproject'),(81,'Can add ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'add_usertotask'),(82,'Can change ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'change_usertotask'),(83,'Can delete ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'delete_usertotask'),(84,'Can view ╨Я╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤М ╨║ ╨╖╨░╨┤╨░╤З╨╡',17,'view_usertotask'),(85,'Can add ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'add_userleveltask'),(86,'Can change ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'change_userleveltask'),(87,'Can delete ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'delete_userleveltask'),(88,'Can view ╨Ф╨╛╨╗╨╢╨╜╨╛╤Б╤В╤М ╨┐╨╛╨╗╤М╨╖╨╛╨▓╨░╤В╨╡╨╗╤П ╨▓ ╨╖╨░╨┤╨░╤З╨░╤Е',16,'view_userleveltask'),(89,'Can add ╨Ч╨░╨┤╨░╤З╨░ ╨║ ╨б╨╡╨║╤Ж╨╕╨╕',21,'add_tasktosection'),(90,'Can change ╨Ч╨░╨┤╨░╤З╨░ ╨║ ╨б╨╡╨║╤Ж╨╕╨╕',21,'change_tasktosection'),(91,'Can delete ╨Ч╨░╨┤╨░╤З╨░ ╨║ ╨б╨╡╨║╤Ж╨╕╨╕',21,'delete_tasktosection'),(92,'Can view ╨Ч╨░╨┤╨░╤З╨░ ╨║ ╨б╨╡╨║╤Ж╨╕╨╕',21,'view_tasktosection'),(93,'Can add ╨Ф╨╡╨┐╨░╤А╤В╨░╨╝╨╡╨╜╤В',22,'add_department'),(94,'Can change ╨Ф╨╡╨┐╨░╤А╤В╨░╨╝╨╡╨╜╤В',22,'change_department'),(95,'Can delete ╨Ф╨╡╨┐╨░╤А╤В╨░╨╝╨╡╨╜╤В',22,'delete_department'),(96,'Can view ╨Ф╨╡╨┐╨░╤А╤В╨░╨╝╨╡╨╜╤В',22,'view_department');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$600000$Y0MPSyxkooB8TFJ2sfwm5k$XWw256BjsGmJqvaTlnAo88gJmdxJesdIQZzOy5EbyzA=','2023-11-29 23:07:32.680830',1,'admin','','','',1,1,'2023-11-01 21:57:28.102897'),(2,'pbkdf2_sha256$600000$iRZe1gCj9YA2MmPKzhwHNF$3SMvNgTaHt/I8K1GvfMrEfMX1Bbp/OqPuKHDCGcGDfQ=',NULL,0,'test','','','',0,1,'2023-11-16 09:17:46.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `core_importancelevel`
--

DROP TABLE IF EXISTS `core_importancelevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `core_importancelevel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `value` int NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `core_importancelevel`
--

LOCK TABLES `core_importancelevel` WRITE;
/*!40000 ALTER TABLE `core_importancelevel` DISABLE KEYS */;
INSERT INTO `core_importancelevel` VALUES (1,'╨Э╨╕╨╖╨║╨╕╨╣',1),(2,'╨б╤А╨╡╨┤╨╜╨╕╨╣',2),(3,'╨Т╤Л╤Б╨╛╨║╨╕╨╣',3);
/*!40000 ALTER TABLE `core_importancelevel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=179 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
INSERT INTO `django_admin_log` VALUES (1,'2023-11-02 00:40:39.932898','1','admin',1,'[{\"added\": {}}]',7,1),(2,'2023-11-02 12:55:12.150333','1','╨Э╨╕╨╖╨║╨╕╨╣',1,'[{\"added\": {}}]',8,1),(3,'2023-11-02 12:55:17.563276','2','╨б╤А╨╡╨┤╨╜╨╕╨╣',1,'[{\"added\": {}}]',8,1),(4,'2023-11-02 12:55:22.716842','3','╨Т╤Л╤Б╨╛╨║╨╕╨╣',1,'[{\"added\": {}}]',8,1),(5,'2023-11-02 12:57:02.459634','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries',1,'[{\"added\": {}}]',11,1),(6,'2023-11-02 12:57:38.397125','1','╨Р╨┤╨╝╨╕╨╜',1,'[{\"added\": {}}]',9,1),(7,'2023-11-02 12:57:52.539060','2','╨Ь╨╡╨╜╨╡╨┤╨╢╨╡╤А',1,'[{\"added\": {}}]',9,1),(8,'2023-11-02 12:58:22.735182','3','╨а╨░╨▒╨╛╤В╤П╨│╨░',1,'[{\"added\": {}}]',9,1),(9,'2023-11-02 13:05:13.375532','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries admin ╨Р╨┤╨╝╨╕╨╜',1,'[{\"added\": {}}]',20,1),(10,'2023-11-02 14:01:59.639326','1','╨Р╨┤╨╝╨╕╨╜',2,'[]',9,1),(11,'2023-11-02 15:37:23.079288','1','╨Я╨╛╤Б╤В╨░╨╜╨╛╨▓╤Й╨╕╨║',1,'[{\"added\": {}}]',16,1),(12,'2023-11-02 15:37:36.319666','2','╨Ю╤В╨▓╨╡╤В╤Б╤В╨▓╨╡╨╜╨╜╤Л╨╣',1,'[{\"added\": {}}]',16,1),(13,'2023-11-02 15:37:47.583647','3','╨б╨╛╨╕╤Б╨┐╨╛╨╗╨╜╨╕╤В╨╡╨╗╤М',1,'[{\"added\": {}}]',16,1),(14,'2023-11-02 15:37:59.789925','4','╨Э╨░╨▒╨╗╤О╨┤╨░╤В╨╡╨╗╤М',1,'[{\"added\": {}}]',16,1),(15,'2023-11-02 15:45:50.840617','2','╨Ю╤В╨▓╨╡╤В╤Б╤В╨▓╨╡╨╜╨╜╤Л╨╣',2,'[{\"changed\": {\"fields\": [\"\\u0423\\u0440\\u043e\\u0432\\u0435\\u043d\\u044c\"]}}]',16,1),(16,'2023-11-02 15:45:58.077044','3','╨б╨╛╨╕╤Б╨┐╨╛╨╗╨╜╨╕╤В╨╡╨╗╤М',2,'[{\"changed\": {\"fields\": [\"\\u0423\\u0440\\u043e\\u0432\\u0435\\u043d\\u044c\"]}}]',16,1),(17,'2023-11-02 15:46:03.700267','4','╨Э╨░╨▒╨╗╤О╨┤╨░╤В╨╡╨╗╤М',2,'[]',16,1),(18,'2023-11-02 17:38:29.451061','1','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡',1,'[{\"added\": {}}]',15,1),(19,'2023-11-02 17:39:07.781737','1','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ===> ╨Ш╨▓╨░╨╜ ╨Я╨╕╨▓╨░╨╜╤Л╤З',1,'[{\"added\": {}}]',17,1),(20,'2023-11-02 18:09:21.500890','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries',2,'[]',11,1),(21,'2023-11-02 18:48:56.677405','2','╨Ъ╨╛╤И╨║╨░',1,'[{\"added\": {}}]',11,1),(22,'2023-11-02 18:49:16.148219','2','╨Ъ╨╛╤И╨║╨░ admin ╨Р╨┤╨╝╨╕╨╜',1,'[{\"added\": {}}]',20,1),(23,'2023-11-03 00:22:58.394078','2','qweqwe',1,'[{\"added\": {}}]',15,1),(24,'2023-11-03 00:27:51.844012','2','qweqwe',3,'',15,1),(25,'2023-11-03 00:28:04.838499','3','╨╣╤Ж╤Г╨╣╤Ж╤Г',1,'[{\"added\": {}}]',15,1),(26,'2023-11-03 00:55:45.771664','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries',2,'[{\"changed\": {\"fields\": [\"\\u0410\\u0434\\u043c\\u0438\\u043d\"]}}]',11,1),(27,'2023-11-03 00:55:51.182116','2','╨Ъ╨╛╤И╨║╨░',2,'[{\"changed\": {\"fields\": [\"\\u0410\\u0434\\u043c\\u0438\\u043d\"]}}]',11,1),(28,'2023-11-03 00:57:14.819369','2','╨Ъ╨╛╤И╨║╨░ admin ╨Р╨┤╨╝╨╕╨╜',3,'',20,1),(29,'2023-11-03 00:57:14.825312','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries admin ╨Р╨┤╨╝╨╕╨╜',3,'',20,1),(30,'2023-11-03 01:21:10.955272','3','╨Ъ╨╛╤И╨║╨░ admin ╨Ь╨╡╨╜╨╡╨┤╨╢╨╡╤А',1,'[{\"added\": {}}]',20,1),(31,'2023-11-03 01:21:28.617311','3','╨Ъ╨╛╤И╨║╨░ admin ╨Ь╨╡╨╜╨╡╨┤╨╢╨╡╤А',3,'',20,1),(32,'2023-11-03 03:21:20.642543','3','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ===> ╨Ы╨╛╨│╨╛╤В╨╕╨┐',1,'[{\"added\": {}}]',14,1),(33,'2023-11-03 03:21:31.837912','4','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ===> ╨Я╨╛╨╕╤Б╨║',1,'[{\"added\": {}}]',14,1),(34,'2023-11-03 03:30:12.562516','1','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ==> ╨Ы╨╛╨│╨╛╤В╨╕╨┐ ===> ╨Ъ╨▓╨░╨┤╤А╨░╤В╨╜╨░╤П ╨▓╨╡╤А╤Б╨╕╤П',1,'[{\"added\": {}}]',18,1),(35,'2023-11-03 03:30:22.563727','2','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ==> ╨Ы╨╛╨│╨╛╤В╨╕╨┐ ===> ╨У╨╛╤А╨╕╨╖╨╛╨╜╤В╨░╨╗╤М╨╜╨░╤П ╨▓╨╡╤А╤Б╨╕╤П',1,'[{\"added\": {}}]',18,1),(36,'2023-11-03 03:30:51.421132','1','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ==> ╨Ы╨╛╨│╨╛╤В╨╕╨┐ ===> ╨Ъ╨▓╨░╨┤╤А╨░╤В╨╜╨░╤П ╨▓╨╡╤А╤Б╨╕╤П',2,'[{\"changed\": {\"fields\": [\"\\u0414\\u0430\\u0442\\u0430 \\u0437\\u0430\\u0432\\u0435\\u0440\\u0448\\u0435\\u043d\\u0438\\u044f\"]}}]',18,1),(37,'2023-11-16 00:07:21.551076','8','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ===> ╨з╨╡╨║╨╗╨╕╤Б╤В 6',3,'',14,1),(38,'2023-11-16 00:07:21.643086','7','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ===> ╨з╨╡╨║╨╗╨╕╤Б╤В 1',3,'',14,1),(39,'2023-11-16 00:07:21.655069','6','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ===> ╨з╨╡╨║╨╗╨╕╤Б╤В 4',3,'',14,1),(40,'2023-11-16 09:17:46.836950','2','test',1,'[{\"added\": {}}]',4,1),(41,'2023-11-16 09:31:05.503220','2','test',2,'[]',4,1),(42,'2023-11-23 20:13:39.633118','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',1,'[{\"added\": {}}]',10,1),(43,'2023-11-23 20:15:00.348781','2','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Frontend',1,'[{\"added\": {}}]',10,1),(44,'2023-11-23 20:16:37.782245','3','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(45,'2023-11-23 20:26:23.960668','4','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Test',1,'[{\"added\": {}}]',10,1),(46,'2023-11-23 20:37:21.547542','5','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Done',1,'[{\"added\": {}}]',10,1),(47,'2023-11-23 20:44:04.452257','3','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(48,'2023-11-23 20:44:51.407917','6','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(49,'2023-11-23 20:45:13.388769','7','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> 123123123',1,'[{\"added\": {}}]',10,1),(50,'2023-11-23 20:45:24.294464','8','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> qwerqwer',1,'[{\"added\": {}}]',10,1),(51,'2023-11-23 20:45:35.893997','9','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> saasdfasdf',1,'[{\"added\": {}}]',10,1),(52,'2023-11-23 20:55:00.953608','7','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> 123123123',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(53,'2023-11-23 20:55:11.352674','8','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> qwerqwer',3,'',10,1),(54,'2023-11-23 20:55:11.368675','5','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Done',3,'',10,1),(55,'2023-11-23 20:55:11.379669','4','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Test',3,'',10,1),(56,'2023-11-23 20:55:11.394671','2','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Frontend',3,'',10,1),(57,'2023-11-23 20:55:11.403673','1','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',3,'',10,1),(58,'2023-11-23 20:55:11.413688','6','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(59,'2023-11-23 20:55:11.428669','9','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> saasdfasdf',3,'',10,1),(60,'2023-11-23 20:55:11.441669','7','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> 123123123',3,'',10,1),(61,'2023-11-23 20:55:20.560501','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(62,'2023-11-23 20:55:38.863663','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',1,'[{\"added\": {}}]',10,1),(63,'2023-11-23 20:55:43.259331','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(64,'2023-11-23 20:55:50.826850','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(65,'2023-11-23 20:58:45.072310','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(66,'2023-11-23 20:59:17.144711','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(67,'2023-11-23 20:59:54.215820','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(68,'2023-11-23 21:01:13.629341','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(69,'2023-11-23 21:01:34.279932','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(70,'2023-11-23 21:05:42.289301','12','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> 123123',1,'[{\"added\": {}}]',10,1),(71,'2023-11-23 21:06:08.953101','12','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> 123123',3,'',10,1),(72,'2023-11-23 21:06:13.544836','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',1,'[{\"added\": {}}]',10,1),(73,'2023-11-23 21:06:22.949003','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(74,'2023-11-23 21:06:36.162748','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(75,'2023-11-23 21:06:40.588028','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(76,'2023-11-23 21:07:59.871267','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',2,'[]',10,1),(77,'2023-11-23 21:08:03.285392','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',2,'[]',10,1),(78,'2023-11-23 21:08:42.815645','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',2,'[]',10,1),(79,'2023-11-23 21:09:04.531983','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',2,'[]',10,1),(80,'2023-11-23 21:09:08.112171','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(81,'2023-11-23 21:11:05.816267','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(82,'2023-11-23 21:11:31.247602','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(83,'2023-11-23 21:11:37.777404','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(84,'2023-11-23 21:12:05.504073','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(85,'2023-11-23 21:12:12.525484','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(86,'2023-11-23 21:12:35.161114','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(87,'2023-11-23 21:12:37.768660','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(88,'2023-11-23 21:12:50.628316','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(89,'2023-11-23 21:13:28.268099','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(90,'2023-11-23 21:13:44.504754','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(91,'2023-11-23 21:14:19.028527','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(92,'2023-11-23 21:14:26.948567','10','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(93,'2023-11-23 21:14:26.955581','13','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> ╨╣╤Ж╤Г╨╣╤Ж╤Г╨╣╤Ж╤Г',3,'',10,1),(94,'2023-11-23 21:14:35.144318','14','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(95,'2023-11-23 21:15:57.591116','14','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(96,'2023-11-23 21:16:00.821884','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(97,'2023-11-23 21:16:14.605119','15','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(98,'2023-11-23 21:32:33.080872','15','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(99,'2023-11-23 21:32:33.087571','11','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',3,'',10,1),(100,'2023-11-23 21:32:42.060205','16','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(101,'2023-11-23 21:32:51.330752','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',1,'[{\"added\": {}}]',10,1),(102,'2023-11-23 21:32:57.812434','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(103,'2023-11-23 21:33:42.127768','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(104,'2023-11-23 21:33:44.845138','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(105,'2023-11-23 21:33:47.160736','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(106,'2023-11-23 21:33:50.964191','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(107,'2023-11-23 21:33:56.046838','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(108,'2023-11-23 21:34:14.134313','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(109,'2023-11-23 21:34:19.588316','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(110,'2023-11-23 21:34:22.248441','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(111,'2023-11-23 21:34:42.703557','16','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(112,'2023-11-23 21:35:39.173627','16','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(113,'2023-11-23 21:36:15.043939','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(114,'2023-11-23 21:38:57.687054','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(115,'2023-11-23 21:39:02.289178','17','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',3,'',10,1),(116,'2023-11-23 21:39:02.294189','16','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(117,'2023-11-23 21:39:13.551501','18','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',1,'[{\"added\": {}}]',10,1),(118,'2023-11-23 21:39:21.580657','19','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(119,'2023-11-23 21:39:25.550561','19','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(120,'2023-11-23 21:40:11.811610','19','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(121,'2023-11-23 21:40:17.291913','20','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(122,'2023-11-23 21:40:20.651349','20','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(123,'2023-11-23 21:40:35.588810','20','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',3,'',10,1),(124,'2023-11-23 21:40:41.933518','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',1,'[{\"added\": {}}]',10,1),(125,'2023-11-23 21:40:46.764722','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(126,'2023-11-23 21:45:15.687243','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(127,'2023-11-23 21:45:18.119295','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[]',10,1),(128,'2023-11-23 21:49:09.885243','18','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Backend',2,'[]',10,1),(129,'2023-11-23 21:49:13.489483','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(130,'2023-11-23 21:49:17.345438','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(131,'2023-11-23 21:49:23.096597','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(132,'2023-11-23 21:51:27.083650','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(133,'2023-11-23 21:51:50.003238','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(134,'2023-11-23 21:52:04.926014','21','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Design',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(135,'2023-11-23 22:05:41.183472','22','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Frontend',1,'[{\"added\": {}}]',10,1),(136,'2023-11-23 22:05:53.210239','22','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Frontend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(137,'2023-11-23 22:05:58.698814','22','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Frontend',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(138,'2023-11-23 22:06:38.645415','23','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Test',1,'[{\"added\": {}}]',10,1),(139,'2023-11-23 22:06:51.097550','23','╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries ===> Test',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(140,'2023-11-23 23:09:36.715086','2','test',2,'[]',7,1),(141,'2023-11-23 23:09:43.064049','2','test',2,'[]',7,1),(142,'2023-11-23 23:18:24.115945','6','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В',3,'',11,1),(143,'2023-11-23 23:20:47.549534','29','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т╤Л╨┐╨╛╨╗╨╜╨╡╨╜╨╜╤Л╨╡',3,'',10,1),(144,'2023-11-23 23:20:47.556546','28','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т ╨┐╤А╨╛╤Ж╨╡╤Б╤Б╨╡',3,'',10,1),(145,'2023-11-23 23:20:47.560558','27','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(146,'2023-11-23 23:20:55.767781','7','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В',3,'',11,1),(147,'2023-11-23 23:22:48.821814','33','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',1,'[{\"added\": {}}]',10,1),(148,'2023-11-23 23:23:38.409436','34','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> sfsadfasdfa',1,'[{\"added\": {}}]',10,1),(149,'2023-11-23 23:23:47.745815','34','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> sfsadfasdfa',3,'',10,1),(150,'2023-11-23 23:23:47.752805','33','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(151,'2023-11-23 23:23:50.776084','32','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т╤Л╨┐╨╛╨╗╨╜╨╡╨╜╨╜╤Л╨╡',2,'[]',10,1),(152,'2023-11-23 23:24:55.664244','32','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т╤Л╨┐╨╛╨╗╨╜╨╡╨╜╨╜╤Л╨╡',2,'[]',10,1),(153,'2023-11-23 23:25:09.846937','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',1,'[{\"added\": {}}]',10,1),(154,'2023-11-23 23:31:10.261950','36','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqweqweqweqweqwe',1,'[{\"added\": {}}]',10,1),(155,'2023-11-23 23:31:19.985948','36','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqweqweqweqweqwe',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(156,'2023-11-24 12:19:17.198522','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(157,'2023-11-24 12:20:00.159414','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(158,'2023-11-24 12:20:50.154351','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(159,'2023-11-24 12:24:15.710673','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(160,'2023-11-24 12:25:01.501383','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(161,'2023-11-24 12:26:11.125505','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(162,'2023-11-24 12:27:26.901243','30','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Э╨╛╨▓╤Л╨╡',3,'',10,1),(163,'2023-11-24 12:27:45.501019','36','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqweqweqweqweqwe',3,'',10,1),(164,'2023-11-24 12:29:15.356010','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(165,'2023-11-24 12:32:29.929381','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(166,'2023-11-24 12:34:49.780655','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(167,'2023-11-24 12:35:02.070179','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(168,'2023-11-24 12:36:24.432492','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(169,'2023-11-24 12:38:52.509969','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(170,'2023-11-24 12:39:49.183585','35','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qweqweqwe',3,'',10,1),(171,'2023-11-24 12:40:42.363093','38','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qwerqwerqwer',1,'[{\"added\": {}}]',10,1),(172,'2023-11-24 12:47:18.451895','41','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qwerqwerqwer',1,'[{\"added\": {}}]',10,1),(173,'2023-11-24 12:48:18.671086','38','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qwerqwerqwer',3,'',10,1),(174,'2023-11-24 12:48:37.411776','31','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т ╨┐╤А╨╛╤Ж╨╡╤Б╤Б╨╡',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(175,'2023-11-24 12:48:43.970358','31','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т ╨┐╤А╨╛╤Ж╨╡╤Б╤Б╨╡',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(176,'2023-11-24 12:48:47.466818','31','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> ╨Т ╨┐╤А╨╛╤Ж╨╡╤Б╤Б╨╡',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(177,'2023-11-28 20:51:04.299117','41','╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В ===> qwerqwerqwer',2,'[{\"changed\": {\"fields\": [\"\\u041f\\u043e\\u0437\\u0438\\u0446\\u0438\\u044f\"]}}]',10,1),(178,'2023-11-28 21:26:29.811730','2','╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡ ==> _╨┐╤А╨╛╨╡╨║╤В_ None',1,'[{\"added\": {}}]',21,1);
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(8,'core','importancelevel'),(12,'project','actionproject'),(13,'project','historyproject'),(11,'project','project'),(9,'project','roleproject'),(10,'project','sectionproject'),(20,'project','usertoproject'),(6,'sessions','session'),(14,'task','checklisttask'),(19,'task','commenttask'),(18,'task','subtaskchecklist'),(15,'task','task'),(21,'task','tasktosection'),(16,'task','userleveltask'),(17,'task','usertotask'),(22,'user','department'),(7,'user','userprofile');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2023-11-01 21:55:10.819346'),(2,'auth','0001_initial','2023-11-01 21:55:12.562999'),(3,'admin','0001_initial','2023-11-01 21:55:13.056913'),(4,'admin','0002_logentry_remove_auto_add','2023-11-01 21:55:13.075896'),(5,'admin','0003_logentry_add_action_flag_choices','2023-11-01 21:55:13.089895'),(6,'contenttypes','0002_remove_content_type_name','2023-11-01 21:55:13.272894'),(7,'auth','0002_alter_permission_name_max_length','2023-11-01 21:55:13.358894'),(8,'auth','0003_alter_user_email_max_length','2023-11-01 21:55:13.396894'),(9,'auth','0004_alter_user_username_opts','2023-11-01 21:55:13.407895'),(10,'auth','0005_alter_user_last_login_null','2023-11-01 21:55:13.528612'),(11,'auth','0006_require_contenttypes_0002','2023-11-01 21:55:13.535616'),(12,'auth','0007_alter_validators_add_error_messages','2023-11-01 21:55:13.546604'),(13,'auth','0008_alter_user_username_max_length','2023-11-01 21:55:13.626877'),(14,'auth','0009_alter_user_last_name_max_length','2023-11-01 21:55:13.726363'),(15,'auth','0010_alter_group_name_max_length','2023-11-01 21:55:13.781130'),(16,'auth','0011_update_proxy_permissions','2023-11-01 21:55:13.792145'),(17,'auth','0012_alter_user_first_name_max_length','2023-11-01 21:55:13.879450'),(18,'sessions','0001_initial','2023-11-01 21:55:13.940449'),(19,'core','0001_initial','2023-11-02 00:36:39.681272'),(20,'user','0001_initial','2023-11-02 00:36:40.668729'),(21,'project','0001_initial','2023-11-02 00:36:41.803205'),(22,'project','0002_alter_actionproject_options_and_more','2023-11-02 01:24:10.969018'),(23,'task','0001_initial','2023-11-02 01:24:13.312781'),(24,'task','0002_alter_userpositiontask_options_alter_task_user','2023-11-02 11:36:19.142620'),(25,'project','0003_usertoproject','2023-11-02 13:04:30.685255'),(26,'task','0003_task_completed_at_alter_checklisttask_completed_at_and_more','2023-11-02 15:24:02.023144'),(27,'task','0004_task_deadline','2023-11-02 15:30:00.318921'),(28,'task','0005_alter_task_section_project','2023-11-02 15:40:29.180491'),(29,'task','0006_alter_checklisttask_completed_at_and_more','2023-11-02 15:40:29.209002'),(30,'task','0007_rename_user_task_director','2023-11-02 16:09:41.130243'),(31,'task','0008_alter_checklisttask_completed_at_and_more','2023-11-02 17:38:22.212371'),(32,'project','0004_project_admin','2023-11-03 00:55:30.720649'),(33,'task','0009_alter_subtaskchecklist_options_alter_task_director','2023-11-03 00:55:30.860332'),(34,'project','0005_alter_project_admin','2023-11-03 01:13:54.555430'),(35,'task','0010_rename_userpositiontasktotask_usertotask','2023-11-03 01:31:31.735826'),(36,'project','0006_alter_project_image','2023-11-03 03:39:34.485332'),(37,'task','0011_rename_userpositiontask_userleveltask_and_more','2023-11-16 11:48:30.480745'),(38,'project','0007_alter_sectionproject_position','2023-11-16 17:44:37.550000'),(39,'task','0012_remove_task_section_project_tasktosection','2023-11-16 17:44:38.096898'),(40,'project','0008_alter_sectionproject_position','2023-11-23 20:07:24.855458'),(41,'project','0009_alter_sectionproject_position','2023-11-23 20:17:18.725219'),(42,'project','0010_alter_sectionproject_position','2023-11-23 20:20:05.536548'),(43,'user','0002_department_alter_userprofile_image_and_more','2023-11-23 22:57:55.850936'),(44,'user','0003_remove_userprofile_department','2023-11-23 23:03:03.701927'),(45,'user','0004_userprofile_department','2023-11-23 23:07:25.096269'),(46,'user','0005_alter_userprofile_image_alter_userprofile_name','2023-11-23 23:09:24.584451'),(47,'task','0013_alter_checklisttask_position_and_more','2023-11-28 21:12:47.773969');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('84mxp3d2rcibnrvw179c3pxcyza92ea0','.eJxVjEEOwiAQRe_C2pDCIFCX7j0DGYZBqoYmpV0Z725JutDte-__twi4rSVsjZcwJXERSpx-WUR6cu0iPbDeZ0lzXZcpyp7IwzZ5mxO_rkf7d1Cwlb7OjrxVZvCgz5hRW09AJhtmD3E0MLDVI_MuEundGADnmHYESqMSny_h-TfT:1r8TeW:Y_t70H4qVgitQy4TNZCHFG1QXQ9SFrBTbIwE6KIOwPY','2023-12-13 23:07:32.722832'),('l61pccaue3zw7jo5tx310lv9lv2w9qst','.eJxVjEEOwiAQRe_C2pDCIFCX7j0DGYZBqoYmpV0Z725JutDte-__twi4rSVsjZcwJXERSpx-WUR6cu0iPbDeZ0lzXZcpyp7IwzZ5mxO_rkf7d1Cwlb7OjrxVZvCgz5hRW09AJhtmD3E0MLDVI_MuEundGADnmHYESqMSny_h-TfT:1r3Pma:5FGhUZxK6Fy6IGFZovv5UWABatKoIpMZULtYGKTEAD0','2023-11-29 23:58:56.910502'),('tny40enq9tpv9jkvhigjcosl4sd02jme','.eJxVjEEOwiAQRe_C2pDCIFCX7j0DGYZBqoYmpV0Z725JutDte-__twi4rSVsjZcwJXERSpx-WUR6cu0iPbDeZ0lzXZcpyp7IwzZ5mxO_rkf7d1Cwlb7OjrxVZvCgz5hRW09AJhtmD3E0MLDVI_MuEundGADnmHYESqMSny_h-TfT:1r6AB2:fUmqz_5pJbRM9xbCNPJ1vnxg-ZEQ3FufPiyUhlieMCM','2023-12-07 13:55:32.866960'),('toncreqancbos1g00is5t5xvqfcijmgg','.eJxVjEEOwiAQRe_C2pDCIFCX7j0DGYZBqoYmpV0Z725JutDte-__twi4rSVsjZcwJXERSpx-WUR6cu0iPbDeZ0lzXZcpyp7IwzZ5mxO_rkf7d1Cwlb7OjrxVZvCgz5hRW09AJhtmD3E0MLDVI_MuEundGADnmHYESqMSny_h-TfT:1qyJGq:gGtbgc-Ul-zQfaTEn_ynFZYyDfuTPJHYuLEhUwdY9E8','2023-11-15 22:01:04.373482');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_actionproject`
--

DROP TABLE IF EXISTS `project_actionproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_actionproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_actionproject`
--

LOCK TABLES `project_actionproject` WRITE;
/*!40000 ALTER TABLE `project_actionproject` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_actionproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_historyproject`
--

DROP TABLE IF EXISTS `project_historyproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_historyproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `action_id` bigint NOT NULL,
  `project_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  `victim_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_historyproje_action_id_ddd9b585_fk_project_a` (`action_id`),
  KEY `project_historyproject_project_id_6a7b5649_fk_project_project_id` (`project_id`),
  KEY `project_historyproject_user_id_1eb63bc5_fk_user_userprofile_id` (`user_id`),
  KEY `project_historyproject_victim_id_1299e045_fk_user_userprofile_id` (`victim_id`),
  CONSTRAINT `project_historyproje_action_id_ddd9b585_fk_project_a` FOREIGN KEY (`action_id`) REFERENCES `project_actionproject` (`id`),
  CONSTRAINT `project_historyproject_project_id_6a7b5649_fk_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`),
  CONSTRAINT `project_historyproject_user_id_1eb63bc5_fk_user_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `user_userprofile` (`id`),
  CONSTRAINT `project_historyproject_victim_id_1299e045_fk_user_userprofile_id` FOREIGN KEY (`victim_id`) REFERENCES `user_userprofile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_historyproject`
--

LOCK TABLES `project_historyproject` WRITE;
/*!40000 ALTER TABLE `project_historyproject` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_historyproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_project`
--

DROP TABLE IF EXISTS `project_project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_project` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `admin_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_project_admin_id_a36882ab_fk_user_userprofile_id` (`admin_id`),
  CONSTRAINT `project_project_admin_id_a36882ab_fk_user_userprofile_id` FOREIGN KEY (`admin_id`) REFERENCES `user_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_project`
--

LOCK TABLES `project_project` WRITE;
/*!40000 ALTER TABLE `project_project` DISABLE KEYS */;
INSERT INTO `project_project` VALUES (1,'╨Ф╨╡╨╗╨░╨╡╨╝ WildBerries','wb','2023-11-02 12:57:02.411668','project/images/23.jpg',1),(2,'╨Ъ╨╛╤И╨║╨░','cat','2023-11-02 18:48:56.674402','project/images/56.jpg',1),(3,'YO','new','2023-11-03 04:00:45.517361','project/images/1_qUJocn9.jpg',1),(8,'╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В','new5','2023-11-23 23:21:02.952511','',1),(9,'╨Э╨╛╨▓╤Л╨╣ ╨┐╤А╨╛╨╡╨║╤В','new6','2023-11-28 21:01:01.497465','',1);
/*!40000 ALTER TABLE `project_project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_roleproject`
--

DROP TABLE IF EXISTS `project_roleproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_roleproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `level_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `level_id` (`level_id`),
  CONSTRAINT `project_roleproject_level_id_c12b9d80_fk_core_importancelevel_id` FOREIGN KEY (`level_id`) REFERENCES `core_importancelevel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_roleproject`
--

LOCK TABLES `project_roleproject` WRITE;
/*!40000 ALTER TABLE `project_roleproject` DISABLE KEYS */;
INSERT INTO `project_roleproject` VALUES (1,'╨Р╨┤╨╝╨╕╨╜',3),(2,'╨Ь╨╡╨╜╨╡╨┤╨╢╨╡╤А',2),(3,'╨а╨░╨▒╨╛╤В╤П╨│╨░',1);
/*!40000 ALTER TABLE `project_roleproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_sectionproject`
--

DROP TABLE IF EXISTS `project_sectionproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_sectionproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `position` int DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `project_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_sectionproject_project_id_7c88b536_fk_project_project_id` (`project_id`),
  CONSTRAINT `project_sectionproject_project_id_7c88b536_fk_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=45 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_sectionproject`
--

LOCK TABLES `project_sectionproject` WRITE;
/*!40000 ALTER TABLE `project_sectionproject` DISABLE KEYS */;
INSERT INTO `project_sectionproject` VALUES (18,'Backend',1,'2023-11-23 21:39:13.549502',1),(21,'Design',1,'2023-11-23 21:40:41.932530',1),(22,'Frontend',3,'2023-11-23 22:05:41.177147',1),(23,'Test',4,'2023-11-23 22:06:38.636415',1),(31,'╨Т ╨┐╤А╨╛╤Ж╨╡╤Б╤Б╨╡',2,'2023-11-23 23:21:02.973416',8),(32,'╨Т╤Л╨┐╨╛╨╗╨╜╨╡╨╜╨╜╤Л╨╡',1,'2023-11-23 23:21:02.992435',8),(41,'qwerqwerqwer',3,'2023-11-24 12:47:18.446895',8),(42,'╨Э╨╛╨▓╤Л╨╡',3,'2023-11-28 21:01:01.507468',9),(43,'╨Т ╨┐╤А╨╛╤Ж╨╡╤Б╤Б╨╡',2,'2023-11-28 21:01:01.536463',9),(44,'╨Т╤Л╨┐╨╛╨╗╨╜╨╡╨╜╨╜╤Л╨╡',1,'2023-11-28 21:01:01.563465',9);
/*!40000 ALTER TABLE `project_sectionproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project_usertoproject`
--

DROP TABLE IF EXISTS `project_usertoproject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `project_usertoproject` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `project_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `project_usertoproject_project_id_60f263b7_fk_project_project_id` (`project_id`),
  KEY `project_usertoproject_role_id_9d4d0d0b_fk_project_roleproject_id` (`role_id`),
  KEY `project_usertoproject_user_id_707811c1_fk_user_userprofile_id` (`user_id`),
  CONSTRAINT `project_usertoproject_project_id_60f263b7_fk_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`),
  CONSTRAINT `project_usertoproject_role_id_9d4d0d0b_fk_project_roleproject_id` FOREIGN KEY (`role_id`) REFERENCES `project_roleproject` (`id`),
  CONSTRAINT `project_usertoproject_user_id_707811c1_fk_user_userprofile_id` FOREIGN KEY (`user_id`) REFERENCES `user_userprofile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project_usertoproject`
--

LOCK TABLES `project_usertoproject` WRITE;
/*!40000 ALTER TABLE `project_usertoproject` DISABLE KEYS */;
/*!40000 ALTER TABLE `project_usertoproject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_checklisttask`
--

DROP TABLE IF EXISTS `task_checklisttask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_checklisttask` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `position` int DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_checklisttask_user_id_9fd84473_fk_task_usertotask_id` (`user_id`),
  CONSTRAINT `task_checklisttask_user_id_9fd84473_fk_task_usertotask_id` FOREIGN KEY (`user_id`) REFERENCES `task_usertotask` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_checklisttask`
--

LOCK TABLES `task_checklisttask` WRITE;
/*!40000 ALTER TABLE `task_checklisttask` DISABLE KEYS */;
INSERT INTO `task_checklisttask` VALUES (3,'╨Ы╨╛╨│╨╛╤В╨╕╨┐',1,NULL,'2023-11-03 03:21:20.603539',1),(4,'╨Я╨╛╨╕╤Б╨║',3,NULL,'2023-11-03 03:21:31.823914',1),(5,'╨Ч╨░╨┤╨░╤З╨░ 3',2,NULL,'2023-11-15 20:08:45.793065',1),(11,'╨з╨╡╨║-╨╗╨╕╤Б╤В 4',4,NULL,'2023-11-16 19:24:43.662683',1);
/*!40000 ALTER TABLE `task_checklisttask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_commenttask`
--

DROP TABLE IF EXISTS `task_commenttask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_commenttask` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `text` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_commenttask_user_id_cb5774d7_fk_task_usertotask_id` (`user_id`),
  CONSTRAINT `task_commenttask_user_id_cb5774d7_fk_task_usertotask_id` FOREIGN KEY (`user_id`) REFERENCES `task_usertotask` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_commenttask`
--

LOCK TABLES `task_commenttask` WRITE;
/*!40000 ALTER TABLE `task_commenttask` DISABLE KEYS */;
/*!40000 ALTER TABLE `task_commenttask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_subtaskchecklist`
--

DROP TABLE IF EXISTS `task_subtaskchecklist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_subtaskchecklist` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `position` int DEFAULT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `checklist_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_subtaskchecklis_checklist_id_e758fdd4_fk_task_chec` (`checklist_id`),
  CONSTRAINT `task_subtaskchecklis_checklist_id_e758fdd4_fk_task_chec` FOREIGN KEY (`checklist_id`) REFERENCES `task_checklisttask` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_subtaskchecklist`
--

LOCK TABLES `task_subtaskchecklist` WRITE;
/*!40000 ALTER TABLE `task_subtaskchecklist` DISABLE KEYS */;
INSERT INTO `task_subtaskchecklist` VALUES (1,'╨Ъ╨▓╨░╨┤╤А╨░╤В╨╜╨░╤П ╨▓╨╡╤А╤Б╨╕╤П',1,'2023-11-03 03:30:50.000000','2023-11-03 03:30:12.535518',3),(2,'╨У╨╛╤А╨╕╨╖╨╛╨╜╤В╨░╨╗╤М╨╜╨░╤П ╨▓╨╡╤А╤Б╨╕╤П',2,NULL,'2023-11-03 03:30:22.560731',3),(3,'╨Я╨╛╨┤╨╖╨░╨┤╨░╤З╨░ 1',1,NULL,'2023-11-16 09:44:49.823088',5),(4,'╨Я╨╛╨┤╨╖╨░╨┤╨░╤З╨░ 2',4,NULL,'2023-11-16 09:44:51.351768',5),(7,'╨Э╨╛╨▓╨╛╨╡ ╨╜╨░╨╖╨▓╨░╨╜╨╕╨╡ ╨┐╨╛╨┤╨╖╨░╨┤╨░╤З╨╕',3,NULL,'2023-11-16 10:54:03.625621',5);
/*!40000 ALTER TABLE `task_subtaskchecklist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_task`
--

DROP TABLE IF EXISTS `task_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_task` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `code` varchar(128) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `project_id` bigint NOT NULL,
  `director_id` bigint NOT NULL,
  `completed_at` datetime(6) DEFAULT NULL,
  `deadline` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `task_task_project_id_0d03694f_fk_project_project_id` (`project_id`),
  KEY `task_task_director_id_49a2b9a8_fk_user_userprofile_id` (`director_id`),
  CONSTRAINT `task_task_director_id_49a2b9a8_fk_user_userprofile_id` FOREIGN KEY (`director_id`) REFERENCES `user_userprofile` (`id`),
  CONSTRAINT `task_task_project_id_0d03694f_fk_project_project_id` FOREIGN KEY (`project_id`) REFERENCES `project_project` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_task`
--

LOCK TABLES `task_task` WRITE;
/*!40000 ALTER TABLE `task_task` DISABLE KEYS */;
INSERT INTO `task_task` VALUES (1,'╨б╨┤╨╡╨╗╨░╤В╤М header ╨▓ ╨┤╨╕╨╖╨░╨╣╨╜╨╡','wb-1','2023-11-02 17:38:29.449061',1,1,NULL,NULL),(3,'╨╣╤Ж╤Г╨╣╤Ж╤Г','wb-2','2023-11-03 00:28:04.775501',1,1,NULL,NULL),(4,'╨Э╨╛╨▓╨░╤П ╨╖╨░╨┤╨░╤З╨░','wb-3','2023-11-15 19:02:54.584388',1,1,NULL,NULL),(5,'╨Э╨╛╨▓╨░╤П ╨╖╨░╨┤╨░╤З╨░','wb-4','2023-11-15 19:42:56.096369',1,1,NULL,NULL),(6,'╨Э╨╛╨▓╨░╤П ╨╖╨░╨┤╨░╤З╨░','wb-5','2023-11-15 19:42:59.039582',1,1,NULL,NULL);
/*!40000 ALTER TABLE `task_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_tasktosection`
--

DROP TABLE IF EXISTS `task_tasktosection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_tasktosection` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `position` int DEFAULT NULL,
  `section_project_id` bigint DEFAULT NULL,
  `task_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_tasktosection_section_project_id_efb94952_fk_project_s` (`section_project_id`),
  KEY `task_tasktosection_task_id_1ba0378a_fk_task_task_id` (`task_id`),
  CONSTRAINT `task_tasktosection_section_project_id_efb94952_fk_project_s` FOREIGN KEY (`section_project_id`) REFERENCES `project_sectionproject` (`id`),
  CONSTRAINT `task_tasktosection_task_id_1ba0378a_fk_task_task_id` FOREIGN KEY (`task_id`) REFERENCES `task_task` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_tasktosection`
--

LOCK TABLES `task_tasktosection` WRITE;
/*!40000 ALTER TABLE `task_tasktosection` DISABLE KEYS */;
INSERT INTO `task_tasktosection` VALUES (2,'2023-11-28 21:26:29.806716',1,NULL,1);
/*!40000 ALTER TABLE `task_tasktosection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_userleveltask`
--

DROP TABLE IF EXISTS `task_userleveltask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_userleveltask` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(128) NOT NULL,
  `level_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_userpositiontas_level_id_bce20eb2_fk_core_impo` (`level_id`),
  CONSTRAINT `task_userpositiontas_level_id_bce20eb2_fk_core_impo` FOREIGN KEY (`level_id`) REFERENCES `core_importancelevel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_userleveltask`
--

LOCK TABLES `task_userleveltask` WRITE;
/*!40000 ALTER TABLE `task_userleveltask` DISABLE KEYS */;
INSERT INTO `task_userleveltask` VALUES (1,'╨Я╨╛╤Б╤В╨░╨╜╨╛╨▓╤Й╨╕╨║',3),(2,'╨Ю╤В╨▓╨╡╤В╤Б╤В╨▓╨╡╨╜╨╜╤Л╨╣',3),(3,'╨б╨╛╨╕╤Б╨┐╨╛╨╗╨╜╨╕╤В╨╡╨╗╤М',2),(4,'╨Э╨░╨▒╨╗╤О╨┤╨░╤В╨╡╨╗╤М',1);
/*!40000 ALTER TABLE `task_userleveltask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `task_usertotask`
--

DROP TABLE IF EXISTS `task_usertotask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task_usertotask` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `level_id` bigint NOT NULL,
  `task_id` bigint NOT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `task_userpositiontasktotask_task_id_ab7a4a2d_fk_task_task_id` (`task_id`),
  KEY `task_userpositiontas_user_id_7148764b_fk_user_user` (`user_id`),
  KEY `task_usertotask_level_id_1cfc1b8b_fk_task_userleveltask_id` (`level_id`),
  CONSTRAINT `task_userpositiontas_user_id_7148764b_fk_user_user` FOREIGN KEY (`user_id`) REFERENCES `user_userprofile` (`id`),
  CONSTRAINT `task_userpositiontasktotask_task_id_ab7a4a2d_fk_task_task_id` FOREIGN KEY (`task_id`) REFERENCES `task_task` (`id`),
  CONSTRAINT `task_usertotask_level_id_1cfc1b8b_fk_task_userleveltask_id` FOREIGN KEY (`level_id`) REFERENCES `task_userleveltask` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task_usertotask`
--

LOCK TABLES `task_usertotask` WRITE;
/*!40000 ALTER TABLE `task_usertotask` DISABLE KEYS */;
INSERT INTO `task_usertotask` VALUES (1,'2023-11-02 17:39:07.779738',2,1,1),(2,'2023-11-03 00:28:04.794499',2,3,1),(3,'2023-11-15 19:02:54.613979',2,4,1),(4,'2023-11-15 19:42:56.110372',2,5,1),(5,'2023-11-15 19:42:59.049579',2,6,1);
/*!40000 ALTER TABLE `task_usertotask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_department`
--

DROP TABLE IF EXISTS `user_department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_department` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_department`
--

LOCK TABLES `user_department` WRITE;
/*!40000 ALTER TABLE `user_department` DISABLE KEYS */;
INSERT INTO `user_department` VALUES (1,'╨Ъ╨╛╨╢╨╡╨▓╨╜╨╕╨║');
/*!40000 ALTER TABLE `user_department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_userprofile`
--

DROP TABLE IF EXISTS `user_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `user_id` int NOT NULL,
  `department_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `user_userprofile_department_id_d60a64b8_fk_user_department_id` (`department_id`),
  CONSTRAINT `user_userprofile_department_id_d60a64b8_fk_user_department_id` FOREIGN KEY (`department_id`) REFERENCES `user_department` (`id`),
  CONSTRAINT `user_userprofile_user_id_2474538d_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_userprofile`
--

LOCK TABLES `user_userprofile` WRITE;
/*!40000 ALTER TABLE `user_userprofile` DISABLE KEYS */;
INSERT INTO `user_userprofile` VALUES (1,'╨Ш╨▓╨░╨╜ ╨Я╨╕╨▓╨░╨╜╤Л╤З','user/images/1.png',1,1),(2,NULL,'',2,1);
/*!40000 ALTER TABLE `user_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-11-30 18:29:46
