"""
Example grader for HW001 in section H01.

This is an example of how the grader should work.

Created by Joshua Katz 12/14/2015
"""

QUESTIONS_1 = "A"
QUESTIONS_2 = "A"
QUESTIONS_3 = "A"
QUESTIONS_4 = "A"
QUESTIONS_5 = "A"


# Test the method provided by the student
def add_two_test(implementation):
    return implementation(2) == 4 and implementation(10) == 12


# Score the lab based on percent correct
def scorer(mulit_choice_correct, written_correct):
    total_mc_points = 50  # 50% of the grade is MC
    total_written_points = 50  # 50% of the grade is

    # Add the percents that were obtained
    return (total_mc_points * mulit_choice_correct) + (total_written_points * written_correct)
