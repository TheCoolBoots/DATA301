import numpy as np

def generateClassGrades():
    grades = np.genfromtxt('grades.txt', delimiter='\t')
    grades = np.nan_to_num(grades)
    maxpts = grades[-1]
    grades = grades[1:-1]

    

    # print(grades.type())

    output = np.apply_along_axis(getLetterGrade, 1, grades, maxpts)
    np.savetxt("grades.out", output, '%i')


def getLetterGrade(studentGrades, maxpts):
    
    if(studentGrades[19]/maxpts[19] >= .9):
        return [studentGrades[0], 4]
   
    projectsGrade = calculateComponentGrade(studentGrades[15:17], maxpts[15:17], .2)
    labGrade = calculateComponentGrade(studentGrades[5:14], maxpts[5:14], .2)
    assignmentGrade = calculateAssignmentGrade(studentGrades[1:5], maxpts[1:5], .1)
    examGrade = calculateComponentGrade(studentGrades[[14,19]], maxpts[[14,19]], .4)
    participationGrade = calculateComponentGrade(studentGrades[[-3]], maxpts[[-3]], .1)
    bonusGrade = calculateComponentGrade(studentGrades[[-2]], maxpts[[-2]], .01)

    finalGrade = projectsGrade + labGrade + assignmentGrade + examGrade + participationGrade + bonusGrade

    if(finalGrade >= .9):
        return [studentGrades[0], 4]
    elif (finalGrade >= .8):
        return [studentGrades[0], 3]
    elif (finalGrade >= .7):
        return [studentGrades[0], 2]
    elif (finalGrade >= .6):
        return [studentGrades[0], 1]
    else:
        return [studentGrades[0], 0]


def calculateComponentGrade(grades, maxPts, weight):
    return weight * sum( (grades / maxPts) / len(grades))

def calculateAssignmentGrade(grades, maxpts, weight):
    assGrades = grades/maxpts
    grades[np.argmin(assGrades)] = 0

    return weight * sum((grades/maxpts) / 3)


'''

for each line in grades.txt
    calculate programming projects grade (20%) (out of 20) [15:17]
    calculate lab grade (20%) (out of 9)            [5:14]
    calculate assignments grade (10%) (out of 74)   [1: 5]
    calculate exam grade (40%) (out of 117)     [14], [19]
    class participation grade (10%) (out of 10)     [-3]
    forum participation (1% bonus) (out of 1)   [-2]

    add all section grades together
    
    return array with [id, grade]

    index 1:    a1  a2  a3  a4  l1  l2  l3  l4  l5  l6  l7  l8  l9  m1  p1  p2  att B   F
                22	22	18	12	1	1	1	1	1	1	1	1	1	50	10	10	10	1	67

'''

generateClassGrades()

#a1 = np.arange(5)
#a2 = np.arange(5)
#print(a1/a2)
#testVectorize2()
