/*
    Este archivo implementa la lógica del frontend para la gestión de
    beneficiarios del sistema Manos Solidarias. Se encarga de cargar,
    registrar, buscar, editar, eliminar y mostrar beneficiarios en la tabla,
    consumiendo los endpoints correspondientes de la API mediante funciones
    comunes de comunicación.
*/

exigirSesion();
document.getElementById("usuarioInfo").textContent = "Sesión: " + obtenerUsuarioActual();
document.getElementById("btnCerrarSesion").addEventListener("click", cerrarSesion);

const form = document.getElementById("beneficiarioForm");
const tablaBody = document.getElementById("tablaBeneficiarios");
const btnCancelar = document.getElementById("btnCancelar");
const tituloFormulario = document.getElementById("tituloFormulario");

let identificacionEditando = null;

function insigniaPrioridad(prioridad) {
    return prioridad;
}

function renderizarTabla(beneficiarios) {
    if (beneficiarios.length === 0) {
        tablaBody.innerHTML = `<tr><td colspan="6" class="sin-datos">No hay beneficiarios para mostrar.</td></tr>`;
        return;
    }

    tablaBody.innerHTML = beneficiarios.map(b => `
        <tr>
            <td>${b.identificacion}</td>
            <td>${b.nombre_completo}</td>
            <td>${b.comunidad}</td>
            <td>${b.integrantes_hogar}</td>
            <td>${insigniaPrioridad(b.prioridad_social)}</td>
            <td class="celda-acciones">
                <button class="btn-primario btn-pequeno" onclick='activarEdicion(${JSON.stringify(b)})'>Editar</button>
                <button class="btn-peligro btn-pequeno" onclick="eliminarBeneficiario('${b.identificacion}')">Eliminar</button>
            </td>
        </tr>
    `).join("");
}

async function cargarTodos() {
    try {
        const respuesta = await apiFetch("/beneficiarios/");
        const datos = await respuesta.json();
        renderizarTabla(datos);
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudieron cargar los beneficiarios.", "error");
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const beneficiario = {
        identificacion: document.getElementById("identificacion").value.trim(),
        nombre_completo: document.getElementById("nombreCompleto").value.trim(),
        comunidad: document.getElementById("comunidad").value.trim(),
        integrantes_hogar: parseInt(document.getElementById("integrantesHogar").value),
        prioridad_social: document.getElementById("prioridadSocial").value
    };

    const esEdicion = identificacionEditando !== null;
    const url = esEdicion ? `/beneficiarios/${identificacionEditando}` : "/beneficiarios/";
    const metodo = esEdicion ? "PUT" : "POST";

    try {
        const respuesta = await apiFetch(url, {
            method: metodo,
            body: JSON.stringify(beneficiario)
        });

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        mostrarMensaje(esEdicion ? "Beneficiario actualizado." : "Beneficiario registrado.");
        salirModoEdicion();
        cargarTodos();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor.", "error");
    }
});

function activarEdicion(beneficiario) {
    identificacionEditando = beneficiario.identificacion;

    document.getElementById("identificacion").value = beneficiario.identificacion;
    document.getElementById("identificacion").disabled = true;
    document.getElementById("nombreCompleto").value = beneficiario.nombre_completo;
    document.getElementById("comunidad").value = beneficiario.comunidad;
    document.getElementById("integrantesHogar").value = beneficiario.integrantes_hogar;
    document.getElementById("prioridadSocial").value = beneficiario.prioridad_social;

    tituloFormulario.textContent = "Editar Beneficiario";
    btnCancelar.classList.remove("hidden");

    window.scrollTo({ top: 0, behavior: "smooth" });
}

function salirModoEdicion() {
    identificacionEditando = null;
    form.reset();
    document.getElementById("identificacion").disabled = false;
    tituloFormulario.textContent = "Registrar Beneficiario";
    btnCancelar.classList.add("hidden");
}

btnCancelar.addEventListener("click", salirModoEdicion);

async function eliminarBeneficiario(identificacion) {
    if (!confirm("¿Seguro que desea eliminar este beneficiario?")) {
        return;
    }

    try {
        const respuesta = await apiFetch(`/beneficiarios/${identificacion}`, { method: "DELETE" });

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        mostrarMensaje("Beneficiario eliminado.");

        if (identificacionEditando === identificacion) {
            salirModoEdicion();
        }

        cargarTodos();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor.", "error");
    }
}

document.getElementById("btnBuscar").addEventListener("click", async () => {
    const identificacion = document.getElementById("buscarIdentificacion").value.trim();

    if (!identificacion) {
        mostrarMensaje("Escriba una identificación para buscar.", "error");
        return;
    }

    try {
        const respuesta = await apiFetch(`/beneficiarios/${identificacion}`);

        if (!respuesta.ok) {
            mostrarMensaje("No se encontró ningún beneficiario con esa identificación.", "error");
            renderizarTabla([]);
            return;
        }

        const beneficiario = await respuesta.json();
        renderizarTabla([beneficiario]);

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error al buscar el beneficiario.", "error");
    }
});

document.getElementById("btnMostrarTodos").addEventListener("click", cargarTodos);

cargarTodos();