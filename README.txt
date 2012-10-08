Poulation snapshots are taken each 10 returned samples, and also the final
state, indicated as the last sample returned. These files have an extension
of .pops.txt 

Each record represents an individual of the population. The columns are separated by a single space, and have the following data:
Column#	Data
1		Iteration number
2		Sample number where the population was taken
3		The individual´s chromosome
4		Fitness (-1 indicates a not yet evaluated individual)

There is a special record separating each iteration, this
has the total time taken to complete  that iteration in seconds.
	
A sample of the file:

0 10 0011000101100101110010011010101011110000 -1.0  
0 10 1011100000001111111101010000111111111110 6.25
0 10 1010010110010011101110110001001000101010 -1.0
0 10 1000010000010100101100100100100010100011 -1.0
0 10 1111110101001111111100110000111100110100 6.25
0 10 1111100100001111110010011000110111110111 5.0
.... Many records
0 39 1111101001100011000010011111100011000101 -1.0
0 39 0100101111111110010111111111111100000010 6.0
0 39 1111111111110111111101100110000010110001 5.75
0 39 0100111111001111101010001111000110100100 5.75
0 39 1010111110111111111100101111010010101000 6.0
0 39 1111111101111110111101001110010011110000 5.75
129.360737085
1 10 1001101110100001010100111001111110100000 -1.0
1 10 1111000000101011111100001111111010010000 6.0
1 10 1010000000100001011010111100100010001001 -1.0
1 10 1110101010100101101101011000011111011101 -1.0
1 10 1011111101110100100011110100110001101111 5.0
.... Many more

Each worker has a corresponding file where data about that worker´s
evolutions are stored. These files or file in the canonical case are named
k?w?s?.workerN.txt where N is the worker number.

Data is stored about each generation:
Column#	Data
0		Iteration number
1		Worker number (doesn't change in each file )
2		Sample ID, of the form: pop:sample:1
3		Generation Number
4		Maximum Fitness
5		Minimum Fitness
6		Average Fitness

Note that the last record of each worker can be truncated
because workers are immediately killed when an optimal solution
is found. 

49 0 pop:sample:140 25 9.25 3.0 5.6328125
49 0 pop:sample:140 26 9.25 3.25 5.4921875
49 0 pop:sample:140 27 9.25 3.25 5.6484375
49 0 pop:sample:140 2 


  
