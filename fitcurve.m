x = [200, 500, 800, 1000, 1500, 2000, 3000, 5000, 100000];
y = [3, 2.2, 1.9, 1.8, 1.5, 1.3, 1.2, 0.9, 0.7];

p = polyfit(x,y,1);

x1 = [200, 500, 800, 1000, 1500, 2000, 3000, 5000, 100000];
y1 = polyval(p,x1);
figure
plot(x,y,'o')
hold on
plot(x1,y1)
hold off

