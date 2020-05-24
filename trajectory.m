clear all; close all;  clc;
%% z-x axis calculations
xi = [0,0.5,1];       % x,z coordinates gathers from the trajectory (assuming this data will be captured by cameras)
zi = [1.3,1.2,1];

% Table size (m)
l = 2.44; % length
w = 0.61; % width
h = 0.7; % height off ground

syms a b c
eqn1 = zi(1) == (a*(xi(1)^2))+(b*xi(1))+c;
eqn2 = zi(2) == (a*(xi(2)^2))+(b*xi(2))+c;
eqn3 = zi(3) == (a*(xi(3)^2))+(b*xi(3))+c;

[A,B] = equationsToMatrix([eqn1, eqn2, eqn3],[a,b,c]);

X = linsolve(A,B); % solving for a,b,c coefficients of quadratic equations

ch = 0.10; % cup height, m (c-ch will work out the intercection with the top or cup rather than table)

a = X(1);
b = X(2);
c = X(3)-ch;

p = [a b c];
r = vpa(roots(p));
xint = r(r>=0); % intersection point along x axis, m
h1 = max(r)-min(r); % distance between the x axis intersections

c = X(3);

x = 0:0.01:3;
z = (a*(x.^2))+(b*x)+c;

d = 0.743; % damping factor

z2 = (d*a*((x-h1).^2))+(b*(x-h1))+c;

%% z-y axis calculations
yii = [0.35, 0.25]; % x,y coordinates gathers from the trajectory (assuming this data will be captured by cameras)
xii = [0 0.5];

syms m b
eqn1 = yii(1) == (m*xii(1))+b;
eqn2 = yii(2) == (m*xii(2))+b;

[A,B] = equationsToMatrix([eqn1, eqn2],[m,b]);

X = linsolve(A,B);

m = X(1);
b = X(2);

yint = (m*xint)+b;

coorint = [yint, xint]; % y,x coordinates of the point where the trajectory intersects the cup (where the cup needs to be positioned on the table)

%% Figures 
figure (1) % x-z view of trajectory
plot(x,z)
ylim([0 1.5])
xlim([0 3])
xlabel('x axis (m)')
ylabel('y axis (m)')
daspect([1 1 1])
grid on

figure (2) % x-y view of trajectory
y = (m*x)+b;
plot(y,x)
xlabel('y axis (m)')
ylabel('x axis (m)')
daspect([1 1 1])
xlim([-1 1])
ylim([0 3])
grid on

figure (3) % 3D view of trajectory
plot3(x,y,z,'--')
xlabel('x axis (m)')
ylabel('y axis (m)')
zlabel('z axis (m)')
xlim([0 3])
ylim([-1 1])
zlim([0 1.5])
set(gca, 'YDir', 'reverse')
grid on
hold on
plot(xint, yint, 'o')
daspect([1 1 1])
