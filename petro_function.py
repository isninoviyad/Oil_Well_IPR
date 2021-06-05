import math

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box
from tkinter import filedialog

import numpy as np



class Additional:
    def __init__(self) :
        # self.coba()
        pass

    def check_empty_row(self, s_dict, nested_dict = False, specify_column = None) :
        '''
        CHECK & REMOVE ROWS WITH EMPTY VALUE.

        Return a dict that previously have empty value to a clean dict that will be projected as a table.

        #s_dict = dictionary storage
            --> the dict can be both ordinary dict with the value within a list or nested dict which is a dict inside a dict that also contains the value in a list.

        #nested_dict = is a boolean(False, True) statement to state the type of the dict originally False
            --> if you have nested dict, please mark it as True

        #specify_column = is a statement whether the function need to specify the column to check or not(check all columns), originally stated as False
            --> if you need to specify the columns, please write it as a list or tuple of the table heads
                for example :
                    specify_column = False #check all column
                    specify_column = ('A', 'B') #check only 'A' and 'B'
                    specify_column = ['A', 'B'] #check only 'A' and 'B' column 
        '''
        
        counted_col = []
        if specify_column == None :
            if nested_dict == False :
                for x in s_dict.keys() :
                    counted_col.append(x)
            else :
                for x in s_dict.keys() :
                    for y in s_dict[x] :
                        if y not in counted_col:
                            counted_col.append(y)
                        else :
                            pass
        else :
            counted_col = specify_column

            if nested_dict == False :
                for x in counted_col :
                    if x in list(s_dict.keys()) :
                        pass
                    else :
                        m_box.showerror(
                        '¯\_(ツ)_/¯',
                        'Mianhae..\nSome of the mandatory variables aren\'t available in your data head !'
                            )
            else :
                a = list(s_dict.keys())[0]

                for x in counted_col :
                    if x in list(s_dict[a].keys()) :
                        pass
                    else :
                        m_box.showerror(
                        '¯\_(ツ)_/¯',
                        'Mianhae..\nSome of the mandatory variables aren\'t available in your data head !'
                            )
        
        if nested_dict == False :
            c = 0
            c_empty = []
            empty = []
            count = []
            for x in range(0, len(list(s_dict.values())[0])):
                for y in counted_col : #ori --> for y in s_dict.keys()
                    empty.append(list(s_dict[y])[c])

                    if len(empty) == len(counted_col): #ori --> if len(empty) == len(s_dict.keys()):
                        for z in empty :
                            if isinstance(z, str) or math.isnan(z) == True :
                                count.append(z)
                            else :
                                pass
                        if len(count) > 0 :
                            c_empty.append(c)
                        else :
                            pass
                    else :
                        pass
                empty = []
                count = []

                c += 1

            #del column for ordinary dict (general)
            minus = 0
            c = 0
            for n in c_empty :
                c_empty[c] = n + minus
                c += 1
                minus -= 1

            for r in c_empty :
                for m in s_dict.keys() :
                    del s_dict[m][r]
                
        else :
            #nested dict + counted specific columns
            val = []
            s_empty = {}

            for x in s_dict.keys() :
                for d in range(0, len(list(s_dict[x].values())[0])) :
                    for y in counted_col : #ori --> for y in s_dict[x] :
                        val.append(s_dict[x][y][d])
                        if len(val) == len(counted_col): #ori --> if len(val) == len(list(s_dict[x].keys())):
                            for t in val :
                                if isinstance(t, str) or math.isnan(t) == True :
                                    if x not in list(s_empty.keys()) :
                                        s_empty[x] = [d]
                                    else :
                                        if d not in s_empty[x] :
                                            s_empty[x].append(d)
                                        else :
                                            pass
                                else :
                                    pass
                        else :
                            pass
                    val = []

            #del column for nested dict (general)
            minus = 0
            for x in s_empty.keys() :
                for y in s_empty[x] :
                    c = y
                    c += minus

                    for z in s_dict[x].keys() :
                        del s_dict[x][z][c]
                    minus -= 1
                minus = 0
            
            #FOR KEY LAYER WITH ZERO VAL
            empty = []
            for x in s_dict.keys() :
                for y in s_dict[x].keys() :
                    if len(list(s_dict[x][y])) == 0 :
                        if x not in empty :
                            empty.append(x)
                        else :
                            pass
                    else :
                        pass
        
            for x in empty :
                del s_dict[x]
            
        return s_dict 


    def make_table(self, frame, s_dict,
                            number = True,
                                entry_state = 'normal',
                                    get_last_row = False ) :
        '''
        FUNCTION TO MAKE TABLE.
        there are two kinds of table that possible to be made :
        1. Number = True
            -> for left side head, instead of using specific name,
            this table uses ordered number such as [1,2,3,4,5,6, etc]
            
            NOTE :
            ** for this kind of table, the last dict as ordinary dict with list inside.
            {'Key1' : [a,b,c,d,e], 'Key2' : [d,e,f,g,h]}
            ** the side number aren't considered as the part of the dict,
            the order only considered by the index of each value inside the list.


        2. Number = False
            -> the left side head are more flexible to use and
            it is possible to contain a specific label name instead of an ordered numbers

            NOTE :
            ** for this kind of table, results written as nested dict.
            {
             'Side_head_key1' : {'Upper_head_key1' : [a,b,c,d,e],
                                 'Upper_head_key2' : [f,g,h,i,j]},
             'Side_head_key2' : {'Upper_head_key1' : [k,l,m,n,o],
                                 'Upper_head_key2' : [p,q,r,s,t]}
                                                }

        '''
        
        total_rows = len(list(s_dict.values())[0]) #assume every col has the same len as 1st col
        total_columns = len(list(s_dict))

        if number == True :
            #CREATE NUMBER IN TABLE
            order_list = ['']
            order = np.arange(1 , total_rows+1)

            for i in order :
                order_list.append(i)
            
            b = 0
            for r in order_list :
                order_lbl = ttk.Label(frame,
                                            text = r,
                                                width = 3)
                order_lbl.grid(row = b, column = 0)
                b += 1
        
        else :
            #CREATE SIDE HEAD IN TABLE
            ''' Mianhabnida, bcs i'm too not in the mood of opening any nested dict,
            so, I choose to separate keys and sub keys in nested into different section.
            then, to sync those two, I prefer to use the references of rows.
            THAT'S ALL..
            :)
            '''

            s_dict_temporary = {}
            order_list = []

            for key, val in s_dict.items():
                n = 1
                for x in s_dict[key].keys():
                    for val in s_dict[key][x] :
                        if n > len(s_dict[key][x]):
                            pass
                        else :
                            order_list.append(key)
                        n += 1

                        if x not in s_dict_temporary.keys():
                            s_dict_temporary[x] = [val]
                        else :
                            s_dict_temporary[x].append(val)

            s_dict = s_dict_temporary.copy()

            sidehead_dict = {}

            b = 1
            ref_r = 0
            row_store = []
            just_r = []

            n = 1
            for r in order_list :
                if r not in just_r :
                    just_r.append(r)

                    sidehead_entry = ttk.Entry(frame,
                                    textvariable = r,
                                            width = 7,
                                                state = entry_state
                                            )
                else :
                    sidehead_entry = ttk.Entry(frame,
                                    textvariable = f'{r}_{n}',
                                            width = 7,
                                                state = entry_state
                                            )
                    n += 1

                sidehead_entry.grid(row = b, column = 0)
                sidehead_entry.delete(0, len(str(sidehead_entry.get()))) #BIAR GA TUMPUK KALO CLICK 2X
                sidehead_entry.insert(0, r)

                if sidehead_entry not in list(sidehead_dict.keys()):
                    sidehead_dict[sidehead_entry] = [ref_r]
                else :
                    sidehead_dict[sidehead_entry].append(ref_r)
                
                b += 1
                ref_r += 1

                #[0,0] table head if nested = True
                data_head_btn_0 = ttk.Button(frame,
                                                width = 6,
                                                    state = 'disabled',
                                                        text = 'Layer'
                                                            )
                data_head_btn_0.grid(row = 0, column = 0)

        #FINAL RESULT DICT
        table_data_dict = {} #empty dict for final dict
        table_data_sublist = [] #empty list for temporary sublist

        #CREATE TABLE HEADER
        n = 0 #head number
        r = 0 #row
        c = 1 #column
        for h, sub_h in s_dict.items() :
            data_head_btn = ttk.Button(frame,
                                    width = 15,
                                        state = 'disabled',
                                            text = list(s_dict)[n]
                                                )
            data_head_btn.grid(row = r, column = c)

            table_data_dict[list(s_dict)[n]] = [] #input {'key' : [empty]} into final dict as the amount of col
            table_data_sublist.append ([]) #create empty list in sublist as the amount of col
            n +=1
            c +=1
    
        #CREATE TABLE ENTRY
        n = 0 #head order
        m = 0 #head_list order

        c = 1 #column
        r = 1 #row
        r_x_c = len(list(s_dict.values())[0])*len(list(s_dict)) #row x column

        for i in range (1, r_x_c+1):
            entry_data_table = ttk.Entry(frame,
                                width = 16,
                                    textvariable = str(list(s_dict)[n]) + '_' + str(m),
                                        state = entry_state
                                                    )
            if r == (len(list(s_dict.values())[0])+1) :
                n += 1
                m = 0
                c += 1
                r = 1
                
            entry_data_table.grid(row = r , column = c )
            entry_data_table.delete(0, len(str(entry_data_table.get()))) #BIAR GA TUMPUK KALO CLICK 2X
            entry_data_table.insert(0, list(s_dict.values())[n][m])

            table_data_sublist[n].append(entry_data_table) #create list member in sublist

            m += 1
            r += 1
        
        last_row = r #ini (last row occupied +1)
        
        #SUMMARIZE SUBLIST INTO FINAL RESULT DICT {'dict_key' : [ sublist ]}
        n = 0
        for x in range(0, len(list(s_dict))):
            member_sub_list = table_data_sublist[n][:]

            table_data_dict[list(s_dict)[n]].extend(member_sub_list)
            n += 1

        #sync keys and sub_keys in nested dict
        last_storage = {}
        if number != True :
            for key, y in sidehead_dict.items() :
                last_storage[key] = {}
                for x in sidehead_dict[key]:
                    for a, b in table_data_dict.items():
                        if a not in last_storage[key].keys() :
                            last_storage[key][a] = [table_data_dict[a][x]]
                        else :
                            last_storage[key][a].append(table_data_dict[a][x])

            table_data_dict = last_storage.copy()
        else :
            pass

        if get_last_row == True :
            return last_row, table_data_dict

        else :
            return table_data_dict
        
        print(table_data_dict)


    def extract_table (self, s_tkinter_dict, nested_dict = False):
        '''
        EXTRACT DICT THAT CONTAIN TKINTER ENTRY TABLE.
        
        '''

        if nested_dict == False :
            n = 0
            store_value = []
            s_test = {}
            for y in range (0, len(list(s_tkinter_dict))):
                s_test[list(s_tkinter_dict)[n]] = []
                #store_value.append ([])
                n += 1
            
            for head, etc in s_tkinter_dict.items():
                store_value.extend(s_tkinter_dict[head])

            n = 0
            m = 1
            for y in store_value :
                try :
                    if '.' in str(y.get()) :
                        s_test[list(s_tkinter_dict)[n]].append(
                                                float(y.get()
                                                    )#float
                                                )
                    else :
                        s_test[list(s_tkinter_dict)[n]].append(
                                                int(y.get()
                                                    )#int
                                                )
                except ValueError :
                    s_test[list(s_tkinter_dict)[n]].append(
                                                y.get()
                                                    )#string
                m += 1 #Ini row+1 baru ganti line ya, wkwkwkwk..
                if m == (len(list(s_tkinter_dict.values())[0])+1):
                    n += 1
                    m = 1

        else :
            #I STRONGLY SUGGEST TO USE ANOTHER DICT TO SAVE THE RESULT
            #USE THE DICT CAN CAUSE AN ADDITIONAL PROBLEM LIKE IT CHANGE THE ORIGINAL DICT UNINTENDEDLY

            n = 0
            d = {}
            for z in s_tkinter_dict.keys():
                try :
                    z_out = z.get()
                except AttributeError :
                    z_out = z

                z_out = z_out.strip()

                if z_out not in list(d.keys()) :
                    d[z_out] = {}
                else :
                    pass

                for b in s_tkinter_dict[z].keys() :
                    if b not in list(d[z_out].keys()) :
                        d[z_out][b]= []
                    else :
                        pass
                    
                    for c in s_tkinter_dict[z][b] :
                        try :
                            c.get()
                            try :
                                if '.' in str(c.get()):
                                    d[z_out][b].append(float(c.get()))
                                else :
                                    d[z_out][b].append(int(c.get()))
                            except ValueError :
                                d[z_out][b].append(str(c.get()))
                        except AttributeError :
                            try :
                                if '.' in str(c) :
                                    d[z_out][b].append(float(c))
                                else :
                                    d[z_out][b].append(int(c))
                            except ValueError :
                                d[z_out][b].append(str(c))

            s_test = d.copy()

        return s_test

    def reverse_head(self, current_dict) :
        #FOR KEY LAYER WITH ZERO VAL
        empty = []
        for x in current_dict.keys() :
            for y in current_dict[x].keys() :
                if len(list(current_dict[x][y])) == 0 :
                    if x not in empty :
                        empty.append(x)
                    else :
                        pass
                else :
                    pass
    
        for x in empty :
            del current_dict[x]

        c_current_dict = current_dict.copy()
        spc = 0
        for y in current_dict.keys() :
            for z in str(y) :
                if z != ' ' :
                    spc += 1
                else :
                    pass
            if spc == 0 :
                del c_current_dict[y]
            spc = 0
        
        current_dict = c_current_dict.copy()
        
        ori_head_0 = list(current_dict.keys())[0]

        for_new_head = []
        for x in current_dict[ori_head_0].keys() :
            for_new_head.append(x)
        
        new_dict = {}
        for x in for_new_head :
            if x not in list(new_dict.keys()) :
                new_dict[x] = {}
            else :
                pass

            for y in current_dict.keys() :
                new_dict[x][y] = current_dict[y][x].copy()
        
        return new_dict

    def head_reorder(self, s_dict, head_key, nested_dict = False) :
        if nested_dict == False :
            new_dict = {}
            head_key1 = []
            head_key2 = []

            for y in list(s_dict.keys()) :
                if y == head_key :
                    head_key1.append(y)
                else :
                    head_key2.append(y)

            head_key1.extend(head_key2)

            for x in head_key1 :
                new_dict[x] = s_dict[x]
        else :
            new_dict = {}
            head_key1 = []
            head_key2 = []

            head_0 = list(s_dict.keys())[0]
            for y in s_dict[head_0].keys() :
                if y == head_key :
                    head_key1.append(y)
                else :
                    head_key2.append(y)
            
            head_key1.extend(head_key2)

            for x in head_key1 :
                for z in s_dict.keys() :
                    if z not in list(new_dict.keys()) :
                        new_dict[z] = {}
                    else :
                        pass

                    new_dict[z][x] = s_dict[z][x].copy()
            
        return new_dict



    def coba(self) :
        s_test1 = { 
                    'Q'     : [1 ,2 ,3 ,'', ''],
                    'Pwf'   : [1 ,'',3 ,4 , ''],
                    'Pr'    : ['',2 ,3 ,4 , '']
                            }

        s_test =    {
                        'Layer1' :  {'Q' : [100,2 ,3    ,''],
                                    'Pwf': [120,'','str',4]},
                        'Layer2' :  {'Q' : [130,2 ,3    ,''],
                                    'Pwf': [140,'',3    ,4]},
                        'Layer3' :  {'Q' : ['', ''],
                                    'Pwf': ['', '']}
                            }

        # result = self.check_empty_row(s_dict = s_test1,
        #                                 specify_column = ('Pwf'),
        #                                     nested_dict = False
        #                                             )
        # result = self.reverse_head(s_test)
        result = self.head_reorder(s_test, 'Pwf', nested_dict = True)
        
        print(result)
        

Additional()













# def check_empty_row (self, s_dict, specify_column = False, nested_dict = False) :
#         '''
#         CHECK & REMOVE ROWS WITH EMPTY VALUE.
#         '''
#         counted_col = []
#         if specify_column == False :
#             if nested_dict == False :
#                 for x in s_dict.keys() :
#                     counted_col.append(x)
#             else :
#                 for x in s_dict.keys() :
#                     for y in s_dict[x] :
#                         if y not in counted_col:
#                             counted_col.append(y)
#                         else :
#                             pass
#         else :
#             counted_col = specify_column

#         if nested_dict == False :
#             if specify_column == False :
#                 #ordinary dict + counted all columns
#                 c = 0
#                 c_empty = []
#                 empty = []
#                 count = []
#                 for x in range(0, len(list(s_dict.values())[0])):
#                     for y in s_dict.keys():
#                         empty.append(list(s_dict[y])[c])

#                         if len(empty) == len(s_dict.keys()):
#                             for z in empty :
#                                 if isinstance(z, str) or math.isnan(z) == True :
#                                     count.append(z)
#                                 else :
#                                     pass
#                             if len(count) > 0 :
#                                 c_empty.append(c)
#                             else :
#                                 pass
#                         else :
#                             pass
#                     empty = []
#                     count = []

#                     c += 1

#             else :
#                 #ordinary dict + counted specific columns

#                 c = 0
#                 c_empty = []
#                 empty = []
#                 count = []
#                 for x in range(0, len(list(s_dict.values())[0])):
#                     for y in counted_col : #specify
#                         empty.append(list(s_dict[y])[c])

#                         if len(empty) == len(counted_col): #specify
#                             for z in empty :
#                                 if isinstance(z, str) or math.isnan(z) == True :
#                                     count.append(z)
#                                 else :
#                                     pass
#                             if len(count) > 0 :
#                                 c_empty.append(c)
#                             else :
#                                 pass
#                         else :
#                             pass
#                     empty = []
#                     count = []

#                     c += 1

#             #del column for ordinary dict (general)
#             minus = 0
#             c = 0
#             for n in c_empty :
#                 c_empty[c] = n + minus
#                 c += 1
#                 minus -= 1

#             for r in c_empty :
#                 for m in s_dict.keys() :
#                     del s_dict[m][r]
                
#         else :
#             if specify_column == False :
#                 #nested dict + counted all columns

#                 val = []
#                 s_empty = {}

#                 for x in s_dict.keys() :
#                     for d in range(0, len(list(s_dict[x].values())[0])) :
#                         for y in s_dict[x].keys() :
#                             val.append(s_dict[x][y][d])
#                             if len(val) == len(list(s_dict[x].keys())):
#                                 for t in val :
#                                     if isinstance(t, str) or math.isnan(t) == True :
#                                         if x not in list(s_empty.keys()) :
#                                             s_empty[x] = [d]
#                                         else :
#                                             if d not in s_empty[x] :
#                                                 s_empty[x].append(d)
#                                             else :
#                                                 pass
#                                     else :
#                                         pass
#                             else :
#                                 pass
#                         val = []

#             else :
#                 #nested dict + counted specific columns

#                 val = []
#                 s_empty = {}

#                 for x in s_dict.keys() :
#                     for d in range(0, len(list(s_dict[x].values())[0])) :
#                         for y in counted_col : #specify
#                             val.append(s_dict[x][y][d])
#                             if len(val) == len(counted_col): #specify
#                                 for t in val :
#                                     if isinstance(t, str) or math.isnan(t) == True :
#                                         if x not in list(s_empty.keys()) :
#                                             s_empty[x] = [d]
#                                         else :
#                                             if d not in s_empty[x] :
#                                                 s_empty[x].append(d)
#                                             else :
#                                                 pass
#                                     else :
#                                         pass
#                             else :
#                                 pass
#                         val = []

#             #del column for nested dict (general)
#             minus = 0
#             for x in s_empty.keys() :
#                 for y in s_empty[x] :
#                     c = y
#                     c += minus

#                     for z in s_dict[x].keys() :
#                         del s_dict[x][z][c]
#                     minus -= 1
#                 minus = 0
            
#             #FOR KEY LAYER WITH ZERO VAL
#             empty = []
#             for x in s_dict.keys() :
#                 for y in s_dict[x].keys() :
#                     if len(list(s_dict[x][y])) == 0 :
#                         if x not in empty :
#                             empty.append(x)
#                         else :
#                             pass
#                     else :
#                         pass
        
#             for x in empty :
#                 del s_dict[x]
            

#         return s_dict




#NESTED DICT EXTRACT WITHOUT USING ADDITIONAL DICT

# n = 0
# for z in s_tkinter_dict.keys():
#     for b in s_tkinter_dict[z].keys() :
#         for c in s_tkinter_dict[z][b] :
#             try :
#                 c.get()
#                 try :
#                     if '.' in str(c.get()):
#                         s_tkinter_dict[z][b][n] = float(c.get())
#                     else :
#                         s_tkinter_dict[z][b][n] = int(c.get())
#                 except ValueError :
#                     s_tkinter_dict[z][b][n] = str(c.get())
#             except AttributeError :
#                 try :
#                     if '.' in str(c) :
#                         s_tkinter_dict[z][b][n] = float(c)
#                     else :
#                         s_tkinter_dict[z][b][n] = int(c)
#                 except ValueError :
#                     s_tkinter_dict[z][b][n] = str(c)
#             n += 1
#         n = 0

# r = 0
# d = {}
# for x in s_tkinter_dict.keys() :
#     x = x.get()
#     if x not in list(d.keys()) :
#         d[x] = [r]
#     else :
#         d[x].append(r)
#     r += 1

# s_test = {}
# for x in d.keys() :
#     for y in d[x] :
#         name = list(s_tkinter_dict.keys())[y]
#         if x not in list(s_test.keys()) :
#             s_test[x] = s_tkinter_dict[name]
#         else :
#             for m in s_tkinter_dict[name].keys() :
#                 s_test[x][m].extend(s_tkinter_dict[name][m])