-- MariaDB dump 10.19-11.2.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: kuma
-- ------------------------------------------------------
-- Server version	11.2.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `addresses`
--

DROP TABLE IF EXISTS `addresses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `addresses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `users_id` int(11) NOT NULL,
  `name` varchar(70) NOT NULL,
  `province` varchar(80) NOT NULL,
  `city` varchar(80) NOT NULL,
  `subdistrict` varchar(80) NOT NULL,
  `postcode` char(5) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`),
  KEY `users_id` (`users_id`),
  CONSTRAINT `addresses_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `addresses`
--

LOCK TABLES `addresses` WRITE;
/*!40000 ALTER TABLE `addresses` DISABLE KEYS */;
/*!40000 ALTER TABLE `addresses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `banners`
--

DROP TABLE IF EXISTS `banners`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `banners` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `banner` text NOT NULL,
  `links` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `banners`
--

LOCK TABLES `banners` WRITE;
/*!40000 ALTER TABLE `banners` DISABLE KEYS */;
/*!40000 ALTER TABLE `banners` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `brands`
--

DROP TABLE IF EXISTS `brands`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `brands` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `brands`
--

LOCK TABLES `brands` WRITE;
/*!40000 ALTER TABLE `brands` DISABLE KEYS */;
INSERT INTO `brands` VALUES
(1,'Adidas'),
(2,'Nike'),
(3,'Puma'),
(4,'Vans'),
(5,'Asics');
/*!40000 ALTER TABLE `brands` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `carts`
--

DROP TABLE IF EXISTS `carts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `carts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `products_id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_id` (`products_id`),
  KEY `users_id` (`users_id`),
  CONSTRAINT `carts_ibfk_1` FOREIGN KEY (`products_id`) REFERENCES `products` (`id`),
  CONSTRAINT `carts_ibfk_2` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `carts`
--

LOCK TABLES `carts` WRITE;
/*!40000 ALTER TABLE `carts` DISABLE KEYS */;
/*!40000 ALTER TABLE `carts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES
(1,'Footwear'),
(2,'Apparel'),
(3,'Accessories'),
(4,'Equipment');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genders`
--

DROP TABLE IF EXISTS `genders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `genders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genders`
--

LOCK TABLES `genders` WRITE;
/*!40000 ALTER TABLE `genders` DISABLE KEYS */;
INSERT INTO `genders` VALUES
(1,'Men'),
(2,'Women'),
(3,'Unisex'),
(4,'Kids');
/*!40000 ALTER TABLE `genders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `users_id` int(11) NOT NULL,
  `status` char(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `users_id` (`users_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `image` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES
(1,'OVO','cara-isi-ulang-saldo-ovo.jpg'),
(2,'BCA','836405_720.jpg'),
(3,'Shopee pay','shopeepay.png'),
(4,'DANA','dana.jpg');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products`
--

DROP TABLE IF EXISTS `products`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `description` text NOT NULL,
  `image` text NOT NULL,
  `sku` varchar(12) NOT NULL,
  `color` varchar(24) NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `sale` smallint(5) unsigned DEFAULT 0,
  `categories_id` int(11) NOT NULL,
  `brands_id` int(11) NOT NULL,
  `genders_id` int(11) NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `categories_id` (`categories_id`),
  KEY `brands_id` (`brands_id`),
  KEY `genders_id` (`genders_id`),
  CONSTRAINT `products_ibfk_1` FOREIGN KEY (`categories_id`) REFERENCES `categories` (`id`),
  CONSTRAINT `products_ibfk_2` FOREIGN KEY (`brands_id`) REFERENCES `brands` (`id`),
  CONSTRAINT `products_ibfk_3` FOREIGN KEY (`genders_id`) REFERENCES `genders` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products`
--

LOCK TABLES `products` WRITE;
/*!40000 ALTER TABLE `products` DISABLE KEYS */;
INSERT INTO `products` VALUES
(1,'W NIKE DUNK LOW-WHITE/BLACK-WHITE','Originally created for the hardwood, the Dunk later took to the streets—and as they say, the rest is history. More than 35 years after its debut, the silhouette still delivers bold, defiant style and remains a coveted look for crews across both sport and culture. Now, the university-hoops OG returns covered in crisp material overlays with heritage-inspired colour-blocking. Modern footwear technology brings the design\'s comfort into the 21st century, while a contrasting combination of black and white gives this make-up a clean feel.','2023-12-31_172030.392466nikdd1503101-1.webp','NIKDD1503101','Black',1549000,0,1,2,1,'2023-12-31 17:20:30'),
(2,'W NIKE DUNK LOW PRM-SPORT RED/SHEEN-STRAW-SAIL','Constructed of white and Team Red smooth leather, the Nike Dunk Low Team Red is an ode to the original look of the 1985 Nike Dunk Low. Nike embroideries on the heel tab and a woven tongue label arrive in a classic fashion. From there, a white and Team Red sole completes the design.','2023-12-31_173119.531775nike1.webp','NIKFB7910600','Red',2099000,0,1,2,1,'2023-12-31 17:31:19'),
(3,'W NIKE DUNK LOW PARRIS GOEBEL QS-PLAYFUL PINK/MULTI-COLOR-BRONZINE','Constructed of white and Team Red smooth leather, the Nike Dunk Low Team Red is an ode to the original look of the 1985 Nike Dunk Low. Nike embroideries on the heel tab and a woven tongue label arrive in a classic fashion. From there, a white and Team Red sole completes the design.','2023-12-31_173236.312626nikfn2721600-1.webp','NIKFN2721600','Pink',1909000,0,1,2,2,'2023-12-31 17:32:36'),
(4,'PUMA SLIPSTREAM LTH-PUMA WHITE-PUMA BLACK-PUMA BLACK','PUMA’s leather products support responsible manufacturing via the Leather Working Group.www.leatherworkinggroup.com','2023-12-31_173510.363658pum38754426-1.webp','PUM38754426','White',1699000,0,1,3,3,'2023-12-31 17:35:10'),
(5,'PUMA SLIPSTREAM WNS-PUMA WHITE-PUMA BLACK-GLACIER GRAY','Back in 1987, the PUMA Slipstream Mid entered the scene as a basketball sneaker. A high-flying, slam-dunking, statement-making basketball sneaker. Now, it’s joined by the Slipstream – a rework of the original that brings an all-new energy to the game while staying true to the OG’s sporting roots.','2023-12-31_174109.603486puma.webp','PUM38627003','White',1699000,60,1,3,2,'2023-12-31 17:41:09'),
(6,'PUMA SLIPSTREAM ALWAYS ON-WARM WHITE-WARM EARTH','Back in 1987, the OG PUMA Slipstream Lo entered the scene as a basketball sneaker. A high-flying, slam-dunking, statement-making basketball sneaker. Now, it’s joined by Slipstream – a rework of the original that brings an all-new energy to the game while staying true to the OG’s sporting roots.','2023-12-31_174235.439874puma1.webp','PUM39005901','White',1699000,60,1,3,3,'2023-12-31 17:42:35'),
(7,'PUMA SLIPSTREAM XTREME-PUMA WHITE-WARM WHITE-COOL LIGHT GRAY','Back in 1987, the OG PUMA Slipstream Lo entered the scene as a basketball sneaker. A high-flying, slam-dunking, statement-making basketball sneaker. Now, it’s joined by Slipstream – a rework of the original that brings an all-new energy to the game while staying true to the OG’s sporting roots.','2023-12-31_174318.411407puma1.webp','PUM39005901','White',2179000,0,1,3,3,'2023-12-31 17:43:18'),
(8,'NIKE LUNAR ROAM-ALABASTER/BLACK-LEMON DROP-GREEN ABYSS','In 2008, Lunar took its legendary lightweight bounce to the streets for the first time. Fast forward 15 years and the plush foam midsole your feet fell in love with is remastered and amplified for the city. Now equipped with breezy textiles and supportive Magwire cables in the upper, it delivers a lightweight, stable feel you\'ll want to wear season after season. And with an eye-grabbing new colourway, this pair is sure to make a bold, springy statement—wherever you roam.','2023-12-31_174435.529501puma1.webp','NIKDV2440700','Multi',2379000,0,1,2,1,'2023-12-31 17:44:35'),
(9,'ADIDAS SAMBA OG-CBLACK/FTWWHT/GUM5','Born on the pitch, the Samba is a timeless icon of street style. This silhouette stays true to its legacy with a tasteful, low-profile, soft leather upper, suede overlays and gum sole, making it a staple in everyone\'s closet - on and off the pitch.','2023-12-31_174556.494824adidas.webp','ADIB75807','Multi',2200000,0,1,1,1,'2023-12-31 17:45:56'),
(10,'ADIDAS SAMBAE W-FTWR WHITE','Born on the pitch, the Samba is a timeless icon of street style. This silhouette stays true to its legacy with a tasteful, low-profile, soft leather upper, suede overlays and gum sole, making it a staple in everyone\'s closet - on and off the pitch.','2023-12-31_174639.209558adidas.webp','ADIB75807','White',2200000,0,1,1,2,'2023-12-31 17:46:39'),
(11,'ASICS JAPAN S PS KIDS STANDARD PS -WHITE/AMETHYST','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_174936.520793asics.webp','ASC1204A008','White',799000,50,1,5,4,'2023-12-31 17:49:36'),
(12,'ASICS JAPAN S TS KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175110.485403asics1.webp','ASC1204A008','White',699000,0,1,5,4,'2023-12-31 17:51:10'),
(13,'ASICS JAPAN KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175128.225091asics1.webp','ASC1204A008','White',799000,0,1,5,4,'2023-12-31 17:51:28'),
(14,'ASICS JAPAN KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175130.436746asics1.webp','ASC1204A008','White',799000,0,1,5,4,'2023-12-31 17:51:30'),
(15,'ASICS JAPAN KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175131.899727asics1.webp','ASC1204A008','White',799000,0,1,5,4,'2023-12-31 17:51:31'),
(16,'ASICS JAPAN KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175133.283376asics1.webp','ASC1204A008','White',799000,0,1,5,4,'2023-12-31 17:51:33'),
(17,'ASICS JAPAN KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175134.534470asics1.webp','ASC1204A008','White',799000,0,1,5,4,'2023-12-31 17:51:34'),
(18,'ASICS JAPAN KIDS STANDARD TS-WHITE/CLASSIC RED','The JAPAN S™ PS shoes originally made their debut in 1981. Now they\'re back and available in kids\' sizing as the JAPAN S™ PS (Pre-School) model. This reworked iteration is formed with a low-top silhouette that\'s complete with a court-inspired toe box and throwback colorways.','2023-12-31_175135.905191asics1.webp','ASC1204A008','White',799000,0,1,5,4,'2023-12-31 17:51:35'),
(19,'VANS UA OLD SKOOL-(GUMSOLE)BLACK/MEDIUM GUM','The Gumsole Old Skool, the Vans classic skate shoe and first to bare the iconic sidestripe, is a low top lace-up featuring sturdy canvas and suede uppers with gum-coloured sidewalls. It also includes re-enforced toe caps to withstand repeated wear, padded collars for support and flexibility, and signature rubber waffle outsoles.','2023-12-31_175347.531864vanvn0001r1gi6-1.webp','VANVN0001R1G','black',1099000,0,1,4,3,'2023-12-31 17:53:47'),
(20,'VANS UA OLD SKOOL-(GUMSOLE)BLACK/MEDIUM GUM','The Gumsole Old Skool, the Vans classic skate shoe and first to bare the iconic sidestripe, is a low top lace-up featuring sturdy canvas and suede uppers with gum-coloured sidewalls. It also includes re-enforced toe caps to withstand repeated wear, padded collars for support and flexibility, and signature rubber waffle outsoles.','2023-12-31_175403.581846vanvn0001r1gi6-1.webp','VANVN0001R1G','black',1099000,0,1,4,3,'2023-12-31 17:54:03'),
(21,'VANS UA OLD SKOOL-(GUMSOLE)BLACK/MEDIUM GUM','The Gumsole Old Skool, the Vans classic skate shoe and first to bare the iconic sidestripe, is a low top lace-up featuring sturdy canvas and suede uppers with gum-coloured sidewalls. It also includes re-enforced toe caps to withstand repeated wear, padded collars for support and flexibility, and signature rubber waffle outsoles.','2023-12-31_175405.051332vanvn0001r1gi6-1.webp','VANVN0001R1G','black',1099000,0,1,4,3,'2023-12-31 17:54:05'),
(22,'VANS UA OLD SKOOL-(GUMSOLE)BLACK/MEDIUM GUM','The Gumsole Old Skool, the Vans classic skate shoe and first to bare the iconic sidestripe, is a low top lace-up featuring sturdy canvas and suede uppers with gum-coloured sidewalls. It also includes re-enforced toe caps to withstand repeated wear, padded collars for support and flexibility, and signature rubber waffle outsoles.','2023-12-31_175406.458320vanvn0001r1gi6-1.webp','VANVN0001R1G','black',1099000,0,1,4,3,'2023-12-31 17:54:06'),
(23,'VANS UA OLD SKOOL-(GUMSOLE)BLACK/MEDIUM GUM','The Gumsole Old Skool, the Vans classic skate shoe and first to bare the iconic sidestripe, is a low top lace-up featuring sturdy canvas and suede uppers with gum-coloured sidewalls. It also includes re-enforced toe caps to withstand repeated wear, padded collars for support and flexibility, and signature rubber waffle outsoles.','2023-12-31_175408.055838vanvn0001r1gi6-1.webp','VANVN0001R1G','black',1099000,0,1,4,3,'2023-12-31 17:54:08');
/*!40000 ALTER TABLE `products` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_orders`
--

DROP TABLE IF EXISTS `products_orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_orders` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `orders_id` int(11) NOT NULL,
  `products_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `orders_id` (`orders_id`),
  KEY `products_id` (`products_id`),
  CONSTRAINT `products_orders_ibfk_1` FOREIGN KEY (`orders_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `products_orders_ibfk_2` FOREIGN KEY (`products_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_orders`
--

LOCK TABLES `products_orders` WRITE;
/*!40000 ALTER TABLE `products_orders` DISABLE KEYS */;
/*!40000 ALTER TABLE `products_orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `products_sizes`
--

DROP TABLE IF EXISTS `products_sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `products_sizes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `products_id` int(11) NOT NULL,
  `sizes_id` int(11) NOT NULL,
  `stocks` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `sizes_id` (`sizes_id`),
  KEY `products_id` (`products_id`),
  CONSTRAINT `products_sizes_ibfk_1` FOREIGN KEY (`sizes_id`) REFERENCES `sizes` (`id`),
  CONSTRAINT `products_sizes_ibfk_2` FOREIGN KEY (`products_id`) REFERENCES `products` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `products_sizes`
--

LOCK TABLES `products_sizes` WRITE;
/*!40000 ALTER TABLE `products_sizes` DISABLE KEYS */;
INSERT INTO `products_sizes` VALUES
(1,1,12,5),
(2,1,13,10),
(3,1,15,3),
(4,2,11,22),
(5,2,10,60),
(6,2,13,46),
(7,3,10,27),
(8,3,15,77),
(9,3,7,19),
(10,4,15,83),
(11,4,9,56),
(12,4,16,11),
(13,5,14,93),
(14,5,16,67),
(15,5,11,35),
(16,6,18,47),
(17,6,15,72),
(18,6,7,71),
(19,7,16,41),
(20,7,20,99),
(21,7,11,52),
(22,8,10,88),
(23,8,12,78),
(24,8,18,16),
(25,9,17,24),
(26,9,19,91),
(27,9,15,65),
(28,10,12,89),
(29,10,15,48),
(30,10,14,39),
(31,11,13,74),
(32,11,18,13),
(33,11,12,29),
(34,12,14,50),
(35,12,13,66),
(36,12,15,31),
(37,13,19,57),
(38,13,14,44),
(39,13,10,28),
(40,14,15,69),
(41,14,19,96),
(42,14,12,86),
(43,15,11,12),
(44,15,14,63),
(45,15,19,34),
(46,16,10,17),
(47,16,18,75),
(48,16,15,53),
(49,17,20,55),
(50,17,19,33),
(51,17,18,59),
(52,18,11,13),
(53,18,13,20),
(54,18,15,92),
(55,19,12,15),
(56,19,16,14),
(57,19,18,23),
(58,20,15,64),
(59,20,19,26),
(60,20,17,18),
(61,21,18,79),
(62,21,12,22),
(63,21,20,37),
(64,22,16,16),
(65,22,19,25),
(66,22,11,40),
(67,23,13,98),
(68,23,20,61),
(69,23,15,43);
/*!40000 ALTER TABLE `products_sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shippings`
--

DROP TABLE IF EXISTS `shippings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shippings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  `cost` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shippings`
--

LOCK TABLES `shippings` WRITE;
/*!40000 ALTER TABLE `shippings` DISABLE KEYS */;
/*!40000 ALTER TABLE `shippings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sizes`
--

DROP TABLE IF EXISTS `sizes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sizes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sizes`
--

LOCK TABLES `sizes` WRITE;
/*!40000 ALTER TABLE `sizes` DISABLE KEYS */;
INSERT INTO `sizes` VALUES
(1,'XS'),
(2,'S'),
(3,'M'),
(4,'L'),
(5,'XL'),
(6,'XXL'),
(7,'35'),
(8,'36'),
(9,'37'),
(10,'38'),
(11,'39'),
(12,'40'),
(13,'41'),
(14,'42'),
(15,'43'),
(16,'44'),
(17,'45'),
(18,'46'),
(19,'47'),
(20,'48');
/*!40000 ALTER TABLE `sizes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(90) NOT NULL,
  `email` varchar(125) NOT NULL,
  `password` char(60) NOT NULL,
  `roles` char(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'admin','admin@gmail.com','$2b$12$7gPXEv7lfIicp.brjv53l.769kD8/xr.f0xioBq2sIdsE963XaMfC','1');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `wishlists`
--

DROP TABLE IF EXISTS `wishlists`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `wishlists` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `products_id` int(11) NOT NULL,
  `users_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `products_id` (`products_id`),
  KEY `users_id` (`users_id`),
  CONSTRAINT `wishlists_ibfk_1` FOREIGN KEY (`products_id`) REFERENCES `products` (`id`),
  CONSTRAINT `wishlists_ibfk_2` FOREIGN KEY (`users_id`) REFERENCES `users` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `wishlists`
--

LOCK TABLES `wishlists` WRITE;
/*!40000 ALTER TABLE `wishlists` DISABLE KEYS */;
/*!40000 ALTER TABLE `wishlists` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-31 19:22:05
