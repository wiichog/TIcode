import pika
import sys
import json
import threading

def sendMessages(messages):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='com')
        
    except:
        print('excep')
        return(False)

    for message in messages:
        channel.basic_publish(exchange='',
                              routing_key='com',
                              body=json.dumps(message))

    print(" [x] Sent %r" % messages)
    connection.close()
    return(True)

def pedir_pedido():
    ok_nombre, ok_nit, ok_ubicacion = False, False, False
    ok_pedido, ok_cantidad, ok_precio = False, False, False
    print('#=====================#')
    print('|      ORDENAR        |')
    print('#=====================#')
    pedidos = []
    cantidades = []
    precios = []
    pedidios_finales = []
    total = 0
    terminar_ordenar = False
    while not terminar_ordenar:
        while not ok_pedido:
            pedido = raw_input('que desea ordenar?: ')
            if len(pedido)>0:
                ok_pedido = True
        while not ok_cantidad:
            cantidad = str(input('Cuantos desea ordenar?: '))
            if len(cantidad)>0:
                ok_cantidad = True
        while not ok_precio:
            precio = str(input('ingrese precio: Q'))
            if len(precio)>0:
                ok_precio = True            
        terminar = raw_input('desea agregar algo mas?: (s/n)')
        pedidos.append(pedido)
        cantidades.append(int(cantidad))
        precios.append(float(precio))

        if terminar != 's':
            terminar_ordenar = True
    for i in range(len(pedidos)):
        temp = {
            "product": pedidos[i],
            "quantity": cantidades[i]
        }
        pedidios_finales.append(temp)
    for i in range(len(precios)):
        total = total + (precios[i] * cantidades[i])

    while not ok_nombre:
        nombre = raw_input('ingrese nombre: ')
        if len(nombre) > 0:
            ok_nombre = True
    while not ok_nit:
        nit = str(raw_input('ingrese nit: '))
        if len(nit) > 0:
            ok_nit = True
    while not ok_ubicacion:
        ubicacion = raw_input('ingrese ubicacion: ')
        if len(ubicacion)>0:
            ok_ubicacion = True


    resumen_orden = respuesta_pedido(nit, nombre, pedidios_finales, total)

    return resumen_orden

# test_respuesta_pedido.py

def respuesta_pedido(NIT, NOMBRE, PRODS, TOTAL):
    respuesta = {
        "type": "web-create-order",
        "customer": NOMBRE,
        "nit": NIT,
        "products": PRODS,
        "total": TOTAL
    }
    return respuesta

def realizar_operacion(NIT, NOMBRE, PRODS, TOTAL):
    mensaje = respuesta_pedido(NIT, NOMBRE, PRODS, TOTAL)
    sendMessages([mensaje])

def test_respuesta_pedido():
    assert respuesta_pedido('1234','Juan',[{'product':'test','quantity':1}],'1.0') == {'customer': 'Juan', 'products': [{'product': 'test', 'quantity': 1}], 'total': 1.0, 'type': 'web-create-order', 'nit': '1234'}

#test_revisar_pedido.py

def revisar_pedido(ID):
    message = {
        "type": "web-check-order-status",
        "order-id": ID
    }
    return message

def test_revisar_pedido():
    assert revisar_pedido(123) == {'type': 'web-check-order-status', 'order-id': 123}

def test_connection():
    assert sendMessages({'Conexion establecida'}) == True 

def test_stress():
    n = 7
    while(n>0):
        thread1 = threading.Thread(target=realizar_operacion, args=('1234','Juan',[{'product':'test','quantity':1}],'1.0'))
        thread1.start()

        n-=1
    while( thread1.isAlive()):
        n = 0
    assert thread1.isAlive() == False
        

def main_menu():
    show = True
    while show:
        print('#=====================#')
        print('|    MENU PRINCIPAL   |')
        print('#=====================#')
        print('*escoja el numero para ingresar*')
        opcion = input(
            "\nque desea hacer?\n1.enviar pedido\n2.verificar orden\n3.salir\n>>")
        if opcion == 1:
            pedido = pedir_pedido()
            print(pedido)
            sendMessages(pedido)
            print("Orden Recibida")
        elif opcion == 2:
            uid = input("Ingrese ID de la orden:\n>>")
            order_check = revisar_pedido(uid)
            print(order_check)
            sendMessages(order_check)
            print("Status: Ok")
        else:
            show = False
            print('opcion no valida')
    print("adios")

#main_menu()
#test_connection()
test_stress()