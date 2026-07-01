/*
    Este archivo implementa la lógica del frontend para la gestión de
    entregas alimentarias del sistema Manos Solidarias. Se encarga de cargar
    beneficiarios y recursos disponibles, registrar entregas, actualizar
    datos permitidos, eliminar entregas, restaurar inventario y mostrar el
    historial de entregas consumiendo los endpoints correspondientes de la API.
*/

exigirSesion();
document.getElementById("usuarioInfo").textContent = "Sesión: " + obtenerUsuarioActual();
document.getElementById("btnCerrarSesion").addEventListener("click", cerrarSesion);

const form = document.getElementById("entregaForm");
const tablaBody = document.getElementById("tablaEntregas");
const btnCancelar = document.getElementById("btnCancelar");
const tituloFormulario = document.getElementById("tituloFormulario");
const pistaEdicion = document.getElementById("pistaEdicion");
const beneficiarioSelect = document.getElementById("beneficiarioSelect");
const recursoSelect = document.getElementById("recursoSelect");

let codigoEditando = null;

let mapaBeneficiarios = {};
let mapaRecursos = {};

function formatoColones(valor) {
    return "₡" + Number(valor).toLocaleString("es-CR", { minimumFractionDigits: 2 });
}

async function cargarListasDeApoyo() {
    try {
        const [respBeneficiarios, respRecursos] = await Promise.all([
            apiFetch("/beneficiarios/"),
            apiFetch("/recursos/")
        ]);

        const beneficiarios = await respBeneficiarios.json();
        const recursos = await respRecursos.json();

        mapaBeneficiarios = {};
        beneficiarioSelect.innerHTML = '<option value="">Seleccione un beneficiario...</option>';
        beneficiarios.forEach(b => {
            mapaBeneficiarios[b.identificacion] = b;
            beneficiarioSelect.innerHTML +=
                `<option value="${b.identificacion}">${b.nombre_completo} (${b.identificacion})</option>`;
        });

        mapaRecursos = {};
        recursoSelect.innerHTML = '<option value="">Seleccione un recurso...</option>';
        recursos.forEach(r => {
            mapaRecursos[r.codigo_recurso] = r;
            recursoSelect.innerHTML +=
                `<option value="${r.codigo_recurso}">${r.nombre} (${r.codigo_recurso})</option>`;
        });

    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudieron cargar beneficiarios y recursos.", "error");
    }
}

function nombreBeneficiario(identificacion) {
    const b = mapaBeneficiarios[identificacion];
    return b ? b.nombre_completo : identificacion;
}

function nombreRecurso(codigo) {
    const r = mapaRecursos[codigo];
    return r ? r.nombre : codigo;
}

function unidadRecurso(codigo) {
    const r = mapaRecursos[codigo];
    return r ? r.unidad_medida : "";
}

function renderizarTabla(entregas) {
    if (entregas.length === 0) {
        tablaBody.innerHTML = `<tr><td colspan="8" class="sin-datos">No hay entregas para mostrar.</td></tr>`;
        return;
    }

    tablaBody.innerHTML = entregas.map(e => `
        <tr>
            <td>${e.codigo_entrega}</td>
            <td>${nombreBeneficiario(e.identificacion_beneficiario)}</td>
            <td>${nombreRecurso(e.codigo_recurso)}</td>
            <td>${e.cantidad_entregada} ${unidadRecurso(e.codigo_recurso)}</td>
            <td>${e.fecha}</td>
            <td>${e.responsable_entrega}</td>
            <td>${formatoColones(e.valor_economico)}</td>
            <td class="celda-acciones">
                <button class="btn-primario btn-pequeno" onclick='activarEdicion(${JSON.stringify(e)})'>Editar</button>
                <button class="btn-peligro btn-pequeno" onclick="eliminarEntrega('${e.codigo_entrega}')">Eliminar</button>
            </td>
        </tr>
    `).join("");
}

async function cargarTodas() {
    try {
        const respuesta = await apiFetch("/entregas/");
        renderizarTabla(await respuesta.json());
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudieron cargar las entregas.", "error");
    }
}

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const esEdicion = codigoEditando !== null;

    try {
        let respuesta;

        if (esEdicion) {
            respuesta = await apiFetch(`/entregas/${codigoEditando}`, {
                method: "PUT",
                body: JSON.stringify({
                    fecha: document.getElementById("fecha").value,
                    responsable_entrega: document.getElementById("responsableEntrega").value.trim()
                })
            });
        } else {
            const entrega = {
                codigo_entrega: document.getElementById("codigoEntrega").value.trim(),
                identificacion_beneficiario: beneficiarioSelect.value,
                codigo_recurso: recursoSelect.value,
                cantidad_entregada: parseInt(document.getElementById("cantidadEntregada").value),
                fecha: document.getElementById("fecha").value,
                responsable_entrega: document.getElementById("responsableEntrega").value.trim()
            };

            respuesta = await apiFetch("/entregas/", {
                method: "POST",
                body: JSON.stringify(entrega)
            });
        }

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        mostrarMensaje(esEdicion ? "Entrega actualizada." : "Entrega registrada y stock descontado.");
        salirModoEdicion();
        await cargarListasDeApoyo();
        await cargarTodas();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor.", "error");
    }
});

function activarEdicion(entrega) {
    codigoEditando = entrega.codigo_entrega;

    document.getElementById("codigoEntrega").value = entrega.codigo_entrega;
    document.getElementById("codigoEntrega").disabled = true;
    beneficiarioSelect.value = entrega.identificacion_beneficiario;
    beneficiarioSelect.disabled = true;
    recursoSelect.value = entrega.codigo_recurso;
    recursoSelect.disabled = true;
    document.getElementById("cantidadEntregada").value = entrega.cantidad_entregada;
    document.getElementById("cantidadEntregada").disabled = true;
    document.getElementById("fecha").value = entrega.fecha;
    document.getElementById("responsableEntrega").value = entrega.responsable_entrega;

    tituloFormulario.textContent = "Editar Entrega";
    btnCancelar.classList.remove("hidden");
    pistaEdicion.style.display = "block";

    window.scrollTo({ top: 0, behavior: "smooth" });
}

function salirModoEdicion() {
    codigoEditando = null;
    form.reset();
    document.getElementById("codigoEntrega").disabled = false;
    beneficiarioSelect.disabled = false;
    recursoSelect.disabled = false;
    document.getElementById("cantidadEntregada").disabled = false;
    tituloFormulario.textContent = "Registrar Entrega";
    btnCancelar.classList.add("hidden");
    pistaEdicion.style.display = "none";
}

btnCancelar.addEventListener("click", salirModoEdicion);

async function eliminarEntrega(codigo) {
    if (!confirm("¿Seguro que desea eliminar esta entrega? Se restaurará el inventario.")) {
        return;
    }

    try {
        const respuesta = await apiFetch(`/entregas/${codigo}`, { method: "DELETE" });

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        mostrarMensaje("Entrega eliminada y stock restaurado.");

        if (codigoEditando === codigo) {
            salirModoEdicion();
        }

        await cargarListasDeApoyo();
        await cargarTodas();

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error de conexión con el servidor.", "error");
    }
}

document.getElementById("btnBuscar").addEventListener("click", async () => {
    const codigo = document.getElementById("buscarCodigoEntrega").value.trim();

    if (!codigo) {
        mostrarMensaje("Escriba un código de entrega para buscar.", "error");
        return;
    }

    try {
        const respuesta = await apiFetch(`/entregas/${codigo}`);

        if (!respuesta.ok) {
            mostrarMensaje("No se encontró ninguna entrega con ese código.", "error");
            renderizarTabla([]);
            return;
        }

        const entrega = await respuesta.json();
        renderizarTabla([entrega]);

    } catch (error) {
        console.error(error);
        mostrarMensaje("Error al buscar la entrega.", "error");
    }
});

document.getElementById("btnMostrarTodos").addEventListener("click", cargarTodas);

(async () => {
    await cargarListasDeApoyo();
    await cargarTodas();
})();