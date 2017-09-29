depth_cutoffs = [3; 4; 5; 6; 3; 4; 5; 6; 3; 4; 5; 6];
num_states_explored = [3307; 21356; 182980; 890192; 3522; 33443; 258959; 1712910; 3237; 29779; 263862; 1734246];
f = fit(depth_cutoffs,num_states_explored,'exp1');
f
h=plot(f,'b',depth_cutoffs,num_states_explored,'b.')
set(h,'MarkerSize',15);

% Annotations
xlabel('Depth cutoff');
ylabel('Number of states explored');

legend('show');
legend('Data points','Fitted curve','location','southwest');
lgd = legend;
lgd.Location = 'southwest';

grid on;