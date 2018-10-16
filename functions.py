import pika
import sys
import json
import logger


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
    startId = logger.genID()
    logger.writeLog(1,'started Order',startId)
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
            pedido = input('que desea ordenar?: ')
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
        terminar = input('desea agregar algo mas?: (s/n)')
        pedidos.append(pedido)
        cantidades.append(int(cantidad))
        precios.append(float(precio))

        if terminar != 's':
            terminar_ordenar = True
        ok_pedido, ok_cantidad, ok_precio = False, False, False

    for i in range(len(pedidos)):
        temp = {
            "product": pedidos[i],
            "quantity": cantidades[i]
        }
        pedidios_finales.append(temp)
    for i in range(len(precios)):
        total = total + (precios[i] * cantidades[i])

    while not ok_nombre:
        nombre = input('ingrese nombre: ')
        if len(nombre) > 0:
            ok_nombre = True
    while not ok_nit:
        nit = str(input('ingrese nit: '))
        if len(nit) > 0:
            ok_nit = True
    while not ok_ubicacion:
        ubicacion = input('ingrese ubicacion: ')
        if len(ubicacion)>0:
            ok_ubicacion = True


    resumen_orden = respuesta_pedido(nit, nombre, pedidios_finales, total)
    logger.writeLog(1,'end order',startId)

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

def main_menu():
    startId = logger.genID()
    logger.writeLog(1,'started software',startId)
    show = True
    while show:
        transaction = logger.genID()
        logger.writeLog(1, 'Running Menu', transaction)
        print('#=====================#')
        print('|    MENU PRINCIPAL   |')
        print('#=====================#')
        print('*escoja el numero para ingresar*')
        opcion = input(
            "\nque desea hacer?\n1.enviar pedido\n2.verificar orden\n3.query\n4.salir\n>>")
        if opcion == '1':
            logger.writeLog(2,'ordenar pedido', transaction)
            pedido = pedir_pedido()
            print(pedido)
            sendMessages(pedido)
            print("ok")
            logger.writeLog(3,'ordenar pedido', transaction)
        elif opcion == '2':
            logger.writeLog(2,'verificar pedido', transaction)
            uid = input("Ingrese ID de la orden:\n>>")
            order_check = revisar_pedido(uid)
            print(order_check)
            sendMessages(order_check)
            print("ok")
            logger.writeLog(3,'verificar pedido', transaction)
        elif opcion == '3':
            logger.writeLog(2,'query chosed', transaction)
            seekfor = input('ingrese algo a buscar:\n>>')
            logger.queryLog(seekfor)
            print('resultado escrito')
            logger.writeLog(3,'query ', transaction)
        else:
            show = False
            print('opcion no valida')
            logger.writeLog(0, 'opcion no valida', transaction)
    print("adios")
    logger.writeLog(1,'finnished software',startId)

main_menu()