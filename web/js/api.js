/*
    Este archivo implementa las funciones generales utilizadas por el
    frontend del sistema Manos Solidarias. Se encarga de administrar la
    sesión del usuario, realizar la comunicación con la API, gestionar la
    autenticación mediante tokens y proporcionar funciones de apoyo para la
    visualización de mensajes y el manejo de errores.
*/

const API_URL = "http://127.0.0.1:8000";

function guardarSesion(token, rol, username) {
    localStorage.setItem("manos_token", token);
    localStorage.setItem("manos_rol", rol);
    localStorage.setItem("manos_username", username);
}

function obtenerToken() {
    return localStorage.getItem("manos_token");
}

function obtenerUsuarioActual() {
    return localStorage.getItem("manos_username") || "Usuario";
}

function haySesionActiva() {
    return obtenerToken() !== null;
}

function cerrarSesion() {
    localStorage.removeItem("manos_token");
    localStorage.removeItem("manos_rol");
    localStorage.removeItem("manos_username");
    window.location.href = "login.html";
}

function exigirSesion() {
    if (!haySesionActiva()) {
        window.location.href = "login.html";
    }
}

async function apiFetch(endpoint, opciones = {}) {
    const headers = {
        "Content-Type": "application/json",
        ...(opciones.headers || {})
    };

    if (opciones.conAuth !== false) {
        const token = obtenerToken();
        if (token) {
            headers["Authorization"] = "Bearer " + token;
        }
    }

    const respuesta = await fetch(API_URL + endpoint, {
        ...opciones,
        headers
    });

    if (respuesta.status === 401) {
        cerrarSesion();
        throw new Error("La sesión expiró. Inicie sesión nuevamente.");
    }

    return respuesta;
}

function mostrarMensaje(texto, tipo = "success") {
    const caja = document.getElementById("messageBox");
    if (!caja) {
        return;
    }

    caja.textContent = texto;
    caja.classList.remove("hidden");
    caja.style.background = tipo === "success" ? "#5a9c8a" : "#d98a7e";

    clearTimeout(caja._timeout);
    caja._timeout = setTimeout(() => {
        caja.classList.add("hidden");
    }, 3500);
}

async function obtenerMensajeError(respuesta) {
    try {
        const datos = await respuesta.json();
        return datos.detail || "Ocurrió un error inesperado.";
    } catch (error) {
        return "Ocurrió un error inesperado.";
    }
}