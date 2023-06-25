
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
# to such scaling artefacts, so as an alternative to LINEAR scaling one my use LESTER scaling.
# LESTER scaling uses the non-linear one-parameter family of curves f_p(x) shown by running the
# demo() function defined in this file.
# 
# The parameter p in (0,1) controlling the strength of the Lester scaling satisfies:
#
#        (p=-1) ==> "max DOWN scaling",  i.e. f_{-1}(x) = 0
#        (p= 0) ==> "no scaling",        i.e. f_{ 0}(x) = x
#        (p=+1) ==> "max UP   scaling",  i.e. f_{+1}(x) = 1
#
# Using these factors, the individual raw marks would be scaled as follows:
#
#        scaled_mark = max_mark * f_{p}(raw_mark/max_mark)
#
# where max_mark is the largest mark possilbe (usually 100), and "p" is a strength which is 
# chosen to achieve the desired property (*). Note that the non-linear nature of LESTER scaling 
# means that the value of p needed to achieve (*) cannot usually be found without iteration. 
# However, it is a simple matter to play a shooting-game to establish the correct value of p 
# to achieve (*) as the family of functions is monotonic in p (and x).
#
# FWIW the hyperbolic is defined/derived as follows. It is the UNIQUELY determined 
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
