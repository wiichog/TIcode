import java.util.ArrayList;

public class Pedido
{
    private String nombreCliente;

    private String ubicacion;

    private String precio;

    private ArrayList <Producto> productos;

    private String tipoPedido;

    private Integer cantidadProductos;

    private String nit;

    private String identificador;

    public Pedido(String nombreCliente, String ubicacion, String precio, ArrayList<Producto> productos, String tipoPedido, Integer cantidadProductos, String nit) {
        this.nombreCliente = nombreCliente;
        this.ubicacion = ubicacion;
        this.precio = precio;
        this.productos = productos;
        this.tipoPedido = tipoPedido;
        this.cantidadProductos = cantidadProductos;
        this.nit = nit;
    }

    public Pedido(String nombreCliente, String ubicacion, String precio, ArrayList<Producto> productos, String tipoPedido, Integer cantidadProductos, String nit, String identificador) {
        this.nombreCliente = nombreCliente;
        this.ubicacion = ubicacion;
        this.precio = precio;
        this.productos = productos;
        this.tipoPedido = tipoPedido;
        this.cantidadProductos = cantidadProductos;
        this.nit = nit;
        this.identificador = identificador;
    }

    public void setIdentificador(String identificador) {        this.identificador = identificador;    }

    public String obtenerIdentificador() {        return identificador;    }

    public String obtenerTipo(){
    return tipoPedido;
}

    public String obtenerLugar(){
        return ubicacion;
    }

    public String obtenerNombreCliente(){
        return nombreCliente;
    }

    public String obtenerPrecio(){
        return precio;
    }

    public ArrayList<Producto> obtenerProductos(){
        return productos;
    }

    public Integer obtenerCantidadDeProductos(){
        return cantidadProductos;
    }

    public String getLugar() {
        // TODO Auto-generated method stub
        return null;
    }

    public String obtenerNit() { return nit;    }
}
