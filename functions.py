#import pika
#import sys
#import json


def sendMessages(messages):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    channel.exchange_declare(exchange='events',
                             exchange_type='fanout')

    for message in messages:
        channel.basic_publish(exchange='events',
                              routing_key='',
                              body=json.dumps(message))
    print(" [x] Sent %r" % message)
    connection.close()


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
            pedido = input('que desea ordenar?: ')
            if len(pedido)>0:
                ok_pedido = True
        while not ok_cantidad:
            cantidad = input('Cuantos desea ordenar?: ')
            if len(cantidad)>0:
                ok_cantidad = True
        while not ok_precio:
            precio = input('ingrese precio: Q')
            if len(precio)>0:
                ok_precio = True            
        terminar = input('desea agregar algo mas?: (s/n)')
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
        nombre = input('ingrese nombre: ')
        if len(nombre) > 0:
            ok_nombre = True
    while not ok_nit:
        nit = input('ingrese nit: ')
        if len(nit) > 0:
            ok_nit = True
    while not ok_ubicacion:
        ubicacion = input('ingrese ubicacion: ')
        if len(ubicacion)>0:
            ok_ubicacion = True


    resumen_orden = respuesta_pedido(nit, nombre, pedidios_finales, total)

    return resumen_orden


def respuesta_pedido(NIT, NOMBRE, PRODS, TOTAL):
    respuesta = {
        "type": "web-create-order",
        "customer": NOMBRE,
        "nit": NIT,
        "products": PRODS,
        "total": TOTAL
    }
    return respuesta


def revisar_pedido(ID):
    message = {
        "type": "web-check-order-status",
        "order-id": ID
    }
    return message


def main_menu():
    show = True
    while show:
        print('#=====================#')
        print('|    MENU PRINCIPAL   |')
        print('#=====================#')
        print('*escoja el numero para ingresar*')
        opcion = input(
            "\nque desea hacer?\n1.enviar pedido\n2.verificar orden\n3.salir\n>>")
        if opcion == '1':
            pedido = pedir_pedido()
            print(pedido)
            # sendMessages(pedidos)
            print("ok")
        elif opcion == '2':
            uid = input("Ingrese ID de la orden:\n>>")
            order_check = revisar_pedido(uid)
            print(order_check)
            # sendMessages(order_check)
            print("ok")
        else:
            show = False
            print('opcion no valida')
    print("adios")

main_menu()
