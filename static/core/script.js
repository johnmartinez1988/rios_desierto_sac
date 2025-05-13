function buscarCliente() {
    const tipoDocumento = document.getElementById('tipo_documento').value;
    const numeroDocumento = document.getElementById('numero_documento').value;
    const resultadoDiv = document.getElementById('resultado');
    const comprasList = document.getElementById('compras');
    comprasList.innerHTML = ''; // Limpiar la lista de compras

    fetch(`/api/cliente/?numero_documento=${numeroDocumento}&tipo_documento=${tipoDocumento}`)
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.error || 'Error al buscar el cliente'); });
            }
            return response.json();
        })
        .then(data => {
            document.getElementById('tipo_doc').textContent = data.tipo_documento;
            document.getElementById('num_doc').textContent = data.numero_documento;
            document.getElementById('nombre').textContent = data.nombre;
            document.getElementById('apellido').textContent = data.apellido;
            document.getElementById('correo').textContent = data.correo || 'N/A';
            document.getElementById('telefono').textContent = data.telefono || 'N/A';

            if (data.compras && data.compras.length > 0) {
                data.compras.forEach(compra => {
                    const listItem = document.createElement('li');
                    listItem.textContent = `${compra.producto} - Fecha: ${compra.fecha} - Monto: ${compra.monto}`;
                    comprasList.appendChild(listItem);
                });
            } else {
                const listItem = document.createElement('li');
                listItem.textContent = 'No se encontraron compras asociadas.';
                comprasList.appendChild(listItem);
            }

            resultadoDiv.style.display = 'block';
        })
        .catch(error => {
            alert(error.message);
            resultadoDiv.style.display = 'none';
        });
}
