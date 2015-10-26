clear
clc

% ===========CONSTANTS===========
TRAIN_DATA_FILE = '../processed_data/features.csv';

% =========READ DATA============
trainData = csvread(TRAIN_DATA_FILE);
trainLabels = zeros(1999,1);
for i = 1:1000
    trainLabels(i) = trainLabels(i) + 1;
end

% ====== TRAIN & TEST SVM MODEL ========
models = cell(6,1);
cVector = [0.1, 0.5, 1, 2.5, 5, 10];

for i = 1:6
    svmOptions = ['-s 0 -t 0 -c ', num2str(cVector(i))];
%     sprintf('-c %f -g %f -v %d -t %d', 2^C(i), 2^gamma(i), folds,d)
    models{i} = svmtrain(trainData, trainLabels, svmOptions);
end

