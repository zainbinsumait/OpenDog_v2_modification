clear all
syms L D  q1 q2  real

%ce code est pour avoir la DHHtransformation de 0 a e numeriquement et 
%donc avoir les coordonnes du point ainsi sa rotation pour calculer ensuite
%les angles de q1,q2,...q6 qui nous permettent d'atteindre ce point avec la
%meme rotation de repere pour le retule

% q1 =0.8727;
% q2 = -1.4027;

L = 200;
D = 215;




T01=DHHomogeneousTransformation(0,0,0,q1)
T12=DHHomogeneousTransformation(L,0,0,q2)
T23=DHHomogeneousTransformation(D,0,0,0)

T03 = simplify(T01*T12*T23)
%T03 = T01*T12*T23
% T06=simplify(T01*T12*T23*T34*T45*T56); car que du numerique
% T0e=T01*T12*T23*T34*T45*T56*T6e;
% T06=T01*T12*T23*T34*T45*T56;
% eProt = [0;0;-e;1]
% 
% bProt = T0e * eProt
% 
% q1c1 = atan2(bProt(2),bProt(1))
% 
% q1c2 = q1c1+pi
% 
% vpa(bProt,18)




