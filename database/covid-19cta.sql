-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 05, 2024 at 02:29 PM
-- Server version: 10.1.38-MariaDB
-- PHP Version: 7.1.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `covid`
--

-- --------------------------------------------------------

--
-- Table structure for table `survey`
--

CREATE TABLE `survey` (
  `id` int(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `age` varchar(200) NOT NULL,
  `phone` longtext NOT NULL,
  `symptoms` longtext NOT NULL,
  `symptops_started` longtext NOT NULL,
  `closeness` longtext NOT NULL,
  `other_medical_issues` longtext NOT NULL,
  `family_members` longtext NOT NULL,
  `any_recent_travel` longtext NOT NULL,
  `same_symptoms` longtext NOT NULL,
  `create_date` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `survey`
--

INSERT INTO `survey` (`id`, `name`, `age`, `phone`, `symptoms`, `symptops_started`, `closeness`, `other_medical_issues`, `family_members`, `any_recent_travel`, `same_symptoms`, `create_date`) VALUES
(1, 'JohnDoe', '41', '+353439890123', 'Symptoms are chills, fever and sweating, usually occurring a few weeks after being bitten.\r\n', 'Three weeks ago that is 21st March 2024', 'No ', 'Yes, Symptoms are chills, fever and sweating, usually occurring a few weeks after being bitten.\r\n', '4', 'Yes, I travelled Lucan from Citywest', 'No', '2024-04-11 11:04:00.008994'),
(2, 'JaneDoe', '37', '+35312349280', 'Symptoms are chills, fever and sweating, usually occurring a few weeks after being bitten.\r\n', 'Three weeks ago that is 21st March 2024', 'Yes, On 23rd March 2024', 'No', '4', 'Yes , From Blackrock to City Center', 'Yes, My brother has fever and sweating,', '2024-04-11 11:12:06.411307');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--
CREATE TABLE `users` (
  `id` int(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `email` varchar(200) NOT NULL,
  `username` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`) VALUES
(1, 'JohnDoe', 'johndoe@email.com', 'john', '$5$rounds=535000$0XqrU7X1Uim2Vd89$QhWdhd2iMrsAC2KcAG1sFTnGfvKBg4EEmmVFBzexOQ0');
