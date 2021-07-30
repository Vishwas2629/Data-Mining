import csv
import itertools
DataFile = open('I:\Data Mining\Code\Groceries.csv', 'r')
minsup = float(input('Enter minimum support value(0.02):'))
f2 = "op.txt"
f1 = "itemsupport.txt"
minconf = 0.39
def Load_data():
   
    DataCaptured = csv.reader(DataFile, delimiter=',')
    data = list(DataCaptured)
    for e in data:
        e = sorted(e)
    count = {}
    for items in data:
        for item in items:
            if item not in count:
                count[(item)] = 1
            else:
                count[(item)] = count[(item)] + 1
    #print("C1 Items", count)
    print("C1 Length : ", len(count))
    print()

    #Thresholding
    count2 = {k: v for k, v in count.items() if v >= minsup*9835}
    #print("Load_data Items : ", count2)
    print("Load_data Length : ", len(count2))
    print()

    return count2, data


def generate_candidate_item(Lk_1, flag, data):
   
    C_item_array = []

    if flag == 1:
        flag = 0
        for item1 in Lk_1:
            for item2 in Lk_1:
                if item2 > item1:
                    C_item_array.append((item1, item2))
        print("C2: ", C_item_array[1:3])
        print("length : ", len(C_item_array))
        print()

    else:
        for item in Lk_1:
            k = len(item)
        for item1 in Lk_1:
            for item2 in Lk_1:
                if (item1[:-1] == item2[:-1]) and (item1[-1] != item2[-1]):
                    if item1[-1] > item2[-1]:
                        C_item_array.append(item2 + (item1[-1],))
                    else:
                        C_item_array.append(item1 + (item2[-1],))
        print("C" + str(k+1) + ": ", C_item_array[1:3])
        print("Length : ", len(C_item_array))
        print()
    L = generateLk(set(C_item_array), data)
    return L, flag


def generateLk(C_item_array, data):
    
    count = {}
    for itemset in C_item_array:
        #print(itemset)
        for transaction in data:
            if all(e in transaction for e in itemset):
                if itemset not in count:
                    count[itemset] = 1
                else:
                    count[itemset] = count[itemset] + 1

    print("Candidate items Length : ", len(count))
    print()

    count2 = {k: v for k, v in count.items() if v >= minsup*9835}
    print(" Length : ", len(count2))
    print()
    return count2


def rules_generator(fitems):
   
    counter = 0
    for itemset in fitems.keys():
        if isinstance(itemset, str):
            continue
        length = len(itemset)

        union_support = fitems[tuple(itemset)]
        for i in range(1, length):

            lefts = map(list, itertools.combinations(itemset, i))
            i=1
            for left in lefts:
                if len(left) == 1:
                    if ''.join(left) in fitems:
                        leftcount = fitems[''.join(left)]
                        conf = union_support / leftcount
                else:
                    if tuple(left) in fitems:
                        leftcount = fitems[tuple(left)]
                        conf = union_support / leftcount
                if conf >= minconf:
                    fo = open(f2, "a+")
                    f22 = open("rulssup.txt", "a+")
                    
                    right = list(itemset[:])
                    for e in left:
                        right.remove(e)
                    fo.write(str(left) + ' (' + str(leftcount) + ')' + ' -> ' + str(right) + ' (' + str(fitems[''.join(right)]) + ')' + ' [' + str(conf) + ']' + '\n')
                    f22.write(str(counter)+' '+str(conf)+'\n')
                    print(str(left) + ' (' + str(leftcount) + ')' + ' -> ' + str(right) + ' (' + str(fitems[''.join(right)]) + ')' + ' [' + str(conf) + ']' + '\n')
                    print(str(left) + ' -> ' + str(right) + ' (' + str(conf) + ')')
                    counter = counter + 1
                    
                    fo.close()
                    f22.close()
    print(counter, "rules generated")


def apriori():
    
    L, data = Load_data()
    flag = 1
    i=1
    FreqItems = dict(L)
    while(len(L) != 0):
        fo = open(f1, "a+")
        f11= open('sup.txt', "a+")
        for k, v in L.items():
            fo.write(str(k) + ' ' + str(v) + '\n\n')
            f11.write(str(i) + ' ' + str(v) + '\n')
            i=i+1
            print(str(k) + ' ' + str(v) + '\n\n')
        fo.close()
        f11.close()

        L, flag = generate_candidate_item(L, flag, data)
        FreqItems.update(L)
    rules_generator(FreqItems)


if __name__ == '__main__':
    import os
    os.remove("itemsupport.txt")
    os.remove("op.txt")
    os.remove("rulssup.txt")
    os.remove("sup.txt")
    
    apriori()
    ################
    from tkinter import *
    import Pmw, sys
    filename = "op.txt"
    root = Tk()            
    top = Frame(root); top.pack(side='top')
    text = Pmw.ScrolledText(top,borderframe=5, vscrollmode='dynamic',hscrollmode='dynamic',labelpos='n',label_text='file %s' % filename,text_width=400,text_height=400,text_wrap='none',)
    text.pack()

    text.insert('end', open(filename,'r').read())
    Button(top, text='Quit', command=root.destroy).pack(pady=15)
    root.mainloop()
    ######################
    filename = "itemsupport.txt"
    root = Tk()            
    top = Frame(root); top.pack(side='top')
    text = Pmw.ScrolledText(top,borderframe=5, vscrollmode='dynamic',hscrollmode='dynamic',labelpos='n',label_text='file %s' % filename,text_width=400,text_height=400,text_wrap='none',)
    text.pack()

    text.insert('end', open(filename,'r').read())
    Button(top, text='Quit', command=root.destroy).pack(pady=15)
    root.mainloop()
    ##################
    import VIEW
