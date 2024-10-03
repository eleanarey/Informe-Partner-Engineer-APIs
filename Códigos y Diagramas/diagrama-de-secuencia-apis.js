sequenceDiagram
    participant Cliente
    participant API_B as API B
    participant API_A as API A

    Cliente->>API_B: GET /bills con start_date y end_date
    API_B->>API_B: Validar autenticación (x-api-key)
    
    alt Autenticación fallida
        API_B -->> Cliente: 401 Unauthorized
    else Solicitud malformada
        API_B -->> Cliente: 400 Bad Request
    else Sin permiso
        API_B -->> Cliente: 403 Forbidden
    else No encontrado
        API_B -->> Cliente: 404 Not Found
    else Error interno del servidor
        API_B->>API_B: Validar conexión al servidor
        alt Error en la conexión al servidor
            API_B -->> Cliente: 500 Internal Server Error
        else Respuesta no válida de upstream
            API_B -->> Cliente: 502 Bad Gateway
        else Servicio no disponible
            API_B -->> Cliente: 503 Service Unavailable
        else Tiempo de espera agotado
            API_B -->> Cliente: 504 Gateway Timeout
        end
    else Autenticación exitosa
        API_B->>API_A: GET /facturas con fecha_inicio y fecha_fin
        API_A->>API_A: Validar autenticación (Bearer Token)
        alt Manejo de errores del lado de cliente o servidor
            API_A-->>API_B: Error de tipo 4xx-5xx
        else Autenticación exitosa
            API_A-->>API_B: 200 OK (facturas JSON)
            API_B->>API_B: Transformar datos (id a invoice_id, cliente a customer)
            API_B-->>Cliente: 200 OK (facturas transformadas)
            alt Respuesta sin contenido
                API_B -->> Cliente: 204 No Content
            end
        end
    end
