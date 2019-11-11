CREATE TABLE `territories` (
  `Num` int NOT NULL,
  `Name` varchar(100) DEFAULT NULL,
  `Force` int(11) NOT NULL DEFAULT 0,
  `Neigbors` varchar(100),
  PRIMARY KEY (`Num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
