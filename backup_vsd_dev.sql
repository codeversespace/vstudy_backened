DROP TABLE IF EXISTS `ans_sheet`;
CREATE TABLE `ans_sheet` (
  `student_id` int DEFAULT NULL,
  `q_id` int DEFAULT NULL,
  `ans_keys` json DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `ans_sheet` VALUES("1213", "1", "{"1": "opt1", "2": "opt4"}");
INSERT INTO `ans_sheet` VALUES("1213", "1", "{"1": "opt1", "2": "opt4"}");
INSERT INTO `ans_sheet` VALUES("1213", "2", "{"3": "opt4"}");
INSERT INTO `ans_sheet` VALUES("1211", "1", "{"1": "opt2", "2": "opt4"}");
INSERT INTO `ans_sheet` VALUES("1212", "1", "{"2": "opt4"}");


DROP TABLE IF EXISTS `categories`;
CREATE TABLE `categories` (
  `cat_id` int NOT NULL AUTO_INCREMENT,
  `cat_title` varchar(255) DEFAULT NULL,
  `cat_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`cat_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `categories` VALUES("1", "Demp", "Demo Description");
INSERT INTO `categories` VALUES("2", "Second Demo", "This is second demo");
INSERT INTO `categories` VALUES("4", "thisd kjbbveruj", "sxkjvbdjvberjdf dfmjcbedjh");
INSERT INTO `categories` VALUES("5", "casjhv", "jyjvh");
INSERT INTO `categories` VALUES("6", "casjhv", "jyjvh");
INSERT INTO `categories` VALUES("7", "thi demddsd 2121", "dsdcdf dws");
INSERT INTO `categories` VALUES("8", "ddddddddddddd", "csd");


DROP TABLE IF EXISTS `level`;
CREATE TABLE `level` (
  `level_id` int NOT NULL AUTO_INCREMENT,
  `level_title` varchar(255) DEFAULT NULL,
  `level_class` varchar(255) DEFAULT NULL,
  `level_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`level_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `level` VALUES("1", "Playgroup", "[1, 2]", "This grouoconcludes hindid");


DROP TABLE IF EXISTS `mcqs`;
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
  PRIMARY KEY (`ques_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `mcqs` VALUES("1", "1", "PM of Inda", "Nitish Kumar", "Narendra Modi", "Yogi Aditynath", "Raul Gandhi", "opt2", "None", "admin", "2022-08-28 17:34:06");
INSERT INTO `mcqs` VALUES("2", "1", "Indian Cricket Team Captain?", "Rohit Sharma", "MS Dhoni", "Virat Kohli", "Rishabh Pant", "opt1", "None", "admin", "2022-08-28 17:35:19");
INSERT INTO `mcqs` VALUES("3", "2", "HTML Full Form?", "Hypertext Markup Language", "Hyper Market", "Hyppo Material Laerning Tool", "Hyperpola lnhuage Text", "opt1", "None", "admin", "2022-08-28 17:38:27");
INSERT INTO `mcqs` VALUES("4", "4", "jh", "yes it is", "no man", "come on", "oh yeah", "no man", "None", "adminDummy", "2022-08-30 13:48:39");
INSERT INTO `mcqs` VALUES("5", "4", "<p><strong>this is blunder</strong></p>", "yes it is", "no man", "come on", "oh yeah", "no man", "None", "admin(Dummy)", "2022-08-30 13:49:45");


DROP TABLE IF EXISTS `quiz`;
CREATE TABLE `quiz` (
  `q_id` int NOT NULL AUTO_INCREMENT,
  `cat_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `max_marks` int DEFAULT NULL,
  `no_of_ques` int DEFAULT NULL,
  `active` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`q_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `quiz` VALUES("1", "1", "Primay", "This is for Primary Group", "10", "5", "1");
INSERT INTO `quiz` VALUES("2", "2", "Second Demo", "This is for Second Demo", "12", "3", "1");
INSERT INTO `quiz` VALUES("3", "5", "test ", "desdc ript dfjdfn", "20", "12", "1");
INSERT INTO `quiz` VALUES("4", "4", "dsc", "csdcs", "12", "11", "0");
INSERT INTO `quiz` VALUES("5", "7", "cas", "hvghv", "5", "5", "1");


DROP TABLE IF EXISTS `subject`;
CREATE TABLE `subject` (
  `sub_id` int NOT NULL AUTO_INCREMENT,
  `sub_title` varchar(255) DEFAULT NULL,
  `sub_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`sub_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `subject` VALUES("1", "hindi", "this dsd");


DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `regId` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `class` int DEFAULT NULL,
  `school` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `regId` (`regId`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `users` VALUES("1", "5249962", "Mobs", "6", "Amrit Public School", "mobs@m.com", "9151604860", "Mobsmau");
INSERT INTO `users` VALUES("2", "5249963", "Demo", "7", "Allenhouse Business School", "demo@d.com", "1234567899", "Demo");


