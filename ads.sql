-- MySQL dump 10.13  Distrib 8.0.29, for Win64 (x86_64)
--
-- Host: localhost    Database: vstudy_dev
-- ------------------------------------------------------
-- Server version	8.0.29

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
-- Table structure for table `ans_sheet`
--

DROP TABLE IF EXISTS `ans_sheet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ans_sheet` (
  `student_id` int DEFAULT NULL,
  `q_id` int DEFAULT NULL,
  `ans_keys` json DEFAULT NULL,
  `started_at` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ans_sheet`
--

LOCK TABLES `ans_sheet` WRITE;
/*!40000 ALTER TABLE `ans_sheet` DISABLE KEYS */;
INSERT INTO `ans_sheet` VALUES (1213,1,'{\"1\": \"opt2\", \"2\": \"opt1\"}','1662814107223'),(1213,2,'{\"3\": \"opt1\"}',NULL),(1213,1,'{\"1\": \"opt2\", \"2\": \"opt1\"}','1662814107223'),(1213,2,'{\"3\": \"opt1\"}',NULL),(1213,1,'{\"1\": \"opt2\", \"2\": \"opt3\"}','1662814107223'),(1213,1,'{\"1\": \"opt2\", \"2\": \"opt3\"}','1662814107223'),(1213,7,'{\"8\": \"opt1\"}',NULL),(1213,7,'{\"8\": \"opt1\"}',NULL),(5249960,1,NULL,'1662815723695.3792'),(4343323,1,NULL,'1662816315282'),(666,1,NULL,'1662816453392'),(1211,1,'{\"1\": \"opt1\", \"2\": \"opt1\"}','1662816687117'),(1226,1,'{}','1662817451808'),(1226,2,NULL,'1662818308847'),(123,9,'{}','1662819369765'),(124,9,'{\"11\": \"opt1\"}','1662819675745');
/*!40000 ALTER TABLE `ans_sheet` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `cat_id` int NOT NULL AUTO_INCREMENT,
  `cat_title` varchar(255) DEFAULT NULL,
  `cat_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Demp','Demo Description'),(2,'Second Demo','This is second demo'),(4,'thisd kjbbveruj','sxkjvbdjvberjdf dfmjcbedjh'),(5,'casjhv','jyjvh'),(6,'casjhv','jyjvh'),(7,'thi demddsd 2121','dsdcdf dws'),(8,'ddddddddddddd','csd');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `level`
--

DROP TABLE IF EXISTS `level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `level` (
  `level_id` int NOT NULL AUTO_INCREMENT,
  `level_title` varchar(255) DEFAULT NULL,
  `level_class` varchar(255) DEFAULT NULL,
  `level_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`level_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `level`
--

LOCK TABLES `level` WRITE;
/*!40000 ALTER TABLE `level` DISABLE KEYS */;
INSERT INTO `level` VALUES (1,'Playgroup','[1, 2]','This grouoconcludes hindid');
/*!40000 ALTER TABLE `level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mcqs`
--

DROP TABLE IF EXISTS `mcqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mcqs` (
  `ques_id` int NOT NULL AUTO_INCREMENT,
  `q_id` int DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `opt1` varchar(255) DEFAULT NULL,
  `opt2` varchar(255) DEFAULT NULL,
  `opt3` varchar(255) DEFAULT NULL,
  `opt4` varchar(255) DEFAULT NULL,
  `ans` varchar(255) DEFAULT NULL,
  `image` varchar(255) DEFAULT NULL,
  `added_by` varchar(255) DEFAULT NULL,
  `date` datetime DEFAULT CURRENT_TIMESTAMP,
  `sub_id` int DEFAULT NULL,
  `class` int DEFAULT NULL,
  PRIMARY KEY (`ques_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mcqs`
--

LOCK TABLES `mcqs` WRITE;
/*!40000 ALTER TABLE `mcqs` DISABLE KEYS */;
INSERT INTO `mcqs` VALUES (1,1,'PM of Inda','Nitish Kumar','Narendra Modi','Yogi Aditynath','Raul Gandhi','opt2',NULL,'admin','2022-08-28 17:34:06',NULL,NULL),(2,1,'Indian Cricket Team Captain?','Rohit Sharma','MS Dhoni','Virat Kohli','Rishabh Pant','opt1',NULL,'admin','2022-08-28 17:35:19',NULL,NULL),(3,2,'HTML Full Form?','Hypertext Markup Language','Hyper Market','Hyppo Material Laerning Tool','Hyperpola lnhuage Text','opt1',NULL,'admin','2022-08-28 17:38:27',NULL,NULL),(4,4,'jh','yes it is','no man','come on','oh yeah','no man',NULL,'adminDummy','2022-08-30 13:48:39',NULL,NULL),(5,4,'<p><strong>this is blunder</strong></p>','yes it is','no man','come on','oh yeah','no man',NULL,'admin(Dummy)','2022-08-30 13:49:45',NULL,NULL),(6,4,'<p>asasas</p>','sssss','aaaaaa','xxxxxxxxxxx','qqqqqqqqq','opt4',NULL,'admin(Dummy)','2022-09-03 02:37:28',1,2),(7,4,'<p>qwqw</p>','qwqw','wqwq','wqwq','wqwq','opt3',NULL,'admin(Dummy)','2022-09-03 02:40:27',1,4),(8,7,'<p>Thisdhsidh</p>','qdw','jjh','jhjhn','jnjh','opt3',NULL,'admin(Dummy)','2022-09-04 17:14:33',1,4),(11,9,'<p>this is one</p>','11','122','33','44','opt1',NULL,'admin(Dummy)','2022-09-10 19:48:44',1,2),(12,9,'<p>this is second</p>','22','33','44','55','opt2',NULL,'admin(Dummy)','2022-09-10 19:49:00',1,2);
/*!40000 ALTER TABLE `mcqs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `quiz`
--

DROP TABLE IF EXISTS `quiz`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `quiz` (
  `q_id` int NOT NULL AUTO_INCREMENT,
  `cat_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `max_marks` int DEFAULT NULL,
  `no_of_ques` int DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `level_id` int DEFAULT NULL,
  `time_per_qstn_ms` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`q_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `quiz`
--

LOCK TABLES `quiz` WRITE;
/*!40000 ALTER TABLE `quiz` DISABLE KEYS */;
INSERT INTO `quiz` VALUES (1,1,'Primay','This is for Primary Group',10,5,1,NULL,'12000'),(2,2,'Second Demo','This is for Second Demo',12,3,1,NULL,NULL),(3,5,'test ','desdc ript dfjdfn',20,12,1,NULL,NULL),(4,4,'dsc','csdcs',12,11,0,NULL,NULL),(5,7,'cas','hvghv',5,5,1,NULL,NULL),(6,8,'playgroup hindi','hindi ki pariksha in english',12,12,1,NULL,NULL),(7,1,'oyurhc','jhcsdbjchds',22,22,1,1,NULL),(9,6,'ye hai india','Laud lassan',2,2,1,1,'60000');
/*!40000 ALTER TABLE `quiz` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `sub_id` int NOT NULL AUTO_INCREMENT,
  `sub_title` varchar(255) DEFAULT NULL,
  `sub_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES (1,'hindi','this dsd'),(2,'asasasa','ss');
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `regId` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `class` int DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` varchar(15) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `regId` (`regId`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,5249962,'Mobs',6,'Amrit Public School','mobs@m.com','9151604860','Mobsmau','admin'),(2,5249963,'Demo',7,'Allenhouse Business School','demo@d.com','1234567899','Demo',NULL),(3,5249960,'Syed Abdullah',2,'213','sayedabdullah11@gmail.com','2121221212','Mobsmau','user'),(4,5249969,'Syed Abdullah',2,'213','sayedabdullah11@gmail.com','2121221212','Mobsmau',NULL),(5,12190,'sayed ',2,'2312','sayedabdullah11@gmail.com','898999998','123','student'),(6,123,'name_row1',1,'school_row1','email1@gmail.com','90009.0','123.0','student'),(7,124,'name_row2',2,'school_row2','email2@gmail.com','100001.0','122.0','student'),(8,125,'name_row3',3,'school_row3','email3@gmail.com','2000002.0','124.0','student'),(9,126,'name_row4',4,'school_row4','email4@gmail.com','3000003.0','125.0','student'),(14,1223,'name_row1',1,'school_row1','email1@gmail.com','90009.0','123.0','student'),(15,1224,'name_row2',2,'school_row2','email2@gmail.com','100001.0','122.0','student'),(16,1225,'name_row3',3,'school_row3','email3@gmail.com','2000002.0','124.0','student'),(17,1226,'name_row4',4,'school_row4','email4@gmail.com','3000003.0','125.0','student'),(18,1228,'name_row1',1,'school_row1','email1@gmail.com','90009.0','123.0','student'),(19,1229,'name_row2',2,'school_row2','email2@gmail.com','100001.0','122.0','student'),(20,1211,'name_row3',3,'school_row3','email3@gmail.com','2000002.0','124.0','student'),(21,111111,'name_row4',4,'school_row4','email4@gmail.com','3000003.0','125.0','student'),(22,632332,'name_row1',1,'school_row1','email1@gmail.com','90009','123','student'),(23,44444,'name_row2',2,'school_row2','email2@gmail.com','100001','122','student'),(24,666,'name_row3',3,'school_row3','email3@gmail.com','2000002','124','student'),(25,4343323,'name_row4',4,'school_row4','email4@gmail.com','3000003','125','student');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-09-10 19:57:45
