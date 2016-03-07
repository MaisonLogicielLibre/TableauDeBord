-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 22, 2016 at 02:10 PM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `tableauDeBord`
--

--
-- Dumping data for table `auth_group`
--

INSERT INTO `auth_group` (`id`, `name`) VALUES
(2, 'Centech'),
(3, 'Executive');

--
-- Dumping data for table `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$20000$x25W2qMuq5ax$56IyxPyMHD0CDqFmFzZyKeAlYZO0I9J/AE+mqgYYWr4=', '2016-02-22 19:08:43', 1, 'root', '', '', 'rignon.noel@openmailbox.org', 1, 1, '2015-09-18 15:32:12'),
(2, 'pbkdf2_sha256$20000$fUI2vCETUAW0$bTWfbVMZ5/NqDZubaKRssP0YzQ7KEHUMqf+5bK+vZ8A=', '2015-09-20 20:06:02', 0, 'exec', '', '', '', 0, 1, '2015-09-20 20:04:37');

--
-- Dumping data for table `auth_user_groups`
--

INSERT INTO `auth_user_groups` (`id`, `user_id`, `group_id`) VALUES
(1, 1, 2),
(2, 2, 3);

--
-- Dumping data for table `home_userprofile`
--

INSERT INTO `home_userprofile` (`userProfile_id`, `phone`, `website`, `picture`, `user_id`, `facebook`, `googlePlus`, `linkedIn`, `twitter`) VALUES
(1, '', '', '', 1, NULL, NULL, NULL, NULL),
(2, '', '', '', 2, '', '', '', '');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
