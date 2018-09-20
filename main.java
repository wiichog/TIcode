public class main {
    //private static final RecepcionDomicilioEvento eventos = new RecepcionDomicilioEvento();
    
    public static void main(String[] args) {
        Pedido pedido = new Pedido();//crear un pedido para ver si funciona
        Thread eventosThread = new Thread(new RecepcionDomicilioEvento(pedido));
        eventosThread.start();
    }
}