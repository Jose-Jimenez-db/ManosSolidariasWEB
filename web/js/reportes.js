/*
    Este archivo implementa la lógica del frontend para la generación de
    reportes del sistema Manos Solidarias. Se encarga de solicitar datos a
    la API, procesar las respuestas recibidas y mostrar en pantalla los
    reportes relacionados con beneficiarios por comunidad, inventario bajo,
    recursos más entregados y costo total de ayuda distribuida.
*/

exigirSesion();
document.getElementById("usuarioInfo").textContent = "Sesión: " + obtenerUsuarioActual();
document.getElementById("btnCerrarSesion").addEventListener("click", cerrarSesion);

function formatoColones(valor) {
    return "₡" + Number(valor).toLocaleString("es-CR", { minimumFractionDigits: 2 });
}

function tablaVacia(mensaje) {
    return `<p class="sin-datos">${mensaje}</p>`;
}

document.getElementById("btnReporte1").addEventListener("click", async () => {
    const contenedor = document.getElementById("resultadoReporte1");

    try {
        const respuesta = await apiFetch("/reportes/beneficiarios-por-comunidad");
        const datos = await respuesta.json();

        if (datos.length === 0) {
            contenedor.innerHTML = tablaVacia("Todavía no hay beneficiarios registrados.");
            return;
        }

        contenedor.innerHTML = `
            <table>
                <thead><tr><th>Comunidad</th><th>Cantidad de beneficiarios</th></tr></thead>
                <tbody>
                    ${datos.map(d => `
                        <tr><td>${d.comunidad}</td><td>${d.cantidad_beneficiarios}</td></tr>
                    `).join("")}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudo generar el reporte.", "error");
    }
});

document.getElementById("btnReporte2").addEventListener("click", async () => {
    const contenedor = document.getElementById("resultadoReporte2");
    const limite = document.getElementById("limiteInventario").value || 10;

    try {
        const respuesta = await apiFetch(`/reportes/inventario-bajo?limite=${limite}`);

        if (!respuesta.ok) {
            mostrarMensaje(await obtenerMensajeError(respuesta), "error");
            return;
        }

        const datos = await respuesta.json();

        if (datos.length === 0) {
            contenedor.innerHTML = tablaVacia(`No hay recursos por debajo de ${limite} unidades.`);
            return;
        }

        contenedor.innerHTML = `
            <table>
                <thead><tr><th>Código</th><th>Nombre</th><th>Cantidad disponible</th></tr></thead>
                <tbody>
                    ${datos.map(r => `
                        <tr><td>${r.codigo_recurso}</td><td>${r.nombre}</td><td>${r.cantidad_disponible} ${r.unidad_medida}</td></tr>
                    `).join("")}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudo generar el reporte.", "error");
    }
});

document.getElementById("btnReporte3").addEventListener("click", async () => {
    const contenedor = document.getElementById("resultadoReporte3");

    try {
        const respuesta = await apiFetch("/reportes/recursos-mas-entregados");
        const datos = await respuesta.json();

        if (datos.length === 0) {
            contenedor.innerHTML = tablaVacia("Todavía no se han registrado entregas.");
            return;
        }

        contenedor.innerHTML = `
            <table>
                <thead><tr><th>#</th><th>Recurso</th><th>Cantidad total entregada</th></tr></thead>
                <tbody>
                    ${datos.map((r, indice) => `
                        <tr>
                            <td>${indice + 1}</td>
                            <td>${r.nombre}</td>
                            <td>${r.cantidad_total_entregada} ${r.unidad_medida}</td>
                        </tr>
                    `).join("")}
                </tbody>
            </table>
        `;
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudo generar el reporte.", "error");
    }
});

document.getElementById("btnReporte4").addEventListener("click", async () => {
    const contenedor = document.getElementById("resultadoReporte4");

    try {
        const respuesta = await apiFetch("/reportes/costo-total-distribuido");
        const datos = await respuesta.json();

        contenedor.innerHTML = `
            <p>Total invertido en ayuda alimentaria distribuida hasta la fecha:</p>
            <div class="metrica-grande">${formatoColones(datos.costo_total_distribuido)}</div>
        `;
    } catch (error) {
        console.error(error);
        mostrarMensaje("No se pudo generar el reporte.", "error");
    }
});