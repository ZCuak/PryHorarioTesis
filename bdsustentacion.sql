- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 30-05-2024 a las 06:13:54
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
(1, 3, 2, 8, 1),
(2, 3, 3, 9, 1),
(6, 4, 2, 8, 1);

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
(1, '201TD02196', 'Ocrospoma Ugaz Frank Anthony', 'frankocrospomaugaz@gmail.com', '920532729'),
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
(7, 'ralarcon@usat.edu.pe', 'ALARCON GARCIA ROGER ERNESTO', 'TP', '987654321', NULL),
(8, 'maranguri@usat.edu.pe', 'ARANGURI GARCIA MARIA YSABEL', 'TC', '912345678', NULL),
(9, 'hzelada@usat.edu.pe', 'ZELADA VALDIVIESO HECTOR MIGUEL', 'TC', '938359471', NULL);

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
(10, 1, 7, 2),
(14, 1, 8, 5),
(15, 1, 9, 5);

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
(1, 1, 7, NULL, NULL, 7, 'Sistema web ...'),
(2, 1, 8, NULL, NULL, 8, 'Aplicación Móvil ...'),
(3, 1, 9, NULL, NULL, 9, 'Solución de BI ...'),
(4, 1, 1, 7, 8, 9, 'Aplicación web y móvil basado en el Algoritmo de Optimización de Colonia de Hormigas para apoyar el proceso de ventas en la panadería Mishka');

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
(68, 'Can view session', 17, 'view_session');

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
  `date_joined` datetime(6) NOT NULL,
  `rol` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `auth_user`
--

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `rol`) VALUES
(1, 'pbkdf2_sha256$600000$erSGiNKcW4hyYvrGOX6BQE$VbKU/zqg/F9sx5VqdeniI8V1VSjmF3+G6io5xJRxu1w=', '2024-05-29 03:36:08.792643', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2024-05-28 08:28:03.890795', NULL);

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
(17, '2024-05-29 05:24:41.484673', '6', 'CHAVARRY CAMPOS JHOSEP RICARDO', 3, '', 3, 1);

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
(19, 'App', '0001_initial', '2024-05-30 04:03:09.091186');

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
('0zjxikla5ve35etqcuvyvj4u1cwfs1a0', '.eJxVjMsOwiAQRf-FtSEDQ6G6dN9vIAwzSNXQpI-V8d-1SRe6veec-1IxbWuN2yJzHFldlFGn341SfkjbAd9Tu006T22dR9K7og-66GFieV4P9--gpqV-aysQini27DF7KAU7YnJiGAxCAQy-9OceklBwnbNFUjaIRC5bhM6p9wfwDTfo:1sCA6i:G75EsSpP_tONc-vVbtChiAJxBUIcBuHxa-_TNL1-7p4', '2024-06-12 03:36:08.800160'),
('tl272e5nitbujzk5qgbixcw1uot0niad', '.eJxVjMsOwiAQRf-FtSEDQ6G6dN9vIAwzSNXQpI-V8d-1SRe6veec-1IxbWuN2yJzHFldlFGn341SfkjbAd9Tu006T22dR9K7og-66GFieV4P9--gpqV-aysQini27DF7KAU7YnJiGAxCAQy-9OceklBwnbNFUjaIRC5bhM6p9wfwDTfo:1sBsBk:YYv8KI7ucy8EsPgTyMedri9XpevV9OL5QCzL6INaxfA', '2024-06-11 08:28:08.360002');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_profesor`
--
ALTER TABLE `app_profesor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT de la tabla `app_profesores_semestre_academico`
--
ALTER TABLE `app_profesores_semestre_academico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_semana_sustentacion`
--
ALTER TABLE `app_semana_sustentacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_semestreacademico`
--
ALTER TABLE `app_semestreacademico`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `app_semestre_academico_profesores`
--
ALTER TABLE `app_semestre_academico_profesores`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT de la tabla `app_sustentacion`
--
ALTER TABLE `app_sustentacion`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=69;

--
-- AUTO_INCREMENT de la tabla `auth_user`
--
ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

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
