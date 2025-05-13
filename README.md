# Guía de Implementación - Ríos del Desierto SAC (Docker)

## Requisitos Previos

Antes de comenzar, asegúrate de tener instalados los siguientes programas:

- **Docker**: [Instrucciones de instalación](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Instrucciones de instalación](https://docs.docker.com/compose/install/)

---

## Pasos para Clonar y Ejecutar el Proyecto

1. **Clona el repositorio:**

   Abre tu terminal y ejecuta el siguiente comando para clonar el repositorio desde GitHub:

   ```bash
   git clone https://github.com/johnmartinez1988/rios_desierto_sac.git
   cd rios_desierto_sac
   
2. **Construir e Iniciar los Contenedores:**

   Una vez dentro del directorio del proyecto, ejecuta el siguiente comando para construir la imagen de Docker y levantar los contenedores:

   ```bash
   docker-compose up --build

3. **Acceder a la Aplicación:**

   Una vez que los contenedores estén en ejecución, abre tu navegador y accede a la siguiente URL:

   ```bash
   http://localhost:8000

4. **Detener los Contenedores:**

   Para detener los contenedores y liberar los recursos de Docker cuando hayas terminado, ejecuta:

   ```bash
   docker-compose down





