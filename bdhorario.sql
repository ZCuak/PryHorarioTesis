-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 26-05-2024 a las 11:30:09
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
-- Base de datos: `bdhorario`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_estudiante`
--

CREATE TABLE `app_estudiante` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_estudiante`
--

INSERT INTO `app_estudiante` (`id`, `nombre`, `apellido`, `email`, `telefono`) VALUES
(1, 'Frank', 'Ocrospoma Ugaz', 'frankocrospomaugaz@gmail.com', '920532729');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_horario`
--

CREATE TABLE `app_horario` (
  `id` int(11) NOT NULL,
  `fecha` date NOT NULL,
  `hora_inicio` time NOT NULL,
  `hora_fin` time NOT NULL,
  `tesis_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_jurado`
--

CREATE TABLE `app_jurado` (
  `id` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `telefono` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_jurado_tesis`
--

CREATE TABLE `app_jurado_tesis` (
  `id` int(11) NOT NULL,
  `id_jurado` int(11) DEFAULT NULL,
  `id_tesis` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `app_tesis`
--

CREATE TABLE `app_tesis` (
  `id` int(11) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `fecha_entrega` date NOT NULL,
  `estudiante_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `app_tesis`
--

INSERT INTO `app_tesis` (`id`, `titulo`, `descripcion`, `fecha_entrega`, `estudiante_id`) VALUES
(1, 'Aplicación web y móvil basado en el Algoritmo de Optimización de Colonia de Hormigas para apoyar el proceso de ventas en la panadería Mishka', 'Aplicación web y móvil basado en el Algoritmo de Optimización de Colonia de Hormigas para apoyar el proceso de ventas en la panadería Mishka', '2024-05-29', 1);

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
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add user', 4, 'add_user'),
(14, 'Can change user', 4, 'change_user'),
(15, 'Can delete user', 4, 'delete_user'),
(16, 'Can view user', 4, 'view_user'),
(17, 'Can add content type', 5, 'add_contenttype'),
(18, 'Can change content type', 5, 'change_contenttype'),
(19, 'Can delete content type', 5, 'delete_contenttype'),
(20, 'Can view content type', 5, 'view_contenttype'),
(21, 'Can add session', 6, 'add_session'),
(22, 'Can change session', 6, 'change_session'),
(23, 'Can delete session', 6, 'delete_session'),
(24, 'Can view session', 6, 'view_session'),
(25, 'Can add estudiante', 7, 'add_estudiante'),
(26, 'Can change estudiante', 7, 'change_estudiante'),
(27, 'Can delete estudiante', 7, 'delete_estudiante'),
(28, 'Can view estudiante', 7, 'view_estudiante'),
(29, 'Can add tesis', 8, 'add_tesis'),
(30, 'Can change tesis', 8, 'change_tesis'),
(31, 'Can delete tesis', 8, 'delete_tesis'),
(32, 'Can view tesis', 8, 'view_tesis'),
(33, 'Can add jurado', 9, 'add_jurado'),
(34, 'Can change jurado', 9, 'change_jurado'),
(35, 'Can delete jurado', 9, 'delete_jurado'),
(36, 'Can view jurado', 9, 'view_jurado'),
(37, 'Can add horario', 10, 'add_horario'),
(38, 'Can change horario', 10, 'change_horario'),
(39, 'Can delete horario', 10, 'delete_horario'),
(40, 'Can view horario', 10, 'view_horario'),
(41, 'Can add jurado tesis', 11, 'add_juradotesis'),
(42, 'Can change jurado tesis', 11, 'change_juradotesis'),
(43, 'Can delete jurado tesis', 11, 'delete_juradotesis'),
(44, 'Can view jurado tesis', 11, 'view_juradotesis'),
(45, 'Can add estudiante', 12, 'add_estudiante'),
(46, 'Can change estudiante', 12, 'change_estudiante'),
(47, 'Can delete estudiante', 12, 'delete_estudiante'),
(48, 'Can view estudiante', 12, 'view_estudiante'),
(49, 'Can add tesis', 14, 'add_tesis'),
(50, 'Can change tesis', 14, 'change_tesis'),
(51, 'Can delete tesis', 14, 'delete_tesis'),
(52, 'Can view tesis', 14, 'view_tesis'),
(53, 'Can add jurado', 15, 'add_jurado'),
(54, 'Can change jurado', 15, 'change_jurado'),
(55, 'Can delete jurado', 15, 'delete_jurado'),
(56, 'Can view jurado', 15, 'view_jurado'),
(57, 'Can add horario', 13, 'add_horario'),
(58, 'Can change horario', 13, 'change_horario'),
(59, 'Can delete horario', 13, 'delete_horario'),
(60, 'Can view horario', 13, 'view_horario'),
(61, 'Can add jurado tesis', 16, 'add_juradotesis'),
(62, 'Can change jurado tesis', 16, 'change_juradotesis'),
(63, 'Can delete jurado tesis', 16, 'delete_juradotesis'),
(64, 'Can view jurado tesis', 16, 'view_juradotesis');

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
(1, 'pbkdf2_sha256$600000$LXvJ74ygdB624YNlbnWGau$P9gSRWlHeiZ9+8hf+5j+jDCdA/kIsP2zw1qxClwIerc=', '2024-05-26 05:48:58.759585', 1, 'admin', '', '', 'admin@gmail.com', 1, 1, '2024-05-25 10:32:14.790398');

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
(1, '2024-05-26 07:18:29.008959', '1', 'Frank Ocrospoma Ugaz', 1, '[{\"added\": {}}]', 12, 1),
(2, '2024-05-26 08:04:11.204045', '1', 'Aplicación web y móvil basado en el Algoritmo de Optimización de Colonia de Hormigas para apoyar el proceso de ventas en la panadería Mishka', 1, '[{\"added\": {}}]', 14, 1);

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
(1, 'admin', 'logentry'),
(7, 'admin_soft', 'estudiante'),
(10, 'admin_soft', 'horario'),
(9, 'admin_soft', 'jurado'),
(11, 'admin_soft', 'juradotesis'),
(8, 'admin_soft', 'tesis'),
(12, 'App', 'estudiante'),
(13, 'App', 'horario'),
(15, 'App', 'jurado'),
(16, 'App', 'juradotesis'),
(14, 'App', 'tesis'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'auth', 'user'),
(5, 'contenttypes', 'contenttype'),
(6, 'sessions', 'session');

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
(1, 'contenttypes', '0001_initial', '2024-05-25 10:31:30.509615'),
(2, 'auth', '0001_initial', '2024-05-25 10:31:30.983789'),
(3, 'admin', '0001_initial', '2024-05-25 10:31:31.120383'),
(4, 'admin', '0002_logentry_remove_auto_add', '2024-05-25 10:31:31.127374'),
(5, 'admin', '0003_logentry_add_action_flag_choices', '2024-05-25 10:31:31.135375'),
(6, 'contenttypes', '0002_remove_content_type_name', '2024-05-25 10:31:31.193062'),
(7, 'auth', '0002_alter_permission_name_max_length', '2024-05-25 10:31:31.247579'),
(8, 'auth', '0003_alter_user_email_max_length', '2024-05-25 10:31:31.264152'),
(9, 'auth', '0004_alter_user_username_opts', '2024-05-25 10:31:31.273147'),
(10, 'auth', '0005_alter_user_last_login_null', '2024-05-25 10:31:31.318141'),
(11, 'auth', '0006_require_contenttypes_0002', '2024-05-25 10:31:31.323141'),
(12, 'auth', '0007_alter_validators_add_error_messages', '2024-05-25 10:31:31.353686'),
(13, 'auth', '0008_alter_user_username_max_length', '2024-05-25 10:31:31.371688'),
(14, 'auth', '0009_alter_user_last_name_max_length', '2024-05-25 10:31:31.387681'),
(15, 'auth', '0010_alter_group_name_max_length', '2024-05-25 10:31:31.402685'),
(16, 'auth', '0011_update_proxy_permissions', '2024-05-25 10:31:31.413684'),
(17, 'auth', '0012_alter_user_first_name_max_length', '2024-05-25 10:31:31.430699'),
(18, 'sessions', '0001_initial', '2024-05-25 10:31:31.465239');

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
('b7xkn9bb00wwycjbkeumrcdmn4j8bqxd', '.eJxVjDkOwjAUBe_iGlmJ4wVT0ucM1vdfcAA5UpxUiLtDpBTQvpl5L5VgW0vaGi9pInVRvTr9bhnwwXUHdId6mzXOdV2mrHdFH7TpcSZ-Xg_376BAK98aJAbHrscohryBTCEMQE4G7HokIQe28yRnBCswOIqxs9ZkJvQswur9ARCpOYc:1sB6kc:EYtcadytQF9ucUE7Iimbu4R9vI7mKEBtHkh6TXx2zhM', '2024-06-09 05:48:58.765772'),
('thudu6xo6yqlr6x875v10mmrevw6h9rg', '.eJxVjDkOwjAUBe_iGlmJ4wVT0ucM1vdfcAA5UpxUiLtDpBTQvpl5L5VgW0vaGi9pInVRvTr9bhnwwXUHdId6mzXOdV2mrHdFH7TpcSZ-Xg_376BAK98aJAbHrscohryBTCEMQE4G7HokIQe28yRnBCswOIqxs9ZkJvQswur9ARCpOYc:1sB4O5:IAYYVjF2g-oYf275thO-Ji3YjCWrxqT9mE3YFHavNeA', '2024-06-09 03:17:33.018559');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `app_estudiante`
--
ALTER TABLE `app_estudiante`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_horario`
--
ALTER TABLE `app_horario`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_tesis` (`tesis_id`);

--
-- Indices de la tabla `app_jurado`
--
ALTER TABLE `app_jurado`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `app_jurado_tesis`
--
ALTER TABLE `app_jurado_tesis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_jurado` (`id_jurado`),
  ADD KEY `id_tesis` (`id_tesis`);

--
-- Indices de la tabla `app_tesis`
--
ALTER TABLE `app_tesis`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_estudiante` (`estudiante_id`);

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
-- AUTO_INCREMENT de la tabla `app_estudiante`
--
ALTER TABLE `app_estudiante`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `app_horario`
--
ALTER TABLE `app_horario`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_jurado`
--
ALTER TABLE `app_jurado`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_jurado_tesis`
--
ALTER TABLE `app_jurado_tesis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `app_tesis`
--
ALTER TABLE `app_tesis`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=65;

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT de la tabla `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `app_horario`
--
ALTER TABLE `app_horario`
  ADD CONSTRAINT `app_horario_ibfk_1` FOREIGN KEY (`tesis_id`) REFERENCES `app_tesis` (`id`);

--
-- Filtros para la tabla `app_jurado_tesis`
--
ALTER TABLE `app_jurado_tesis`
  ADD CONSTRAINT `app_jurado_tesis_ibfk_1` FOREIGN KEY (`id_jurado`) REFERENCES `app_jurado` (`id`),
  ADD CONSTRAINT `app_jurado_tesis_ibfk_2` FOREIGN KEY (`id_tesis`) REFERENCES `app_tesis` (`id`);

--
-- Filtros para la tabla `app_tesis`
--
ALTER TABLE `app_tesis`
  ADD CONSTRAINT `app_tesis_ibfk_1` FOREIGN KEY (`estudiante_id`) REFERENCES `app_estudiante` (`id`);

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
