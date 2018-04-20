load minute_save.txt

wndw =  100
figure('visible','off')
minute=1000-minute_save;
plot(minute(1:end),'r')
hold on
avg=filter(ones(wndw,1)/wndw, 1, 1000-minute_save);
plot(avg(wndw/2:end))

print -djpg moisture_minute.jpg
