## Modelling Education Loan


### Problem Statement

Set up a model for deploying for a startup working with education loans, for small amounts. The PS is two-fold:  
* __Loan Sanctioning:__ Study the data and decide whether or not to sanction the amount as loan, and how much.
* __Student Monitoring and Warning:__ Monitor the current performance of the student, and raise warnings/flags when required.


### Feature Set

The idea is to model the placement packages of the students from known data and predict the same for the applicant. For the monitoring part, we monitor the current performance of the candidate and try to update our predictions in a similar manner, getting a better estimate with time.

For the former part, we work with a dataset about placement records of various concerned institutes and students. We maintain the logs of every institute, including past and current student records. The complete set of features would look like:
* Entrance Examination Ranking
* Class 10 Records
* Class 12 Records

Another attribute would be the applied loan amount, which would later be compared with the predicted package and then decision announced.

For the monitoring system, we have the same, along with two additional features, updated on a monthly basis (say):
* Current Performance
* Attendance Records

### The Model
#### The Sanctioning
The model is a deep neural network with the 3 input features as mentioned and 4 hidden nodes (best accuracy tested; to change, update the variable `hidden_layers`). The output is a number, which is the prediction of the expected placement package.  
* **Inputs:**  The CSV files for student data and institute data, in the format as attached. The format is a free choice as long as you change the variables `rel_input_sanction`, `rel_output_sanction` and `input_institute_name` accordingly.
* The flow has been vectorised to the best possible extent.
* The parameters that can be tweaked for improving performance include`epsilon`, `max_iter`, `hidden_layers`, `learning_rate` and `momentum_rate`
* To train the model, run `python neural_net.py train` for the first time. For predicting and testing, you can run `python neural_net predict` which opens an interactive terminal where you can enter the student details and get the predicted package.

### Packages Required
As of the current version of the code, _no external packages_ would be required. The list of imports is as follows:
* numpy
* csv
* joblib
* sys
* math
* random

### Status
* [_Completed_] Currently implemented a Random Forest on a sample training data 10 decision trees (max_depth = 12). The votes of the trees can be taken as a measure of the confidence which would decide amount of loan to be approved. [Accuracy: 78%]
* [_Completed_] Implemented a Deep Neural network to model the sanctioning process.
* [_Completed_] Vectorise and optimise the code.
* [_Suggestion_] Look at prospects of clustering the institutes based on certain similarities in trends.
* Deployable Version ready, see `client.py`.
