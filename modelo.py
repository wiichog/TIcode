def modelo(total, pedidos_finales):
    pedidos = 0
    no_inventario = 0
    file = open('inventario.txt','r')
    modelo = open('modelo.txt','r')
    line_modelo = modelo.readline()
    line = file.readline()
    inventario = {}
#-----------------inventario de prueba --------------------------------------------
    while(line != ""):
        elemento,cantidad = line.split(':')
        inventario[elemento] = cantidad
        line = file.readline()
#-----------------inventario de prueba --------------------------------------------
#-----------------contando cuanto pedidos --------------------------------------------
    cantidad_pedido = inventario['cantidades']
    cantidad_no = inventario['noEnInventario']
    for i  in pedidos_finales:
        print(str(inventario[i['product']])[:-1]< i['quantity'])
        if(str(inventario[i['product']])[:-1] == 0 or str(inventario[i['product']])[:-1]<str(i['quantity'])):
            cantidad_no = int(cantidad_no)+1
    print(cantidad_no)
    if(cantidad_no != 0):
        cantidad_pedido = int(cantidad_pedido) + 1


#--------------------------------------------------------------------------------------------------
    modelo = open('modelo.txt','w')
    modelo.write('totalPedidos:'+str(cantidad_pedido)+'\n')
    modelo.write('pedidos no cumplido:'+str(cantidad_no)+'\n')
    modelo.write('total ultimo pedido:'+str(total)+'\n')

    file.close()
    modelo.close()

modelo(20,[{"product": 'pollo',"quantity": 4}])
