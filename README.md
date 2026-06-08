RentCar - Sistema de Gestión de Renta de Vehículos

RentCar es una solución de software integral y robusta para la administración de flotas de vehículos, gestión de clientes, empleados, contratos de renta y control técnico mediante inspecciones previas. Diseñada con un enfoque corporativo y una interfaz de usuario premium basada en componentes visuales modernos.

Este proyecto ha sido diseñado como el trabajo final de grado académico, cumpliendo con los rigurosos requerimientos de ingeniería de software para el control transaccional del negocio.

Stack Tecnológico

Backend: Python 3.x / Django Web Framework.

Base de Datos: PostgreSQL para transacciones seguras y normalizadas.

Frontend: Django Templates + Tailwind CSS (Diseño responsivo corporativo en paleta Slate & Indigo Business).

Iconografía: Phosphor Icons.

Módulos del Sistema (Requerimientos de la Diapositiva)

Gestión de Tipos de Vehículos: Categorización de la flota.

Gestión de Marcas y Modelos: Relaciones dinámicas para marcas y sus modelos correspondientes.

Gestión de Tipos de Combustible: Combustibles activos/inactivos.

Gestión de Vehículos: Datos de motor, chasis, placa, precio de renta y estados físicos.

Gestión de Clientes: Clasificación jurídica/física y validación de límite de crédito en tiempo real.

Gestión de Empleados: Registro de tanda laboral e histórico de ingreso.

Proceso de Inspección: Lista de comprobación técnica previa a la transacción de renta.

Proceso de Renta y Devolución: Integridad de estados de la flota y cálculo de comisiones.

Consultas y Reportes: Filtrado de rentas por criterios dinámicos y reportes exportables entre fechas.

Configuración y Ejecución del Proyecto

1. Variables de Entorno

Crea un archivo .env en la raíz del proyecto basado en el siguiente ejemplo:

DEBUG=True
SECRET_KEY=tu_secreto_aqui
DB_NAME=rentacar_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432


2. Instalación de Dependencias

python -m venv venv
# Activar entorno
# En Windows: venv\Scripts\activate
# En macOS/Linux: source venv/bin/activate
pip install -r requirements.txt


3. Base de Datos y Migraciones

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser


4. Iniciar Servidor

python manage.py runserver


Accede en tu navegador a http://127.0.0.1:8000/.
