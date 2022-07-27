function Tiip1=DHHomogeneousTransformation(aim1,alim1,di,thi)

Ttx=[1 0 0 aim1
    0 1 0  0
    0 0 1   0
    0 0 0 1];

Trx=[1 0             0         0
    0 cos(alim1) -sin(alim1)   0
    0 sin(alim1)  cos(alim1)   0
    0  0              0       1];

Ttz=[1 0 0 0
    0 1 0  0
    0 0 1  di
    0 0 0 1];
Trz=[cos(thi) -sin(thi) 0  0
    sin(thi) cos(thi)   0  0
    0          0        1  0
    0          0        0  1];


Tiip1=Ttx*Trx*Ttz*Trz;