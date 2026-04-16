import socket


HOST = 'localhost'
PORT = 5000



def conectar_servidor():
    """
    Crea un socket TCP/IP y lo conecta al servidor en HOST:PORT.
    Retorna el socket conectado o lanza una excepción si falla.
    """
    try:
        
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        
        cliente_socket.connect((HOST, PORT))
        print(f"[CLIENTE] Conectado al servidor {HOST}:{PORT}")
        print("[CLIENTE] Escribí tus mensajes (escribí 'éxito' para salir):\n")
        return cliente_socket
    except ConnectionRefusedError:
        print(f"[ERROR] No se pudo conectar a {HOST}:{PORT}. ¿El servidor está corriendo?")
        raise
    except Exception as e:
        print(f"[ERROR] Error al conectar: {e}")
        raise


def enviar_mensajes(cliente_socket):
    """
    Bucle: el usuario escribe mensajes que se envían al servidor.
    Para cuando el usuario escribe 'éxito'.
    """
    while True:
        try:
            
            mensaje = input("user: ").strip()

            
            if mensaje.lower() == 'éxito':
                print("[CLIENTE] Cerrando conexión. ¡Hasta luego!")
                break

            
            if not mensaje:
                print("[AVISO] No podés enviar un mensaje vacío.")
                continue

            
            cliente_socket.sendall(mensaje.encode('utf-8'))

            
            respuesta = cliente_socket.recv(1024).decode('utf-8')
            print(f"[SERVIDOR] {respuesta}\n")

        except KeyboardInterrupt:
            print("\n[CLIENTE] Interrumpido por el usuario.")
            break
        except ConnectionResetError:
            print("[ERROR] El servidor cerró la conexión inesperadamente.")
            break
        except Exception as e:
            print(f"[ERROR] Error al enviar mensaje: {e}")
            break



if __name__ == '__main__':
    print("=" * 45)
    print("   CLIENTE DE CHAT - SOCKETS")
    print("=" * 45)

    try:
        
        cliente_socket = conectar_servidor()

        
        with cliente_socket:
            enviar_mensajes(cliente_socket)

    except Exception:
        print("[CLIENTE] No se pudo iniciar el cliente.")
