import socket
import sqlite3
import datetime


HOST = 'localhost'
PORT = 5000
DB_NAME = 'mensajes.db'



def inicializar_db():
    """
    Crea la base de datos SQLite y la tabla 'mensajes' si no existe.
    Campos: id, contenido, fecha_envio, ip_cliente.
    """
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido   TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente  TEXT NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()
        print("[DB] Base de datos inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo inicializar la base de datos: {e}")
        raise



def guardar_mensaje(contenido, ip_cliente):
    """
    Inserta un mensaje recibido en la tabla 'mensajes'.
    Retorna el timestamp generado para enviarlo como confirmación al cliente.
    """
    try:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, timestamp, ip_cliente))
        conexion.commit()
        conexion.close()
        print(f"[DB] Mensaje guardado: '{contenido}' de {ip_cliente} a las {timestamp}")
        return timestamp
    except sqlite3.Error as e:
        print(f"[ERROR] No se pudo guardar el mensaje en la DB: {e}")
        raise



def inicializar_socket():
    """
    Crea y configura el socket del servidor.
    Usa SO_REUSEADDR para evitar el error 'puerto ocupado' al reiniciar.
    """
    try:
        
        servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        
        servidor_socket.bind((HOST, PORT))

        
        servidor_socket.listen(5)

        print(f"[SERVIDOR] Escuchando en {HOST}:{PORT}...")
        return servidor_socket
    except OSError as e:
        print(f"[ERROR] No se pudo inicializar el socket: {e}")
        raise


def aceptar_conexiones(servidor_socket):
    """
    Bucle principal del servidor: acepta clientes y recibe sus mensajes
    hasta que el cliente se desconecta o envía una cadena vacía.
    """
    print("[SERVIDOR] Esperando conexiones (Ctrl+C para detener)...\n")

    while True:
        try:
            
            cliente_socket, direccion_cliente = servidor_socket.accept()
            ip_cliente = direccion_cliente[0]
            print(f"[CONEXIÓN] Cliente conectado desde {ip_cliente}:{direccion_cliente[1]}")

            
            with cliente_socket:
                while True:
                    try:
                        
                        datos = cliente_socket.recv(1024)

                        
                        if not datos:
                            print(f"[CONEXIÓN] Cliente {ip_cliente} desconectado.\n")
                            break

                        mensaje = datos.decode('utf-8').strip()
                        print(f"[MENSAJE] De {ip_cliente}: {mensaje}")

                        
                        timestamp = guardar_mensaje(mensaje, ip_cliente)

                        
                        respuesta = f"Mensaje recibido: {timestamp}"
                        cliente_socket.sendall(respuesta.encode('utf-8'))

                    except ConnectionResetError:
                        print(f"[AVISO] El cliente {ip_cliente} cerró la conexión abruptamente.\n")
                        break

        except KeyboardInterrupt:
            print("\n[SERVIDOR] Cerrando servidor...")
            break
        except Exception as e:
            print(f"[ERROR] Error inesperado al manejar cliente: {e}")



if __name__ == '__main__':
    print("=" * 45)
    print("   SERVIDOR DE CHAT - SOCKETS + SQLITE")
    print("=" * 45)

    inicializar_db()

    
    servidor_socket = inicializar_socket()

    try:
        
        aceptar_conexiones(servidor_socket)
    finally:
        
        servidor_socket.close()
        print("[SERVIDOR] Socket cerrado. ¡Adios!")
