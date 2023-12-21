-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1
-- Généré le : jeu. 21 déc. 2023 à 18:26
-- Version du serveur : 10.4.27-MariaDB
-- Version de PHP : 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `electricity_bill_management_system_db`
--

-- --------------------------------------------------------

--
-- Structure de la table `bill`
--

CREATE TABLE `bill` (
  `bill_id` int(11) NOT NULL,
  `bill_date` date NOT NULL,
  `due_date` date NOT NULL,
  `total_amount` float NOT NULL,
  `payment_status` tinyint(1) NOT NULL,
  `meter_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `electricity_reading`
--

CREATE TABLE `electricity_reading` (
  `reading_id` int(11) NOT NULL,
  `reading_date` date NOT NULL,
  `reading_value` int(11) NOT NULL,
  `meter_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `electricity_reading`
--

INSERT INTO `electricity_reading` (`reading_id`, `reading_date`, `reading_value`, `meter_id`) VALUES
(30009, '2020-12-12', 349, 5950);

-- --------------------------------------------------------

--
-- Structure de la table `meter`
--

CREATE TABLE `meter` (
  `meter_id` int(11) NOT NULL,
  `meter_location` text NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `meter`
--

INSERT INTO `meter` (`meter_id`, `meter_location`, `user_id`) VALUES
(5950, 'hdazfz ighr', 9786);

-- --------------------------------------------------------

--
-- Structure de la table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `firstname` varchar(20) NOT NULL,
  `lastname` varchar(20) NOT NULL,
  `address` text NOT NULL,
  `phone_number` int(11) NOT NULL,
  `email` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `user`
--

INSERT INTO `user` (`user_id`, `firstname`, `lastname`, `address`, `phone_number`, `email`) VALUES
(9786, 'khalil', 'chai', 'gzeragezg', 642661, 'zfefzfezfe@zefze'),
(12786, 'zakaria', 'zouhir', 'gzeragezg', 98, 'zfefzfezfe@zefze');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `bill`
--
ALTER TABLE `bill`
  ADD PRIMARY KEY (`bill_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `meter_id` (`meter_id`);

--
-- Index pour la table `electricity_reading`
--
ALTER TABLE `electricity_reading`
  ADD PRIMARY KEY (`reading_id`),
  ADD KEY `meter_id_ER` (`meter_id`);

--
-- Index pour la table `meter`
--
ALTER TABLE `meter`
  ADD PRIMARY KEY (`meter_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Index pour la table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `bill`
--
ALTER TABLE `bill`
  MODIFY `bill_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- AUTO_INCREMENT pour la table `electricity_reading`
--
ALTER TABLE `electricity_reading`
  MODIFY `reading_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30010;

--
-- AUTO_INCREMENT pour la table `meter`
--
ALTER TABLE `meter`
  MODIFY `meter_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9869;

--
-- AUTO_INCREMENT pour la table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12787;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `bill`
--
ALTER TABLE `bill`
  ADD CONSTRAINT `bill_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `meter_id` FOREIGN KEY (`meter_id`) REFERENCES `meter` (`meter_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `electricity_reading`
--
ALTER TABLE `electricity_reading`
  ADD CONSTRAINT `meter_id_ER` FOREIGN KEY (`meter_id`) REFERENCES `meter` (`meter_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Contraintes pour la table `meter`
--
ALTER TABLE `meter`
  ADD CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
