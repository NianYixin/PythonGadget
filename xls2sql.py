# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 11:37:14 2016

@author: liuziyi

"""

import xlrd
#'0001'-->'0002'
def stringAdd(one):
    return (str(int(one)+1)).zfill(4)
workbook = xlrd.open_workbook(r'1.xls')
test=workbook.sheet_names() 
sheet_name = workbook.sheet_names()
sheet_name = sheet_name[1]
sheet1 = workbook.sheet_by_index(1) # sheet索引从0开始  
sheet1 = workbook.sheet_by_name('Sheet1')

print (sheet1.name,sheet1.nrows,sheet1.ncols)
#print(sheet1.cell(2,1).value.encode('utf-8'))
#print(sheet1.cell_value(1,0).encode('utf-8'))
#print(sheet1.row(1)[0].value.encode('utf-8'))
row = sheet1.nrows#行数
col = sheet1.ncols#列数

topclass=[]#一级分类列表(id,name)
start='0001'#一级分类从0001开始
substart='0001'#二级分类的开始
othersub='9999'
nowtopclass='0001'#当前一级分类
subclass=[]#二级分类列表(id,name,parent_id)

lastsub=[]
subcount=0
for i in range(2,row):
    #数据库使用utf-8编码
    #一级分类
    if( sheet1.cell(i,1).value.encode('utf-8')!=b''):
        new_class=(start,sheet1.cell(i,2).value[2:])
        start=stringAdd(start)
        
        topclass.append(new_class)
        nowtopclass=new_class[0]
        substart='0001'
        
        if subcount!=0:
            lastsub.append(subcount)
            subcount=0
    #some one named other,so...
    if sheet1.cell(i,3).value[-2:]!='99':
        subclass.append((nowtopclass+substart,
                         sheet1.cell(i,4).value,
                         nowtopclass))
        substart=stringAdd(substart)
    else:
        subclass.append((nowtopclass+othersub,
                         sheet1.cell(i,4).value,
                         nowtopclass))
        
    subcount+=1
lastsub.append(subcount)
'''
'{0},{1}'.format('kzc',18)

p=['kzc',18]
'{0[0]},{0[1]}'.format(p)
Out[8]: 'kzc,18'

'''
#先导子类，再导父类
sql='INSERT INTO TGP_PRODUCT_CLASS \
(CLASS_ID,CLASS_CODE,CLASS_NAME,ORG_ID,PARENT_CLASS_CODE,IS_DEL,MAX_SON_NO)\
 VALUES (SGP_PRODUCT_CLASS_ID.NEXTVAL,\'{0[0]}\',\'{0[1]}\',100001,\'{0[2]}\',\'0\',0);' 

sql2='INSERT INTO TGP_PRODUCT_CLASS \
(CLASS_ID,CLASS_CODE,CLASS_NAME,ORG_ID,PARENT_CLASS_CODE,IS_DEL,MAX_SON_NO)\
 VALUES (SGP_PRODUCT_CLASS_ID.NEXTVAL,\'{0[0]}\',\'{0[1]}\',100001,\'0\',\'0\',{1});'        

sql3='INSERT INTO TGP_PRODUCT_CLASS \
(CLASS_ID,CLASS_CODE,CLASS_NAME,ORG_ID,PARENT_CLASS_CODE,IS_DEL,MAX_SON_NO)\
 VALUES (SGP_PRODUCT_CLASS_ID.NEXTVAL,\'{0}\',\'{1}\',100001,\'-1\',\'0\',{2});'
         
file_object = open('test.txt', 'w')
#ID硬编码
for each in subclass:
    file_object.write(sql.format(each))
    file_object.write('\n')
    

#计算当前子集个数
i=0    
for each in topclass:
    lastsub[i]=lastsub[i]-1
    file_object.write(sql2.format(each,lastsub[i]))
    i+=1
    file_object.write('\n')

#and the root...
file_object.write(sql3.format('0','root',len(topclass)))    

file_object.close()