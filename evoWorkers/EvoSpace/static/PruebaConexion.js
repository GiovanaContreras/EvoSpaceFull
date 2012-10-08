var numgen = 1000;


//////////////////////////////////////////// METODO QUE HACE LA CONEXION AL SERVIDOR ///////////////////////////////////
//function Solicitud() {
Conexion = true; // Variable que manipula la conexion.
if (Conexion) //return;  // Previene uso repetido del boton.
    Conectar();
if (Conexion) {
    // Preparacion.
    Conexion.open("POST", '/EvoSpace', false);
    // Manejando eventos.
    Conexion.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    Conexion.onreadystatechange = poblacion;
    // Solicitud al servidor.
    Conexion.send(JSON.stringify({jsonrpc:'2.0',method:'getSample',params:[400],id:"jsonrpc"}));
}
function Conectar() {

    if (XMLHttpRequest) Conexion = new XMLHttpRequest();
    else if (ActiveXObject)
        Conexion = new ActiveXObject("Microsoft.XMLHTTP");
}

   function poblacion() {

        if (Conexion.readyState != 4)
            return;
        if (Conexion.status == 200) {
            var data = JSON.parse(Conexion.response);

            population = JSON.parse(data.result);

            var new_pop = [];

            for (var i = 0, c = population.sample.length; i < c; i++) {

                new_pop.push(population.sample[i].chromosome);

            }
            id = population.sample_id;

/////////////////////////////////////////////Llamada a las funciones de evolucion/////////////////////////////////
            var numgen = 100;
            var k = 0;

            for (var k = 0; k < numgen; k++) {

                var evo = Selection(new_pop)
                var cross = crossover(evo);
                var uni = union(cross);
                var mut = mutation(uni);
                mutFinal = mut;
                fit = FitFinal(mutFinal);

                max = maximo(fit, k);
                fitfin = JSON.stringify(max);

                var whilefit = FitnessStop(mutFinal);
                if (whilefit <= 0) {
                    //whilefit ya es 0
                    k = numgen;
                }
                new_pop = mutFinal;

                postMessage(fitfin);
            }
        }
        obback = objback(fit,id);
        putback = PutBack(obback);


    }


///////////////////////////////////////////////// METODO PARA OBTENER NUMEROS DE FORMA ALEATORIA /////////////////////////

function rand(min, max) {
    // Math.floor gives 'better' random numbers than Math.round, apparently.
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

/////////////////////////////////////////////// METODO PARA OBTENER EL FITNESS DEL CROMOSOMA ////////////////

function fitness(chromosome) {
    var target = "hola mundo";
    // higher fitness is better
    var f = 0; // start at 0 - the best fitness
    for (var i = 0, c = target.length; i < c; i++) {
        // subtract the ascii difference between the target character and the chromosome character. Thus 'c' is fitter than 'd' when compared to 'a'.
        f -= Math.abs(target.charCodeAt(i) - chromosome[i]);
    }
    return f;
}

/////////////////////////////////////////// METODO DE SELECCION, LA SELECCION SE LLEVA ACABO POR TORNEO /////////////////////

function Selection(population) {
    new_gen = [];
    var candidates = [];
    var parents = [];
    for (var i = 0,n = 0, c = population.length; i < c; i += 2,n++) {
        for (var j = 0; j < 2; j++) {
            r = rand(0, population.length - 1);
            candidates[0] = population[r];
            r = rand(0, population.length - 1);
            candidates[1] = population[r];
            r = Math.random();
            if (fitness(candidates[0]) > fitness(candidates[1])) {
                parents[j] = candidates[0];
            } else {
                parents[j] = candidates[1];
            }
        }
        new_gen[n] = parents;
        parents = [];
    }
    return new_gen;
}

////////////////////////////////////////////// METODO DE CRUCE EL CRUCE SE HACE EN UN SOLO PUNTO ///////////////////////

function crossover(evo) {
    var crossoverProb = 0.9;
    var newevo = [];
    for (var i = 0, c = evo.length; i < c; i++) {
        r = Math.random();
        if (r < crossoverProb) {
            var new_parents = [];
            // perform crossover on parents to produce new children:
            crossoverPoint = rand(1, evo[i][0].length - 2); // don't allow crossover to occur at the far ends of the chromosome - that's just a straight swap and therefore simply cloning.
            new_parents[0] = evo[i][0].slice(0, crossoverPoint);
            new_parents[0] = new_parents[0].concat(evo[i][1].slice(crossoverPoint));


            new_parents[1] = evo[i][1].slice(0, crossoverPoint);
            new_parents[1] = new_parents[1].concat(evo[i][0].slice(crossoverPoint));
            newevo[i] = new_parents;
        }
        else {
            // attack of the clones:
            newevo[i] = evo[i];
        }
    }
    return newevo;
}

/////////////////////////////////////////////// METODO UNION NO RECUERDO PARA QUE SIRVE ///////////////////////////////////////

function union(evo) {
    // alert("UNION    " + evo[0]);
    var pop = [];
    for (var i = 0, c = evo.length; i < c; i++) {
        pop.push(evo[i][0]);
        pop.push(evo[i][1]);
    }
    return pop;
}


function FitnessStop(mutFinal) {

    var fitarray2 = [];
    for (var i = 0, c = mutFinal.length; i < c; i++) {

        var fitness2 = fitness(mutFinal[i])

        if (fitness2 == 0) {

            var comfit = 0;
        }


        else{
             var comfit = 1;
        }
    }

    return comfit;
}

///////////////////////////////////////////////////////// METODO MUTACION /////////////////////////////////////////


/*function mutation(evo) {

    var mutationProb = 0.6;
    var target = "hola mundo";
    var new_gen = [];
    for (var i = 0, c = evo.length; i < c; i++) {
        new_gen.push(evo[i]);
        r = Math.random();
        if (r < mutationProb) {
            // chose a point in the chromosome to mutate - can be anywhere
            mutationPoint = rand(0, evo[i].length - 1);
            //[104,111,108,97,32,109,117,110,100,111]
            var numero = rand(0, 9);
            var n = target.charCodeAt(numero);
            new_gen[i][mutationPoint] = n;
        }
        else {
            // attack of the clones:
            new_gen[i] = evo[i];
        }
    }
    return new_gen;
}*/


  function mutation(evo) {
        //alert("mutacion      "+JSON.stringify(evo));
var mutationProb=0.2;

        var new_gen = [];


        for (var i = 0, c = evo.length; i < c; i++) {

            new_gen.push(evo[i]);
            r = Math.random();

            if (r < mutationProb) {

                // chose a point in the chromosome to mutate - can be anywhere
                mutationPoint = rand(0, evo[i].length - 1);
                new_gen[i][mutationPoint] += rand(-5, 5);
            }
            else {
                // attack of the clones:
                new_gen[i] = evo[i];

            }
        }

        return new_gen;
    }
/////////////////////////////////////////////// METODO QUE OBTIENE EL ULTIMO FITNESS ///////////////////////////////////////

function FitFinal(mutFinal) {
    var fitarray = [];
    for (var i = 0, c = mutFinal.length; i < c; i++) {
        var ind = {};
        // var fitness={"DefaultContext":0.0 }
        ind.id = null;
        ind.fitness = {"DefaultContext":fitness(mutFinal[i])};
        ind.chromosome = mutFinal[i];
        fitarray.push(ind);
    }
    return fitarray;
}

///////////////////////////////////////////// METODO PARA OBTENER EL FITNESS MAXIMO Y LE MINIMO //////////////////////////////

function maximo(fitarray,k) {

    var values = [];
    var val = {};
    var i = 0;
    var mn = fitarray[0].fitness.DefaultContext;
    var mxm = fitarray[0].fitness.DefaultContext;
    var suma = 0;
    var sumatotal = 0;
    var chrommn = 0;
    var chromxm = 0;
    var chromsuma = 0;
    var total = 0;



    for (i = 0; i < fitarray.length; i++) {
        if (fitarray[i].fitness.DefaultContext <= mxm) {
            mxm = fitarray[i].fitness.DefaultContext;
            var listamax = fitarray[i].chromosome;
            chromxm = chromosomeToString(fitarray[i].chromosome);
        }
    }
    for (i = 0; i < fitarray.length; i++) {
        if (fitarray[i].fitness.DefaultContext >= mn) {
            mn = fitarray[i].fitness.DefaultContext;
            var listamn = fitarray[i].chromosome;
            chrommn = chromosomeToString(fitarray[i].chromosome);
        }
    }

    val.mn = mn;
    val.chromm = chrommn;
    val.listamn = listamn;

    val.mxm = mxm;
    val.chromxm = chromxm;
    val.listamax = listamax;
    val.generacion=k+1;
    values.push(val);

    return val;

}

///////////////////////////////////////////////METODO DE CONVERTIR A STRING ////////////////////////////////

function chromosomeToString(uni) {
    var str = '';
    for (var i = 0, c = uni.length; i < c; i++) {
        str += String.fromCharCode(uni[i]);
    }
    return str;
}

///////////////////////////////////////////Funcion que crea el objeto que se va a enviar al servidor/////////////////////

function objback(fitarray, popid) {
    var sample_back = {};
    sample_back.sample = fitarray;
    sample_back.sample_id = popid;
    return sample_back;
}

////////////////////////////////////////////funcion que regresa nueva poblacion al servidor//////////////////////////////

function PutBack(obback) {


    Conexion = true; // Variable que manipula la conexion.
    if (Conexion) //return;  // Previene uso repetido del boton.
        Conectar();
    if (Conexion) {
        // Preparacion.
        Conexion.open("POST", '/EvoSpace', false);
        // Manejando eventos.
        Conexion.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        // Conexion.onreadystatechange = poblacion;
        // Solicitud al servidor.
        Conexion.send(JSON.stringify({"jsonrpc": "2.0", "method": "putSample", "params": [obback], "id":"1" }));
    }

    function Conectar() {
        if (XMLHttpRequest) Conexion = new XMLHttpRequest();
        else if (ActiveXObject)
            Conexion = new ActiveXObject("Microsoft.XMLHTTP");
    }
}
