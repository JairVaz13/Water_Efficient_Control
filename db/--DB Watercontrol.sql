--
-- Base de datos: `WhaterControl`
--
--
-- Estructura de tabla para la tabla `dispensadores`
--

CREATE TABLE `dispensadores` (
  `id_dispensador` int(11) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `id_recipiente` int(11) NOT NULL,
  `token` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `dispensadores`
--

INSERT INTO `dispensadores` (`id_dispensador`, `estado`, `id_recipiente`, `token`) VALUES
(1, '0', 1, '19010962-7ae9-464b-aa8f-869049655914');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ia_recipiente_sensor`
--

CREATE TABLE `ia_recipiente_sensor` (
  `id` int(11) NOT NULL,
  `id_recipiente` int(11) NOT NULL,
  `id_sensor` int(11) NOT NULL,
  `valor` float NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `ia_recipiente_sensor`
--

INSERT INTO `ia_recipiente_sensor` (`id`, `id_recipiente`, `id_sensor`, `valor`, `fecha`) VALUES
(1, 1, 1, 7.2, '2025-04-05 00:00:00'),
(2, 1, 1, 7.2, '2025-04-05 00:00:00'),
(3, 1, 1, 7.2, '2025-04-05 00:00:00'),
(4, 1, 1, 7.2, '2025-04-05 00:00:00'),
(5, 1, 1, 7.2, '2025-04-05 00:00:00'),
(6, 1, 1, 7.2, '2025-04-05 00:00:00'),
(7, 1, 1, 7.2, '2025-04-05 00:00:00'),
(8, 1, 1, 7.2, '2025-04-05 00:00:00'),
(9, 1, 1, 7.2, '2025-04-05 00:00:00'),
(10, 1, 1, 7.2, '2025-04-05 00:00:00'),
(11, 1, 2, 1280, '2025-04-05 00:00:00'),
(12, 1, 2, 1350, '2025-04-05 00:00:00'),
(13, 1, 2, 1350, '2025-04-05 00:00:00'),
(14, 1, 2, 1350, '2025-04-05 00:00:00'),
(15, 1, 2, 1350, '2025-04-05 00:00:00'),
(16, 1, 2, 1390, '2025-04-05 00:00:00'),
(17, 1, 2, 1390, '2025-04-05 00:00:00'),
(18, 1, 2, 1390, '2025-04-05 00:00:00'),
(19, 1, 2, 1390, '2025-04-05 00:00:00'),
(20, 1, 2, 1390, '2025-04-05 00:00:00'),
(21, 1, 3, 25, '2025-04-05 00:00:00'),
(22, 1, 3, 25, '2025-04-05 00:00:00'),
(23, 1, 3, 25, '2025-04-05 00:00:00'),
(24, 1, 3, 25, '2025-04-05 00:00:00'),
(25, 1, 3, 26, '2025-04-05 00:00:00'),
(26, 1, 3, 26, '2025-04-05 00:00:00'),
(27, 1, 3, 26, '2025-04-05 00:00:00'),
(28, 1, 3, 26, '2025-04-05 00:00:00'),
(29, 1, 3, 23, '2025-04-05 00:00:00'),
(30, 1, 3, 23, '2025-04-05 00:00:00');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recipientes`
--

CREATE TABLE `recipientes` (
  `id_recipiente` int(11) NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `token` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `recipientes`
--

INSERT INTO `recipientes` (`id_recipiente`, `ubicacion`, `tipo`, `capacidad`, `token`) VALUES
(1, 'Santiago', 'Tinaco', 1500, '19010962-7ae9-464b-aa8f-869049655914');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sensores`
--

CREATE TABLE `sensores` (
  `id_sensor` int(11) NOT NULL,
  `tipo` varchar(50) NOT NULL,
  `token` varchar(40) NOT NULL,
  `id_recipiente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `sensores`
--

INSERT INTO `sensores` (`id_sensor`, `tipo`, `token`, `id_recipiente`) VALUES
(1, 'ph', '19010962-7ae9-464b-aa8f-869049655914', 1),
(2, 'tds', '19010962-7ae9-464b-aa8f-869049655914', 1),
(3, 'temperatura', '19010962-7ae9-464b-aa8f-869049655914', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `token` varchar(36) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `email`, `contrasena`, `token`) VALUES
(1, 'oscar', 'nose@gmail.com', '$2b$12$G66MulHX5IlbMIAzOxOCiuhvE6u3/Spq3GnWP39.Mm0xpNGWVQIcu', '19010962-7ae9-464b-aa8f-869049655914');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `dispensadores`
--
ALTER TABLE `dispensadores`
  ADD PRIMARY KEY (`id_dispensador`),
  ADD KEY `id_recipiente` (`id_recipiente`);

--
-- Indices de la tabla `ia_recipiente_sensor`
--
ALTER TABLE `ia_recipiente_sensor`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_recipiente` (`id_recipiente`),
  ADD KEY `id_sensor` (`id_sensor`),
  ADD KEY `idx_fecha_ia` (`fecha`);

--
-- Indices de la tabla `recipientes`
--
ALTER TABLE `recipientes`
  ADD PRIMARY KEY (`id_recipiente`);

--
-- Indices de la tabla `sensores`
--
ALTER TABLE `sensores`
  ADD PRIMARY KEY (`id_sensor`),
  ADD KEY `id_recipiente` (`id_recipiente`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_usuario_email` (`email`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `dispensadores`
--
ALTER TABLE `dispensadores`
  MODIFY `id_dispensador` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `ia_recipiente_sensor`
--
ALTER TABLE `ia_recipiente_sensor`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT de la tabla `recipientes`
--
ALTER TABLE `recipientes`
  MODIFY `id_recipiente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT de la tabla `sensores`
--
ALTER TABLE `sensores`
  MODIFY `id_sensor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `dispensadores`
--
ALTER TABLE `dispensadores`
  ADD CONSTRAINT `dispensadores_ibfk_2` FOREIGN KEY (`id_recipiente`) REFERENCES `recipientes` (`id_recipiente`);

--
-- Filtros para la tabla `ia_recipiente_sensor`
--
ALTER TABLE `ia_recipiente_sensor`
  ADD CONSTRAINT `ia_recipiente_sensor_ibfk_1` FOREIGN KEY (`id_recipiente`) REFERENCES `recipientes` (`id_recipiente`),
  ADD CONSTRAINT `ia_recipiente_sensor_ibfk_2` FOREIGN KEY (`id_sensor`) REFERENCES `sensores` (`id_sensor`);

--
-- Filtros para la tabla `sensores`
--
ALTER TABLE `sensores`
  ADD CONSTRAINT `sensores_ibfk_2` FOREIGN KEY (`id_recipiente`) REFERENCES `recipientes` (`id_recipiente`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
