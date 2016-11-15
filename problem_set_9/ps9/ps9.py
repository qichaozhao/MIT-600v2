# 6.00 Problem Set 9
#
# Intelligent Course Advisor
#
# Name:
# Collaborators:
# Time:
#

from itertools import chain, combinations

SUBJECT_FILENAME = "subjects.txt"
SHORT_SUBJECT_FILENAME = "shortened_subjects.txt"
VALUE, WORK = 0, 1

#
# Problem 1: Building A Subject Dictionary
#
def loadSubjects(filename):
    """
    Returns a dictionary mapping subject name to (value, work), where the name
    is a string and the value and work are integers. The subject information is
    read from the file named by the string filename. Each line of the file
    contains a string of the form "name,value,work".

    returns: dictionary mapping subject name to (value, work)
    """

    # The following sample code reads lines from the specified file and prints
    # each one.
    catalogue = {}

    inputFile = open(filename)
    for line in inputFile:
        # split the line into a list
        tmp = line.split(',')

        # add to dict
        catalogue[tmp[0]] = (int(tmp[1]), int(tmp[2]))

    return catalogue
    # value, and work of each subject and create a dictionary mapping the name
    # to the (value, work).

def printSubjects(subjects):
    """
    Prints a string containing name, value, and work of each subject in
    the dictionary of subjects and total value and work of all subjects
    """
    totalVal, totalWork = 0,0
    if len(subjects) == 0:
        return 'Empty SubjectList'
    res = 'Course\tValue\tWork\n======\t====\t=====\n'
    subNames = subjects.keys()
    subNames.sort()
    for s in subNames:
        val = subjects[s][VALUE]
        work = subjects[s][WORK]
        res = res + s + '\t' + str(val) + '\t' + str(work) + '\n'
        totalVal += int(val)
        totalWork += int(work)
    res = res + '\nTotal Value:\t' + str(totalVal) +'\n'
    res = res + 'Total Work:\t' + str(totalWork) + '\n'
    print res

#
# Problem 2: Subject Selection By Greedy Optimization
#

def cmpValue(subInfo1, subInfo2):
    """
    Returns True if value in (value, work) tuple subInfo1 is GREATER than
    value in (value, work) tuple in subInfo2
    """
    return subInfo1[VALUE] > subInfo2[VALUE]

def cmpWork(subInfo1, subInfo2):
    """
    Returns True if work in (value, work) tuple subInfo1 is LESS than than work
    in (value, work) tuple in subInfo2
    """
    return subInfo1[WORK] < subInfo2[WORK]

def cmpRatio(subInfo1, subInfo2):
    """
    Returns True if value/work in (value, work) tuple subInfo1 is 
    GREATER than value/work in (value, work) tuple in subInfo2
    """
    return subInfo1[VALUE] / float(subInfo1[WORK]) > subInfo2[VALUE] / float(subInfo2[WORK])

def greedyAdvisor(subjects, maxWork, comparator):
    """
    Returns a dictionary mapping subject name to (value, work) which includes
    subjects selected by the algorithm, such that the total work of subjects in
    the dictionary is not greater than maxWork.  The subjects are chosen using
    a greedy algorithm.  The subjects dictionary should not be mutated.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    comparator: function taking two tuples and returning a bool
    returns: dictionary mapping subject name to (value, work)
    """
    catalogue = subjects
    catalogue_keys = subjects.keys()
    selected = {}
    maxWork = maxWork
    curWork = 0
    comp = comparator


    # loop until we break
    while True:
        # print "a new loop"
        # set an initial cur_best value
        cur_best = (0, 0)
        cur_best_key = ""

        # loop through catalogue and find the best subject
        for idx, s in enumerate(catalogue_keys):
            # print "a new catalogue loop"

            # check if it is already selected, if so, skip
            if s not in selected:
                # print "key " + str(s) + " is not in selected"
                # check if its our 1st time through
                if cur_best_key == "":
                    cur_best_key = s
                    cur_best = catalogue[s]

                # else:
                elif comp(catalogue[s], cur_best):
                    cur_best_key = s
                    cur_best = catalogue[s]

                    # print cur_best_key
                else:
                    pass

            else:
                pass

            # print "current cur_best is: " + str(cur_best_key)

        # print "best key out of this catalogue loop is: " + str(cur_best_key)

        if (curWork + cur_best[1]) > maxWork:
            # break
            break
        else:
            # add the cur_best selection to our selected catalogue and increment curWork
            # print cur_best
            selected[cur_best_key] = cur_best
            curWork += cur_best[1]
            # printSubjects(selected)
            # print "new selected: " + str(selected)

    return selected

#
# Problem 3: Subject Selection By Brute Force
#
def bruteForceAdvisor(subjects, maxWork):
    """
    Returns a dictionary mapping subject name to (value, work), which
    represents the globally optimal selection of subjects using a brute force
    algorithm.

    subjects: dictionary mapping subject name to (value, work)
    maxWork: int >= 0
    returns: dictionary mapping subject name to (value, work)
    """

    # basically we need to test every arrangement of values in our input dictionary
    # first lets get a list of keys
    keys = subjects.keys()

    # we need to generate every single possible subset of this keys list
    keyset = set(list(generateSubsets(keys)))
    # print keyset

    best_val_sum = 0
    best_comb = None
    # now we need to go through each item in keyset and find the best
    for k in keyset:
        tmp_work_sum = 0
        tmp_val_sum = 0

        for l in k:
            tmp_work_sum += subjects[l][1]
            tmp_val_sum += subjects[l][0]

        if tmp_work_sum <= maxWork and tmp_val_sum > best_val_sum:
            best_val_sum = tmp_val_sum
            best_comb = k

    # build our output
    output = {}
    for m in best_comb:
        output[m] = subjects[m]

    return output


def generateSubsets(list):
    """
    accepts a list and generates every single possible subset of combinations, return list of lists
    :param list:
    :return:
    """
    s = list
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


if __name__ == '__main__':

    maxWork = 7
    comparator = cmpRatio

    data_sel = raw_input("""Which data set you wanna use?
    1 = Reduced
    2 = Full
    """)

    if data_sel == "1":
        datafile = SHORT_SUBJECT_FILENAME
    else:
        datafile = SUBJECT_FILENAME

    sel = raw_input("""What do you wanna do?
    1 = Greedy
    2 = Brute Force
    """)

    if sel == "1":
        # greedy
        print datafile

        data = loadSubjects(datafile)
        # print data

        print "We are calculating for greedy optimisation!"
        # data = {'6.00': (10, 1), '6.01': (8, 4), '6.02': (5, 8), '6.03': (1, 1), '6.04': (5, 15)}
        output = greedyAdvisor(data, maxWork, comparator)

        print output

    elif sel == "2":
        print datafile

        data = loadSubjects(datafile)
        # print data

        print "We are calculating for bruteForce optimisation!"
        # data = {'6.00': (10, 1), '6.01': (8, 4), '6.02': (5, 8), '6.03': (1, 1), '6.04': (5, 15)}
        output = bruteForceAdvisor(data, maxWork)

        print "best combination: " + str(output)