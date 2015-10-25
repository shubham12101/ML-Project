clear
clc

% ===========CONSTANTS===========
% TRAIN_DATA_FILE = '../processed_data/';

% =========READ DATA============
% trainData = csvread(TRAIN_DATA_FILE);
trainLabel = zeros(1999,1);
for i = 1:1000
    trainLabel(i) = trainLabel(i) + 1;
end

% ====== TRAIN & TEST SVM MODEL ========
models = cell(6,1);

smvOptions = ['-s 0 -t 0 -c ', num2str(c)];

