clear
clc

% ===========CONSTANTS===========
TYPE = 'type1';
PROCESSED_DATAPATH = strcat('../types/',TYPE,'/processed_data/');

TRAIN_DATA_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_features.csv');

TRAIN_POSITIVE_DATA_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_positive_starred_features.csv');
TRAIN_NEGATIVE_DATA_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_negative_starred_features.csv');

TRAIN_POSITIVE_LABELS_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_positive_starred.review_labels');
TRAIN_NEGATIVE_LABELS_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_negative_starred.review_labels');

TEST_DATA_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_unlabelled_features.csv');

TEST_POSITIVE_DATA_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_unlabelled_positive_starred_features.csv');
TEST_NEGATIVE_DATA_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_unlabelled_negative_starred_features.csv');

TEST_LABEL_FILE = strcat(PROCESSED_DATAPATH,TYPE,'_unlabeled.review_rating');

% TEST_POSITIVE_LABELS_FILE=
% TEST_NEGATIVE_LABELS_FILE=


% =========READ DATA============
trainData = csvread(TRAIN_DATA_FILE);
trainRow = size(trainData,1);
trainCol = size(trainData,2);
display(size(trainData));

trainLabels = zeros(trainRow,1);
for i = 1:4639
    trainLabels(i) = trainLabels(i) + 1;
end

trainPositiveData = csvread(TRAIN_POSITIVE_DATA_FILE);
trainNegativeData = csvread(TRAIN_NEGATIVE_DATA_FILE);

trainPositiveLabels = csvread(TRAIN_POSITIVE_LABELS_FILE);
trainNegativeLabels = csvread(TRAIN_NEGATIVE_LABELS_FILE);

testData = csvread(TEST_DATA_FILE);
testRow = size(testData,1);
testCol = size(testData,2);

testPositiveData = csvread(TEST_POSITIVE_DATA_FILE);
testNegativeData = csvread(TEST_NEGATIVE_DATA_FILE);

testLabels = dlmread(TEST_LABEL_FILE,'\n');
testLabels = testLabels';
testPositiveLabels = testLabels;
testNegativeLabels = testLabels;

lvl1TestLabels = zeros(testRow,1);
for i = 1:testRow
    if (testLabels(i) > 3)
        lvl1TestLabels(i) = 1;
    else
        lvl1TestLabels(i) = 0;
    end
end

% ====== TRAIN & TEST SVM MODEL ========
% bestcv = 0;
% for log2c = -1:4,
%     cmd = ['-v 5 -t 0 -c ', num2str(2^log2c)];
%     cv = svmtrain(trainLabels, trainData, cmd);
%     if (cv >= bestcv),
%       bestcv = cv; 
%       bestc = 2^log2c;
%     end
%     fprintf('%g %g (best c=%g, rate=%g)\n', log2c, cv, bestc, bestcv);
% end
% 
% bestcv = 0;
% for log2c = -1:3,
%   for log2g = -4:1,
%     cmd = ['-v 5 -c ', num2str(2^log2c), ' -g ', num2str(2^log2g)];
%     cv = svmtrain(trainLabels, trainData, cmd);
%     if (cv >= bestcv),
%       bestcv = cv;
%       bestc = 2^log2c;
%       bestg = 2^log2g;
%     end
%     fprintf('%g %g %g (best c=%g, g=%g, rate=%g)\n', log2c, log2g, cv, bestc, bestg, bestcv);
%   end
% end

% cmd = ['-v 5 -c ', 2, ' -g ', 0.0625];
% 

% cmd = '-s 0 -t 0 -c 0.5 -v 5';
cmd = '-s 0 -t 0 -c 0.5';
lvl1Model = svmtrain(trainLabels, trainData, cmd);
 
lvl2PositiveModel = svmtrain(trainPositiveLabels, trainPositiveData, cmd);
lvl2NegativeModel = svmtrain(trainNegativeLabels, trainNegativeData, cmd);

lvl1Labels = zeros(testRow,1);
lvl2Labels = zeros(testRow,1);
% 
for i = 1:testRow
    [predLabel, predAccuracy, d1] = svmpredict(lvl1TestLabels(i), testData(i,:), lvl1Model);
    lvl1Labels(i) = predLabel;
    if predLabel == 1
        [predLabel2, predAccuracy2, d2] = svmpredict(testLabels(i), testPositiveData(i,:), lvl2PositiveModel);
        if predLabel2 == 1
            lvl2Labels(i) = 5;
        else
            lvl2Labels(i) = 4;
        end
    else
        [predLabel2, predAccuracy2, d2] = svmpredict(testLabels(i), testNegativeData(i,:), lvl2NegativeModel);
        if predLabel2 == 1
            lvl2Labels(i) = 2;
        else
            lvl2Labels(i) = 1;
        end
    end
end

[predictLabels, accuracy, decValues] = svmpredict(lvl1TestLabels, testData, lvl1Model);
CMatLevel1 = confusionmat(lvl1TestLabels, lvl1Labels);
CMatLevel2 = confusionmat(testLabels, lvl2Labels);