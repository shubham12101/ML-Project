clear
clc

% ===========CONSTANTS===========
TRAIN_DATA_FILE = '../processed_data/features.csv';

% =========READ DATA============
trainData = csvread(TRAIN_DATA_FILE);
trainLabels = zeros(7914,1);
for i = 1:4000
    trainLabels(i) = trainLabels(i) + 1;
end

% ====== TRAIN & TEST SVM MODEL ========
% models = cell(6,1);
% cVector = [0.1, 0.5, 1, 2.5, 5, 10];
% 
% for i = 1:6
%     svmOptions = ['-v 5 -s 0 -t 0 -c ', num2str(cVector(i))];
%     models{i} = svmtrain(trainData, trainLabels, svmOptions);
% end

bestcv = 0;
for log2c = -1:3,
    cmd = ['-v 5 -c ', num2str(2^log2c)];
    cv = svmtrain(trainLabels, trainData, cmd);
    if (cv >= bestcv),
      bestcv = cv; 
      bestc = 2^log2c;
    end
    fprintf('%g %g (best c=%g, rate=%g)\n', log2c, cv, bestc, bestcv);
end

