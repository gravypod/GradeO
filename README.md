# GradeO: Automated Grader

## What is GradeO?
GradeO is a poorly named automated lab-grading system for a class I will be a teacher assistant in next semester.

## What does it do?
There are a few features that GradeO implements.

* Grade labs based using an automated script.
* Dispatch emails to students about their grades.
* Output information useful to class graders.
* Save grades to a CSV file allowing grade data to be imported into a Google Spreadsheets.
* Move graded labs into another folder.

## Usage
1. Simple run of GradeO that will only output to console.

        python gradeo.py --grader hw001_cs100_h01.py --labs labs/

2. Same as above, but will prefer using a short printing mode.

        python gradeo.py --grader hw001_cs100_h01.py --labs labs/ --short_print

3. Grade everything and store data into a CSV file named "grades.csv"

        python gradeo.py --grader hw001_cs100_h01.py --labs labs/ --csv grades.csv

4. Grade everything and move into folder "graded/".

        python gradeo.py --grader hw001_cs100_h01.py --labs labs/ -move_finished a/finished/path/

    > Note that the folder must be created. If there is a folder "graded" has been graded in the same directory, labs will be moved in there.

5. Finally, grade all labs and send emails to everyone who has submitted a lab. This will only send emails to people who have an incorrect answer on their lab. 

        python gradeo.py --grader hw001_cs100_h01.py --labs labs/ --enable_email --enable_default INCORRECT

    > Note that by running this, you will need to supply your UCID login to enable sending emails. In addition, it is preferable to only run this after you have graded everything at least once. This will email people, and it is preferable to not spam students.*

6. Graders can also collect student preferences for emails. These can be stored into a json file. This example will reference the [email dispatch file.](https://github.com/gravypod/GradeO/blob/master/examples/email_dispatch.json)

        python gradeo.py --grader hw001_cs100_h01.py --labs labs/ --enable_email --email_pref email_dispatch.json

    > Note that by default, if a user does not have a setting in the [email dispatch file](https://github.com/gravypod/GradeO/blob/master/examples/email_dispatch.json) they will never get an email. To change this use the email_default setting from above.*


## File Naming and Standards

Currently all files submitted to grade must follow a standard. Later that can be changed by parsing the contents of the files looking for comments.

### Auto Grader Script
    
* The auto grader script must be have the homework number to grade, the class name, and the section number.


        hw001_cs100_h01.py


> This will grade homework #001, for CS100, in section H01


* The contents of the file will include any information needed to grade labs. Answers to multiple choice questions are defined as follows.


        ANSWERS_1 = "A"
        ANSWERS_2 = "B"
        ANSWERS_3 = "B"
        ANSWERS_4 = "D"
        ANSWERS_5 = "A"

* Following this, the test cases for functions will be implemented. All assigned labs should specify **PEP compliant names**.

        def add_two_test(implementation):
            return implementation(2) == 4 and implementation(10) == 12


> Note that all test functions must end with "_test"

* The final, and most important step is grading and weighting the sections.

        def scorer(mc_correct, written_correct):
            mc_points = 50 # 50% for MC
            written_pints = 50 # 50% written
            return (mc_correct * mc_points) + (written_correct * written_points)

> Note that mc\_correct and written\_correct are decimals from 0 to 1.

### Lab Submissions
* Lab submissions must follow a standard file name convention.

        hw001_jk369.py

> This is a lab for HW001 from the student jk369

* Students must answer multiple choice questions following this format

        QUESTION_1 = "A"
        QUESTION_2 = "B"
        QUESTION_3 = "C"
        QUESTION_4 = "D"
        QUESTION_5 = "E"

* All functions inside the lab must follow the provided naming within the lab assignment.

        def add_two(number):
            # Works on add_two(2) == 4
            # But not on add_two(10) == 12
            # Close but no cigar.
            return number + 2.0000000000000000000000000000001 

## TODO
* Automatically store data into google sheets.
* Check similarity of submissions using a AST diff algorithm. 
* Sandbox the submitted code further to prevent running code on the host machine.
* Allow GradeO to point to a set of grader scripts for bulk-grading of multiple classes and sections.
* Pull information about the lab from comments in the file.
* Implement a [Levenshtine distance](https://en.wikipedia.org/wiki/Levenshtein_distance) to find function implementations if there is a spelling mistake in the header.
* Obviously, clean the code.