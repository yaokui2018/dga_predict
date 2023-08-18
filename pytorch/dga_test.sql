# Host: localhost  (Version: 5.5.53)
# Date: 2023-08-12 23:16:53
# Generator: MySQL-Front 5.3  (Build 4.234)

/*!40101 SET NAMES utf8 */;

#
# Structure for table "dga"
#

DROP TABLE IF EXISTS `dga`;
CREATE TABLE `dga` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) DEFAULT NULL,
  `label` tinyint(3) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "dga"
#

/*!40000 ALTER TABLE `dga` DISABLE KEYS */;
INSERT INTO `dga` VALUES (1,'buymashop.net',0),(2,'hjy1314.com',0),(3,'hostsrv.org',0),(4,'qopsykurbvhd.biz',1),(5,'rgfoeutppkhu.org',1),(6,'urcareylqoto.ru',1),(7,'hekaya.news',0),(8,'for68.com',0),(9,'ljvxtcwpjncldf.com',1);
/*!40000 ALTER TABLE `dga` ENABLE KEYS */;
