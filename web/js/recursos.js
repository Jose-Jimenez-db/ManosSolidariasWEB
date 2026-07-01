/*
    Este archivo implementa la lógica del frontend para la gestión de
    recursos alimenticios del sistema Manos Solidarias. Se encarga de cargar,
    registrar, buscar por código, editar, eliminar y mostrar los recursos
    disponibles en la tabla, consumiendo los endpoints correspondientes de
    la API mediante funciones comunes de comunicación.
*/

exigirSesion();
document.getElementById("usuarioInfo").textContent = "Sesión: " + obtenerUsuarioActual();
document.getElementById("btnCerrarSesion").addEventListener("click", cerrarSesion);

const form = document.getElementById("recursoForm");
const tablaBody = document.getElementById("tablaRecursos");
const btnCancelar = document.getElementById("btnCancelar");
const tituloFormulario = document.getElementById("tituloFormulario");

let codigoEditando = null;

function formatoColones(valor) {
    return "₡" + Number(valor).toLocaleString("es-CR", { minimumFractionDigits: 2 });
}

function renderizarTabla(recursos) {
    if (recursos.length === 0) {
        tablaBody.innerHTML = `<tr><td colspan="6" class="sin-datos">No hay recursos para mostrar.</td></tr>`;
        return;
    }

    tablaBody.innerHTML = recursos.map(r => `
        <tr>
            <td>${r.codigo_recurso}</td>
            <td>${r.nombre}</td>
            <td>${r.categoria}</td>
            <td>${r.cantidad_disponible} ${r.unidad_medida}</td>
            <td>${formatoColones(r.costo_unitario)}</td>
            <td class="celda-acciones">
                <button class="btn-primario btn-pequeno" onclick='activarEdicion(${JSON.stringify(r)})'>Editar</button>
                <button class="btn-peligro btn-pequeno" onclick="eliminarRecurso('${r.codigo_recurso}')">Eliminar</button>
            </td>
        </tr>
    `).join("");
}

async function cargarTodos() {
    try {
        const respuesta = await apiFetch("/recursos/");
        renderizarTabla(await respuesta.json());
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudieron cargar los recursos.", "error");
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const recurso = {
        codigo_recurso: document.getElementById("codigoRecurso").value.trim(),
        nombre: document.getElementById("nombre").value.trim(),
        categoria: document.getElementById("categoria").value.trim(),
        unidad_medida: document.getElementById("unidadMedida").value.trim(),
        cantidad_disponible: parseInt(document.getElementById("cantidadDisponible").value),
        costo_unitario: parseFloat(document.getElementById("costoUnitario").value)
    };

    const esEdicion = codigoEditando !== null;
    const url = esEdicion ? `/recursos/${codigoEditando}` : "/recursos/";
    const metodo = esEdicion ? "PUT" : "POST";

    try {
        const respuesta = await apiFetch(url, {
            method: metodo,
            body: JSON.stringify(recurso)
        });

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        mostrarMensaje(esEdicion ? "Recurso actualizado." : "Recurso registrado.");
        salirModoEdicion();
        cargarTodos();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor.", "error");
    }
});

function activarEdicion(recurso) {
    codigoEditando = recurso.codigo_recurso;

    document.getElementById("codigoRecurso").value = recurso.codigo_recurso;
    document.getElementById("codigoRecurso").disabled = true;
    document.getElementById("nombre").value = recurso.nombre;
    document.getElementById("categoria").value = recurso.categoria;
    document.getElementById("unidadMedida").value = recurso.unidad_medida;
    document.getElementById("cantidadDisponible").value = recurso.cantidad_disponible;
    document.getElementById("costoUnitario").value = recurso.costo_unitario;

    tituloFormulario.textContent = "Editar Recurso Alimenticio";
    btnCancelar.classList.remove("hidden");

    window.scrollTo({ top: 0, behavior: "smooth" });
}

function salirModoEdicion() {
    codigoEditando = null;
    form.reset();
    document.getElementById("codigoRecurso").disabled = false;
    tituloFormulario.textContent = "Registrar Recurso Alimenticio";
    btnCancelar.classList.add("hidden");
}

btnCancelar.addEventListener("click", salirModoEdicion);

async function eliminarRecurso(codigo) {
    if (!confirm("¿Seguro que desea eliminar este recurso?")) {
        return;
    }

    try {
        const respuesta = await apiFetch(`/recursos/${codigo}`, { method: "DELETE" });

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        mostrarMensaje("Recurso eliminado.");

        if (codigoEditando === codigo) {
            salirModoEdicion();
        }

        cargarTodos();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor.", "error");
    }
}

document.getElementById("btnBuscarCodigo").addEventListener("click", async () => {
    const codigo = document.getElementById("buscarCodigo").value.trim();

    if (!codigo) {
        mostrarMensaje("Escriba un código para buscar.", "error");
        return;
    }

    try {
        const respuesta = await apiFetch(`/recursos/${encodeURIComponent(codigo)}`);

        if (!respuesta.ok) {
            mostrarMensaje("No se encontró ningún recurso con ese código.", "error");
            renderizarTabla([]);
            return;
        }

        const recurso = await respuesta.json();
        renderizarTabla([recurso]);

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error al buscar el recurso.", "error");
    }
});

document.getElementById("btnMostrarTodos").addEventListener("click", cargarTodos);

cargarTodos();