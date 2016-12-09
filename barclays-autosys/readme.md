## Barclays Autosys Management

Machine is a graph of various jobs as nodes. The graph is described completely using `JIL`. Below is a simple machine described in JIL.

```
# Example of a Machine
insert_machine: lowgate
type: a
# Example of Jobs
insert_job: Nightly_Download
job_type: box
date_conditions: yes
days_of_week: all
start_times: "02:00"
insert_job: Watch_4_file
job_type: ft
box_name: Nightly_Download
watch_file: /DOWNLOAD/MAINFRAME/SALES.RAW
watch_file_type: generate
machine: lowgate
insert_job: filter_data
job_type: cmd
box_name: Nightly_Download
condition: success(Watch_4_file)
command: filter_mainframe_info
machine: lowgate
std_in_file: /DOWNLOAD/MAINFRAME/SALES.RAW
insert_job: parse_data
job_type: cmd
box_name: Nightly_Download
condition: success(filter_data)
machine: lowgate
command: isql -U mutt -P jeff
std_in_file: /DOWNLOAD/MAINFRAME/SALES.SQL
std_out_file: /LOG/parse_data.out
std_err_file: /LOG/LOG/parse_data.err
```

This is a machine with 4 jobs, with *filter_data* conditioned on the success of *Watch_4_file* and *parse_data* conditioned on the success of *filter_data*. The other jobs are in the same __box__ as the first, and hence are run at the same time *(maybe)*. The days of running etc. are specified.

### Logs
Logs are queried using the `autorep` command, and common usage is given [here](https://amahana.wordpress.com/2013/11/16/unicenter-autosys-jm-commands/). According the understood purpose, the output of `Autorep –j <job_name> -s`, which is a summary of report of the job, can be used. It has the following fields:
* Job Name
* Last Start
* Last End
* Status
* Run/Ntry
* Pri/Xit

Output of the above command looks like:  
Job Name | Last Start | Last End | Status | Run/Ntry | Pri/Xit  
--- | --- | --- | --- | --- | ---
Nightly_Download | 05/10/2007 06:01:03 | 05/10/2007 06:03:20 | SU | 1261419/1 | 0  
Watch_4_file | 05/10/2007 06:01:13 | 05/10/2007 06:01:16 | SU | 1261419/1 | 0  
filter_data | 05/10/2007 06:01:26 | 05/10/2007 06:01:48 | SU | 1261419/1 | 0  
parse_data | 05/10/2007 06:01:26 | 05/10/2007 06:01:48 | SU | 1261419/1 | 0  

It is still not clear how we can have data in time domain if the script only returns last run details.


### Clarity Required
The following topics are not very clear from online resources (or based on the requirement) and need more clarification.
* Machine Types
* With regard to [__box jobs__](http://autosys-tutorial-beginner.blogspot.in/2015/09/chapter-6-box-jobs.html), how do you handle them?
* The query only returns last run details. How to obtain the logs for a period?
* What are the fields *Run/Ntry* and *Pri/Xit* in the logs?
