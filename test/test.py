lists=[{'title':['=',1]},{'name':['like','chang']}]
lists=[{'id':5},{'name':'abc'}]
str1=' '
where_list=[]
# def pare(op=[]):
#     if op:
#         if op[0] == '=':
#             pass
#         if op[0] == 'like':
#             op[1] = "'%" + str(op[1]) + "%'"
#     return op
# for list in lists:
#     (field,value), = list.items()
#     value=pare(value)
#     str1=field+' '+str(value[0])+' '+str(value[1])
#     where_list.append(str1)
#     print(where_list)
fields_list = []
for list in lists:
    str1 = ' '
    (field,value), = list.items()
    print(field,value)
    str1 = ' ' + field + '=' + str(value)
    fields_list.append(str1)
str1 = ' , '.join(fields_list)

print(str1)