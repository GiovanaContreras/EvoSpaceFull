__author__ = 'mariosky'

def trap(u, a=0.75, b=1, z=3 , l=4):
    if sum(u)  <= z :
        return (a/z) * (z - sum(u))
    else:
        return (b/(l-z))*(sum(u)-z)

def trap_m(u,l):
    return sum([trap(m) for m in [u[i:i+l] for i in range(0,len(u),l)]])



#print trap_m([0,0,0,0,  0,0,1,0, 0,0,0,0, 1,0,0,0],4)
#print trap_m([1,1,1,1,  1,1,1,1, 1,1,1,1, 1,1,1,1],4)

