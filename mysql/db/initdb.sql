-- MySQL dump 10.13  Distrib 8.0.41, for macos15 (x86_64)
--
-- Host: 127.0.0.1    Database: fastapi_app
-- ------------------------------------------------------
-- Server version	8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Historial_Tarea`
--

DROP TABLE IF EXISTS `Historial_Tarea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Historial_Tarea` (
  `id_historial_tarea` int NOT NULL AUTO_INCREMENT,
  `id_tarea` int DEFAULT NULL,
  `estado_anterior_historial_tarea` varchar(20) DEFAULT NULL,
  `estado_nuevo_historial_tarea` varchar(20) DEFAULT NULL,
  `fecha_cambio_historial_tarea` date DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_historial_tarea`),
  KEY `fk_historial_tarea_tarea` (`id_tarea`),
  KEY `fk_historial_tarea_usuario` (`id_usuario`),
  CONSTRAINT `fk_historial_tarea_tarea` FOREIGN KEY (`id_tarea`) REFERENCES `Tarea` (`id_tarea`),
  CONSTRAINT `fk_historial_tarea_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Historial_Tarea`
--

LOCK TABLES `Historial_Tarea` WRITE;
/*!40000 ALTER TABLE `Historial_Tarea` DISABLE KEYS */;
/*!40000 ALTER TABLE `Historial_Tarea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Proyecto`
--

DROP TABLE IF EXISTS `Proyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Proyecto` (
  `id_proyecto` int NOT NULL AUTO_INCREMENT,
  `nombre_proyecto` varchar(50) DEFAULT NULL,
  `descripcion_proyecto` text,
  `id_usuario` int DEFAULT NULL,
  PRIMARY KEY (`id_proyecto`),
  KEY `fk_proyecto_usuario` (`id_usuario`),
  CONSTRAINT `fk_proyecto_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Proyecto`
--

LOCK TABLES `Proyecto` WRITE;
/*!40000 ALTER TABLE `Proyecto` DISABLE KEYS */;
INSERT INTO `Proyecto` VALUES (5,'cambiado','cambiado',1),(6,'string','string',1),(7,'nuevo proyecto 2','probando',1);
/*!40000 ALTER TABLE `Proyecto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Tarea`
--

DROP TABLE IF EXISTS `Tarea`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Tarea` (
  `id_tarea` int NOT NULL AUTO_INCREMENT,
  `titulo_tarea` varchar(100) DEFAULT NULL,
  `descripcion_tarea` text,
  `estado_tarea` varchar(20) DEFAULT NULL,
  `fecha_limite_tarea` datetime DEFAULT NULL,
  `id_proyecto` int DEFAULT NULL,
  `id_usuario` int DEFAULT NULL,
  `id_responsable` int DEFAULT NULL,
  PRIMARY KEY (`id_tarea`),
  KEY `fk_tarea_proyecto` (`id_proyecto`),
  KEY `fk_tarea_usuario` (`id_usuario`),
  CONSTRAINT `fk_tarea_proyecto` FOREIGN KEY (`id_proyecto`) REFERENCES `Proyecto` (`id_proyecto`),
  CONSTRAINT `fk_tarea_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Tarea`
--

LOCK TABLES `Tarea` WRITE;
/*!40000 ALTER TABLE `Tarea` DISABLE KEYS */;
INSERT INTO `Tarea` VALUES (2,'probando','string','pendiente','2025-05-20 18:30:00',7,1,NULL),(3,'probando','string','pendiente','2025-05-20 18:30:00',7,1,NULL),(4,'probando otra vez','string','pendiente','2025-05-20 18:30:00',7,1,NULL),(5,'Realizar frontend','Se necesita realizar el desarrollo del formulario','pendiente','2028-05-22 01:09:54',7,1,2),(6,'Realizar frontend','Se necesita realizar el desarrollo del formulario','pendiente','2028-05-22 01:09:54',7,1,2);
/*!40000 ALTER TABLE `Tarea` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario`
--

DROP TABLE IF EXISTS `Usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `nombre_usuario` varchar(50) DEFAULT NULL,
  `correo_usuario` varchar(50) DEFAULT NULL,
  `clave_usuario` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario`
--

LOCK TABLES `Usuario` WRITE;
/*!40000 ALTER TABLE `Usuario` DISABLE KEYS */;
INSERT INTO `Usuario` VALUES (1,'daniel0802','danielestupi0802@gmail.com','$2b$12$G0zGmA7WEtNcXI9ccYt./OI45EdZyfaAJa4SKhPf7SXQL7MSLcBqy'),(2,'string','string','$2b$12$TYp71lhM.vVGKnmJNbWKBeKApBLcaFU3dn/cGuXJITEYNK8cvLymq');
/*!40000 ALTER TABLE `Usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Usuario_Proyecto`
--

DROP TABLE IF EXISTS `Usuario_Proyecto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Usuario_Proyecto` (
  `id_usuario_proyecto` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int DEFAULT NULL,
  `id_proyecto` int DEFAULT NULL,
  `rol_usuario_proyecto` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_usuario_proyecto`),
  KEY `fk_usuario_proyecto_usuario` (`id_usuario`),
  KEY `fk_usuario_proyecto_proyecto` (`id_proyecto`),
  CONSTRAINT `fk_usuario_proyecto_proyecto` FOREIGN KEY (`id_proyecto`) REFERENCES `Proyecto` (`id_proyecto`),
  CONSTRAINT `fk_usuario_proyecto_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `Usuario` (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Usuario_Proyecto`
--

LOCK TABLES `Usuario_Proyecto` WRITE;
/*!40000 ALTER TABLE `Usuario_Proyecto` DISABLE KEYS */;
INSERT INTO `Usuario_Proyecto` VALUES (1,1,7,'admin');
/*!40000 ALTER TABLE `Usuario_Proyecto` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-24 11:16:22
