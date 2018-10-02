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
    pedidos = []
    cantidades = []
    precios = []
    pedidios_finales = []
    total = 0
    terminar_ordenar = False
    while not terminar_ordenar:
        pedido = input('que desea ordenar?: ')
        cantidad = int(input('Cuantos desea ordenar?: '))
        precio = float(input('ingrese precio: Q'))
        terminar = input('desea agregar algo mas?: (s/n)')
        pedidos.append(pedido)
        cantidades.append(cantidad)
        precios.append(precio)

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

    nombre = input('ingrese nombre: ')
    nit = input('ingrese nit: ')
    ubicacion = input('ingrese ubicacion: ')

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
        opcion = input(
            "que desea hacer?\n1.enviar pedido\n2.verificar orden\n3.salir\n>>")
        if opcion == '1':
            pedido = pedir_pedido()
            print(pedido)
            # sendMessages(pedidos)
            print("ok")
        elif opcion == '2':
            uid = input("Ingrese ID de la orden: ")
            order_check = revisar_pedido(uid)
            print(order_check)
            # sendMessages(order_check)
            print("ok")
        else:
            show = False
    print("adios")

main_menu()