// static/js/api.js

export async function fetchProtectedData(endpoint, options = {}) {
    const token = localStorage.getItem('firebaseToken');
    
    // Si no hay token, no intentes hacer la petición
    if (!token) {
        console.error("Acceso denegado: No hay token de Firebase.");
        return null;
    }

    // Asegura que siempre se envíe el header de autorización
    const headers = {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json' // Generalmente útil para APIs
    };

    try {
        const response = await fetch(endpoint, {
            ...options,
            headers: headers
        });

        if (response.status === 401) {
             // Si Django devuelve No Autorizado, borra el token y redirige
             localStorage.removeItem('firebaseToken');
             window.location.href = "{% url 'login' %}"; // Redirige al login
             return null;
        }

        return response.json();

    } catch (error) {
        console.error("Error al acceder al endpoint protegido:", error);
        return null;
    }
}