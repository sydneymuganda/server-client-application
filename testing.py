a=["apple"]
l=len(a)
s=""
if l<1:
    s="no files available"
else:
    for file in a:
        s=file+"\n"+s

print(s)
# print(len(a))
# a.append(1)
# print(len(a))
# a.append(1)
# print(len(a))