'''
Linda Zhang
Class: CS 677
Date: 03/26/2022
'''
import pandas as pd


pd.options.mode.chained_assignment = None
data=pd.read_csv('SPY.csv')

'''
Homework Problem #1.1
Description of Problem: I created a new column called "True_Label".
I used the "Return" column to determine if it was a '-' or a '+'.
I set the training year from 2016,2017,and 2018.
The testing year is set at 2019 and 2020.
'''
data['True_Label']=data['Return'].apply(lambda x:'-' if x<0 else '+')
training=data[data['Year']<=2018]
test=data[data['Year']>2018]
print('Question 1.1 #######################################################')
print(data.head())

'''
Homework Problem #1.2
Description of Problem: I took the first training data which contains the 
first three year(training data) and determined assumed that all of the days are
independent of each other. I then calculated the probability that the sign
 '+' will appear next.
'''
#counted all of the day 'True_Label' column had a postive
up_day=len(training['True_Label'][training['True_Label']== '+'])
#divided over the total number of days
prob_up=up_day/len(training['True_Label'])
print('Question 1.2 #######################################################')
print('The probability the next day will be postive is', prob_up*100)


'''
Homework Problem #1.3
Description of Problem: I took the first training data which contains the 
first three year(training data) and looked at different consecutive 'down days'.
I determine the proability of it being a postive day next compared to a negative
day after.
'''
#grouped 'True_Label' by '+' sign so if we looking for '--' its grouped by '+--'
sign = training['True_Label'].groupby((training['True_Label'] == '+').cumsum()).cumcount()

print('Question 1.3 #######################################################')
th_negprob = sum(sign.diff() <= -3) / (sum(sign >=3)+sum(sign.diff() <= -3))*100
print('Proability of a positive day after three negative days:')
print(th_negprob)

tw_negprob = sum(sign.diff() <= -2) / (sum(sign >=2)+sum(sign.diff() <= -2))*100
print('Proability of a positive day after two negative days:')
print(tw_negprob)

one_negprob = sum(sign.diff() <= -1) / (sum(sign >=1)+sum(sign.diff() <= -1))*100
print('Proability of a positive day after one negative days:')
print(one_negprob)


'''
Homework Problem #1.4
Description of Problem: I took the first training data which contains the 
first three year(training data) and looked at different consecutive 'up days'.
I determine the proability of it being a postive day next compared to a negative
day after.
'''
#grouped 'True_Label' by '+' sign so if we looking for '++' its grouped by '-++'
new_sign = training['True_Label'].groupby((training['True_Label'] == '-').cumsum()).cumcount()

print('Question 1.4 #######################################################')
print('Proability of a negative day after three positive days:')
th_posprob = sum(new_sign.diff() <= -3) / (sum(new_sign >=3)+sum(new_sign.diff() <= -3))*100
print(th_posprob)
print('Proability of a negative day after two positive days:')
tw_posprob = sum(new_sign.diff() <= -2) / (sum(new_sign >=2)+sum(new_sign.diff() <= -2))*100
print(tw_posprob)
print('Proability of a negative day after one positive days:')
one_posprob = sum(new_sign.diff() <= -1) / (sum(new_sign >=2)+sum(new_sign.diff() <= -1))*100
print(one_posprob)


'''
Homework Problem #2.1
Description of Problem: I first created a function that would take in a string
and search for the patter. In order to be able to search for the value, I had
to change it into a string. I then created compute function which would look
at the W value and predict the values for Year 2019 to 2020 based on the count
of the pattern that was counted in Year 2016,2017 and 2018.
'''
#turn into string
training_string=''.join(training['True_Label'])
test_string=''.join(test['True_Label'])


#for this function it would intake the sting that is being searched and pattern
#Then it would count the number of times that pattern appear in the string
def pattern_count(str_search,pattern):
    str_search, pattern = str_search.strip(), pattern.strip()
    if pattern == '': return 0
    ind, count, start_flag = 0,0,0
    while True:
        try:
            if start_flag == 0:
                ind = str_search.index(pattern)
                start_flag = 1
            else:
                ind += 1 + str_search[ind+1:].index(pattern)
            count += 1
        except:
            break
    return count

def compute(w):
    list_p=[]
    count=0
    #loop each line starting from w value
    for i in range(len(test))[w:]:
        #Depending on the W value it will take the first W number of values from
        #year 2019 and 2020 to determine the next value and this would loop.
        if w==2:
            o=list(test['True_Label'])[i-2:i]
            k=o[0]+o[1]
        elif w==3:
            o=list(test['True_Label'])[i-3:i]
            k=o[0]+o[1]+o[2]
        elif w==4:
            o=list(test['True_Label'])[i-4:i]
            k=o[0]+o[1]+o[2]+o[3]
        #uses the training data to count the amount of time it appears
        up=pattern_count(training_string,k+'+')
        down=pattern_count(training_string,k+'-')
        #calculates the percentage
        p=up/(up+down) 
        #adds it to a list
        list_p.append(p)
    count+=1
    return list_p

#created a copy of testing(2019 and 2020) in case of error
#Made two new columns per W value one with percentage of what the sign would be
#the other one with actual sign. 
df_2=test.copy()
df_2['guess2']=0
df_2['guess2'][2:]=compute(2)
df_2['Guess2_sign']=0
df_2['Guess2_sign'][2:]=df_2['guess2'][2:].apply(lambda x: '+' if x > 0.5 else '-')

df_2['guess3']=0
df_2['guess3'][3:]=compute(3)
df_2['Guess3_sign']=0
df_2['Guess3_sign'][3:]=df_2['guess3'][3:].apply(lambda x: '+' if x > 0.5 else '-')

df_2['guess4']=0
df_2['guess4'][4:]=compute(4)
df_2['Guess4_sign']=0
df_2['Guess4_sign'][4:]=df_2['guess4'][4:].apply(lambda x: '+' if x > 0.5 else '-')

print('Question 2.1 #######################################################')
print(df_2.head())



'''
Homework Problem #2.2
Description of Problem: I created a funciton to calculate when the selected
column is equal to the True_value. After counting which one matches, I calculated
the accuracy of the selected column
'''
def compare_signs(column,w):
    accurate=0
    count=0
    for i in test.index[w:]:
        if(column[i]=='+')& (test['True_Label'][i] == '+') :
            accurate+=1
        if (column[i]=='-') & (test['True_Label'][i] == '-'):
            accurate+=1
        count +=1
    acc=accurate/count
    return acc
print('Question 2.2 #######################################################')
print('Accuracy of W=2')
print(compare_signs(df_2['Guess2_sign'],2))
print('Accuracy of W=3')
print(compare_signs(df_2['Guess3_sign'],3))
print('Accuracy of W=4')
print(compare_signs(df_2['Guess4_sign'],4))


'''
Homework Problem #3.1
Description of Problem: Created an ensemble column which looks at W=2, W=3 and
W=4 column to determine which sign is more popular and assign it to that value.
'''
def ensemble_signs(df_2):
    ens=[]
    count=0
    for i in range(4,len(df_2)):
        
        g2=df_2.iloc[i]['Guess2_sign']
        g3=df_2.iloc[i]['Guess3_sign']
        g4=df_2.iloc[i]['Guess4_sign']
        
        if g2==g3:
            ens.append(g2)
        elif g2==g4:
            ens.append(g2)
        elif g3==g4:
            ens.append(g3)
        count +=1
    return ens
df_2['ensemble']=0
zero=[0,0,0,0]
df_2['ensemble']=zero+ensemble_signs(df_2)
print('Question 3.1 #######################################################')
print(df_2.head(6))


'''
Homework Problem #3.2
Description of Problem: Looked at the accuracy of the ensemble column. I used 
the function of looking at the accuracy I made earlier.
'''
print('Question 3.2 #######################################################')
print('Accuracy of the ensemble column')
print(compare_signs(df_2['ensemble'],4))


'''
Homework Problem #3.3
Description of Problem:Created a function to check the accuracy of predicting
'-' labels. I first compared the signs and then if it match it adds 1 to the
value.
'''
def compare_signs_neg(column,w):
    accurate=0
    count=0
    for i in test.index[w:]:
        if (column[i]=='-') & (test['True_Label'][i] == '-'):
            accurate+=1
        count +=1
    acc=accurate/count
    return acc
print('Question 3.3 #######################################################')
print('Negative Prediction Accuracy for ensemble')
print(compare_signs_neg(df_2['ensemble'],4))
print('Negative Prediction Accuracy for W=2')
print(compare_signs_neg(df_2['Guess2_sign'],2))
print('Negative Prediction Accuracy for W=3')
print(compare_signs_neg(df_2['Guess3_sign'],3))
print('Negative Prediction Accuracy for W=4')
print(compare_signs_neg(df_2['Guess4_sign'],4))


'''
Homework Problem #3.4
Description of Problem:Created a function to check the accuracy of predicting
'+' labels. I first compared the signs and then if it match it adds 1 to the
value.
'''
def compare_signs_pos(column,w):
    accurate=0
    count=0
    for i in test.index[w:]:
        if(column[i]=='+')& (test['True_Label'][i] == '+') :
            accurate+=1
        count +=1
    acc=accurate/count
    return acc
print('Question 3.4 #######################################################')
print('Positive Prediction Accuracy for ensemble')
print(compare_signs_pos(df_2['ensemble'],4))
print('Positive Prediction Accuracy for W=2')
print(compare_signs_pos(df_2['Guess2_sign'],2))
print('Positive Prediction Accuracy for W=3')
print(compare_signs_pos(df_2['Guess3_sign'],3))
print('Positive Prediction Accuracy for W=4')
print(compare_signs_pos(df_2['Guess4_sign'],4))


'''
Homework Problem #4.1
Description of Problem:Created a function to calculate the True Positive Value
'''
def tp(column,w):
    found=0
    count=0
    for i in test.index[w:]:
        if(column[i]=='+')& (test['True_Label'][i] == '+') :
            found+=1
        count +=1
    return found
print('Question 4.1 #######################################################')
print('True Positive for W=2')
print(tp(df_2['Guess2_sign'],4))
print('True Positive for W=3')
print(tp(df_2['Guess3_sign'],4))
print('True Positive for W=4')
print(tp(df_2['Guess4_sign'],4))
print('True Positive for ensemble')
print(tp(df_2['ensemble'],4))


'''
Homework Problem #4.2
Description of Problem:Created a function to calculate the False Positive Value
'''
def fp(column,w):
    found=0
    count=0
    for i in test.index[w:]:
        if(column[i]=='+')& (test['True_Label'][i] == '-') :
            found+=1
        count +=1
    return found
print('Question 4.2 #######################################################')
print('False Positive for W=2')
print(fp(df_2['Guess2_sign'],4))
print('False Positive for W=3')
print(fp(df_2['Guess3_sign'],4))
print('False Positive for W=4')
print(fp(df_2['Guess4_sign'],4))
print('False Positive for ensemble')
print(fp(df_2['ensemble'],4))



'''
Homework Problem #4.3
Description of Problem:Created a function to calculate the True Negative Value
'''
def tn(column,w):
    found=0
    count=0
    for i in test.index[w:]:
        if(column[i]=='-')& (test['True_Label'][i] == '-') :
            found+=1
        count +=1
    return found
print('Question 4.3 #######################################################')
print('True Negative for W=2')
print(tn(df_2['Guess2_sign'],4))
print('True Negative for W=3')
print(tn(df_2['Guess3_sign'],4))
print('True Negative for W=4')
print(tn(df_2['Guess4_sign'],4))
print('True Negative for ensemble')
print(tn(df_2['ensemble'],4))


'''
Homework Problem #4.4
Description of Problem:Created a function to calculate the False Negative Value
'''
def fn(column,w):
    found=0
    count=0
    for i in test.index[w:]:
        if(column[i]=='-')& (test['True_Label'][i] == '+') :
            found+=1
        count +=1
    return found
print('Question 4.4 #######################################################')
print('False Negative for W=2')
print(fn(df_2['Guess2_sign'],4))
print('False Negative for W=3')
print(fn(df_2['Guess3_sign'],4))
print('False Negative for W=4')
print(fn(df_2['Guess4_sign'],4))
print('False Negative for ensemble')
print(fn(df_2['ensemble'],4))


'''
Homework Problem #4.5
Description of Problem:Created a function to calculate the True Positive Rate Value
'''
def tpr(column,w):
    tpr_v=float(tp(column,w))/float((tp(column,w))+float(fn(column,w)))
    return tpr_v
print('Question 4.5 #######################################################')
print('True Positive Rate for W=2')
print(tpr(df_2['Guess2_sign'],4))
print('True Positive Rate for W=3')
print(tpr(df_2['Guess3_sign'],4))
print('True Positive Rate for W=4')
print(tpr(df_2['Guess4_sign'],4))
print('True Positive Rate for ensemble')
print(tpr(df_2['ensemble'],4))



'''
Homework Problem #4.6
Description of Problem:Created a function to calculate the True Negative Rate Value
'''
def tnr(column,w):
    tnr_v=float(tn(column,w))/float((tn(column,w))+float(fp(column,w)))
    return tnr_v
print('Question 4.6 #######################################################')
print('True Negative Rate for W=2')
print(tnr(df_2['Guess2_sign'],4))
print('True Negative Rate for W=3')
print(tnr(df_2['Guess3_sign'],4))
print('True Negative Rate for W=4')
print(tnr(df_2['Guess4_sign'],4))
print('True Negative Rate for ensemble')
print(tnr(df_2['ensemble'],4))


'''
Homework Problem #4.7
Description of Problem:Created a table of the findings
'''
table={'W':['2','3','4','ensemble'],
       'Ticker':['S&P 500','S&P 500','S&P 500','S&P 500'],
       'TP':[tp(df_2['Guess2_sign'],4),tp(df_2['Guess3_sign'],4),tp(df_2['Guess4_sign'],4),tp(df_2['ensemble'],4)],
       'FP':[fp(df_2['Guess2_sign'],4),fp(df_2['Guess3_sign'],4),fp(df_2['Guess4_sign'],4),fp(df_2['ensemble'],4)],
       'TN':[tn(df_2['Guess2_sign'],4),tn(df_2['Guess3_sign'],4),tn(df_2['Guess4_sign'],4),tn(df_2['ensemble'],4)],
       'FN':[fn(df_2['Guess2_sign'],4),fn(df_2['Guess3_sign'],4),fn(df_2['Guess4_sign'],4),fn(df_2['ensemble'],4)],
       'accuracy':[compare_signs(df_2['Guess2_sign'],4),compare_signs(df_2['Guess3_sign'],4),compare_signs(df_2['Guess4_sign'],4),compare_signs(df_2['ensemble'],4)],
       'TPR':[tpr(df_2['Guess2_sign'],4),tpr(df_2['Guess3_sign'],4),tpr(df_2['Guess4_sign'],4),tpr(df_2['ensemble'],4)],
       'TNR':[tnr(df_2['Guess2_sign'],4),tnr(df_2['Guess3_sign'],4),tnr(df_2['Guess4_sign'],4),tnr(df_2['ensemble'],4)]}
print('Question 4.7 #######################################################')
print(pd.DataFrame(table))




