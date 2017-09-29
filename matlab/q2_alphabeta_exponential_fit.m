depth_cutoffs = [3; 4; 5; 6; 3; 4; 5; 6; 3; 4; 5; 6];
num_states_explored = [429; 845; 4317; 8665; 302; 756; 3335; 10728; 342; 829; 4055; 10222];
f = fit(depth_cutoffs,num_states_explored,'exp1');
f
h=plot(f,'r',depth_cutoffs,num_states_explored,'r.')
set(h,'MarkerSize',15);

% Annotations
xlabel('Depth cutoff');
ylabel('Number of states explored');
%axis([min(freqrange), max(freqrange), min(dbgain)-downoff,max(dbgain)+upoff])
%set(gca,'xscale','log');
%set(gca,'yscale','log');

legend('show');
legend('Data points','Fitted curve','location','southwest');
lgd = legend;
lgd.Location = 'southwest';

grid on;