import com.rabbitmq.client.*;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.concurrent.TimeoutException;



public class RecepcionDomicilioEvento {
    private final static String QUEUE_NAME = "hello";
    private Pedido pedido;
    public RecepcionDomicilioEvento(Pedido pedido){
        this.pedido = pedido;
    }
    public void tramitarPedido() throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);
		if(pedido.obtenerTipo().equals("domicilio")){
		    String message = "{\n" +
                    "  \"type\": \"web-create-order\",\n" +
                    "  \"customer\": \""+pedido.obtenerNombreCliente()+"\",\n" +
                    "  \"nit\": \""+pedido.obtenerNit()+"\"";
		    if(pedido.obtenerProductos() != null){
		        message = message + ",\n  \"products\": [\n";
                for(Producto producto : pedido.obtenerProductos()){
                    message = message +"    {\n" +
                            "      \"product\": \""+producto.obtenerNombre()+"\",\n" +
                            "      \"quantity\": "+producto.obtenerCantidad()+"\n" +
                            "    },\n";
                }
                message = message.substring(0, message.length()-2)+"\n]\n}";
            }else {
                message = message + "\n}";
            }
            channel.basicPublish("", QUEUE_NAME, null, message.getBytes());

            Consumer consumer = new DefaultConsumer(channel) {
                @Override
                public void handleDelivery(String consumerTag, Envelope envelope,
                                           AMQP.BasicProperties properties, byte[] body)
                        throws IOException {
                    String message = new String(body, "UTF-8");
                    JSONObject json = null;
                    try {
                        json = new JSONObject(message);
                        String type = json.getString("type");
                        if (type.equals("web-create-order-ok")){
                            System.out.println("Order procesada con exito");
                        }else if (type.equals("web-create-order-error")){
                            try {
                                System.out.println("Error con la orden: " + json.getString("message"));
                            } catch (JSONException e1) {
                                e1.printStackTrace();
                            }
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


                }
            };
            channel.basicConsume(QUEUE_NAME, true, consumer);

        }

        channel.close();
        connection.close();
    }

    public void revisarPedido() throws IOException, TimeoutException {
        String message = "{\n" +
                "  \"type\": \"web-check-order-status\",\n" +
                "  \"order-id\": 1\n" +
                "}";
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("localhost");
        Connection connection = factory.newConnection();
        Channel channel = connection.createChannel();
        channel.queueDeclare(QUEUE_NAME, false, false, false, null);
        channel.basicPublish("", QUEUE_NAME, null, message.getBytes());

        channel.basicPublish("", QUEUE_NAME, null, message.getBytes());

        Consumer consumer = new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope,
                                       AMQP.BasicProperties properties, byte[] body)
                    throws IOException {
                String message = new String(body, "UTF-8");
                JSONObject json = null;
                try {
                    json = new JSONObject(message);
                    System.out.println("Orden en proceso, en la etapa "+json.getString("status"));

                } catch (JSONException e) {
                    e.printStackTrace();
                }


            }
        };


    }
    
}
