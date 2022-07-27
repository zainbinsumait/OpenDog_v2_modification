clear all 
syms S L D alpha beta Nh nh NL nl

L = 200 ;
D = 215; 
S = 360;
N = 70; %number of tooth in the big gear of the upper and the lower leg
nu = 24;

nl = 32;

f1 = N/nu; %upper leg speed = 24/70*mtor_speed or motor_speed = 70/24*upper_speed
f2 = N/nl;


x2 = ones(1,45);
for n = 20:50
    x2(n) = n;
end
alpha = x2*pi/180;
alpha_deg = alpha*180/pi

rot_h = alpha*180/pi * f1 *1/360 % rotation of upper leg
beta = acos((S-L*cos(alpha))/D)-alpha
beta_deg = beta * 180/pi

rot_l = (beta)* 180/pi * f2 *1/360
x = D*cos((alpha + beta))+ L*cos(alpha)
y = D*sin((alpha + beta)) +L*sin(alpha)

%to avoid the complexe numbers and take the real solutions
m = 1;
for k = 1:length(x)
    if isreal(y(k))
        Yr(m) = y(k); % Yr is the list of the distance reel in Y
        Alpha_y(m) = alpha(k); % the angle for this real distance
        Beta_r(m) = beta(k);
        m = m+1;
    end

end



