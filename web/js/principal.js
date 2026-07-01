/*
    Este archivo implementa la lógica del frontend para la página principal
    del sistema Manos Solidarias. Se encarga de verificar que exista una
    sesión activa, mostrar la información del usuario autenticado y permitir
    el cierre de sesión desde la interfaz principal de la aplicación.
*/

exigirSesion();

document.getElementById("usuarioInfo").textContent = "Sesión: " + obtenerUsuarioActual();

document.getElementById("btnCerrarSesion").addEventListener("click", cerrarSesion);