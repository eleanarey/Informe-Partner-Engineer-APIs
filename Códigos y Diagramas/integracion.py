'''
Explicación del Script:
Consulta de API B (consultar_api_b): Se envía una solicitud GET con los parámetros start_date y end_date, 
autenticando con la clave x-api-key. Se manejan diferentes errores HTTP como 401 Unauthorized, 403 Forbidden, 
y errores del servidor como 500 Internal Server Error.
Consulta de API A (consultar_api_a): Se realiza la solicitud a la API A con autenticación de tipo Bearer Token. 
Al igual que en la API B, se maneja la autenticación y otros errores de respuesta.
Transformación de Datos (transformar_datos): Los datos recibidos de la API A son transformados para cumplir con 
el formato esperado por la API B. Aquí, los campos se renombran (ej. id a invoice_id, cliente a customer, etc.).
Validación: Los datos transformados se validan para asegurarse de que contienen los campos obligatorios antes de 
ser enviados al cliente.
Envío de Respuesta: Se imprime la respuesta final con las facturas transformadas en formato JSON.
Ejecución:Al ejecutar este script con los parámetros de fecha, primero consultará la API B, luego la API A, 
transformará los datos, los validará, y finalmente imprimirá la respuesta en formato JSON.
'''

import requests
import json

# Configuración de las APIs
api_b_url = "https://api.sistemaB.com/bills"
api_a_url = "https://api.sistemaA.com/facturas"

api_b_key = "tu_api_key_de_sistemaB"
api_a_token = "tu_token_de_sistemaA"

# Función para consultar la API B
def consultar_api_b(start_date, end_date):
    headers = {
        'x-api-key': api_b_key
    }
    params = {
        'start_date': start_date,
        'end_date': end_date
    }

    response = requests.get(api_b_url, headers=headers, params=params)
    return response

# Función para consultar la API A
def consultar_api_a(start_date, end_date):
    headers = {
        'Authorization': f'Bearer {api_a_token}'
    }
    params = {
        'fecha_inicio': start_date,
        'fecha_fin': end_date
    }

    response = requests.get(api_a_url, headers=headers, params=params)
    return response

# Función para transformar los datos de la API A al formato de la API B
def transformar_datos(api_a_data):
    facturas_transformadas = []
    for factura in api_a_data['facturas']:
        factura_transformada = {
            'invoice_id': factura['id'],
            'customer': factura['cliente'],
            'amount_due': factura['monto'],
            'date_issued': factura['fecha_emision'],
            'status': factura['estado']
        }
        facturas_transformadas.append(factura_transformada)
    return facturas_transformadas

# Función principal que realiza la integración
def ejecutar_integracion(start_date, end_date):
    # Paso 1 - Consulta de API B
    print(f"Consultando API B para fechas {start_date} - {end_date}...")
    response_b = consultar_api_b(start_date, end_date)

    if response_b.status_code == 401:
        print("Error: 401 Unauthorized en API B.")
        return
    elif response_b.status_code == 400:
        print("Error: 400 Bad Request en API B.")
        return
    elif response_b.status_code == 403:
        print("Error: 403 Forbidden en API B.")
        return
    elif response_b.status_code == 404:
        print("Error: 404 Not Found en API B.")
        return
    elif response_b.status_code >= 500:
        print(f"Error: {response_b.status_code} Server Error en API B.")
        return

    # Paso 2 - Consulta de API A
    print(f"Consultando API A para fechas {start_date} - {end_date}...")
    response_a = consultar_api_a(start_date, end_date)

    if response_a.status_code == 401:
        print("Error: 401 Unauthorized en API A.")
        return
    elif response_a.status_code >= 400:
        print(f"Error: {response_a.status_code} Error en API A.")
        return

    # Extraer los datos de la API A
    api_a_data = response_a.json()

    # Paso 3 - Transformar los datos
    print("Transformando datos de la API A al formato de la API B...")
    facturas_transformadas = transformar_datos(api_a_data)

    # Paso 4 - Validación de la Respuesta
    print("Validando datos transformados...")
    for factura in facturas_transformadas:
        if not all(key in factura for key in ['invoice_id', 'customer', 'amount_due', 'date_issued', 'status']):
            print("Error: Factura transformada incompleta.")
            return
    
    # Paso 5 - Enviar la respuesta al cliente
    print("Respuesta final:")
    print(json.dumps(facturas_transformadas, indent=2))

# Ejecutar el script de integración con un rango de fechas
if __name__ == "__main__":
    start_date = "2023-01-01"
    end_date = "2023-01-31"
    ejecutar_integracion(start_date, end_date)
