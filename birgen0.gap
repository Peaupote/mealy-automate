GRAPE_DREADNAUT_EXE:="/home/peaupote/Documents/works/cours/projet/nauty26r11/dreadnaut";; # dreadnautB# dreadnautY
#GRAPE_BLISS_EXE:="/Applications/gap-4.10.1/pkg/grape-4.8.1/bin/x86_64-apple-darwin16.5.0-default64-kv3/bliss";;

#nx stands for number of letters
nx:=2;
#ns stands for number of states
ns:=2;
n:=0;#:=nx*ns;       # hgraph
nn:=0;#:=n+nx+ns;    # hhgraph (with colour-classes)
cc:=[]; #:=[[1..n],[n+1..n+nx],[n+nx+1..n+nx+ns]];
ccp:="";#
str:="";
disp:=1000000;
#m is the n^2 matrix;
m:=[];
ix:=[];#:=IdentityMat(nx);
is:=[];#:=IdentityMat(ns);
adjacencies:=[];
#all is the whole list
#all:=[];
#nb is the cardinal (all/iso)
nb:=0;
nbi:=0;
name:="file.gap";

tt:=0;
tt1:=0;#timer;
tt2:=0;#timer;
tt3:=0;#timer;


###############################################################
# backtracking ################################################
###############################################################

bgw := function(i,j)
#w stands for "writing"
local ix,is,jx,js,h,k,r,ch;
ch:=[];
m[i][j]:=1; Add(ch,[i,j]);
#Mea
for k in [1..n]
do  if m[i][k]=-1
then m[i][k]:=0;
Add(ch,[i,k]);
fi;od;
#Cor
for h in [1..n]
do  if m[h][j]=-1
then m[h][j]:=0;
Add(ch,[h,j]);
fi;od;
ix:=RemInt(i-1,nx)+1;   #letter wrt i
is:=QuoInt(i-1,nx)+1;   #state  wrt i
jx:=RemInt(j-1,nx)+1;   #letter wrt j
js:=QuoInt(j-1,nx)+1;   #state  wrt j
#Inv
for h in [(is-1)*nx+1..is*nx]
do  for k in [1..ns]
do  r:=(k-1)*nx+jx;
if m[h][r]=-1
then m[h][r]:=0;
Add(ch,[h,r]);
fi;od;od;
#Rev
for h in [1..ns]
do  for k in [(js-1)*nx+1..js*nx]
do  r:=(h-1)*nx+ix;
if m[r][k]=-1
then m[r][k]:=0;
Add(ch,[r,k]);
fi;od;od;
return ch;
end;

bge := function(ch)
#e stands for "erasing"
local d;
#Print("here c=",c);
for d in ch
do  m[d[1]][d[2]]:=-1;
od;
#c:=[];
end;


###############################################################
# nauty #######################################################
###############################################################

NautyString := function()
local s,adj,i,j,p;
#renvoie le codage nauty du HH-graphe courant
#As+\n : seems to give only rigid ones
#(so does bliss)
s:="";
Append(s,str);
adjacencies := List([ 1..nn ],x->Positions(m[x],1));
for i in [1..nn]
do  adj:=adjacencies[i];
if adj=[]
then    if i<nn
then Append(s,", ;");#################
else Append(s,", . ");
fi;
else    for j in [1..Length(adj)]
do  if j<Length(adj)
then Append(s,String(adj[j]));Append(s,", ");
elif i<nn
then Append(s,String(adj[j]));Append(s,"; ");
else Append(s,String(adj[j]));Append(s,". ");
fi;
od;
fi;
od;
Append(s,ccp);

return s;
end;

path:=DirectoryCurrent();
stringIN:="";
stringOUT:="";
streamIN:=InputTextString(stringIN);
streamOUT:=OutputTextString(stringOUT,false);

CanonicalLabellingNauty := function()
local ttt;
ttt:=Runtime();
stringIN:=NautyString();
Append(stringIN," p c *=13 k=0 99 x b q");
#Print(stringIN);
tt:=tt+Runtime()-ttt;
streamIN:=InputTextString(stringIN); #As
#
#d:     : digraph
#$1     : origin for vertex numbering
#n??    : number of vertices
#g      : read the graph
#
#p      : cartesian
#*=13   : adjacencies as vertex-invariant
#k=1 10 : mininvarlevel and maxinvarlevel
#c      : canonical labelling
#x      : run nauty
#b      : type the canonical label
#q      : quit
#
stringOUT:="";
streamOUT:=OutputTextString(stringOUT,false);

#
Process(path, GRAPE_DREADNAUT_EXE, streamIN, streamOUT, [] );
#
stringOUT:=stringOUT{[PositionSublist(stringOUT,".\n")+3..Length(stringOUT)]};
stringOUT:=stringOUT{[1..PositionSublist(stringOUT,"\n")]};
stringOUT:=Concatenation("[",ReplacedString(stringOUT," ",","),"]");
Print(stringOUT);
Print("\n");

return PermList(EvalString(stringOUT)); #canonicalLabelling:=
end;
###############################################################
# canonical testing ###########################################
###############################################################

hcan := function() # from n^2 01-matrix #with colour-classes
#builds the grape of HH_{1,1}-graph (unoriented & no loops) with colour-classes
#uses it to check whether the 01-matrix m defines a helix-canonical Mealy machine
local p,px,ps,pm,b,ttt;

ttt:=Runtime();
p:=CanonicalLabellingNauty();
tt1:=tt1+Runtime()-ttt;

ttt:=Runtime();
p:=List([n+1..nn],x->x^p)-n;# permuting alphabet,stateset
px:=PermList(p{[1..nx]});                                                           # perm on one block [1..nx]
px:=PermList(Concatenation(List([1..ns],k->ListPerm(px,nx)+(k-1)*nx)));             # -> perm on row/columns
ps:=PermList(p{[nx+1..nx+ns]}-nx);                                                  # perm between ns blocks
ps:=PermList(Concatenation(List(ListPerm(ps,ns),b->List([1..nx],k->(b-1)*nx+k))));  # -> perm on row/columns
pm:=PermutationMat(px*ps,nn);
tt2:=tt2+Runtime()-ttt;

ttt:=Runtime();
b:=pm*m=m*pm;
tt3:=tt3+Runtime()-ttt;

return b;
end;

###############################################################
# various versions for padding ################################
###############################################################

bgp_gener_all_file := function(i)
#p stands for "padding"
#i denotes the index of the current row
local j,ch;
if i>n
then    nb:=nb+1;
        if RemInt(nb,disp)=0 then Print("# ",nb,"...\n");fi;
        AppendTo(name,List([ 1..n ],x->Position(m[x]{[ 1..n ]},1)),",\n");
else    for j in [1..n]
        do  if m[i][j]=-1
            then    ch:=bgw(i,j);
                    bgp_gener_all_file(i+1);
                    bge(ch);
                    fi;
            od;
        fi;
end;

bgp_gener_iso_file := function(i)
#p stands for "padding"
#i denotes the index of the current row
local j,ch;
if i>n
then    nb:=nb+1;
        if RemInt(nb,disp)=0 then Print("# ",nb,"...\n");fi;
        if hcan() then AppendTo(name,List([ 1..n ],x->Position(m[x]{[ 1..n ]},1)),",\n");fi;
#       if hcan() then AppendTo(name,m,",\n");fi;
else    for j in [1..n]
        do  if m[i][j]=-1
            then    ch:=bgw(i,j);
                    bgp_gener_iso_file(i+1);
                    bge(ch);
                    fi;
            od;
        fi;
end;

bgp_count_all := function(i)
#p stands for "padding"
#i denotes the index of the current row
local j,ch;
if i>n
then    nb:=nb+1;
        if RemInt(nb,disp)=0 then Print("# ",nb,"...\n");fi;
else    for j in [1..n]
        do  if m[i][j]=-1
            then    ch:=bgw(i,j);
                    bgp_count_all(i+1);
                    bge(ch);
                    fi;
            od;
        fi;
end;

bgp_count_iso := function(i)
#p stands for "padding"
#i denotes the index of the current row
local j,ch;
if i>n
then    nb:=nb+1;
        if RemInt(nb,disp)=0 then Print("# ",nb,"...\n");fi;
        if hcan() then nbi:=nbi+1;fi;
else    for j in [1..n]
        do  if m[i][j]=-1
            then    ch:=bgw(i,j);
                    bgp_count_iso(i+1);
                    bge(ch);
                    fi;
            od;
        fi;
end;

###############################################################
# master ######################################################
###############################################################

gbir := function(arg)
# g stands for "generation"
# kx,  ks,  count/gener,  all/iso,    file?
#           true/false,   true/false, ["name"]
local kx,ks,x,s,i,j,count,all,file;
kx:=arg[1];
ks:=arg[2];
if Length(arg)>2 then count:=arg[3]; else count:=true;fi;
if Length(arg)>3 then   all:=arg[4]; else   all:=true;fi;
file:=Length(arg)>4;
if file then name:=arg[5];fi;
nx:=kx;
ns:=ks;
n:=nx*ns;       # hgraph
nn:=n+nx+ns;    # hhgraph (with colour-classes)
nb:=0;
nbi:=0;
#
cc:=[[1..n],[n+1..n+nx],[n+nx+1..n+nx+ns]];
ccp:=ReplacedString(ReplacedString(String(cc) ,"], [","|"),"..",":");
ccp:=Concatenation("f",ccp{[2..Length(ccp)-1]});
str:=Concatenation("d $1 n",String(nn),"g ");

ix:=IdentityMat(nx);
is:=IdentityMat(ns);
m:=[];
for s in [1..ns]        #state
do	for x in [1..nx]    #letter
do  Add(m,Concatenation([1..n]*0,ix[x],is[s]));
od;od;
for s in [1..nx+ns] do Add(m,[1..nn]*0); od; #the nx+ns last rows
#backtrack initialisation
for i in [1..n]
do  for j in [1..n]
do  m[i][j]:=-1;od;od;
#Print("initial HHgraph:\n");
#PrintArray(m);

if count #file is then ignored
then    if all
        then    bgp_count_all(1); return nb;
        else    bgp_count_iso(1); return nbi;
                fi;
else    if all
        then    bgp_gener_all_file(1);
        else    bgp_gener_iso_file(1);
                fi;
        fi;
end;


#bgm := function()
##m stands for "mealym"
#local t,o,i,j,h,k;
#t:=NullMat(ns,nx);
#o:=NullMat(ns,nx);
#for i in [1..n]
#do  for j in [1..n]
#    do  if m[i][j]=1
#        then h:=QuoInt(i-1,nx)+1;
#             k:=RemInt(i-1,nx)+1;
#             t[h][k]:=QuoInt(j-1,nx)+1;
#             o[h][k]:=RemInt(j-1,nx)+1;
#             fi;
#        od;od;
#return MealyMachine(t,o);
#end;


#bgr := function()
##r stands for "random"
#local r,c;
#for r in [1..n]
#do  repeat c:=Random([1..n]);
#    #Print("##crand:",c,"\n");
#    until(m[r][c]=-1);
#    bgw(r,c);
#    od;
#return m;
#end;
