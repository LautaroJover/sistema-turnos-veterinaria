const API_URL = "http://127.0.0.1:8000";

export async function peticionApi(endpoint, metodo = "GET", cuerpo = null, token = null) {
  const headers = { "Content-Type": "application/json" };
  if (token) headers["Authorization"] = `Bearer ${token}`;

  const config = { method: metodo, headers };
  if (cuerpo) config.body = JSON.stringify(cuerpo);

  const respuesta = await fetch(`${API_URL}${endpoint}`, config);
  const datos = await respuesta.json();
  if (!respuesta.ok) {
    throw new Error(datos.detail || "Error en la petición al servidor");
  }
  return datos;
}