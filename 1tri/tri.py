import collections,sys, string

# use with python 3

X=0
Y=1
tPointi=collections.namedtuple('tPointi', ['X', 'Y'])
vertices=[]

#definitions:
#vertex: v.  v structure: tVertexStructure.  index: vnum. 

class tVertexStructure:
    def __init__(self, vnum, v, ear):
        self.vnum=vnum
        self.v=v
        self.ear=ear

def Add(v):
    global vertices
    vertices.append(v)

def Area2(a,b,c): #a,b,c are v's
    return (b[0] - a[0]) * (c[1] - a[1]) -(c[0] - a[0]) * (b[1] - a[1]);

def AreaPoly2():
    sum = 0
    p=vertices[0]
    for i in range(1,len(vertices)-1):
        a=vertices[i]
        b=vertices[i+1]
        sum+=Area2(p.v,a.v,b.v)
    
    return sum

def AreaSign(  a,  b,  c ):    
    area2=Area2(a,b,c)
    
    # The area should be an integer. */
    if      ( area2 >  0.5 ): return  1;
    elif ( area2 < -0.5 ): return -1;
    else:                     return  0;  #when -0.5<=area2<=0.5.   How it comes???

def Diagonal( a, b ): #whether a,b is a diagonal, where a,b are vStructure's
    return InCone( a, b ) and InCone( b, a ) and Diagonalie( a, b )

def Diagonalie(  a,  b ): 
    #make sure ab is not involved with an intersection with any other non-adjacent edges of the poly.
    #,where a,b are vStructure's
    for i in range(len(vertices)):
        c=vertices[i]
        c1=vertices[mod(i+1)]
        if c.vnum!=a.vnum and c1.vnum!=a.vnum and c.vnum!=b.vnum and c1.vnum!=b.vnum and \
        Intersect( a.v, b.v, c.v, c1.v ):
            return False;
    return True


def EarInit( ):
    # Initialize v1->ear for all vertices. 
    print("newpath\n");
    for i in range(len(vertices)):
        v0=vertices[i]
        v1=vertices[mod(i+1)]
        v2=vertices[mod(i+2)]
        v1.ear = Diagonal( v0, v2 );
    
    print("closepath stroke\n\n")

def Intersect( a,  b,  c, d ):
    if IntersectProp( a, b, c, d ): #whether it is proper intersection
        return  True;
    elif Between( a, b, c ) or Between( a, b, d ) or Between( c, d, a ) or Between( c, d, b ):
        return True;
    else:
        return False;

def IntersectProp(a,b,c,d):
    if Collinear(a,b,c) or  Collinear(a,b,d) or Collinear(c,d,a) or Collinear(c,d,b):
        #any three v's are collinear
        return False
    return Xor( Left(a,b,c), Left(a,b,d) ) and Xor( Left(c,d,a), Left(c,d,b) )

def InCone( a, b ): # a,b are vStructure's
    # a0,a,a1 are consecutive vertices. */
    a1=vertices[mod(a.vnum+1)]
    a0=vertices[mod(a.vnum-1)]

    # If a is a convex vertex ... */
    if LeftOn( a.v, a1.v, a0.v ):  # on is ok for convex.
        return Left( a.v, b.v, a0.v ) and Left( b.v, a.v, a1.v )

    # Else a is reflex: */
    return not (LeftOn( a.v, b.v, a1.v ) and LeftOn( b.v, a.v, a0.v ) ) #eliminating the exception case.

def Left( a, b, c ):   #left, lefon, collinear, between is vague!!!
    #whether c is left of ab
    return  AreaSign( a, b, c ) > 0;

def LeftOn( a, b, c ):
   return  AreaSign( a, b, c ) >= 0;

def Collinear( a, b, c ):
   return  AreaSign( a, b, c ) == 0;

def Between( a, b, c ):
    if not Collinear( a, b, c ):
        return False;
   
    if a[0] != b[0]:
        return ((a[0] <= c[0]) and (c[0] <= b[0])) or ((a[0] >= c[0]) and (c[0] >= b[0]));
    else:
        return ((a[1] <= c[1]) and (c[1] <= b[1])) or ((a[1] >= c[1]) and (c[1] >= b[1]));


def mod(x):
    length=len(vertices)
    y=x
    while True:
        if y>=0 and y<=length-1:
            break;
        elif y<0:
            y+=length
        else: #x>length-1    
            y-=length
    return y        

def next(v):
    num=v.vnum
    return vertices[mod(num+1)]

def prev(v):
    num=v.vnum
    return vertices[mod(num-1)]

def PrintVertices( ):
    # Compute bounding box for Encapsulated PostScript. */
    xmin = xmax = 0;
    ymin = ymax = 0;
    for v in vertices:
        if v.v[0] > xmax:
            xmax = v.v[0];
        elif v.v[0] < xmin:
            xmin = v.v[0];
        if v.v[1] > ymax:
            ymax = v.v[1];
        elif v.v[1] < ymin:
            ymin = v.v[1];
   
    # PostScript header
    print("%!PS\n");
    print("%%Creator: tri.c (Joseph O'Rourke)\n");
    print("%%BoundingBox: {0} {1} {2} {3}\n".format(xmin, ymin, xmax, ymax) );
    print("%%EndComments\n");
    print(".00 .00 setlinewidth\n");
    print("{0} {1} translate\n".format(-xmin+72, -ymin+72) );
    # The +72 shifts the figure one inch from the lower left corner */

    # Output vertex info as a PostScript comment. */
    print("\n% number of vertices = {0}\n".format(len(vertices)) );
    for v in vertices:
        print( "% vnum={0}:\tx={1}\ty={2}\n".format(v.vnum, v.v[0], v.v[1]) );

    # Draw the polygon. */
    print("\n%Polygon:\n");
    print("newpath\n");
    v = vertices[0];
    print("{0}\t{1}\tmoveto\n".format(v.v[0], v.v[1] ) );
    for i in range(1, len(vertices)):
        v=vertices[i];
        print("{0}\t{1}\tlineto\n".format(v.v[0], v.v[1]) );

    print("closepath stroke\n");    


def ReadVertex():
    line = sys.stdin.readline() #lines is a list of line.
    x, y = line.split(',')
    x, y = int(x), int(y)
    
    print('x={0}, y={1}'.format(x,y))

def PrintDiagonal( a, b ):  #a,b are vStructures
    print("%%Diagonal: ({0},{1})\n".format(a.vnum, b.vnum ) );  #To print a percent sign, use %%
    print("{0}\t{1}\tmoveto\n".format(a.v[0], a.v[1] ));
    print("{0}\t{1}\tlineto\n".format(b.v[0], b.v[1] ));




def ReadVertices():
    vnum = 0;
    print('Please enter the coordinates (x,y) of at least 3 vertices, in counterclockwise order,')
    print('one line per vertex, and end the inputs by ctrl+z:')
    while True:
        lines = sys.stdin.readlines()
        for line in lines:
            x,y=line.split(',')
            vnum+=1
            v=tVertexStructure(vnum, [x,y], False)  
        while vnum>=3:
            break;
        print('Coordinates of more vertices are needed.') 
        
    global nvertices    
    nvertices = vnum;
    #if nvertices < 3:
    #    print("Error in ReadVertices: nvertices={0}<3\n".format('nvertices') )
    #    sys.exit()

def ReadVertices2():
    v0=[1,1]
    v1=[0,2]
    v2=[-1,1]
    v3=[-1,-1]
    v4=[0,-2]
    v5=[1,-1]
    #global vertices
    vnum=0    
    v=tVertexStructure(vnum, v0, False)      
    vnum+=1
    Add(v)
        
    v=tVertexStructure(vnum, v1, False)  
    vnum+=1
    Add(v)    
    
    v=tVertexStructure(vnum, v2, False)  
    vnum+=1
    Add(v)    
    
    v=tVertexStructure(vnum, v3, False)  
    vnum+=1
    Add(v)
        
    v=tVertexStructure(vnum, v4, False)  
    vnum+=1
    Add(v)
        
    v=tVertexStructure(vnum, v5, False)  
    vnum+=1
    Add(v)
    

def Triangulate( ):
    # v0, v1, v2, v3, v4;     five consecutive vertices 
    n = len(vertices);        # number of vertices; shrinks to 3. 
    earfound=False       # for debugging and error detection only. */

    EarInit();
    print("\nnewpath\n");
    global vertices
    # Each step of outer loop removes one ear. */
    while n > 3:  
        # Inner loop searches for an ear. 
        for v2 in vertices:
            if v2.ear:
                earfound = True;
                # Ear found. Fill variables. */
                v3 =next(v2)
                v4 = next(v3);
                v1 = prev(v2);
                v0 = prev(v1);
    
                # (v1,v3) is a diagonal */
                PrintDiagonal( v1, v3 );
                
                # Update earity of diagonal endpoints */
                v1.ear = Diagonal( v0, v3 );
                v3.ear = Diagonal( v1, v4 );
                
                # Cut off the ear v2 */                
                vertices.remove(v2)
                n-=1;                
      
        if not earfound:
            print("%%Error in Triangulate:  No ear found.\n");
            PrintPoly();
            print("showpage\n%%%%EOF\n");
            sys.exit()
 
    print("closepath stroke\n\n");
    
def test():
    pass

def Xor(x,y): #True iff one of the arguments is True.
    return x^y

def main():
    #test();
    
    #ReadVertex()
    #ReadVertices();
    ReadVertices2();
    PrintVertices()
    print("%Area of polygon = {0}\n".format(0.5 * AreaPoly2() ) );
    
    Triangulate();
    print("showpage\n%%EOF\n");

if __name__=='__main__':  #__init__ is for a class.
    main()

