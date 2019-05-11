## Encoding data
Given the `ML3AllSites` dataset, we can classify each column into 6 types: (positive) integers, unordered multiple choices, Boolean-like values, long texts, other valid responses and NA's.

(Note: the 1177th row is wrongly encoded in the original dataset, but we fixed it in the `ML3AllSitesC`. However, it again includes some more bugs in date related columns like column 124 Date.x because of Microsoft Excel. Anyway, we eventually fixed them when reading the dataset when calling `dataFormat.py`)

A detailed codebook is available in `/doc/codebook.pdf`, and further reference is in `/code/dataFormat.py`, which is organized in the order of original dataset.

### (Postive) Integers
Many columns belong to this type, for examples, best grade 1 (column 21), mcdv1 (column 71), temperature in lab (column 126) and intrinsic (column 247). If the choices are exactly ordered, say “1” is “unhappy”, and “10” is “happy”, we consider this column as this type. Tough “2” may not be twice happier than “1”, nevertheless, 2 is indeed happier. Note that some columns may include float numbers, say intrinsic, but we can multiply a factor to scale all responses to integers. Also, some responses could be negative values, say mcdv1, but we still can add a number to shift all of them to non-negative values.

Each value in these columns is the real value instead of probability. 


### Unordered Multiple Choices
Many columns belong to this type, for examples, ethnicity (column 42), gender (column 44), major (column 70) and V position (column 115). Note that these columns may include natural language response, say major, but we have classified all responses into several choices.

Each choice of these columns are exclusive and unordered. Therefore, we cannot just simply encode them into integers. Or we will have to face the explanatory problem: If we encode “computer science” into “1” and “mathematics” into “2”, do we mean a “mathematics” is equal to 2 “computer science”? Therefore, we choose one-hot encoding to use the same number as choices of Boolean values to represent the participant’s choice. In this case, we can consider each value as the probability that this participant will choose this response.

### Boolean-like Values
A few columns belong to this type. Some are natural language responses but there is a true answer, say anagrams (column 5 and 6) and attention correct (column 10), and the test is highly concerning about whether the participant correct or not instead of what they answered. Others are multiple choices with exactly 2 possible answers like mcmost (column 76 to 80), and for simplicity we prefer to use 1 Boolean value to represent his/her choice.

In general, we can consider this type as a special multiple choice type. Namely, each value in this column is a probability.

### Long Texts
There are exactly 3 columns belongs to this type: highpower (column 45), lowpower (column 67) and Notes (column 134). Because of time limition, we skiped to process these 3 columns.

### Other Valid Responses
Some natural language responses that describe a real number belong to this type, for example, K ratio (column 66), worst grade 2 (column 118) and SR TF Correct (column 133). Some obviously unrelated or redundant data is also this type. For an example, Date Computer (column 220) is a duplicate to Month Computer, Day Computer and Year Computer (column 222 to 224).

### NA's
In order to distinguish normal data and NA's, we use a valid mask. For each encoded feature, we use a Boolean value to indicate whether it is normal or NA. Namely, each row in original dataset is coded into 2 rows, where one is a valid mask and the other is the real data.

For simplicity, we set all NA’s to 0 just like dropout. When computing error, we use the mask to set these features’ loss to 0.

## Preprocessing Data
### Scaling to $[0, 1]$
Notice that the coded data can be further devided into 2 types: real values and probabilities. Notice that real values could be from negative infinity to positive infinity. (There may be some more restrictions like temperature in lab cannot be lower than -460. But in general its range is way larger than $[0, 1]$.) But for our prediction simplicity, we will linearly scale the largest value seen to $1$ and the smallest to $0$.

Here are some more things we can do, but because of time limit, we skipped them. The straightforward problem for this naïve scaling is we might be trapped by outliers. For example, (this example is already fixed.) some participant claimed his/her/its age is about 150. If we directly apply the scaling, most 20-ish responses will be scaled into about $0.007$, and the only response that is greater than $0.3$ is that 150, which will make this feature hard to predict precisely. Therefore, we should throw out these outliers.

But a further thought is that this situation can also happen when the response distributed unevenly. For example, many people answer either about 1 to 2 or 8 to 9. In this case, we use a lot of space to encode unlikely values, which leads to the same result. In this case, a nonlinear scale method will be helpful. A rudimentary thought is we sort all values in the dataset and linearly scale first 10% values to the range $[0, 0.1)$, second 10% to $[0.1, 0.2)$, and so on.

Another problem is that we cannot predict any larger or smaller values than values in the dataset. A plausible justification could be that it is generally unlikely to see an extreme small or large value. But if we adopt the nonlinear scale method, we can map negative infinity (or the smallest valid value) to the smallest value in dataset into $[0, 0.1)$, and all values in dataset to $[0.1, 0.9)$, and so on.

### Grouping Features
Notice that this dataset is all about 10 psychological tests. Therefore, we can assume the features in the same tests are more related than features between different tests. Namely the dimensionality in each tests is relatively small. Therefore, we can group features in terms of tests. Some global information about this participant, like demographic features and personality features, is grouped into another global set instead of test sets, which is called group 0. Some definitely unrelated data like participant ID (column 1) is grouped into another set, called group 11.

In this way, we can try to use group 0 and each test group to predict blank features in this test just by picking 2 group indices instead of a huge number of feature indices.

### Selecting Features
Notice that all group 11 features can be discard based on our prior knowledge. (Actually we should use graphical model to prove it.) A further thing we should do is run Chow Liu Algorithm on group 0 and each test group to find weak-dependent intra-test features (Namely, all its edges are weak.) and eliminate them, and then run it on the whole feature space to try to further eliminate features.

### Discarding Almost NA Data Points
Notice that there are several almost blank rows in the original datasets. These data points cannot tell us many things. We can use NA masks to identify them. More specifically, we remove these rows whose mask has more than $100$ `False`.

## Formalizing Interpolation
Given the preprocessed data, each data point is a vector with some blanks, and the whole dataset is a matrix with blanks. Our goal is to fill the blanks. Notice that we can do this because the dimensionality of this matrix is limited. Namely, many features are related to each other. For example, those who claimed they are high self-esteemed (column 252) are generally less stressed (column 253) and their mood (column 248) is better. Therefore, we can consider the dataset as a limited-rank matrix with some blanks whose size is $2434 \times 261$.

A straight forward idea to this problem is consider the blanks as noise, and our goal becomes to detect and eliminate this noise. Notice that the rank of this matrix is limited, therefore we can transform it into a much smaller matrix and restore it. Assuming the noise is relatively smaller than the information that this matrix gives, when we are transform or compressing this matrix, the noise will be eliminated, and then we can decompress it to restore the blanked values.

## Constructing Models
Given this formalization of interpolation, we choose AutoEncoder as our basic model because it can compress and decompress the given inputs. Notice that since we already grouped features, we can first encode each groups and then encode the whole data points. (Fig. 1 network.png) In this way, we can dramatically eliminate the number of weights because our first layer is not dense.

Notice that we encode the multiple choice columns into several features. Therefore, we can append a softmax layer to each multiple choice column. One thing to notice that for non-choice features, we have to directly output its value instead of pass it to softmax layer, or it will always return 1.

(When I am writing this report, I notice that I can expend each non-choice features into 2 features $x$ and $\bar x = 1-x$. In this case, we can directly pass all features of the same column to a softmax, instead of using masks to identify non-choice features.)

Here is another interesting but may not useful though. Notice that we assumed the rank of this matrix is limited. Namely the transformation can actually be linear. Namely we literally can multiply 2 small matrices to get this matrix. Therefore, we can further define this problem as find 2 matrices $A$ and $B$ to minimize $||M - AB||$, which is literally an optimization problem. But the drawback is that we ignore the meaning of each feature, say sum of several features should always be $1$. But it might be not a bad start, and we can further use Ada boost to combine it with our AutoEncoder.