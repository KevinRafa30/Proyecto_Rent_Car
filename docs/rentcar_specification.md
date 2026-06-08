ESPECIFICACIONES TÉCNICAS - SISTEMA RENTCAR

Documento de Requerimientos Académicos (UNAPEC)

Este documento es la fuente única de verdad para el diseño de la base de datos, lógica de negocio y vistas del sistema RentCar. Cualquier agente de desarrollo debe cumplir estrictamente con los modelos, campos y flujos descritos a continuación.

1. MÓDULOS DE GESTIÓN (MAESTROS CRUD)

Todos los módulos de gestión deben permitir las operaciones de creación, lectura, actualización y eliminación lógica o física, controlando el campo "Estado".

1.1 Gestión de Tipos de Vehículos

Identificador: Autonumérico (Clave Primaria).

Descripción: Texto (ej. Automóvil, Camioneta, Furgoneta, etc.).

Estado: Activo / Inactivo.

1.2 Gestión de Marcas

Identificador: Autonumérico (Clave Primaria).

Descripción: Texto (ej. Toyota, Honda, Kia, etc.).

Estado: Activo / Inactivo.

1.3 Gestión de Modelos

Identificador: Autonumérico (Clave Primaria).

Identificador Marca: Relación (Clave Foránea) con Marcas.

Descripción: Texto (ej. Corolla, Camry, Corona, etc.).

Estado: Activo / Inactivo.

1.4 Gestión de Tipos de Combustible

Identificador: Autonumérico (Clave Primaria).

Descripción: Texto (ej. Gasolina, Gasoil, Gas Natural, GLP, etc.).

Estado: Activo / Inactivo.

1.5 Gestión de Vehículos

Identificador: Autonumérico (Clave Primaria).

Descripción: Texto descriptivo (Marca + Modelo + Año).

No. Chasis: Texto único.

No. Motor: Texto único.

No. Placa: Texto único.

Tipo Vehículo: Relación (Clave Foránea) con Tipos de Vehículos.

Marca: Relación (Clave Foránea) con Marcas.

Modelo: Relación (Clave Foránea) con Modelos.

Tipo Combustible: Relación (Clave Foránea) con Tipos de Combustible.

Estado: Disponible / Rentado / En Mantenimiento.

1.6 Gestión de Clientes

Identificador: Autonumérico (Clave Primaria).

Nombre: Texto completo.

Cédula: Texto único (Validación obligatoria de formato dominicano de 11 dígitos).

No. Tarjeta CR: Número de tarjeta de crédito para garantía.

Límite de Crédito: Numérico decimal.

Tipo Persona: Física / Jurídica.

Estado: Activo / Inactivo.

1.7 Gestión de Empleados

Identificador: Autonumérico (Clave Primaria).

Nombre: Texto completo del empleado.

Cédula: Texto único.

Tanda Labor: Selección obligatoria (Matutina / Vespertina / Nocturna).

Porciento Comisión: Decimal (Porcentaje a ganar sobre las rentas ejecutadas).

Fecha Ingreso: Fecha de registro en la empresa.

Estado: Activo / Inactivo.

2. PROCESOS TRANSACCIONALES (FLUJOS CORE)

2.1 Proceso de Inspección (Previo a Renta)

Se debe realizar una inspección física obligatoria del vehículo antes de realizar cualquier contrato de renta.

Identificador Transacción: Autonumérico (Clave Primaria).

Vehículo: Relación con Vehículos (Filtra solo vehículos con estado 'Disponible').

Identificador Cliente: Relación con Clientes.

Tiene Ralladuras: Booleano (Sí / No).

Cantidad Combustible: Selección obligatoria (1/4, 1/2, 3/4, Lleno).

Tiene Goma Repuesto: Booleano (Sí / No).

Tiene Gato: Booleano (Sí / No).

Tiene Roturas Cristal: Booleano (Sí / No).

Estado Gomas: Checks individuales para cada neumático:

Goma delantera izquierda (Buen estado / Mal estado).

Goma delantera derecha (Buen estado / Mal estado).

Goma trasera izquierda (Buen estado / Mal estado).

Goma trasera derecha (Buen estado / Mal estado).

Fecha: Registro de fecha y hora de la inspección.

Empleado Inspección: Relación con Empleados (Filtra los encargados del taller/inspección).

Estado: Activo / Inactivo / Procesado.

2.2 Proceso de Renta y Devolución

No. Renta: Autonumérico (Clave Primaria).

Empleado: Relación con Empleados (Quien asiste al cliente).

Vehículo: Relación con Vehículos (Solo vehículos 'Disponible').

Cliente: Relación con Clientes.

Fecha Renta: Fecha de inicio de la renta.

Fecha Devolución: Fecha acordada para el retorno del vehículo.

Monto x Día: Precio de alquiler diario.

Cantidad de Días: Entero.

Comentario: Texto descriptivo opcional.

Estado: Activo (Vehículo en uso) / Devuelto (Vehículo retornado con éxito).

Reglas de Negocio Obligatorias (Backend):

Bloqueo de Vehículo: Al guardar una nueva renta, el estado del Vehículo debe pasar automáticamente a Rentado.

Liberación de Vehículo: Al procesar una devolución (cambiar estado de la renta a Devuelto), el vehículo debe cambiar automáticamente a Disponible.

Límite de Crédito: No se debe permitir guardar una renta si el costo total (Monto x Día * Cantidad de Días) supera el Límite de Crédito configurado en el perfil del Cliente.

Cálculo de Comisión: Al guardar la renta, se calcula automáticamente el monto de comisión del empleado multiplicando el costo total de la renta por el porcentaje de comisión del empleado.

3. CONSULTAS Y REPORTES

3.1 Consulta de Rentas por Criterios

Debe existir una pantalla con filtros interactivos que permita buscar registros de rentas usando combinaciones de:

Cliente seleccionado.

Vehículo seleccionado.

Rango de fechas (Fecha de inicio y fin).

3.2 Reporte de Rentas para Exportación

Un módulo generador de reportes formales que agrupe y totalice las rentas ejecutadas filtrando por:

Rango de fechas específico.

Tipo de Vehículo (ej. ver solo rentas de camiones o automóviles).

