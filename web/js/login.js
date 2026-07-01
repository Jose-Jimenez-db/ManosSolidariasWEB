/*
    Este archivo implementa la lógica del frontend para el proceso de
    autenticación del sistema Manos Solidarias. Se encarga de validar el
    inicio de sesión del usuario, enviar las credenciales a la API,
    almacenar la información de la sesión y redirigir al usuario a la
    página principal cuando la autenticación es exitosa.
*/

if (haySesionActiva()) {
    window.location.href = "principal.html";
}

const loginForm = document.getElementById("loginForm");

loginForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    try {
        const respuesta = await apiFetch("/auth/login", {
            method: "POST",
            conAuth: false,
            body: JSON.stringify({ username, password })
        });

        if (!respuesta.ok) {
            const mensaje = await obtenerMensajeError(respuesta);
            mostrarMensaje(mensaje, "error");
            return;
        }

        const datos = await respuesta.json();
        guardarSesion(datos.access_token, datos.rol, username);

        window.location.href = "principal.html";

    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudo conectar con el servidor.", "error");
    }
});