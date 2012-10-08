function PutBack() {

    if (Conexion) //return;  // Previene uso repetido del boton.

        Conectar();


    if (Conexion) {
        // Preparacion.
        Conexion.open("POST", '/EvoSpace', true);
        // Manejando eventos.
        Conexion.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // Conexion.onreadystatechange = poblacion;
        // Solicitud al servidor.
        Conexion.send(JSON.stringify({"jsonrpc": "2.0", "method": "putSample", "params": [obback], "id": 1 }));
    }


    function Conectar() {


        alert("oshkasjdhflasjhdlkfahsldhflasdhflahsjd");

        if (window.XMLHttpRequest) Conexion = new XMLHttpRequest();

        else if (window.ActiveXObject)

            Conexion = new ActiveXObject("Microsoft.XMLHTTP");
    }

    ;


}
;
