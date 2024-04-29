
	




def rp(grades):
	h1dict = {'A':10,'B':8.75,'C':7.5,'D':6.25,'E':5,'S':2.5,'U':0}
	h2dict = {'A':20,'B':17.5,'C':15,'D':12.5,'E':10,'S':5,'U':0}
	total_rp = 0

	for ele in grades[:3]:
		total_rp+=h2dict[ele]
	for ele in grades[3:6]:
		total_rp+=h1dict[ele]
	return total_rp

def avg_rp(grades):
	#if only 1 record in grades
	if len(grades)==1:
		return rp(grades)
	#if more than 1 record in grades
	n = len(grades)
	total = 0
	for ele in grades:
		total += rp(ele)
	return total//n




grade_lst = (['U',"A","B","A","A","C"],['U','S','B','B','A','U'])	

print(avg_rp(grade_lst))