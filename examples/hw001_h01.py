"""
Example grader for HW001 in section H01.

This is an example of how the grader should work.

Created by Joshua Katz 12/14/2015
"""

ANSWERS_1 = "A"
ANSWERS_2 = "B"
ANSWERS_3 = "B"
ANSWERS_4 = "D"
ANSWERS_5 = "A"

# Test the method provided by the student
def multiply_by_two_test(implementation):

	if not implementation(2) == 4:
		return False

	if not implementation(10) == 20:
		return False

	return True

# Score the lab based on percent correct
def score(mulit_choice_correct, written_correct):

	total_mc_points = 50 # 50% of the grade is MC 
	total_written_points = 50 # 50% of the grade is 

	# Add the percents that were obtained
	return (total_mc_points * mulit_choice_correct) + (total_written_points * written_correct)