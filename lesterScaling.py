
# Each of the LESTER SCALING FUNCTIONS provided in this library is is a function f(x,p) 
# defined on x in [0,1] and p in (-1,+1) in such a way that the following properties hold:
#
#      (0) f(x,p) in [0,1].
#      (1) f(x,0) = x 
#      (2) f(1,p) = 1.
#      (3) f(0,p) = 0.
#      (4) f(x,p) < f(y,p)  if and only if x < y.
#      (5) f(x,p) = f(y,p)  if and only if x = y.
#      (6) lim_{p->+1} f(x,p) = 1 for all x in (0,1].
#      (7) lim_{p->-1} f(x,p) = 0 for all x in [0,1).
#
# In other words:
#
#    * each of the LESTER SCALING FUNCTIONS is a non-linear endpoint-preserving and rank-preserving
# rescalings of x on the unit interval [0,1], 
#    * p=0 is is the trivial mapping x --> x,
#    * maximal up-weigthing is approached as p --> +1, and
#    * maximal dn-weigthing is approached as p --> -1.

# A Moore scaling factor "S" is sometimes chosen by examiners.
#
# When chosen, the interpretation of "S" is that it is the factor by which
# the mean of the raw mark distribution should be multipled to reach the 
# mean of the scaled mark distribution. I.e.:
#
#             <scaled> = <unscaled> * S            (*)
# 
# or equivalently, since S is a constant (per distribution):
#
#             <scaled> = <unscaled * S>.
#
# This means that the simplest implementation of a scaling that could satisfy (*) above would
# be a simply multiplication of every mark in the distribution by the factor "S". This could be
# called "LINEAR scaling".  However, if S>>1, then linear scaling can lead individuals who already
# scored a raw mark close to 100% receving a scaled score of more than 100%! Many examiners object
# to such scaling artefacts, so as an alternative to LINEAR scaling one my one of the non-linear
# scaling functions provided by this library.
#
# Using one or more of these scaling functions, f, the individual raw marks would be scaled as follows:
#
#        scaled_mark = max_mark * f(raw_mark/max_mark, p)
#
# where max_mark is the largest mark possible (usually 100), and "p" is a strength which is 
# chosen to achieve the desired property (*). Note that the non-linear nature of LESTER scaling 
# means that the value of p needed to achieve (*) cannot usually be found without iteration. 
# However, it is a simple matter to play a shooting-game to establish the correct value of p 
# to achieve (*) as the family of functions is monotonic in p (and x).
#
# FWIW the hyperbolic scaling function is defined/derived as follows. It is the UNIQUELY determined 
# family of conics (in (x,f_p(x)) space [I suspect most if not all are hyperbolae] which have 
# the properties that: 
#
#     (a) they pass through the top right and bottom left corners of the unit square, 
#     (b) they are symmetric about the line from top-left to bottom right of that square,
#   , (c) (at fixed "p") each curves's midpoint mid(t) satisfieis 
#                           mid(t) = (1/2 - t/2, 1/2 + t/2)
#           ... i.e.  the last-mentioned diagonal is traversed at uniform speed if "p" 
#           is varied at constant speed, and 
#     (d) they are assymptotic to the boundaries of the unit square at extreme p = +- 1.

def hyperbolic(x, p):
    validate(p)
    from numpy import sign, sqrt
    # Avoid numerical instability very close to y=x:
    # print("DEBUG lesterScaling x= ",x," p= ",p)
    if (abs(p)<0.0001):  # Was <0.000001 (five zeros after decimal point) when first camsis upload done. Prefer 0.0001 (three zeros after decimal point) now.
        ans = x
    else:
        s = sign(p)
        a = (1.0-abs(p))**2
        b = a*(1.0-x) + 2.0*x + s - 1.0
        c = x*( a*(x-2.0) + 2.0*s + 2.0)
        ans = (b - s*sqrt(b**2 - a*c))/a
    #print("DEBUG lesterScaling                                        ans= ",ans)
    return ans

def skewTopHinged(x, p):
    validate(p)
    return x ** ((1.0 - p)/(1.0 + p))

def skewBottomHinged(x, p):
    return 1.0 - skewTopHinged(1.0 - x, -p)

def skewSymmetric(x, p):
    return 0.5*(skewTopHinged(x,p) + skewBottomHinged(x,p))

scaling_functions =  [ \
        hyperbolic, \
        skewSymmetric, \
        skewTopHinged, \
        skewBottomHinged, \
        ]

def validate(p):
    if p>=1 or p<=-1:
        raise ValueError("The strength parameter for a mark rescaling must be in (-1,1). I.e. it must must be less than 1.0 and greater than -1.0. You chose "+str(p))

def plot_scaling_function_curves(functions=scaling_functions, p_values=None, figsize=(10,10), pdfPathPrefix="", pngPathPrefix=""):
    import matplotlib.pyplot as plt
    import numpy as np
    
    if p_values == None:
        # create a  symmetric range of p_values which fit in (-1,1) and which are delta apart.
        delta = 0.0999
        p_values = [ -delta*n for n in range(    -int(np.floor(1.0/delta)),  +int(np.floor(1.0/delta))+1 ) ]
        
        
    for scaling_function in functions:
        
        function_name = str(scaling_function.__name__)

        x = np.linspace(0, 1, 100)
    
        #create line plot with multiple lines
        plt.rcParams["figure.figsize"] = figsize
        plt.gca().set_aspect('equal')
        plt.gca().set(xlabel="x     (raw mark fraction)")
        plt.gca().set(ylabel="f(x,p)     (scaled mark fraction)")
    
        for p in p_values:
          rounded_p = round(p,2)
          # Round p for reasons of space, but don't mislead readers into thinking that p is allowed to be 1 or -1:
          p_for_label = rounded_p if (abs(rounded_p) != 1.0) else p
          plt.plot(x, scaling_function(x,p), linewidth=2, label="p="+str(p_for_label))
       
        #add legend
        plt.legend()
        
        plt.title("Curves from the " + function_name + " scaling function")
       
        if pdfPathPrefix != "":
            plt.savefig(pdfPathPrefix + function_name + ".pdf", \
                metadata={'CreationDate': None} ) # prevent the PDF changing for trivial reasons.

        if pngPathPrefix != "":
            plt.savefig(pngPathPrefix + function_name + ".png", \
                metadata={'CreationDate': None} ) # prevent the PNG changing for trivial reasons.
    
        #display plot
        plt.show()

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement
    plot_scaling_function_curves()
