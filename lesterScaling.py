from numpy import sign, sqrt

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
# FWIW the lester_scale_function is defined/derived as follows. It is the UNIQUELY determined 
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

def f(x, p):
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

def lester_scale_function(x,p):
    return f(x,p)


def demo_specific_curves(curves, figsize=(10,10), filename=""):
    import matplotlib.pyplot as plt
    import numpy as np
    
    x = np.linspace(0, 1, 100)

    #create line plot with multiple lines
    plt.rcParams["figure.figsize"] = figsize
    plt.gca().set_aspect('equal')
    plt.gca().set(xlabel="x     (raw mark fraction)")
    plt.gca().set(ylabel="f(x,p)     (scaled mark fraction)")

    for p,lab in curves:
      plt.plot(x, lester_scale_function(x,p), linewidth=2, label=lab)
    
    #add legend
    plt.legend()
   
    if filename != "":
        plt.savefig(filename, \
            metadata={'CreationDate': None} ) # prevent the PDF changing for trivial reasons.

    #display plot
    plt.show()

def demo(filename=""):
    import numpy as np
    
    curves = [ (p, "p="+str(round(p,1)) ) for p in np.arange(+0.9999999,-0.9999999,-0.0999) ]
    demo_specific_curves(curves, filename=filename)

if __name__ == '__main__':
    # Execute when the module is not initialized from an import statement
    demo()
