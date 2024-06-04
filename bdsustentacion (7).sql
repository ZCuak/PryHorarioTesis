-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 03-06-2024 a las 22:51:49
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.1.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bdsustentacion`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_curso`
--

CREATE TABLE `app_curso` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_curso`
--

INSERT INTO `app_curso` (`id`, `nombre`) VALUES
(3, 'Proyecto de Investigación'),
(4, 'Seminario de Tesis II');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_cursos_grupos`
--

CREATE TABLE `app_cursos_grupos` (
  `id` int(11) NOT NULL,
  `curso_id` int(11) NOT NULL,
  `grupo_id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `semestre_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_cursos_grupos`
--

INSERT INTO `app_cursos_grupos` (`id`, `curso_id`, `grupo_id`, `profesor_id`, `semestre_id`) VALUES
(8, 3, 2, 13, 1),
(10, 4, 2, 13, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_estudiante`
--

CREATE TABLE `app_estudiante` (
  `id` int(11) NOT NULL,
  `codigo_universitario` varchar(20) NOT NULL,
  `apellidos_nombres` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_estudiante`
--

INSERT INTO `app_estudiante` (`id`, `codigo_universitario`, `apellidos_nombres`, `email`, `telefono`) VALUES
(1, '201TD02196', 'OCROSPOMA UGAZ FRANK ANTHONY', 'frankocrospomaugaz@gmail.com', '920532729'),
(7, '201VP00835', 'CHAVARRY CAMPOS JHOSEP RICARDO', 'JCHAVARRY@gmail.com', '921335467'),
(8, '201EP02888', 'LOPEZ SILVA ROCIO DEL CARMEN', 'RLOPEZ@gmail.com', '970652316'),
(9, '171CV71666', 'SANCHEZ RIVAS JOSE CARLOS', 'JSANCHEZ@gmail.com', '954690965'),
(10, '201VP00123', 'MENDOZA CRESPO IVAN', 'IMENDOZA@gmail.com', '921331234'),
(11, '201EP02321', 'TEJADA TORRES ERIKA', 'ETEJADA@gmail.com', '970654321'),
(12, '171CV71444', 'VARGAS POLO PAUL', 'PVARGAS@gmail.com', '954698888');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_grupo`
--

CREATE TABLE `app_grupo` (
  `id` int(11) NOT NULL,
  `nombre` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_grupo`
--

INSERT INTO `app_grupo` (`id`, `nombre`) VALUES
(2, 'A'),
(3, 'B'),
(4, 'C');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_horario_sustentaciones`
--

CREATE TABLE `app_horario_sustentaciones` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `sustentacion_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_profesor`
--

CREATE TABLE `app_profesor` (
  `id` int(11) NOT NULL,
  `email` varchar(100) NOT NULL,
  `apellidos_nombres` varchar(100) NOT NULL,
  `dedicacion` enum('TC','TP') NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_profesor`
--

INSERT INTO `app_profesor` (`id`, `email`, `apellidos_nombres`, `dedicacion`, `telefono`, `user_id`) VALUES
(10, 'ralarcon@usat.edu.pe', 'ALARCON GARCIA ROGER ERNESTO', 'TP', '987654321', 10),
(11, 'maranguri@usat.edu.pe', 'ARANGURI GARCIA MARIA YSABEL', 'TC', '912345678', 11),
(12, 'hzelada@usat.edu.pe', 'ZELADA VALDIVIESO HECTOR MIGUEL', 'TC', '938359471', 12),
(13, 'jaquino@usat.edu.pe', 'AQUINO TRUJILLO JURY YESENIA', 'TC', '985746213', 16),
(20, 'hmera@usat.edu.pe', 'MERA MONTENEGRO HUILDER JUANITO', 'TP', '987654321', 17),
(21, 'riman@usat.edu.pe', 'IMAN ESPINOZA RICARDO DAVID', 'TC', '938359471', 19),
(22, 'consuelo@usat.edu.pe', 'DEL CASTILLO CASTRO CONSUELO', 'TC', '936329471', 20),
(23, 'zumaran@usat.edu.pe', 'CASTILLO ZUMARAN SEGUNDO', 'TC', '938356571', 21),
(26, 'kreyes@usat.edu.pe', 'REYES BURGOS KARLA CECILIA', 'TC', '958746123', 24),
(27, 'mvilchez@usat.edu.pe', 'VILCHEZ RIVAS MARLON EUGENIO', 'TC', '958653214', 25);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_profesores_semestre_academico`
--

CREATE TABLE `app_profesores_semestre_academico` (
  `id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `semestre_id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_profesores_semestre_academico`
--

INSERT INTO `app_profesores_semestre_academico` (`id`, `profesor_id`, `semestre_id`, `fecha`, `hora_inicio`, `hora_fin`) VALUES
(30, 10, 1, '2024-05-06', '13:30:00', '16:30:00'),
(31, 10, 1, '2024-05-07', '15:30:00', '20:00:00'),
(32, 10, 1, '2024-05-08', '14:30:00', '16:00:00'),
(33, 10, 1, '2024-05-09', '18:30:00', '21:00:00'),
(34, 10, 1, '2024-05-10', '15:30:00', '18:00:00'),
(35, 10, 1, '2024-05-13', '15:30:00', '18:00:00'),
(36, 10, 1, '2024-05-14', '19:30:00', '22:30:00'),
(37, 10, 1, '2024-05-15', '16:00:00', '19:30:00'),
(38, 10, 1, '2024-05-16', '20:00:00', '23:30:00'),
(39, 10, 1, '2024-05-17', '16:30:00', '23:00:00'),
(40, 21, 1, '2024-05-06', '15:00:00', '19:00:00'),
(41, 21, 1, '2024-05-07', '16:30:00', '20:30:00'),
(42, 21, 1, '2024-05-08', '19:00:00', '22:00:00'),
(43, 21, 1, '2024-05-09', '15:00:00', '18:00:00'),
(44, 21, 1, '2024-05-10', '18:30:00', '23:00:00'),
(45, 21, 1, '2024-05-09', '20:30:00', '23:00:00'),
(46, 21, 1, '2024-05-13', '09:30:00', '13:30:00'),
(47, 21, 1, '2024-05-14', '15:00:00', '17:00:00'),
(48, 21, 1, '2024-05-15', '14:30:00', '15:00:00'),
(49, 21, 1, '2024-05-16', '11:00:00', '12:30:00'),
(50, 21, 1, '2024-05-17', '14:30:00', '16:30:00'),
(51, 10, 1, '2024-04-01', '17:00:00', '20:00:00'),
(52, 10, 1, '2024-04-02', '20:00:00', '22:30:00'),
(53, 10, 1, '2024-04-03', '18:00:00', '20:00:00'),
(54, 10, 1, '2024-04-04', '18:30:00', '21:00:00'),
(55, 10, 1, '2024-04-05', '18:00:00', '21:00:00'),
(56, 21, 1, '2024-04-01', '19:30:00', '22:30:00'),
(57, 21, 1, '2024-04-02', '19:00:00', '21:30:00'),
(58, 21, 1, '2024-04-03', '20:30:00', '22:00:00'),
(59, 21, 1, '2024-04-04', '17:30:00', '19:30:00'),
(60, 21, 1, '2024-04-05', '18:30:00', '21:00:00'),
(61, 27, 1, '2024-05-06', '20:30:00', '22:00:00'),
(62, 27, 1, '2024-05-07', '18:00:00', '22:00:00'),
(63, 27, 1, '2024-05-08', '20:30:00', '22:30:00'),
(64, 27, 1, '2024-05-09', '18:30:00', '19:30:00'),
(65, 27, 1, '2024-05-10', '17:30:00', '21:30:00'),
(66, 27, 1, '2024-05-06', '20:30:00', '22:00:00'),
(67, 27, 1, '2024-05-07', '18:00:00', '22:00:00'),
(68, 27, 1, '2024-05-08', '20:30:00', '22:30:00'),
(69, 27, 1, '2024-05-09', '18:30:00', '19:30:00'),
(70, 27, 1, '2024-05-10', '17:30:00', '21:30:00'),
(71, 27, 1, '2024-05-13', '16:30:00', '22:00:00'),
(72, 27, 1, '2024-05-14', '19:00:00', '00:00:00'),
(73, 27, 1, '2024-05-15', '18:00:00', '21:00:00'),
(74, 27, 1, '2024-05-16', '18:00:00', '22:00:00'),
(75, 27, 1, '2024-05-17', '18:00:00', '21:30:00'),
(76, 27, 1, '2024-05-18', '20:00:00', '22:30:00'),
(77, 27, 1, '2024-05-06', '20:30:00', '22:00:00'),
(78, 27, 1, '2024-05-07', '18:00:00', '22:00:00'),
(79, 27, 1, '2024-05-08', '20:30:00', '22:30:00'),
(80, 27, 1, '2024-05-09', '18:30:00', '19:30:00'),
(81, 27, 1, '2024-05-10', '17:30:00', '21:30:00'),
(82, 27, 1, '2024-05-13', '16:30:00', '22:00:00'),
(83, 27, 1, '2024-05-14', '19:00:00', '00:00:00'),
(84, 27, 1, '2024-05-15', '18:00:00', '21:00:00'),
(85, 27, 1, '2024-05-16', '18:00:00', '22:00:00'),
(86, 27, 1, '2024-05-17', '18:00:00', '21:30:00'),
(87, 27, 1, '2024-05-18', '20:00:00', '22:30:00'),
(88, 27, 1, '2024-04-01', '17:30:00', '22:00:00'),
(89, 27, 1, '2024-04-02', '19:00:00', '20:30:00'),
(90, 27, 1, '2024-04-03', '18:30:00', '22:00:00'),
(91, 27, 1, '2024-04-04', '20:30:00', '22:00:00'),
(92, 27, 1, '2024-04-05', '18:00:00', '21:30:00'),
(93, 20, 1, '2024-04-01', '19:30:00', '22:00:00'),
(94, 20, 1, '2024-04-02', '17:00:00', '20:00:00'),
(95, 20, 1, '2024-04-03', '18:00:00', '23:00:00'),
(96, 20, 1, '2024-04-04', '20:00:00', '21:30:00'),
(97, 20, 1, '2024-04-05', '17:30:00', '20:30:00'),
(98, 20, 1, '2024-05-06', '18:00:00', '20:30:00'),
(99, 20, 1, '2024-05-07', '18:30:00', '21:30:00'),
(100, 20, 1, '2024-05-08', '17:00:00', '20:00:00'),
(101, 20, 1, '2024-05-09', '17:30:00', '21:00:00'),
(102, 20, 1, '2024-05-10', '18:00:00', '22:30:00'),
(103, 20, 1, '2024-05-13', '11:00:00', '14:30:00'),
(104, 20, 1, '2024-05-14', '17:30:00', '20:00:00'),
(105, 20, 1, '2024-05-15', '18:00:00', '21:00:00'),
(106, 20, 1, '2024-05-16', '19:30:00', '21:30:00'),
(107, 20, 1, '2024-05-17', '17:30:00', '21:00:00'),
(108, 23, 1, '2024-04-01', '18:30:00', '21:30:00'),
(109, 23, 1, '2024-04-02', '19:30:00', '21:30:00'),
(110, 23, 1, '2024-04-03', '19:30:00', '22:30:00'),
(111, 23, 1, '2024-04-04', '19:00:00', '21:00:00'),
(112, 23, 1, '2024-04-05', '19:30:00', '22:00:00'),
(113, 23, 1, '2024-05-06', '18:00:00', '20:30:00'),
(114, 23, 1, '2024-05-07', '18:00:00', '20:30:00'),
(115, 23, 1, '2024-05-08', '18:30:00', '21:00:00'),
(116, 23, 1, '2024-05-09', '18:00:00', '19:30:00'),
(117, 23, 1, '2024-05-10', '17:30:00', '20:30:00'),
(118, 23, 1, '2024-05-13', '13:30:00', '16:00:00'),
(119, 23, 1, '2024-05-14', '17:00:00', '20:30:00'),
(120, 23, 1, '2024-05-15', '17:00:00', '19:30:00'),
(121, 23, 1, '2024-05-16', '17:30:00', '20:30:00'),
(122, 23, 1, '2024-05-17', '17:30:00', '23:00:00'),
(123, 26, 1, '2024-04-01', '19:00:00', '22:30:00'),
(124, 26, 1, '2024-04-02', '19:30:00', '22:00:00'),
(125, 26, 1, '2024-04-03', '18:30:00', '20:00:00'),
(126, 26, 1, '2024-04-04', '20:00:00', '22:00:00'),
(127, 26, 1, '2024-04-05', '18:30:00', '20:30:00'),
(128, 26, 1, '2024-05-06', '19:30:00', '21:30:00'),
(129, 26, 1, '2024-05-07', '20:00:00', '22:30:00'),
(130, 26, 1, '2024-05-08', '18:30:00', '21:30:00'),
(131, 26, 1, '2024-05-09', '19:00:00', '23:00:00'),
(132, 26, 1, '2024-05-10', '20:00:00', '22:00:00'),
(133, 26, 1, '2024-05-13', '12:30:00', '16:30:00'),
(134, 26, 1, '2024-05-14', '17:00:00', '21:00:00'),
(135, 26, 1, '2024-05-15', '18:00:00', '23:00:00'),
(136, 26, 1, '2024-05-16', '19:30:00', '21:00:00'),
(137, 26, 1, '2024-05-17', '18:00:00', '20:30:00'),
(138, 11, 1, '2024-04-01', '19:30:00', '21:30:00'),
(139, 11, 1, '2024-04-02', '19:30:00', '21:00:00'),
(140, 11, 1, '2024-04-03', '18:30:00', '21:00:00'),
(141, 11, 1, '2024-04-04', '18:00:00', '19:30:00'),
(142, 11, 1, '2024-04-05', '18:30:00', '20:00:00'),
(143, 11, 1, '2024-05-06', '18:00:00', '20:00:00'),
(144, 11, 1, '2024-05-07', '17:00:00', '19:00:00'),
(145, 11, 1, '2024-05-08', '18:00:00', '19:30:00'),
(146, 11, 1, '2024-05-09', '16:00:00', '17:30:00'),
(147, 11, 1, '2024-05-10', '17:30:00', '19:30:00'),
(148, 11, 1, '2024-05-13', '18:30:00', '22:00:00'),
(149, 11, 1, '2024-05-14', '18:30:00', '20:00:00'),
(150, 11, 1, '2024-05-15', '19:00:00', '20:30:00'),
(151, 11, 1, '2024-05-16', '19:00:00', '22:00:00'),
(152, 11, 1, '2024-05-17', '17:30:00', '19:30:00'),
(153, 22, 1, '2024-04-01', '19:00:00', '21:30:00'),
(154, 22, 1, '2024-04-02', '20:00:00', '22:00:00'),
(155, 22, 1, '2024-04-03', '19:00:00', '20:30:00'),
(156, 22, 1, '2024-04-04', '19:30:00', '21:30:00'),
(157, 22, 1, '2024-04-05', '18:30:00', '20:30:00'),
(158, 22, 1, '2024-05-06', '18:30:00', '21:30:00'),
(159, 22, 1, '2024-05-07', '18:30:00', '19:30:00'),
(160, 22, 1, '2024-05-08', '19:00:00', '21:30:00'),
(161, 22, 1, '2024-05-09', '17:30:00', '19:00:00'),
(162, 22, 1, '2024-05-10', '18:30:00', '20:30:00'),
(163, 22, 1, '2024-05-13', '18:00:00', '20:30:00'),
(164, 22, 1, '2024-05-14', '18:30:00', '21:00:00'),
(165, 22, 1, '2024-05-15', '19:30:00', '21:30:00'),
(166, 22, 1, '2024-05-16', '18:30:00', '20:00:00'),
(167, 22, 1, '2024-05-17', '19:00:00', '20:30:00'),
(168, 12, 1, '2024-04-01', '19:00:00', '21:30:00'),
(169, 12, 1, '2024-04-02', '19:00:00', '21:00:00'),
(170, 12, 1, '2024-04-03', '20:30:00', '22:00:00'),
(171, 12, 1, '2024-04-04', '19:30:00', '21:30:00'),
(172, 12, 1, '2024-04-05', '20:30:00', '23:30:00'),
(173, 12, 1, '2024-05-06', '19:30:00', '21:00:00'),
(174, 12, 1, '2024-05-07', '19:30:00', '22:00:00'),
(175, 12, 1, '2024-05-08', '20:00:00', '22:30:00'),
(176, 12, 1, '2024-05-09', '19:00:00', '21:00:00'),
(177, 12, 1, '2024-05-10', '20:30:00', '22:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_profile`
--

CREATE TABLE `app_profile` (
  `id` bigint(20) NOT NULL,
  `rol` varchar(1) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_profile`
--

INSERT INTO `app_profile` (`id`, `rol`, `user_id`) VALUES
(4, 'A', 1),
(16, 'P', 10),
(17, 'P', 11),
(24, 'P', 16),
(25, 'P', 17),
(27, 'P', 19),
(28, 'P', 20),
(29, 'P', 21),
(32, 'P', 24),
(33, 'P', 25),
(34, 'P', 12);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_semana_sustentacion`
--

CREATE TABLE `app_semana_sustentacion` (
  `id` int(11) NOT NULL,
  `semestre_academico_id` int(11) NOT NULL,
  `curso_id` int(11) NOT NULL,
  `tipo_sustentacion` enum('PARCIAL','FINAL') NOT NULL,
  `semana_inicio` int(11) NOT NULL,
  `semana_fin` int(11) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `duracion_sustentacion` int(11) NOT NULL,
  `compensan_horas` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_semana_sustentacion`
--

INSERT INTO `app_semana_sustentacion` (`id`, `semestre_academico_id`, `curso_id`, `tipo_sustentacion`, `semana_inicio`, `semana_fin`, `fecha_inicio`, `fecha_fin`, `duracion_sustentacion`, `compensan_horas`) VALUES
(1, 1, 3, 'PARCIAL', 8, 9, '2024-05-06', '2024-05-18', 30, 0),
(2, 1, 4, 'PARCIAL', 5, 5, '2024-04-01', '2024-04-06', 30, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_semestreacademico`
--

CREATE TABLE `app_semestreacademico` (
  `id` int(11) NOT NULL,
  `nombre` varchar(7) NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_fin` date NOT NULL,
  `vigencia` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_semestreacademico`
--

INSERT INTO `app_semestreacademico` (`id`, `nombre`, `fecha_inicio`, `fecha_fin`, `vigencia`) VALUES
(1, '2024-I', '2024-03-20', '2024-07-15', 1),
(2, '2024-II', '2024-08-20', '2024-12-15', 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_semestre_academico_profesores`
--

CREATE TABLE `app_semestre_academico_profesores` (
  `id` int(11) NOT NULL,
  `semestre_id` int(11) NOT NULL,
  `profesor_id` int(11) NOT NULL,
  `horas_asesoria_semanal` int(2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_semestre_academico_profesores`
--

INSERT INTO `app_semestre_academico_profesores` (`id`, `semestre_id`, `profesor_id`, `horas_asesoria_semanal`) VALUES
(16, 1, 10, 2),
(17, 1, 11, 1),
(18, 1, 12, 8),
(19, 1, 20, 6),
(20, 1, 21, 8),
(21, 1, 22, 4),
(22, 1, 23, 8),
(23, 1, 26, 8),
(24, 1, 27, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_sustentacion`
--

CREATE TABLE `app_sustentacion` (
  `id` int(11) NOT NULL,
  `cursos_grupos_id` int(11) NOT NULL,
  `estudiante_id` int(11) NOT NULL,
  `jurado1_id` int(11) DEFAULT NULL,
  `jurado2_id` int(11) DEFAULT NULL,
  `asesor_id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_sustentacion`
--

INSERT INTO `app_sustentacion` (`id`, `cursos_grupos_id`, `estudiante_id`, `jurado1_id`, `jurado2_id`, `asesor_id`, `titulo`) VALUES
(14, 8, 7, NULL, NULL, 10, 'Sistema web ...'),
(15, 8, 8, NULL, NULL, 11, 'Aplicación Móvil ...'),
(16, 8, 9, NULL, NULL, 12, 'Solución de BI ...'),
(31, 10, 10, 20, 26, 22, 'Sistema web ...'),
(32, 10, 11, 12, 21, 23, 'Aplicación Móvil ...'),
(33, 10, 12, 26, 27, 12, 'Solución de BI ...'),
(60, 8, 1, NULL, NULL, 23, 'wea');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add curso', 1, 'add_curso'),
(2, 'Can change curso', 1, 'change_curso'),
(3, 'Can delete curso', 1, 'delete_curso'),
(4, 'Can view curso', 1, 'view_curso'),
(5, 'Can add grupo', 2, 'add_grupo'),
(6, 'Can change grupo', 2, 'change_grupo'),
(7, 'Can delete grupo', 2, 'delete_grupo'),
(8, 'Can view grupo', 2, 'view_grupo'),
(9, 'Can add estudiante', 3, 'add_estudiante'),
(10, 'Can change estudiante', 3, 'change_estudiante'),
(11, 'Can delete estudiante', 3, 'delete_estudiante'),
(12, 'Can view estudiante', 3, 'view_estudiante'),
(13, 'Can add profesor', 4, 'add_profesor'),
(14, 'Can change profesor', 4, 'change_profesor'),
(15, 'Can delete profesor', 4, 'delete_profesor'),
(16, 'Can view profesor', 4, 'view_profesor'),
(17, 'Can add semestre academico', 5, 'add_semestreacademico'),
(18, 'Can change semestre academico', 5, 'change_semestreacademico'),
(19, 'Can delete semestre academico', 5, 'delete_semestreacademico'),
(20, 'Can view semestre academico', 5, 'view_semestreacademico'),
(21, 'Can add cursos grupos', 6, 'add_cursosgrupos'),
(22, 'Can change cursos grupos', 6, 'change_cursosgrupos'),
(23, 'Can delete cursos grupos', 6, 'delete_cursosgrupos'),
(24, 'Can view cursos grupos', 6, 'view_cursosgrupos'),
(25, 'Can add sustentacion', 7, 'add_sustentacion'),
(26, 'Can change sustentacion', 7, 'change_sustentacion'),
(27, 'Can delete sustentacion', 7, 'delete_sustentacion'),
(28, 'Can view sustentacion', 7, 'view_sustentacion'),
(29, 'Can add horario sustentaciones', 8, 'add_horariosustentaciones'),
(30, 'Can change horario sustentaciones', 8, 'change_horariosustentaciones'),
(31, 'Can delete horario sustentaciones', 8, 'delete_horariosustentaciones'),
(32, 'Can view horario sustentaciones', 8, 'view_horariosustentaciones'),
(33, 'Can add profesores semestre academico', 9, 'add_profesoressemestreacademico'),
(34, 'Can change profesores semestre academico', 9, 'change_profesoressemestreacademico'),
(35, 'Can delete profesores semestre academico', 9, 'delete_profesoressemestreacademico'),
(36, 'Can view profesores semestre academico', 9, 'view_profesoressemestreacademico'),
(37, 'Can add semana sustentacion', 10, 'add_semanasustentacion'),
(38, 'Can change semana sustentacion', 10, 'change_semanasustentacion'),
(39, 'Can delete semana sustentacion', 10, 'delete_semanasustentacion'),
(40, 'Can view semana sustentacion', 10, 'view_semanasustentacion'),
(41, 'Can add semestre academico profesores', 11, 'add_semestreacademicoprofesores'),
(42, 'Can change semestre academico profesores', 11, 'change_semestreacademicoprofesores'),
(43, 'Can delete semestre academico profesores', 11, 'delete_semestreacademicoprofesores'),
(44, 'Can view semestre academico profesores', 11, 'view_semestreacademicoprofesores'),
(45, 'Can add log entry', 12, 'add_logentry'),
(46, 'Can change log entry', 12, 'change_logentry'),
(47, 'Can delete log entry', 12, 'delete_logentry'),
(48, 'Can view log entry', 12, 'view_logentry'),
(49, 'Can add permission', 13, 'add_permission'),
(50, 'Can change permission', 13, 'change_permission'),
(51, 'Can delete permission', 13, 'delete_permission'),
(52, 'Can view permission', 13, 'view_permission'),
(53, 'Can add group', 14, 'add_group'),
(54, 'Can change group', 14, 'change_group'),
(55, 'Can delete group', 14, 'delete_group'),
(56, 'Can view group', 14, 'view_group'),
(57, 'Can add user', 15, 'add_user'),
(58, 'Can change user', 15, 'change_user'),
(59, 'Can delete user', 15, 'delete_user'),
(60, 'Can view user', 15, 'view_user'),
(61, 'Can add content type', 16, 'add_contenttype'),
(62, 'Can change content type', 16, 'change_contenttype'),
(63, 'Can delete content type', 16, 'delete_contenttype'),
(64, 'Can view content type', 16, 'view_contenttype'),
(65, 'Can add session', 17, 'add_session'),
(66, 'Can change session', 17, 'change_session'),
(67, 'Can delete session', 17, 'delete_session'),
(68, 'Can view session', 17, 'view_session'),
(69, 'Can add profile', 20, 'add_profile'),
(70, 'Can change profile', 20, 'change_profile'),
(71, 'Can delete profile', 20, 'delete_profile'),
(72, 'Can view profile', 20, 'view_profile');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user`
--

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$600000$erSGiNKcW4hyYvrGOX6BQE$VbKU/zqg/F9sx5VqdeniI8V1VSjmF3+G6io5xJRxu1w=', '2024-06-01 19:50:17.578331', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2024-05-28 08:28:03.890795'),
(10, 'pbkdf2_sha256$600000$0sOJLKTaKV22N5RKBwSg72$W8tSkPPdLvjhx2/LuQzPcYYeMENnagttbU0g7JXR9l4=', '2024-06-01 15:53:37.921805', 0, 'ralarcon', 'ALARCON', 'GARCIA ROGER ERNESTO', 'ralarcon@usat.edu.pe', 1, 1, '2024-05-30 05:57:56.693998'),
(11, 'pbkdf2_sha256$600000$yrJurMoLQ1X1tiynQ1EkJy$zWqRnAPZYsD7Ep0dTE4XKNtVFVPDqFofPhkKkegb4/M=', '2024-06-01 19:38:07.126514', 0, 'maranguri', 'ARANGURI', 'GARCIA MARIA YSABEL', 'maranguri@usat.edu.pe', 1, 1, '2024-05-30 05:57:57.204841'),
(12, 'pbkdf2_sha256$600000$tQ5VuKQ7s4woa9Quy07w0K$WO8Atod5AdktQd+kjBx2WKShAQIVL/gC3Z2bGYr8k3o=', '2024-06-01 19:48:15.955462', 0, 'hzelada', 'ZELADA', 'VALDIVIESO HECTOR MIGUEL', 'hzelada@usat.edu.pe', 1, 1, '2024-05-30 05:57:57.711827'),
(16, 'pbkdf2_sha256$600000$ER3o8oHhUtB2DbvEcwKBoh$vsMeZS7JMkYqDN0bumx3P5alYU8YZliiNm8V/vlNrl8=', NULL, 0, 'jaquino', 'AQUINO', 'TRUJILLO JURY YESENIA', 'jaquino@usat.edu.pe', 1, 1, '2024-05-31 09:21:19.776325'),
(17, 'pbkdf2_sha256$600000$9CR4wqTDjr7PffExcJXOA6$sE0wucs7YPnd+RvD8pxJvkEZxaRz0L3UAQyqlv1V8vI=', '2024-06-01 19:16:44.356545', 0, 'mhuilder', 'MERA', 'MONTENEGRO HUILDER JUANITO', 'mhuilder@usat.edu.pe', 1, 1, '2024-05-31 09:31:46.536038'),
(19, 'pbkdf2_sha256$600000$Ix53tzmQAwmiBtyQBkdKR5$xF1wAzPHq69ZLhcTiPKLP6iqlrAWoEcNbcXcW0zUWAI=', '2024-06-01 15:57:27.265768', 0, 'riman', 'IMAN', 'ESPINOZA RICARDO DAVID', 'riman@usat.edu.pe', 1, 1, '2024-05-31 09:33:33.444534'),
(20, 'pbkdf2_sha256$600000$hKf8Tlx6fjWXuH8djMLDQX$zYtWDC/BzB31oS3VygZUzY/zutzw41MzEivhJcxB4tM=', '2024-06-01 19:43:12.063918', 0, 'consuelo', 'DEL', 'CASTILLO CASTRO CONSUELO', 'consuelo@usat.edu.pe', 1, 1, '2024-05-31 09:40:35.493314'),
(21, 'pbkdf2_sha256$600000$VQnUWuXjFDPPPGYXRSWpKr$k7Wbpg9s5cpJf3Wq2/7595qHwWVqqUixPN5Valiiyi0=', '2024-06-01 19:20:52.505575', 0, 'zumaran', 'CASTILLO', 'ZUMARAN SEGUNDO', 'zumaran@usat.edu.pe', 1, 1, '2024-05-31 09:40:35.965038'),
(24, 'pbkdf2_sha256$600000$yzZKQkzi7qjDRgc8hGe7MX$oqQbQ25PkuMDRjN2epV3GHYWYs+MszX4Efb2aBIs4vc=', '2024-06-01 19:26:48.037990', 0, 'kreyes', 'REYES', 'BURGOS KARLA CECILIA', 'kreyes@usat.edu.pe', 1, 1, '2024-05-31 10:10:07.684315'),
(25, 'pbkdf2_sha256$600000$qI9398NjQwcmPdWoAYAqgk$+3b2QNcGeTvV07EDciqqC27Uvav1qnz0zMYz3VKfZVs=', '2024-06-01 16:02:37.661956', 0, 'mvilchez', 'VILCHEZ', 'RIVAS MARLON EUGENIO', 'mvilchez@usat.edu.pe', 1, 1, '2024-05-31 10:12:42.420617');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_groups`
--

CREATE TABLE `auth_user_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `auth_user_user_permissions`
--

CREATE TABLE `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2024-05-28 08:37:33.137634', '1', 'Ocrospoma Ugaz Frank Anthony', 1, '[{\"added\": {}}]', 3, 1),
(2, '2024-05-28 08:47:03.115241', '1', '2024-II', 1, '[{\"added\": {}}]', 5, 1),
(3, '2024-05-28 08:47:51.286457', '3', 'Proyecto de Investigación', 1, '[{\"added\": {}}]', 1, 1),
(4, '2024-05-28 08:48:03.382537', '4', 'Seminario de Tesis II', 1, '[{\"added\": {}}]', 1, 1),
(5, '2024-05-28 08:51:36.568479', '2', 'A', 1, '[{\"added\": {}}]', 2, 1),
(6, '2024-05-28 08:51:39.897418', '3', 'B', 1, '[{\"added\": {}}]', 2, 1),
(7, '2024-05-28 08:51:41.635910', '4', 'C', 1, '[{\"added\": {}}]', 2, 1),
(8, '2024-05-28 10:41:10.398306', '1', '2024-I', 2, '[{\"changed\": {\"fields\": [\"Nombre\"]}}]', 5, 1),
(9, '2024-05-28 20:16:08.717787', '6', 'ZELADA VALDIVIESO HECTOR MIGUEL', 3, '', 4, 1),
(10, '2024-05-28 20:16:08.721786', '5', 'ARANGURI GARCIA MARIA YSABEL', 3, '', 4, 1),
(11, '2024-05-28 20:16:08.729949', '4', 'ALARCON GARCIA ROGER ERNESTO', 3, '', 4, 1),
(12, '2024-05-28 23:11:53.087260', '2', '2024-II', 1, '[{\"added\": {}}]', 5, 1),
(13, '2024-05-29 05:01:57.065289', '4', 'SANCHEZ RIVAS JOSE CARLOS', 3, '', 3, 1),
(14, '2024-05-29 05:01:57.069276', '3', 'LOPEZ SILVA ROCIO DEL CARMEN', 3, '', 3, 1),
(15, '2024-05-29 05:01:57.071283', '2', 'CHAVARRY CAMPOS JHOSEP RICARDO', 3, '', 3, 1),
(16, '2024-05-29 05:05:58.836875', '5', 'CHAVARRY CAMPOS JHOSEP RICARDO', 3, '', 3, 1),
(17, '2024-05-29 05:24:41.484673', '6', 'CHAVARRY CAMPOS JHOSEP RICARDO', 3, '', 3, 1),
(18, '2024-05-30 04:58:13.566994', '9', 'ZELADA VALDIVIESO HECTOR MIGUEL', 3, '', 4, 1),
(19, '2024-05-30 04:58:13.570544', '8', 'ARANGURI GARCIA MARIA YSABEL', 3, '', 4, 1),
(20, '2024-05-30 04:58:13.575541', '7', 'ALARCON GARCIA ROGER ERNESTO', 3, '', 4, 1),
(21, '2024-05-30 06:07:27.799927', '1', 'OCROSPOMA UGAZ FRANK ANTHONY', 2, '[{\"changed\": {\"fields\": [\"Apellidos nombres\"]}}]', 3, 1),
(22, '2024-05-30 23:26:40.919923', '13', 'AQUINO TRUJILLO JURY YESENIA', 1, '[{\"added\": {}}]', 4, 1),
(23, '2024-05-31 05:26:19.606172', '1', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-07 12:00:00 18:00:00', 1, '[{\"added\": {}}]', 19, 1),
(24, '2024-05-31 06:40:27.597536', '13', 'AQUINO TRUJILLO JURY YESENIA', 2, '[]', 4, 1),
(25, '2024-05-31 09:21:12.076577', '16', 'adca', 1, '[{\"added\": {}}]', 4, 1),
(26, '2024-05-31 09:21:20.299142', '13', 'AQUINO TRUJILLO JURY YESENIA', 2, '[{\"changed\": {\"fields\": [\"User\"]}}]', 4, 1),
(27, '2024-05-31 09:30:22.694898', '16', 'adca', 3, '', 4, 1),
(28, '2024-05-31 09:31:46.977831', '17', 'MERA MONTENEGRO HUILDER JUANITO', 1, '[{\"added\": {}}]', 4, 1),
(29, '2024-05-31 09:32:03.684849', '13', 'AQUINO TRUJILLO JURY YESENIA', 2, '[{\"changed\": {\"fields\": [\"Telefono\"]}}]', 4, 1),
(30, '2024-05-31 09:32:35.329087', '18', 'REYES BURGOS KARLA CECILIA', 1, '[{\"added\": {}}]', 4, 1),
(31, '2024-05-31 09:33:33.912677', '19', 'IMAN ESPINOZA RICARDO DAVID', 1, '[{\"added\": {}}]', 4, 1),
(32, '2024-05-31 09:38:12.191884', '19', 'IMAN ESPINOZA RICARDO DAVID', 3, '', 4, 1),
(33, '2024-05-31 09:38:12.195444', '18', 'REYES BURGOS KARLA CECILIA', 3, '', 4, 1),
(34, '2024-05-31 09:38:12.199424', '17', 'MERA MONTENEGRO HUILDER JUANITO', 3, '', 4, 1),
(35, '2024-05-31 09:48:41.219788', '24', 'REYES BURGOS KARLA CECILIA', 1, '[{\"added\": {}}]', 4, 1),
(36, '2024-05-31 09:48:55.465081', '20', 'MERA MONTENEGRO HUILDER JUANITO', 2, '[{\"changed\": {\"fields\": [\"Email\"]}}]', 4, 1),
(37, '2024-05-31 09:49:07.142523', '24', 'REYES BURGOS KARLA CECILIA', 2, '[{\"changed\": {\"fields\": [\"Email\"]}}]', 4, 1),
(38, '2024-05-31 10:15:09.293342', '1', '2024-I Proyecto de Investigación PARCIAL', 1, '[{\"added\": {}}]', 18, 1),
(39, '2024-05-31 10:15:25.921980', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Semana fin\", \"Fecha fin\"]}}]', 18, 1),
(40, '2024-05-31 10:16:16.778756', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Semana inicio\", \"Semana fin\", \"Fecha inicio\", \"Fecha fin\"]}}]', 18, 1),
(41, '2024-05-31 10:16:39.296689', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Semana fin\", \"Fecha fin\"]}}]', 18, 1),
(42, '2024-05-31 10:16:57.023392', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Semana fin\", \"Fecha fin\"]}}]', 18, 1),
(43, '2024-05-31 21:14:05.654413', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Fecha inicio\", \"Fecha fin\"]}}]', 18, 1),
(44, '2024-05-31 21:59:19.156106', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Fecha inicio\", \"Fecha fin\"]}}]', 18, 1),
(45, '2024-05-31 22:00:46.554940', '2', '2024-I Seminario de Tesis II PARCIAL', 1, '[{\"added\": {}}]', 18, 1),
(46, '2024-05-31 22:01:00.544730', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Fecha fin\", \"Compensan horas\"]}}]', 18, 1),
(47, '2024-05-31 22:08:22.822310', '2', ' 2024-I ALARCON GARCIA ROGER ERNESTO  2024-05-31 15:30:00 19:30:00', 2, '[{\"changed\": {\"fields\": [\"Fecha\", \"Hora inicio\", \"Hora fin\"]}}]', 19, 1),
(48, '2024-05-31 22:35:25.924796', '2', ' 2024-I ALARCON GARCIA ROGER ERNESTO  2024-05-06 15:30:00 19:30:00', 2, '[{\"changed\": {\"fields\": [\"Fecha\"]}}]', 19, 1),
(49, '2024-05-31 22:35:37.829027', '1', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-06 12:00:00 18:00:00', 2, '[{\"changed\": {\"fields\": [\"Fecha\"]}}]', 19, 1),
(50, '2024-06-01 08:06:37.016775', '1', '2024-I Proyecto de Investigación PARCIAL', 2, '[{\"changed\": {\"fields\": [\"Fecha fin\"]}}]', 18, 1),
(51, '2024-06-01 08:13:42.102967', '1', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-06 10:00:00 12:00:00', 2, '[{\"changed\": {\"fields\": [\"Hora inicio\", \"Hora fin\"]}}]', 19, 1),
(52, '2024-06-01 08:37:18.717001', '29', ' 2024-I VILCHEZ RIVAS MARLON EUGENIO  2024-05-29 14:00:00 15:00:00', 3, '', 19, 1),
(53, '2024-06-01 08:37:18.719993', '28', ' 2024-I VILCHEZ RIVAS MARLON EUGENIO  2024-05-22 14:00:00 15:00:00', 3, '', 19, 1),
(54, '2024-06-01 08:37:18.724517', '27', ' 2024-I VILCHEZ RIVAS MARLON EUGENIO  2024-05-15 14:00:00 15:00:00', 3, '', 19, 1),
(55, '2024-06-01 08:37:18.727536', '26', ' 2024-I REYES BURGOS KARLA CECILIA  2024-05-28 10:00:00 11:00:00', 3, '', 19, 1),
(56, '2024-06-01 08:37:18.730543', '25', ' 2024-I REYES BURGOS KARLA CECILIA  2024-05-21 10:00:00 11:00:00', 3, '', 19, 1),
(57, '2024-06-01 08:37:18.733059', '24', ' 2024-I REYES BURGOS KARLA CECILIA  2024-05-14 10:00:00 11:00:00', 3, '', 19, 1),
(58, '2024-06-01 08:37:18.737071', '23', ' 2024-I CASTILLO ZUMARAN SEGUNDO  2024-05-27 08:00:00 09:00:00', 3, '', 19, 1),
(59, '2024-06-01 08:37:18.740072', '22', ' 2024-I CASTILLO ZUMARAN SEGUNDO  2024-05-20 08:00:00 09:00:00', 3, '', 19, 1),
(60, '2024-06-01 08:37:18.745617', '21', ' 2024-I CASTILLO ZUMARAN SEGUNDO  2024-05-13 08:00:00 09:00:00', 3, '', 19, 1),
(61, '2024-06-01 08:37:18.748627', '20', ' 2024-I DEL CASTILLO CASTRO CONSUELO  2024-05-26 14:00:00 15:00:00', 3, '', 19, 1),
(62, '2024-06-01 08:37:18.751609', '19', ' 2024-I DEL CASTILLO CASTRO CONSUELO  2024-05-19 14:00:00 15:00:00', 3, '', 19, 1),
(63, '2024-06-01 08:37:18.754128', '18', ' 2024-I DEL CASTILLO CASTRO CONSUELO  2024-05-12 14:00:00 15:00:00', 3, '', 19, 1),
(64, '2024-06-01 08:37:18.757146', '17', ' 2024-I IMAN ESPINOZA RICARDO DAVID  2024-05-25 10:00:00 11:00:00', 3, '', 19, 1),
(65, '2024-06-01 08:37:18.760172', '16', ' 2024-I IMAN ESPINOZA RICARDO DAVID  2024-05-18 10:00:00 11:00:00', 3, '', 19, 1),
(66, '2024-06-01 08:37:18.763702', '15', ' 2024-I IMAN ESPINOZA RICARDO DAVID  2024-05-11 10:00:00 11:00:00', 3, '', 19, 1),
(67, '2024-06-01 08:37:18.765711', '14', ' 2024-I MERA MONTENEGRO HUILDER JUANITO  2024-05-24 08:00:00 09:00:00', 3, '', 19, 1),
(68, '2024-06-01 08:37:18.769694', '13', ' 2024-I MERA MONTENEGRO HUILDER JUANITO  2024-05-17 08:00:00 09:00:00', 3, '', 19, 1),
(69, '2024-06-01 08:37:18.772698', '12', ' 2024-I MERA MONTENEGRO HUILDER JUANITO  2024-05-10 08:00:00 09:00:00', 3, '', 19, 1),
(70, '2024-06-01 08:37:18.776199', '11', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-23 14:00:00 15:00:00', 3, '', 19, 1),
(71, '2024-06-01 08:37:18.779196', '10', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-16 14:00:00 15:00:00', 3, '', 19, 1),
(72, '2024-06-01 08:37:18.781198', '9', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-09 14:00:00 15:00:00', 3, '', 19, 1),
(73, '2024-06-01 08:37:18.786358', '8', ' 2024-I ARANGURI GARCIA MARIA YSABEL  2024-05-22 10:00:00 11:00:00', 3, '', 19, 1),
(74, '2024-06-01 08:37:18.788322', '7', ' 2024-I ARANGURI GARCIA MARIA YSABEL  2024-05-15 10:00:00 11:00:00', 3, '', 19, 1),
(75, '2024-06-01 08:37:18.790295', '6', ' 2024-I ARANGURI GARCIA MARIA YSABEL  2024-05-08 10:00:00 11:00:00', 3, '', 19, 1),
(76, '2024-06-01 08:37:18.793834', '5', ' 2024-I ALARCON GARCIA ROGER ERNESTO  2024-05-21 08:00:00 09:00:00', 3, '', 19, 1),
(77, '2024-06-01 08:37:18.796854', '4', ' 2024-I ALARCON GARCIA ROGER ERNESTO  2024-05-14 08:00:00 09:00:00', 3, '', 19, 1),
(78, '2024-06-01 08:37:18.799856', '3', ' 2024-I ALARCON GARCIA ROGER ERNESTO  2024-05-07 08:00:00 09:00:00', 3, '', 19, 1),
(79, '2024-06-01 08:37:18.803373', '2', ' 2024-I ALARCON GARCIA ROGER ERNESTO  2024-05-06 15:30:00 19:30:00', 3, '', 19, 1),
(80, '2024-06-01 08:37:18.806372', '1', ' 2024-I ZELADA VALDIVIESO HECTOR MIGUEL  2024-05-06 10:00:00 12:00:00', 3, '', 19, 1),
(81, '2024-06-01 19:16:01.306855', '17', 'mhuilder', 2, '[{\"changed\": {\"fields\": [\"password\"]}}]', 15, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(12, 'admin', 'logentry'),
(1, 'App', 'curso'),
(6, 'App', 'cursosgrupos'),
(3, 'App', 'estudiante'),
(2, 'App', 'grupo'),
(8, 'App', 'horariosustentaciones'),
(4, 'App', 'profesor'),
(9, 'App', 'profesoressemestreacademico'),
(19, 'App', 'profesores_semestre_academico'),
(20, 'App', 'profile'),
(10, 'App', 'semanasustentacion'),
(18, 'App', 'semana_sustentacion'),
(5, 'App', 'semestreacademico'),
(11, 'App', 'semestreacademicoprofesores'),
(7, 'App', 'sustentacion'),
(14, 'auth', 'group'),
(13, 'auth', 'permission'),
(15, 'auth', 'user'),
(16, 'contenttypes', 'contenttype'),
(17, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2024-05-28 08:26:28.689939'),
(2, 'auth', '0001_initial', '2024-05-28 08:26:29.114623'),
(3, 'admin', '0001_initial', '2024-05-28 08:26:29.220750'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-05-28 08:26:29.229785'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-05-28 08:26:29.240330'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-05-28 08:26:29.320179'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-05-28 08:26:29.367456'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-05-28 08:26:29.384122'),
(9, 'auth', '0004_alter_user_username_opts', '2024-05-28 08:26:29.392658'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-05-28 08:26:29.428816'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-05-28 08:26:29.432770'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-05-28 08:26:29.440857'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-05-28 08:26:29.458927'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-05-28 08:26:29.474000'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-05-28 08:26:29.487439'),
(16, 'auth', '0011_update_proxy_permissions', '2024-05-28 08:26:29.502500'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-05-28 08:26:29.516040'),
(18, 'sessions', '0001_initial', '2024-05-28 08:26:29.545152'),
(19, 'App', '0001_initial', '2024-05-30 04:03:09.091186'),
(20, 'App', '0002_curso_cursos_grupos_estudiante_grupo_profesor_and_more', '2024-05-30 05:32:51.961122'),
(21, 'App', '0003_curso_cursos_grupos_estudiante_grupo_profesor_and_more', '2024-05-30 05:35:47.201973');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('9lrfbbbrnezr4taoikrfz00lds6fglgi', '.eJxVjMsOwiAQRf-FtSEDQ6G6dN9vIAwzSNXQpI-V8d-1SRe6veec-1IxbWuN2yJzHFldlFGn341SfkjbAd9Tu006T22dR9K7og-66GFieV4P9--gpqV-aysQini27DF7KAU7YnJiGAxCAQy-9OceklBwnbNFUjaIRC5bhM6p9wfwDTfo:1sCwGo:UlcHJhousMN0j3HqE4bJuzsY_OUMMbTx7oHalS8lc9U', '2024-06-14 07:01:46.740696'),
('k4er0ph3bbc7v37nypk2orn6wusu2yl6', 'e30:1sCvCv:JovMIFbCL3-Q_fHAco4-XVuLuBz28jdZSCKUEQ5hqJc', '2024-06-14 05:53:41.246867'),
('pcw45anhcoas15mqvab76i6k3g8dtbs7', 'e30:1sDUg5:0ZbjCFLNlJhpPqXk4Gg0quZhJQ2NTtqZdmg-x7yT6TM', '2024-06-15 19:46:09.978185'),
('raqcm1y2pgjrh37cgze4avlugvdlgz79', 'e30:1sDUgw:yrCYx-X_Bly9kvEpD-da8mJYU8fwp_kPSXjBW_UCtZM', '2024-06-15 19:47:02.237768'),
('tl272e5nitbujzk5qgbixcw1uot0niad', '.eJxVjMsOwiAQRf-FtSEDQ6G6dN9vIAwzSNXQpI-V8d-1SRe6veec-1IxbWuN2yJzHFldlFGn341SfkjbAd9Tu006T22dR9K7og-66GFieV4P9--gpqV-aysQini27DF7KAU7YnJiGAxCAQy-9OceklBwnbNFUjaIRC5bhM6p9wfwDTfo:1sBsBk:YYv8KI7ucy8EsPgTyMedri9XpevV9OL5QCzL6INaxfA', '2024-06-11 08:28:08.360002'),
('uaf1wswm4ek31bm6q2v5rc6zfmkzfowa', '.eJzdVllvozAQ_isWz21EQo5u3hzwEqeAWQORkt1VxGEauilUHK1WVf_7jtMcjfZoGylSt5IFznhmGH_fHHlQFmFTLxdNJcpFlihDpa2cPZdFYfxD5PIguQ7zq6IVF3ldZlFLqrQ2p1XLLhKxGm10Dxwsw2oJ1h2hDlLRTzpJX4v7appqvSiJuqKdqG1NTVVt0E8vPl2ooYgG3V63k4owbmtaFHXjjqb2uuD0RlwX4K8owzIrlOHXByVuyqqoFldlc1tUynAjgK-5ZfFTxHWBEoFofieqOrsK4-xbo6qploOvtQkoYtjflkUqqqKUP78E1GHI58GEWhZDk4DP0Ix4xKFSsxI34KoU8j5qp3tOlcczBSRNkoV5LcX6GE8xByMd2y7z0GTMPOIiTnXMDQYurpsyTIo2qM6JhQ2Mptgy6JQSj6Ex0X3GkU3NgFg73Q7oUhs7iHguBDfHW2_IwFNqgF5YbcO3MNeZg0x4UdBjJuGIcId4vvx2ndXNSt7ay6pa3IToXkSo1WrBUSriZbi9lto7VwcglFAvsjyLJdxK-9NQU4equj1Is3xtACIpfTx7j3xYzCVz5FFrKuHQKYBGLCCH28Q5mg1OIAQ0CrgJDF9ibmGkE51a65j2ZHDsmAGnWzZszOE58_Bo7W5HBr5dZfEeDGQ_be6y1d-46X8Mbjzs6GNgh9MphkqBQpHEWMw7IOafYO85eQHtHSsv87yvkmLV7GkBdEb0gzPCdM48l9kYBSaeo8-A6SXCjj9mzuzE1aJjz18HPQ9sySXyiBk4xkHbuhfh6cH3xE2Wywkj0fdFlVWI0hNiDo3IkE1d59DfGYJaOGxMNuGQzczxiUNMDkAH1DKgrU8C7FCfHQH1UwfcwC034BWmhgfEvWlKwNL-BL36O_Q7Qt4V9D6ZyCyGvAXsYU7SS3x0lr9yQr8mzd84EGB1_usKgD9MJgwAl4GxiwNLOaL9T6n1bJbYcowAHYEJQbATt39Y7TeXwffHX7vJY2k:1sEEYE:dwY_uPHM1hpptiu7BnTfZG_0TWJr25_VKmTn0jhM1y4', '2024-06-17 20:45:06.333048');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `app_curso`
--
ALTER TABLE `app_curso`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_cursos_grupos`
--
ALTER TABLE `app_cursos_grupos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKcursos_gru897692` (`semestre_id`),
  ADD KEY `FKcursos_gru420796` (`profesor_id`),
  ADD KEY `FKcursos_gru119177` (`curso_id`),
  ADD KEY `FKcursos_gru94794` (`grupo_id`);

--
-- Indices de la tabla `app_estudiante`
--
ALTER TABLE `app_estudiante`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `codigo_universitario` (`codigo_universitario`);

--
-- Indices de la tabla `app_grupo`
--
ALTER TABLE `app_grupo`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_horario_sustentaciones`
--
ALTER TABLE `app_horario_sustentaciones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKhorario_su981527` (`sustentacion_id`);

--
-- Indices de la tabla `app_profesor`
--
ALTER TABLE `app_profesor`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `user_id` (`user_id`);

--
-- Indices de la tabla `app_profesores_semestre_academico`
--
ALTER TABLE `app_profesores_semestre_academico`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKprofesores748958` (`profesor_id`),
  ADD KEY `FKprofesores67448` (`semestre_id`);

--
-- Indices de la tabla `app_profile`
--
ALTER TABLE `app_profile`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_id` (`user_id`);

--
-- Indices de la tabla `app_semana_sustentacion`
--
ALTER TABLE `app_semana_sustentacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKsemana_sus777011` (`semestre_academico_id`),
  ADD KEY `FKsemana_sus164933` (`curso_id`);

--
-- Indices de la tabla `app_semestreacademico`
--
ALTER TABLE `app_semestreacademico`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_semestre_academico_profesores`
--
ALTER TABLE `app_semestre_academico_profesores`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKsemestre_981314` (`semestre_id`),
  ADD KEY `FKsemestre_368974` (`profesor_id`);

--
-- Indices de la tabla `app_sustentacion`
--
ALTER TABLE `app_sustentacion`
  ADD PRIMARY KEY (`id`),
  ADD KEY `FKsustentaci593842` (`cursos_grupos_id`),
  ADD KEY `FKsustentaci744459` (`estudiante_id`),
  ADD KEY `FKsustentaci542190` (`asesor_id`),
  ADD KEY `FKsustentaci486616` (`jurado2_id`),
  ADD KEY `FKsustentaci486617` (`jurado1_id`);

--
-- Indices de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indices de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indices de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indices de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  ADD KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`);

--
-- Indices de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  ADD KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`);

--
-- Indices de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`);

--
-- Indices de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indices de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `app_curso`
--
ALTER TABLE `app_curso`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `app_cursos_grupos`
--
ALTER TABLE `app_cursos_grupos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `app_estudiante`
--
ALTER TABLE `app_estudiante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `app_grupo`
--
ALTER TABLE `app_grupo`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `app_horario_sustentaciones`
--
ALTER TABLE `app_horario_sustentaciones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT de la tabla `app_profesor`
--
ALTER TABLE `app_profesor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT de la tabla `app_profesores_semestre_academico`
--
ALTER TABLE `app_profesores_semestre_academico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=178;

--
-- AUTO_INCREMENT de la tabla `app_profile`
--
ALTER TABLE `app_profile`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `app_semana_sustentacion`
--
ALTER TABLE `app_semana_sustentacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `app_semestreacademico`
--
ALTER TABLE `app_semestreacademico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT de la tabla `app_semestre_academico_profesores`
--
ALTER TABLE `app_semestre_academico_profesores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `app_sustentacion`
--
ALTER TABLE `app_sustentacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT de la tabla `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=73;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT de la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=82;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_cursos_grupos`
--
ALTER TABLE `app_cursos_grupos`
  ADD CONSTRAINT `FKcursos_gru119177` FOREIGN KEY (`curso_id`) REFERENCES `app_curso` (`id`),
  ADD CONSTRAINT `FKcursos_gru420796` FOREIGN KEY (`profesor_id`) REFERENCES `app_profesor` (`id`),
  ADD CONSTRAINT `FKcursos_gru897692` FOREIGN KEY (`semestre_id`) REFERENCES `app_semestreacademico` (`id`),
  ADD CONSTRAINT `FKcursos_gru94794` FOREIGN KEY (`grupo_id`) REFERENCES `app_grupo` (`id`);

--
-- Filtros para la tabla `app_horario_sustentaciones`
--
ALTER TABLE `app_horario_sustentaciones`
  ADD CONSTRAINT `FKhorario_su981527` FOREIGN KEY (`sustentacion_id`) REFERENCES `app_sustentacion` (`id`);

--
-- Filtros para la tabla `app_profesor`
--
ALTER TABLE `app_profesor`
  ADD CONSTRAINT `fk_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `app_profesores_semestre_academico`
--
ALTER TABLE `app_profesores_semestre_academico`
  ADD CONSTRAINT `FKprofesores67448` FOREIGN KEY (`semestre_id`) REFERENCES `app_semestreacademico` (`id`),
  ADD CONSTRAINT `FKprofesores748958` FOREIGN KEY (`profesor_id`) REFERENCES `app_profesor` (`id`);

--
-- Filtros para la tabla `app_profile`
--
ALTER TABLE `app_profile`
  ADD CONSTRAINT `App_profile_user_id_b93ddc45_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `app_semana_sustentacion`
--
ALTER TABLE `app_semana_sustentacion`
  ADD CONSTRAINT `FKsemana_sus164933` FOREIGN KEY (`curso_id`) REFERENCES `app_curso` (`id`),
  ADD CONSTRAINT `FKsemana_sus777011` FOREIGN KEY (`semestre_academico_id`) REFERENCES `app_semestreacademico` (`id`);

--
-- Filtros para la tabla `app_semestre_academico_profesores`
--
ALTER TABLE `app_semestre_academico_profesores`
  ADD CONSTRAINT `FKsemestre_368974` FOREIGN KEY (`profesor_id`) REFERENCES `app_profesor` (`id`),
  ADD CONSTRAINT `FKsemestre_981314` FOREIGN KEY (`semestre_id`) REFERENCES `app_semestreacademico` (`id`);

--
-- Filtros para la tabla `app_sustentacion`
--
ALTER TABLE `app_sustentacion`
  ADD CONSTRAINT `FKsustentaci486616` FOREIGN KEY (`jurado2_id`) REFERENCES `app_profesor` (`id`),
  ADD CONSTRAINT `FKsustentaci486617` FOREIGN KEY (`jurado1_id`) REFERENCES `app_profesor` (`id`),
  ADD CONSTRAINT `FKsustentaci542190` FOREIGN KEY (`asesor_id`) REFERENCES `app_profesor` (`id`),
  ADD CONSTRAINT `FKsustentaci593842` FOREIGN KEY (`cursos_grupos_id`) REFERENCES `app_cursos_grupos` (`id`),
  ADD CONSTRAINT `FKsustentaci744459` FOREIGN KEY (`estudiante_id`) REFERENCES `app_estudiante` (`id`);

--
-- Filtros para la tabla `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Filtros para la tabla `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Filtros para la tabla `auth_user_groups`
--
ALTER TABLE `auth_user_groups`
  ADD CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `auth_user_user_permissions`
--
ALTER TABLE `auth_user_user_permissions`
  ADD CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);

--
-- Filtros para la tabla `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
