var generation = 1000;
var r;
var target = "hola mundo"
var crossoverProb = 0.9;
var populationSize = 50;
var r;
var candidates = [];
var parents = [];
var mutationProb = 0.2;
var evoFinal;
var crossFinal;
var mutFinal;




function Generations(generation) {

    var evo = Selection(population);
    evoFinal = evo;
    var cross = crossover(evo);  
    crossFinal = cross;
    var uni = union(cross);
    var mut = mutation(uni);
    mutFinal = mut;
    var fit = FitFinal(mutFinal);
    var max = maximo(fit);

}
;
///////////////////////////////METODO DE FITNESS ////////////////////////////////

function fitness(chromosome) {
    //alert("CHORMOSOMO  " + chromosome);

    // higher fitness is better
    var f = 0; // start at 0 - the best fitness
    for (var i = 0, c = target.length; i < c; i++) {
        // subtract the ascii difference between the target character and the chromosome character. Thus 'c' is fitter than 'd' when compared to 'a'.
        f -= Math.abs(target.charCodeAt(i) - chromosome[i]);

    }

    //   alert("fitness    " + f);
    return f;
}

///////////////////////////////METODO DE CONVERTIR A STRING ////////////////////////////////

function chromosomeToString(uni) {

    var str = '';
    for (var i = 0, c = uni.length; i < c; i++) {


        str += String.fromCharCode(uni[i]);
    }
    return str;
}

;

function rand(min, max) {
    // Math.floor gives 'better' random numbers than Math.round, apparently.
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

//////////////////////// METODO PARA SACAR EL MAXIMO Y EL MINIMO //////////
function maximo(fitarray) {

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
    var i = 0;

    for (i = 0; i < fitarray.length; i++) {

        if (fitarray[i].fitness.DefaultContext >= mxm) {
            mxm = fitarray[i].fitness.DefaultContext;
            chromxm = chromosomeToString(fitarray[i].chromosome);
        }

    }

    for (i = 0; i < fitarray.length; i++) {
        if (fitarray[i].fitness.DefaultContext <= mn) {
            mn = fitarray[i].fitness.DefaultContext;
            chrommn = chromosomeToString(fitarray[i].chromosome);
        }
    }

    val.mxm = mxm;
    val.chromm = chrommn;
    val.mn = mn;
    val.chromxm = chromxm;
    val.avg = total;
    val.chromsuma = chromsuma;

    values.push(val);

    return val;

}
;

///////////////////////////////EVOLUCION ////////////////////////////////

function Selection(population) {

    // alert("SELECCION      "+JSON.stringify(population));

    var new_gen = [];
    for (var i = 0,n = 0, c = population.length; i < c; i += 2,n++) {

        for (var j = 0; j < 2; j++) {
            r = rand(0, population.length - 1);

            candidates[0] = population[r];
            // alert("canditatos    "+JSON.stringify(population[r].chromosome));


            r = rand(0, population.length - 1);

            candidates[1] = population[r];

            //  alert("candidato 1  "+population[r]);
            // run tournament to determine winning candidate:
            r = Math.random();

            if (fitness(candidates[0]) < fitness(candidates[1])) {

                // keep fittest candidate
                parents[j] = candidates[0];
                //alert("Parent en 0    "+JSON.stringify(parents[j]));

            } else {

                parents[j] = candidates[1];

            }


        }

        new_gen[n] = parents;
        parents = [];

    }
    // alert("nueva generacion   " + JSON.stringify(new_gen));
    return new_gen;


}

;
function crossover(evo) {

    //  alert("cruce1      " + JSON.stringify(evo));
    //alert("cruce    " + JSON.stringify(evo[0][0].chromosome));
    //alert("cruce    3" + JSON.stringify(evo[0][1].chromosome));
    var newevo = [];

    for (var i = 0, c = evo.length; i < c; i++) {

        r = Math.random();


        if (r < crossoverProb) {
            var new_parents = [];
            // perform crossover on parents to produce new children:
            crossoverPoint = rand(1, evo[i][0].length - 2); // don't allow crossover to occur at the far ends of the chromosome - that's just a straight swap and therefore simply cloning.
            // alert("PUNTO DE CRUCE      "+JSON.stringify(evo[i][0].chromosome));


            new_parents[0] = evo[i][0].slice(0, crossoverPoint);
            //  alert("evo posicion 0   "+evo[0][0]);

            new_parents[0] = new_parents[0].concat(evo[i][1].slice(crossoverPoint));
            //alert("new parents 0        " + new_parents);


            new_parents[1] = evo[i][1].slice(0, crossoverPoint);
            //  alert("evo posicion 1   "+evo[0][1]);

            new_parents[1] = new_parents[1].concat(evo[i][0].slice(crossoverPoint));
            // alert("new parents 1     " + new_parents[i + 1]);

            newevo[i] = new_parents;

        }

        else {
            // attack of the clones:
            newevo[i] = evo[i];
        }
    }
    //  alert("CRUCE----" + JSON.stringify(newevo));

    return newevo;
}

;

function mutation(evo) {
    //alert("mutacion      "+JSON.stringify(evo));


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


;

function union(evo) {
    // alert("UNION    " + evo[0]);
    var pop = [];

    for (var i = 0, c = evo.length; i < c; i++) {

        pop.push(evo[i][0]);
        pop.push(evo[i][1]);


    }
    return pop;


}

;

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




