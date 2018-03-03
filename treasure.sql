-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 03, 2018 at 07:40 PM
-- Server version: 5.7.21-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `treasure`
--

-- --------------------------------------------------------

--
-- Table structure for table `articles`
--

CREATE TABLE `articles` (
  `id` int(11) NOT NULL,
  `store_id` int(11) DEFAULT NULL,
  `category_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(100) NOT NULL,
  `body` text NOT NULL,
  `create_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `articles`
--

INSERT INTO `articles` (`id`, `store_id`, `category_id`, `title`, `author`, `body`, `create_date`) VALUES
(1, 1, 0, 'The Last Day', 'Janice', 'Flask-MySQLdb depends, and will install for you, recent versions of Flask (0.10.1 or later) and mysqlclient. Flask-MySQLdb is compatible with and tested on Python 2.7, 3.4 and 3.5.', '2018-02-12 03:08:50'),
(2, NULL, 0, 'Python Flask', 'Anna', '<p>If you go that way, yes. It didn&#39;t work for me, and following @Divz&#39;s answer seems way easier to me, anyway -- What I would suggest is using dpkg --get-selections | grep mysql-server- to get your exact MySQL version, then go for sudo dpkg-reconfigure mysql-server-5.x (replace 5.x with your server version, btw). I commented @Divz&#39;s answer with this precision, but it&#39;s masked by the several &quot;thanks&quot; comments. Come to see the detail information about it</p>', '2018-02-12 03:08:50'),
(4, 1, 0, 'Tomorrow', 'angelo', '<p>Tomorrow is the next day of yesterday! yessss</p>', '2018-02-14 10:47:31'),
(5, NULL, 0, 'Treasure Island', 'angelo', '<p><strong>Outline buttons</strong></p><p>In need of a button, but not the hefty background colors they bring? Replace the default modifier classes with the .btn-outline-* ones to remove all background images and colors on any button.</p>', '2018-02-14 12:32:05'),
(6, NULL, 0, '205CDE', 'angelo', '<p><strong>This is 205CDE page</strong></p>', '2018-03-03 09:41:21');

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `store_id` int(11) DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  `book_name` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `ISBN` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `issue_date` varchar(255) DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `store_id`, `category_id`, `book_name`, `author`, `ISBN`, `publisher`, `issue_date`, `price`, `create_at`) VALUES
(1, 1, 2, 'The Healing Self', 'Deepak Chopra, Rudolph E.', NULL, 'Rider', '2012', 195, '2018-02-22 08:48:12'),
(2, 1, 3, '12 Rules for Life: An Antidote to Chaos', 'Jordan Peterson', '9780241351642', 'Allen Lane', '1998', 225, '2018-02-22 08:50:27'),
(3, 3, 7, 'Is Shame Necessary?: New Uses for an Old Tool(HB)', 'Jennifer Jacquet', '9781846146114', 'Allen Lane', '2006', 288, '2018-02-22 08:52:33'),
(4, 2, 8, 'When: The Scientific Secrets of Perfect Timing', 'Daniel H. Pink', '9780525535041', 'RiverHead Books', '2017', 171, '2018-02-22 08:55:02');

-- --------------------------------------------------------

--
-- Table structure for table `categories`
--

CREATE TABLE `categories` (
  `id` int(11) NOT NULL,
  `category` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `categories`
--

INSERT INTO `categories` (`id`, `category`) VALUES
(1, 'Dictionary & Reference'),
(2, 'Language'),
(3, 'History'),
(4, 'Biography & Memoir'),
(5, 'Philosophy'),
(6, 'Religion'),
(7, 'Social Science'),
(8, 'Education'),
(9, 'Business & Finance'),
(10, 'Computer & Information Technology'),
(11, 'Engineering'),
(12, 'Natural Science'),
(13, 'Health & Medicine'),
(14, 'Art'),
(15, 'Leisure'),
(16, 'Geography & Travel'),
(17, 'Children'),
(18, 'Self-Help'),
(19, 'Other');

-- --------------------------------------------------------

--
-- Table structure for table `stores`
--

CREATE TABLE `stores` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `profile` varchar(255) DEFAULT NULL,
  `contact` varchar(255) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `create_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `stores`
--

INSERT INTO `stores` (`id`, `user_id`, `name`, `profile`, `contact`, `address`, `create_at`) VALUES
(1, 1, 'I-Book', 'well', '12344321', 'CityU, Kowloon Tong, KLN, HK', '2018-02-14 11:52:49'),
(2, 1, 'Angel\'s Store', '', NULL, 'yesyesyes', '2018-02-14 12:09:11'),
(3, 2, 'Amazon book store', 'babalala', NULL, NULL, '2018-02-19 07:49:54'),
(4, 1, '205CDE', 'Founded in 2008, Stack Overflow is the largest, most trusted online community for developers to learn, share their knowledge, and build their careers.', '88886987', 'TEST', '2018-03-03 09:07:45');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `username` varchar(30) NOT NULL,
  `password` varchar(255) NOT NULL,
  `register_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `username`, `password`, `register_date`) VALUES
(1, 'angelo', 'angelo@gmail.com', 'angelo', '$5$rounds=535000$7hGvZZRKukk1eTMe$GwCAl..A04bLVvgxO8rs6YXVyyJTqXeRHWRPgUOBDz5', '2018-02-12 05:01:36'),
(2, 'Janice', 'janice@gmail.com', 'Janice', 'janice', '2018-03-03 09:12:57'),
(3, 'Annn', 'ann@gmail.com', 'Annn', 'Annn', '2018-03-03 09:12:57');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `articles`
--
ALTER TABLE `articles`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `categories`
--
ALTER TABLE `categories`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stores`
--
ALTER TABLE `stores`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `articles`
--
ALTER TABLE `articles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `categories`
--
ALTER TABLE `categories`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `stores`
--
ALTER TABLE `stores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
