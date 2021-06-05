import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as m_box
from tkinter import filedialog

import numpy as np
import pandas as pd
import math

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from petro_function import Additional as pf



class Controller():
    def __init__(self):
        self.model = Model()
        self.view = View()


    def main(self):
        self.view.main()


    def enter_click(self):
        '''
        Extention of enter button, in order to execute the overall process into final result.
        '''
        ipr_name = self.two_phase_ipr.get()
        s = {}

        for caption, x in self.collect_entry.items() :
            s[caption] = self.collect_entry[caption]['val'].get()

        well_name = s['Well Name']

        if ipr_name == 'Fetkovich - Two Phase' or ipr_name == 'Test Data':
            s_test = pf.extract_table(self, self.table_data_final_dict)

            if self.file_exist == True :
                Q_head = self.Q_sync_head.get()
                Pwf_head = self.pwf_sync_head.get()

                if Q_head == Pwf_head :
                    m_box.showwarning(
                            '¯\_(ツ)_/¯',
                            'Mianhamnida, please references your data with different head !'
                                                        )
                else :
                    s_test_final = {}
                    for x in s_test.keys() :
                        if x == Q_head :
                            s_test_final['Q'] = s_test[x]
                        elif x == Pwf_head :
                            s_test_final['Pwf'] = s_test[x]
                        else :
                            s_test_final[x] = s_test[x]

                    self.s_test = s_test_final.copy()

            else :
                self.s_test = s_test.copy()

            items = ('Q', 'Pwf')
            try :
                s_test2 = pf.check_empty_row(self,
                                                self.s_test,
                                                    specify_column = items
                                                            )
                if not s_test2 == {} :
                    if all(i in list(s_test2.keys())  for i in items)   and(
                    len(s_test2[i]) >= 2           for i in items)   and(
                    s['Pr'] != ''                        )           and(
                    s['Pb'] != ''                        )         :

                        ipr_i = Model.Ipr(self = Model, ipr = ipr_name,

                                                    Q   = s_test2['Q'],
                                                    Pwf = s_test2['Pwf'],
                                                    Pr  = float(s['Pr']),
                                                    Pb  = float(s['Pb'])
                                                        )
                        Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_i)

                    else :
                        m_box.showwarning(
                            '¯\_(ツ)_/¯',
                            'Mianhae..\nplease, make sure you have fullfil your data completely !\nThe value of Pr and Pb is mandatory.'
                                )
                else :
                    m_box.showwarning(
                    '¯\_(ツ)_/¯',
                    'Mianhae..\nYou have a bad data, make sure to complete your data !'
                        )
            except AttributeError:
                #only if Q_head == Pwf_head
                pass

        elif ipr_name == 'Composite IPR' :
            items = ('Q', 'Pwf', 'Pr', 'Pb')
            s_test = pf.extract_table(self,
                                        self.table_data_final_dict,
                                            nested_dict = True
                                                        )
            layer_group = {}
            try :
                for x in self.collect_LG_cb.keys() :
                    layer_group[x] = []
                    c = 0
                    for y in self.collect_LG_cb[x] :
                        val = y.state()
                        lyr = self.collect_LG[c]

                        if val == ('selected',) :
                            layer_group[x].append(lyr)
                        else : #('alternate',), ()
                            # layer_group[x].append(0)
                            pass
                        c += 1
            except AttributeError :
                layer_group['Group 0'] = []


            if self.file_exist == True :
                Q_head      = self.Q_sync_head.get()
                Pwf_head    = self.pwf_sync_head.get()
                Pr_head     = self.pr_sync_head.get()
                Pb_head     = self.pb_sync_head.get()

                if  Q_head      in (Pwf_head, Pr_head, Pb_head)     or(
                    Pwf_head    in (Q_head, Pr_head, Pb_head))      or(
                    Pr_head     in (Q_head, Pwf_head, Pb_head))     or(
                    Pb_head     in (Q_head, Pwf_head, Pr_head)) :

                    m_box.showwarning(
                            '¯\_(ツ)_/¯',
                            'Mianhamnida, please references your data with different head !'
                                                        )

                else :
                    s_test2 = {}
                    for x in s_test.keys() :
                        s_test2[x] = {}
                        for y in s_test[x].keys() :
                            if y == Q_head :
                                s_test2[x]['Q'] = s_test[x][y].copy()
                            elif y == Pwf_head :
                                s_test2[x]['Pwf'] = s_test[x][y].copy()
                            elif y == Pr_head :
                                s_test2[x]['Pr']  = s_test[x][y].copy()
                            elif y == Pb_head :
                                s_test2[x]['Pb']   = s_test[x][y].copy()
                            else :
                                s_test2[x][y] = s_test[x][y].copy()

                    s_test_done = s_test2.copy()

            else :
                s_test_done = s_test.copy()

            try :
                s_test_clean = pf.check_empty_row(self,
                                                    s_test_done,
                                                        specify_column = items,
                                                            nested_dict = True
                                                                    )


                if not s_test_clean == {} :
                    #CLEAN LAYER GROUP THAT CONTAINS EMPTY VAL KEYS
                    empty_lyr = {}
                    for key_i in layer_group.keys() :
                        empty_lyr[key_i] = []
                        for val_i in layer_group[key_i] :
                            if val_i in list(s_test_clean.keys()) :
                                empty_lyr[key_i].append(val_i)
                            else :
                                pass
                    layer_group = empty_lyr.copy()

                    for x in s_test_clean.keys() :
                        if all(i in list(s_test_clean[x].keys()) for i in items) :
                            if (len(s_test_clean[x][j]) >= 1 for j in items) :

                                status = 'good_output'

                            else :
                                m_box.showerror('¯\_(ツ)_/¯',
                                        'Mianhamnida..\nYou don\'t have sufficient data for some layer'
                                                )
                                status = 'bad_output'
                                break

                        else :
                            m_box.showerror('¯\_(ツ)_/¯',
                                'Mianhae..\nMake sure you have a complete Q, Pwf, Pr, and Pb data'
                                    )
                            status = 'bad_output'
                            break
                else :
                    layer_group = {'Group 0' : []}
                    m_box.showerror('¯\_(ツ)_/¯',
                                'Mianhae..\nYou have bad data, make sure to complete it'
                                    )
                    status = 'bad_output'

                if status == 'good_output' :
                    try :
                        ipr_i, ipr_comp, ipr_layer = Model.ipr_composite(self = Model,
                                                                    s_test = s_test_clean,
                                                                        layer_group = layer_group
                                                                            )
                        Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_i, one_pack = True)
                        Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_comp)
                        Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_layer)
                        # Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_i)

                    except ValueError : #not enough values to unpack(expect 3, got 2)
                        ipr_i, ipr_comp = Model.ipr_composite(self = Model,
                                                                    s_test = s_test_clean,
                                                                        layer_group = layer_group
                                                                            )
                        Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_i, one_pack = True)
                        Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_comp)
                else :
                    pass

            except (AttributeError, UnboundLocalError) :
                print('tributeerror')
                #means one of this issues happaned (Pwf_head == Q_head == Pr_head == Pb_head)
                pass


        else : #single phase, two-phase vogel, partial phase vogel
            try :
                ipr_i = Model.Ipr(self = Model, ipr = ipr_name,

                            Pb  = float(s['Pb']),    Q         = float(s['Q']),
                            Pr  = float(s['Pr']),    rw        = float(s['rw']),
                            Pwf = float(s['Pwf']),   K         = float(s['Permeability']),
                            h   = float(s['h']),     viscosity = float(s['Viscosity']),
                            Bo  = float(s['Bo']),    skin      = float(s['Skin']),
                            re  = float(s['re'])
                                                        )
            except ValueError :
                try :
                    ipr_i = Model.Ipr(self = Model, ipr = ipr_name,

                                Q       = float(s['Q']),
                                Pr      = float(s['Pr']),
                                Pwf     = float(s['Pwf']),
                                Pb      = float(s['Pb'])
                                                            )
                except ValueError :
                    m_box.showwarning(
                        '¯\_(ツ)_/¯',
                        'Mianhamnida Yeorobun..\nplease, make sure you have put a value on Pwf, Q, Pr, and Pb !'
                                                            )
            Plot_PopUp().multiple_plot_show('Q', 'Pwf', well_name, ipr_i)


class Model():
    def __init__(self):
        pass

    def Ipr(self, ipr, Q, Pb, Pr, Pwf, **s):
        '''
        To calculate the inflow performance rate.
        '''
        list_pwf = []
        det = -1
        if 'Pr_max' not in s.keys() :
            s['Pr_max'] = Pr

            if Pr > Pb :
                det = ((0-s['Pr_max'])/8) #--> x Data + 2

                a_pwf = np.arange(s['Pr_max'], Pb, det).tolist()
                a_pwf.append(Pb)

                b_pwf = np.arange(Pb, 0, det).tolist()
                b_pwf.append(0)

                a_pwf.extend(b_pwf)

                list_pwf = a_pwf

            elif Pb >= Pr :
                det = ((0-s['Pr_max'])/9) #--> x Data + 1

                list_pwf = np.arange(s['Pr_max'], 0, det).tolist()
                list_pwf.append(0)

        else :
            #for composite ipr, to make a uniform data
            det = ((0-s['Pr_max'])/9) #--> x Data + 1

            list_pwf = np.arange(s['Pr_max'], 0, det).tolist()
            list_pwf.append(0)

        Q_rate = []

        if ipr  == 'Single Phase' :
            #for undersaturated, single phase oil well

            PI = float(Q/(Pr-Pwf))

            for pwf_p in list_pwf :
                rate = float(PI * (Pr-pwf_p))
                Q_rate.append(round(rate, 3))

        elif ipr == 'Vogel - Two Phase' :
            #for two phase oil well
            try :
                PI = float ( (s['K'] * s['h']) /
                            ( 141.2 * s['Bo'] * s['viscosity'] *
                            ( np.log(s['re']/s['rw']) - 0.75 + s['skin']) )
                                        )
                qmax = float(PI*Pr/1.8)
            except KeyError :
                qmax = Q /(
                        1 - 0.2 * (Pwf/Pr) - 0.8 * ((Pwf/Pr)**2)
                                        )

            for pwf_p in list_pwf :
                rate   = float (qmax *
                                  ( 1- 0.2 * (pwf_p/Pr ) - 0.8 * ((pwf_p/Pr)**2)
                                        )
                                            )
                Q_rate.append(round(rate, 3))

        elif ipr == 'Fetkovich - Two Phase':
            #for two phase oil well

            Q_1 = []
            Pwf_1 = []
            for x in Q :
                Q_1.append(math.log10(float(x)))
            for y in Pwf :
                Pwf_1.append(math.log10(Pr**2 - (float(y)**2)))

            slope = (Pwf_1[0]-Pwf_1[-1])/(Q_1[0]-Q_1[-1])
            n = 1/slope

            i = -1
            qmax = float(Q[i])/(
                    (1-((float(Pwf[i])/Pr)**2))**n
                            )

            for pwf_p in list_pwf :
                rate = qmax * (1-(pwf_p/Pr)**2)**n  #(-NEGATIF) powered by 2
                try :
                    Q_rate.append(round(rate, 3))
                except TypeError :
                    # Q_rate.append(float('NaN'))
                    Q_rate.append(rate)

        elif ipr == 'Vogel - Partial Two Phase':
            #for undersaturated reservoir Pr > Pb, but with pwf < pb

            try :
                PI = float(
                        (s['K'] * s['h']) /
                        (141.2 * s['Bo'] * s['viscosity'] *
                        (np.log(s['re']/s['rw']) - 0.75 + s['skin'])
                                    )
                                        )
            except KeyError :
                PI = float(Q/(Pr-Pwf)) #TEMPORARY (PLS CHECK FOR THIS CASE, WHAT KIND OF PI CALCULATION THAT SHOULD BE USE)

            for pwf_p in list_pwf  :
                if pwf_p > Pb :
                    rate_Qb = float (PI*(Pr-pwf_p))

                    Q_rate.append(round(rate_Qb, 3))

                else :
                    rate_Qv = float (PI*(Pr-Pb)+(PI*Pb/1.8)*
                                    (1-0.2*(pwf_p/Pb)-0.8*(pwf_p/Pb)**2)
                                        )
                    Q_rate.append(round(rate_Qv, 3))

        elif ipr == 'Test Data':
            pass

        elif ipr == 'Composite IPR':
            pass

        ipr_i = {}
        ipr_i[ipr] = {}

        ipr_i[ipr]['Q'] = Q_rate
        ipr_i[ipr]['Pwf'] = list_pwf

        return ipr_i

    def ipr_composite(self, s_test, layer_group) :
        #Looking for max Pr of the layers
        Pr_max = 0
        for x in s_test.keys() :
            for y in s_test[x].keys() :
                if y == 'Pr' :
                    for z in s_test[x][y] :
                        if z >= Pr_max :
                            Pr_max = float(z)
                        else :
                            pass
                else :
                    pass

        Q_i = {}
        ipr_i = {}

        for p in s_test.keys() :
            d = {}
            for k in range(0, len(list(s_test[p].values())[0])) :
                for l in s_test[p].keys() :
                    if l not in d.keys() :
                        d[l] = [s_test[p][l][k]]
                    else :
                        d[l].append(s_test[p][l][k])

            f = 0
            if d['Pr'][f] >= d['Pb'][f]         and (
               d['Pwf'][f] >= d['Pb'][f])  :

                ipr ='Single Phase'
                well_dict = self.Ipr(self, ipr = ipr,

                                    Q       = d['Q'][f],
                                    Pb      = d['Pb'][f],
                                    Pr      = d['Pr'][f],
                                    Pr_max  = Pr_max,
                                    Pwf     = d['Pwf'][f]
                                            )


            elif d['Pr'][f] >= d['Pb'][f]       and (
                 d['Pwf'][f] < d['Pb'][f])  :

                ipr ='Vogel - Partial Two Phase'
                well_dict = self.Ipr(self, ipr = ipr,

                                    Q       = d['Q'][f],
                                    Pb      = d['Pb'][f],
                                    Pr      = d['Pr'][f],
                                    Pr_max  = Pr_max,
                                    Pwf     = d['Pwf'][f]
                                            )

            elif d['Pr'][f] < d['Pb'][f] :
                if len(list(d['Q'])) < 0: #JUST SKIP IT FOR A WHILE UNTIL I CAN FIND A WAY TO AVOID GETTING COMPLEX NUMBER
                    ipr ='Fetkovich - Two Phase'
                    well_dict = self.Ipr(self, ipr = ipr,

                                    Q       = d['Q'],
                                    Pb      = d['Pb'],
                                    Pr      = d['Pr'][f],
                                    Pr_max  = Pr_max,
                                    Pwf     = d['Pwf']
                                            )

                else :
                    ipr ='Vogel - Two Phase'
                    well_dict = self.Ipr(self, ipr = ipr,

                                    Q       = d['Q'][f],
                                    Pb      = d['Pb'][f],
                                    Pr      = d['Pr'][f],
                                    Pr_max  = Pr_max,
                                    Pwf     = d['Pwf'][f]
                                            )

            else :
                #FOR UNSTATED ONE, USE SINGLE PHASE ASSUMPTION
                ipr ='Single Phase'
                well_dict = self.Ipr(self, ipr = ipr,

                                    Q       = d['Q'][f],
                                    Pb      = d['Pb'][f],
                                    Pr      = d['Pr'][f],
                                    Pr_max  = Pr_max,
                                    Pwf     = d['Pwf'][f]
                                            )

            # wellname = f'{p}\n{ipr}'
            wellname = f'{p}'
            Q_i[wellname] = well_dict[ipr]['Q'].copy()

            ipr_i[wellname] = {}
            ipr_i[wellname]['Q'] = well_dict[ipr]['Q'].copy()
            ipr_i[wellname]['Pwf'] = well_dict[ipr]['Pwf'].copy()

        #FOR COMPOSITE IPR
        ipr_comp = {}
            
        Pwf_i = well_dict[ipr]['Pwf'].copy()

        c = 0
        for pwf_val in well_dict[ipr]['Pwf'] :
            Pwf_i[c] = round(float(pwf_val), 3)
            c += 1

        Q_sum = []
        for x in range(0, len(list(Q_i.values())[0])) :
            a = 0
            for y in Q_i.keys() :
                a = a + Q_i[y][x]

            Q_sum.append(round(a, 3))

        ipr_comp['Composite IPR'] = {}
        ipr_comp['Composite IPR']['Q'] = Q_sum
        ipr_comp['Composite IPR']['Pwf'] = Pwf_i

        #FOR GROUP LAYER
        ipr_layer = {}

        for c0 in layer_group.keys() :
            c = str(c0)
            lyr_name = ''
            awal = True
            for lyr in layer_group[c] :
                if awal == True :
                    lyr_name = f'{lyr}'
                else :
                    lyr_name = f'{lyr_name},{lyr}'

                awal = False
            
            c = f'{c}\n({lyr_name})'

            if len(layer_group[c0]) != 0 :
                ipr_layer[c]        = {}
                ipr_layer[c]['Q']   = []
                ipr_layer[c]['Pwf'] = Pwf_i

                for idx in range(0, len(list(Q_i.values())[0])) :
                    Q_lyr_sum       = 0
                    for layer_name in layer_group[c0] :
                        try :
                            Q_lyr_sum += ipr_i[layer_name]['Q'][idx]
                        except KeyError :
                            pass
                    
                    ipr_layer[c]['Q'].append(round(Q_lyr_sum,3))
            else :
                pass
            
        c = 0
        for grp in layer_group.keys() :
            if len(layer_group[grp]) == 0 :
                c += 1
            else :
                pass

        if c == len(list(layer_group.keys())):
            return ipr_i, ipr_comp

        else :
            return ipr_i, ipr_comp, ipr_layer


class View(tk.Tk):
    PAD = 10
    def __init__(self):
        super().__init__()

        self.entry_captions =   {
            'Well Name'             : {'val' : 'E-408 & L-1485'  , 'unit' : ''        },
            'Depth'                 : {'val' : 10_000    , 'unit' : ['ft','m' ]},
            'Q'                     : {'val' : 1000      , 'unit' : ['BPD'    ]},
            'Pwf'                   : {'val' : 3000      , 'unit' : ['psi'    ]},
            'Pr'                    : {'val' : 5651      , 'unit' : ['psi'    ]},

            'Porosity'              : {'val' : 0.19      , 'unit' : ''        },
            'Permeability'          : {'val' : 8.2       , 'unit' : ['mD','D' ]},
            'h'                     : {'val' : 53        , 'unit' : ['ft','m' ]},
            'Pb'                    : {'val' : 3000      , 'unit' : ['psi'    ]},
            'Bo'                    : {'val' : 1.1       , 'unit' : ['bbl/STB']},
            'Viscosity'             : {'val' : 1.7       , 'unit' : ['cP'     ]},
            'Ct'                    : {'val' : 0.0000129 , 'unit' : ['psi^-1' ]},
            'Skin'                  : {'val' : 0         , 'unit' : ''         },
            'A'                     : {'val' : 640       , 'unit' : ['acres'  ]},
            're'                    : {'val' : 2980      , 'unit' : ['ft'     ]},
            'rw'                    : {'val' : 0.328     , 'unit' : ['ft'     ]}
                                }


        self.title("IPR")
        self.iconbitmap(
                r"C:\Users\windows 10\OneDrive\COREL (NOT ROCKET SCIENCE)\XO-CO\xoco-icon.ico"
                            )
        self.controller = Controller

        self.collect_entry = {}
        self.sub_collect_entry = {}

        self.gen_table_len = 10

        for_who = 'Isni'

        if for_who == 'Isni' :
            self.location_directory = r'C:\Users\windows 10\Documents\MY PYTHON NOTE\Phyton Tutorial'
        elif for_who == 'User' :
            self.location_directory = r"C:"

        #MAIN FRAME
        self.make_main_frame()
        self.make_label()

        #OUTER_FRM, ROW = :-1
        #FRM, COLUMN 0
        self.make_main_entry()
        self.unit_entry()

        #FRM2_table, under FRM2
        self.test_data_table()

        #OUTER_FRM, ROW = LAST
        self.entry_btn()


    def main(self):
        self.mainloop()


    def make_main_frame(self):
        self.main_frm = ttk.Frame(self)
        self.main_frm.grid(padx = self.PAD, pady = self.PAD, column = 0, row = 0)

        outer_label = ttk.Label(self.main_frm,
                            text = 'Production Analysis\n',
                                font = ('Calibri', 12, 'bold')
                                            )
        outer_label.pack()

        self.outer_frm = ttk.Frame(self.main_frm,
                                        borderwidth = 10,
                                            relief = 'groove'
                                                    )
        self.outer_frm.pack()

        #COLUMN 0 DI OUTER_FRM
        self.r_outer_frm = 0
        self.frm = ttk.Frame(self.outer_frm)
        self.frm.grid(column = 0,
                            row = self.r_outer_frm,
                                pady = 10,
                                    padx = 10
                                        )

        #COLUMN 1 DI OUTER_FRM
        self.c_outer_frm = 1
        self.frm2 = ttk.Frame(self.outer_frm, relief = 'ridge')
        self.frm2.grid(column = self.c_outer_frm,
                                row = 0,
                                    pady = 10,
                                        padx = 10,
                                            sticky = 'n'
                                                    )

        #FRM2 FOR TABEL, IN ROW 1
        self.r_frm2 = 0
        lbl_data_test = ttk.Label(self.frm2, text = 'DATA TEST')
        lbl_data_test.grid(column = 0,
                                    row = self.r_frm2,
                                        pady = 5,
                                            padx = 5
                                                )

        self.r_frm2 += 1
        self.frm2_table = ttk.Frame(self.frm2)
        self.frm2_table.grid(column = 0,
                                row = self.r_frm2,
                                    pady = 10,
                                        padx = 10
                                            )
        self.frm2_table.grid_rowconfigure(0, weight=1)
        self.frm2_table.grid_columnconfigure(0, weight=1)
        # Set grid_propagate to False to allow 5-by-5 buttons resizing later
        self.frm2_table.grid_propagate(False)

        self.r_frm2 += 1
        self.frm2_select_data = ttk.Frame(self.frm2, relief = 'solid')
        self.frm2_select_data.grid (column = 0,
                                        row = self.r_frm2,
                                            padx = 5,
                                                pady = 5,
                                                    ipady = 3,
                                                        ipadx = 5,
                                                    sticky = 'ew')


    def make_label(self):
        self.r_frm = 0
        for caption, sub_caption in self.entry_captions.items():
            #buat label
            self.label = ttk.Label(self.frm, text = caption+'\t')
            self.label.grid(column = 0,
                                row = self.r_frm,
                                    sticky = 'w')
            #buat :
            self.label = ttk.Label(self.frm, text = ':  ')
            self.label.grid(column = 1,
                                row = self.r_frm,
                                    sticky = 'w')
            self.r_frm += 1


    def make_main_entry(self):
        self.r_frm = 0
        for caption, sub_caption in self.entry_captions.items():
            self.entry = ttk.Entry(self.frm,
                                        textvariable = caption
                                                )
            self.entry.grid(column = 2,
                                row = self.r_frm
                                        )
            self.entry.insert(0, self.entry_captions[caption]['val'])

            #PUT VAL to DICT
            self.collect_entry[caption] = {} #IT HAS TO BE 2 STEPS WAYS DUE TO NESTED DICT
            self.collect_entry[caption]['val'] = self.entry

            '''
            self.sub_collect_entry['val'] = self.entry #INI BUAT NAMBAH isi dictionary KALO NON-NESTED DICT
            '''
            self.r_frm += 1


    def unit_entry(self):
        # combostyle = ttk.Style()
        # combostyle.theme_create('combostyle', parent='alt', settings = {'TCombobox':{'configure':{'selectbackground': 'Blue', 'relief': 'flat', 'fieldbackground': 'White','background': 'White'}}})
        # combostyle.theme_use('combostyle')

        self.r_frm = 0
        for caption, sub_caption in self.entry_captions.items():
            if self.entry_captions[caption]['unit'] == '' :
                self.unit_cbx = ttk.Combobox(self.frm,
                                    textvariable = 'unit_'+ caption,
                                        state = 'disabled',
                                            width = 7
                                                )
            else :
                self.unit_cbx = ttk.Combobox(self.frm,
                                    textvariable = str('unit_'+ caption),
                                        state = 'readonly',
                                            values = self.entry_captions[caption]['unit'],
                                                width = 7
                                                    )
                self.unit_cbx.current(0)
            self.unit_cbx.grid(column = 3,
                                    row = self.r_frm,
                                        sticky = 'ew',
                                            pady = 0.5,
                                                padx = 0.5
                                                    )

            #PUT UNIT into DICT
            self.collect_entry[caption]['unit'] = self.unit_cbx
            self.r_frm += 1


    def disable_ipr(self):
        frm_disable_ipr = ttk.Frame(self.inside_canvas)
        frm_disable_ipr.grid(column = 0, row = 0)

        table_data =   {
                        'Q' : [],
                        'Pwf' : []
                            }
        for n in range(0,self.gen_table_len) :
            for x in table_data.keys() :
                table_data[x].append('')

        s_dict = pf.make_table(self, frm_disable_ipr,
                                    table_data,
                                        number = True,
                                            entry_state = 'disabled'
                                                )


    def data_test(self):
        self.frm_data_test_ipr = ttk.Frame(self.inside_canvas)
        self.frm_data_test_ipr.grid(column = 0, row = 0)

        table_data =   {
                        'Q' : [],
                        'Pwf' : []
                            }

        for n in range(0,self.gen_table_len) :
            for x in table_data.keys() :
                table_data[x].append('')


        s_dict = pf.make_table(self, self.frm_data_test_ipr,
                                    table_data,
                                        number = True
                                            )


    def composite_ipr(self, *source_type):
        self.frm_composite_ipr = ttk.Frame(self.inside_canvas)
        self.frm_composite_ipr.grid(column = 0, row = 0)

        table_data = {}
        if len(source_type) == 0 : #empty
            #ORIGINALLY EMPTY
            table_data = {
                'Layer1' : {'Q' : [2000] , 'Pwf' : [3000] , 'Pr' : [4000], 'Pb' : [5000]},
                'Layer2' : {'Q' : [''] , 'Pwf' : [''] , 'Pr' : [''], 'Pb' : ['']},
                'Layer3' : {'Q' : [''] , 'Pwf' : [''] , 'Pr' : [''], 'Pb' : ['']}
                             }

        else : #JANGAN LUPA, *ARGS ITU TUPLE wkwkwk.. **KWARGS ITU DICT
            if source_type[0] == 1 : #from file
                lst = pd.DataFrame(self.file_read)

                side_name = 'Layer'

                head_for_row = {}
                for y in lst :
                    if y == side_name :
                        list_head = list(lst[y])
                        c = 0
                        for x in list_head :
                            if x not in head_for_row.keys() :
                                head_for_row[x] = [c]
                            else :
                                head_for_row[x].append(c)
                            c += 1
                    else :
                        pass

                for a in head_for_row.keys() :
                    table_data[a] = {}

                    for d in lst :
                        if d == side_name :
                            pass
                        else :
                            table_data[a][d] = []

                        for n in head_for_row[a] :
                            if d == side_name :
                                pass
                            else :
                                table_data[a][d].append(list(lst[d])[n])

            elif source_type[0] == 2 : #from add
                table_data = self.table_data_final_dict.copy()

            elif source_type[0] == 3 : #from del
                table_data = self.table_data_final_dict.copy()

            elif source_type[0] == 4 : #from head_sync
                table_data = self.table_data_final_dict.copy()

        #15 rows table
        c = 0
        for x in table_data.keys() :
            for y in list(table_data[x].values())[0] :
                c += 1

        if c < self.gen_table_len :
            for n in range(0, self.gen_table_len) :
                if '' not in list(table_data.keys()) :
                    table_data[''] = {}
                else :
                    pass

                for y in table_data[list(table_data.keys())[0]].keys() :
                    if y not in list(table_data[''].keys()) :
                        table_data[''][y] = ['']
                    else :
                        table_data[''][y].append('')

                c = 0
                for x in table_data.keys() :
                    for y in list(table_data[x].values())[0] :
                        c += 1

                if c >= self.gen_table_len :
                    break
                else :
                    pass
            btn_state = 'disabled'
        else :
            if c == self.gen_table_len :
                btn_state = 'disabled'
            else :
                btn_state = 'normal'


        r, self.table_data_entry = pf.make_table(self, self.frm_composite_ipr,
                                            table_data,
                                                number = False,
                                                    get_last_row = True)

        self.table_data_final_dict = self.table_data_entry.copy()

        nested_key = list(self.table_data_final_dict[(
                     list(self.table_data_final_dict.keys())[0])].keys())

        #ADD_COLUMN_BUTTON
        identity = 3
        r_last = r
        add_row_button = ttk.Button(self.frm_composite_ipr,
                                text = '+',
                                        command = lambda : self.add_row_table(identity)
                                            )
        add_row_button.grid(column = 1, row = r_last,
                                columnspan = len(nested_key),
                                    sticky = 'ew'
                                            )

        del_row_button = ttk.Button(self.frm_composite_ipr,
                                text = '-',
                                    width = 3,
                                        command = lambda : self.del_row_table(identity),
                                            state = btn_state
                                                )
        del_row_button.grid(column = 0,
                                row = r_last,
                                    sticky = 'ew'
                                        )


    def fetkovich_two_phase(self, *source_type):
        self.inside_inside_canvas1 = ttk.Frame(self.inside_canvas)
        self.inside_inside_canvas1.grid(column = 0, row = 0)

        table_data = {}
        if len(source_type) == 0 : #empty
            #ORIGINALLY EMPTY
            table_data =        {
                           'Q'      : [ '','',''],
                           'Pwf'    : [ '','','']
                                }

        else : #JANGAN LUPA, *ARGS ITU TUPLE wkwkwk.. **KWARGS ITU DICT
            if source_type[0] == 1 : #from file
            #INPUT DATA TRUE
                #GET THE DATA
                lst = pd.DataFrame(self.file_read)

                #STORE AS DICT IN HEAD
                list_head = list(lst.columns.values)

                for x in list_head :
                    table_data[x] = list(lst[x])

            elif source_type[0] == 2 : #from add
                table_data = self.table_data_final_dict.copy()

            elif source_type[0] == 3 : #from del
                table_data = self.table_data_final_dict.copy()

            elif source_type[0] == 4 : #from head_sync
                table_data = self.table_data_final_dict.copy()

        if len(list(table_data.values())[0]) < self.gen_table_len :
            for n in range (0, self.gen_table_len) :
                for x in table_data.keys() :
                    table_data[x].append('')

                if len(list(table_data.values())[0]) >= self.gen_table_len :
                    break
                else :
                    pass
            btn_state = 'disabled'
        else :
            if len(list(table_data.values())[0]) == self.gen_table_len :
                btn_state = 'disabled'
            else :
                btn_state = 'normal'

        r , self.table_data_final_dict = pf.make_table(self,
                                            self.inside_inside_canvas1,
                                                table_data,
                                                    number = True,
                                                        get_last_row = True
                                                            )

        #ADD_COLUMN_BUTTON
        identity = 1
        r_last = r
        add_row_button = ttk.Button(self.inside_inside_canvas1,
                                text = '+',
                                    command = lambda : self.add_row_table(identity)
                                            )
        add_row_button.grid(column = 1, row = r_last,
                            columnspan = len(list(self.table_data_final_dict.keys())),
                                    sticky = 'ew'
                                            )

        del_row_button = ttk.Button(self.inside_inside_canvas1,
                                text = '-',
                                    width = 3,
                                        command = lambda : self.del_row_table(identity),
                                            state = btn_state
                                                )
        del_row_button.grid(column = 0, row = r_last, sticky = 'ew')


    def ipr_handler(self, event) :
        self.file_exist = False
        #self.input_data_entry.set(str(self.file))

        for widget in self.inside_canvas.winfo_children():
            widget.destroy()

        current = self.two_phase_ipr.get()

        if current      == 'Vogel - Two Phase' :
            self.disable_ipr()
        elif current    == 'Fetkovich - Two Phase' :
            self.fetkovich_two_phase()
        elif current    == 'Vogel - Partial Two Phase' :
            self.disable_ipr()
        elif current    == 'Single Phase' :
            self.disable_ipr()
        elif current    == 'Data Test' :
            self.data_test()
        elif current    == 'Composite IPR' :
            self.composite_ipr()

        #TEMPLATE DATA
        self.select_data_test()
        self.head_sync()
        self.reverse_head()
        self.layer_grouping()

        #FOR POPUP WINDOWS
        self.popup_windows_initiation()


    def popup_windows_initiation(self) :
        if self.two_phase_ipr.get() == 'Composite IPR' :
            s_dict = {}
            for x in range(0, 5) :
                s_dict[f'A{x}'] = {}
                s_dict[f'A{x}']['Q'] = [1,2,3,4,5]
                s_dict[f'A{x}']['Pwf'] = [1,2,3,4,5]
            
            self.app_dict = s_dict.copy()

            self.app = Windows_PopUp('Group Layer', self.app_dict)
            self.app.withdraw()
        
        else :
            pass


    def add_row_table(self, source):
        if source == 1 : #Fetkovich - Two Phase
            s_test = pf.extract_table(self, self.table_data_final_dict)

            for n in s_test.keys():
                s_test[n].append('')

        elif source == 2 : #Data Test
            pass

        elif source == 3 : #Composite IPR
            s_test = pf.extract_table(self,
                                self.table_data_final_dict,
                                    nested_dict = True
                                        )

            if '' not in list(s_test.keys()) :
                s_test[''] = {}
            else :
                pass

            for y in s_test[list(s_test.keys())[0]].keys() :
                if y not in list(s_test[''].keys()) :
                    s_test[''][y] = ['']
                else :
                    s_test[''][y].append('')

        self.table_data_final_dict = s_test.copy()
        self.file_sync(2)


    def del_row_table(self, source):

        if source == 1 : #Fetkovich - Two Phase
            s_test = pf.extract_table(self, self.table_data_final_dict)

            if len(list(s_test.values())[0]) <= 1 :
                m_box.showwarning('¯\_(ツ)_/¯',
                                'You are running out of row.'
                                        )
            else :
                for n in s_test.keys():
                    del s_test[n][-1]

                self.table_data_final_dict = s_test.copy()

                self.file_sync(3)

        elif source == 2 : #Data Test
            pass

        elif source == 3 : #Composite IPR
            s_test = pf.extract_table(self,
                                        self.table_data_final_dict,
                                            nested_dict = True
                                                )

            if len(list(s_test.keys())) <= 1 :
                m_box.showwarning('¯\_(ツ)_/¯',
                                'You are running out of row.'
                                        )
            else :
                last_key = list(s_test.keys())[-1]
                sub_last_key = list(s_test[last_key].keys())[0]

                if len(s_test[last_key][sub_last_key]) > 1 :
                    for n in s_test[last_key].keys() :
                        del s_test[last_key][n][-1]
                else :
                    del s_test[last_key]

                self.table_data_final_dict = s_test.copy()
                self.file_sync(3)


    def test_data_table(self, **kwargs):
        self.two_phase_ipr = tk.StringVar()

        self.r_frm += 1

        ipr_choice =  [
                        'Vogel - Two Phase',
                        'Fetkovich - Two Phase',
                        'Vogel - Partial Two Phase',
                        'Single Phase',
                        'Composite IPR'
                                ]

        #                        'Data Test', #WAITTTT

        blank_lbl1 = ttk.Label(self.frm, text = '')
        blank_lbl1.grid(column = 0,
                                row = self.r_frm,
                                    columnspan = 4
                                            )

        self.r_frm += 1
        ipr_label = ttk.Label(self.frm, text = 'IPR')
        ipr_label.grid(column = 0,
                                row = self.r_frm,
                                    columnspan = 2,
                                        sticky = 'e'
                                            )


        #CREATE FRAME + SCROLLBAR
                    #super specific frame
        self.table_canvas = tk.Canvas(self.frm2_table)
        self.table_canvas.grid(column = 0,
                                    row = 0,
                                        sticky = 'nsew')

                    #create scroll bar
        hor = ttk.Scrollbar(self.frm2_table,
                                orient = 'horizontal',
                                    command = self.table_canvas.xview
                                            )
        hor.grid(column = 0, row=1, sticky = 'ew')

        ver = ttk.Scrollbar(self.frm2_table,
                                orient = 'vertical',
                                    command = self.table_canvas.yview
                                            )
        ver.grid(column = 1, row = 0, sticky = 'ns')

            #create frame inside canvas to be converted into create_window,
            #instead of using grid/pack, it is supposed to use create_window
        self.inside_canvas = ttk.Frame(self.table_canvas)
        self.inside_canvas.bind("<Configure>",
                            lambda e: self.table_canvas.configure(
                                scrollregion = self.table_canvas.bbox("all")
                                )
                            )
            #create a create_window to allow the widgets(button,lbl, frm, etc) become canvas widgets
        self.table_canvas.create_window((0, 0), window=self.inside_canvas, anchor="nw")
        self.table_canvas.configure( yscrollcommand = ver.set,
                                        xscrollcommand = hor.set
                                            )


        #UPDATE BUTTONS FRAMES IDLETASKS TO LET TKINTER CALCULATE BUTTONS SIZES
        self.frm2_table.update_idletasks()
        self.frm2_table.config ( width = 267 + ver.winfo_width(),
                                    height = 220
                                        ) #set table visible size (ori : 265 x 130)

        self.twophase_cbx = ttk.Combobox(self.frm,
                                textvariable = self.two_phase_ipr,
                                    state = 'readonly',
                                        width = 7,
                                            values = ipr_choice
                                                )
        self.twophase_cbx.current(0)
        self.twophase_cbx.bind('<<ComboboxSelected>>',
                                    self.ipr_handler
                                        )
        self.twophase_cbx.grid(column = 2,
                                    row = self.r_frm,
                                        columnspan = 2,
                                            sticky = 'ew'
                                                )

        #just for initial state
        self.disable_ipr()
        self.select_data_test()
        self.head_sync()
        self.reverse_head()
        self.layer_grouping()


    def select_data_test(self) :
        self.input_data_entry = tk.StringVar()

        ipr_state = self.two_phase_ipr.get()

        for widget in self.frm2_select_data.winfo_children() :
            widget.destroy()

        type_ipr = (
                    'Fetkovich - Two Phase',
                    'Data Test',
                    'Composite IPR'
                        )

        if  any(ipr_state ==  i for i in type_ipr) :
            state_btn = 'normal'
        else :
            state_btn = 'disabled'

        #select data btn for input data test
        select_data_btn = ttk.Button(self.frm2_select_data,
                                    text = 'Input\nData',
                                        state = state_btn,
                                            width = 8,
                                                command = lambda : self.file_opener()
                                                        )
        select_data_btn.grid(row = 2 ,  rowspan = 4, column = 5, sticky = 'nsew')


    def file_opener(self) :
        ipr_state = self.two_phase_ipr.get()

        try :
            self.file = filedialog.askopenfilename(
                initialdir = self.location_directory,
                    filetypes = [('Excel Files', '*.xlsx')]
                        )

        except(OSError,FileNotFoundError):
            m_box.showwarning (
                            '¯\_(ツ)_/¯',
                            "READ !!\nYou haven't entered any files !"
                                    )
            self.file = ''

        except Exception as error :
            m_box.showwarning('¯\_(ツ)_/¯',
                              'ERRORRRR...\nmianhamnida yeorobun !'
                                    )

        if self.file != '' :
            self.file_read          = pd.read_excel(self.file)

            if ipr_state == 'Composite IPR' :
                data_head      = list(self.file_read.columns)
                if 'Layer' in data_head     or(
                    'layer' in data_head    ) :

                    data_head.remove('Layer')
                else :
                    del data_head[0]
            else :
                data_head = list(self.file_read.columns)

            self.selected_data_head = data_head

            self.file_exist         = True

            self.file_sync(1)
            self.reverse_head(file = True)
            self.head_sync(file = True)
        else :
            pass


    def layer_grouping(self) :
        ipr_state = self.two_phase_ipr.get()

        if ipr_state == 'Composite IPR' :
            btn_state = 'normal'

        else :
            btn_state = 'disabled'

        layer_group          =  ttk.Button(self.frm2_select_data,
                                                    state = btn_state,
                                                        width = 8,
                                                            text = 'Layer\nGroup'
                                                                    )
        layer_group.bind(       "<Button>", lambda e : self.group_layer_extension('show'))

        layer_group.grid(       row = 2 ,  rowspan = 4, column = 3, sticky = 'nsew', padx = 3)


    def group_layer_extension(self, cmd) :
        c_dict = pf.extract_table(self, self.table_data_final_dict,
                                                nested_dict = True
                                                        )
        b = []
        for x in c_dict.keys() :
            y = str(x)
            if y.strip() == '' :
                b.append(x)

        for z in b :
            del c_dict[z]

        a = list(c_dict.keys())
        b = list(self.app_dict.keys())

        update = False
        if len(a) == len(b) :
            for x in range(0, len(a)) :
                a_x = a[x]
                b_x = b[x]

                if a_x != b_x :
                    update = True
                    break
                else :
                    pass
        else :
            update = True
        
        if update == True :
            for widget in self.app.master_popup.winfo_children():
                widget.destroy()

            self.collect_LG, self.collect_LG_cb, self.collect_LG_var = self.app.main_function(c_dict)
            self.app_dict = c_dict.copy()

        if cmd == 'show' :
            self.app.deiconify()
        else :
            pass


    def reverse_head(self, file = False) :
        self.reverse_head_state = tk.IntVar()
        ipr_state = self.two_phase_ipr.get()

        if file == True :

            if      ipr_state    == 'Fetkovich - Two Phase' :
                cb_val              = 'disabled'
            elif    ipr_state   == 'Composite IPR'          :
                cb_val              = 'normal'
        elif file == False :
            cb_val              = 'disabled'

        reverse_frame           = ttk.Frame(self.frm2_select_data)
        reverse_frame.grid(         column      = 0,
                                    row         = 0,
                                    columnspan  = 4,
                                    pady        = 1,
                                    padx        = 1,
                                    sticky      = 'ew')

        self.reverse_btn       = ttk.Checkbutton(reverse_frame,
                                    variable    = self.reverse_head_state,
                                    onvalue     = 1,
                                    offvalue    = 0,
                                    state       = cb_val   )
        self.reverse_btn.bind(     "<Button-1>",
                                    lambda event: self.head_sync_handler(event, 'reverse')
                                                        )

        self.reverse_btn.grid(     column      = 0,
                                    row         = 0,

                                    pady        = 1,
                                    padx        = 1,
                                    sticky      = 'w'     )

        reverse_head_lbl        = ttk.Label(reverse_frame,
                                    text        = 'Reverse Data Head'    )

        reverse_head_lbl.grid(      column      = 1,
                                    row         = 0,
                                    columnspan  = 3,

                                    pady        = 1,
                                    sticky      = 'ew'  )

    def head_sync(self, file = False, reverse = False) :
        self.Q_sync_head    = tk.StringVar()
        self.pwf_sync_head  = tk.StringVar()
        self.pr_sync_head   = tk.StringVar()
        self.pb_sync_head   = tk.StringVar()

        if file == True :
            if reverse == False :
                btn_on = self.selected_data_head
            elif reverse == True :
                btn_on = self.reverse_file_head
        else :
            pass

        if file == True :
            ipr_state = self.two_phase_ipr.get()
            if      ipr_state    == 'Fetkovich - Two Phase' :
                Q_btn_state         = 'readonly'
                pwf_btn_state       = 'readonly'
                pr_btn_state        = 'disabled'
                pb_btn_state        = 'disabled'

                btn_val             = self.selected_data_head

            elif    ipr_state   == 'Composite IPR'          :
                Q_btn_state         = 'readonly'
                pwf_btn_state       = 'readonly'
                pr_btn_state        = 'readonly'
                pb_btn_state        = 'readonly'

                btn_val             = btn_on

        elif file == False :
            Q_btn_state         = 'disabled'
            pwf_btn_state       = 'disabled'
            pr_btn_state        = 'disabled'
            pb_btn_state        = 'disabled'

            btn_val             = ('','','')


        empty_lbl_for_fun       = ttk.Label(self.frm2_select_data,
                                    text        = '     ')
        empty_lbl_for_fun.grid(     column      = 2,
                                    row         = 1,
                                    rowspan     = 6)

        #HEAD SYNC PROPERTIES
        frame = self.frm2_select_data
        title_sync_lbl          = ttk.Label(frame,
                                    text        = '*reference data head :')
        title_sync_lbl.grid(        column      = 0,
                                    row         = 1,
                                    columnspan  = 2,
                                    padx        = 1,
                                    sticky      = 'ew'  )

        items = ['Q', 'Pwf', 'Pr', 'Pb']
        row = 2
        for x in items :
            head_label          = ttk.Label(frame,
                                    text        = x)
            head_label.grid(        column      = 0,
                                    row         = row,
                                    padx        = 1,
                                    sticky      = 'ew'  )
            row += 1

        #------head of Q------
        self.Q_sync_btn         = ttk.Combobox(frame,
                                    state       = Q_btn_state,
                                    textvariable= self.Q_sync_head ,
                                    values      = btn_val,
                                    width       = 7     )
        self.Q_sync_btn.current(0)
        self.Q_sync_btn.bind(       '<<ComboboxSelected>>',
                                    lambda event : self.head_sync_handler(event, 1)
                                                        )
        self.Q_sync_btn.grid(       column      = 1,
                                    row         = 2,
                                    sticky      = 'ew'  )

        #------head of Pwf------
        self.pwf_sync_btn       = ttk.Combobox(frame,
                                    state       = pwf_btn_state,
                                    textvariable= self.pwf_sync_head,
                                    values      = btn_val,
                                    width       = 7     )
        self.pwf_sync_btn.current(0)
        self.pwf_sync_btn.bind(     '<<ComboboxSelected>>',
                                    lambda event: self.head_sync_handler(event, 2)
                                                        )
        self.pwf_sync_btn.grid(     column      = 1,
                                    row         = 3,
                                    sticky      = 'ew'  )

        #------head of Pr------
        self.pr_sync_btn       = ttk.Combobox(frame,
                                    state       = pr_btn_state,
                                    textvariable= self.pr_sync_head,
                                    values      = btn_val,
                                    width       = 7     )
        self.pr_sync_btn.current(0)
        self.pr_sync_btn.bind(     '<<ComboboxSelected>>',
                                    lambda event: self.head_sync_handler(event, 3)
                                                        )
        self.pr_sync_btn.grid(      column      = 1,
                                    row         = 4,
                                    sticky      = 'ew'  )

        #------head of Pb------
        self.pb_sync_btn       = ttk.Combobox(frame,
                                    state       = pb_btn_state,
                                    textvariable= self.pb_sync_head,
                                    values      = btn_val,
                                    width       = 7     )
        self.pb_sync_btn.current(0)
        self.pb_sync_btn.bind(     '<<ComboboxSelected>>',
                                    lambda event: self.head_sync_handler(event, 4)
                                                        )
        self.pb_sync_btn.grid(      column      = 1,
                                    row         = 5,
                                    sticky      = 'ew'  )



    def head_sync_handler(self, event, *source):
        ipr_state = self.two_phase_ipr.get()

        Q_head      = self.Q_sync_head.get()
        pwf_head    = self.pwf_sync_head.get()
        pr_head     = self.pr_sync_head.get()
        pb_head     = self.pb_sync_head.get()

        if ipr_state == 'Fetkovich - Two Phase' :
            current_dict = pf.extract_table(self, self.table_data_final_dict,
                                                nested_dict = False
                                                        )
            if source[0] == 1 :
                sync_dict = pf.head_reorder(self, current_dict, Q_head, nested_dict = False)
            elif source[0] == 2 :
                sync_dict = pf.head_reorder(self, current_dict, pwf_head, nested_dict = False)

        elif ipr_state == 'Composite IPR' :
            current_dict = pf.extract_table(self, self.table_data_final_dict,
                                                nested_dict = True
                                                        )
            if  source[0] == 1 :
                sync_dict = pf.head_reorder(self,current_dict, Q_head  , nested_dict = True)
            elif source[0] == 2 :
                sync_dict = pf.head_reorder(self,current_dict, pwf_head, nested_dict = True)
            elif source[0] == 3 :
                sync_dict = pf.head_reorder(self,current_dict, pr_head , nested_dict = True)
            elif source[0] == 4 :
                sync_dict = pf.head_reorder(self,current_dict, pb_head , nested_dict = True)
            elif source[0] == 'reverse' :
                check_state = self.reverse_head_state.get()
                if check_state ==   0 :
                    sync_dict = pf.reverse_head(self, current_dict)
                elif check_state == 1 :
                    sync_dict = pf.reverse_head(self, current_dict)

        else :
            pass

        if source[0] == 'reverse' :
            more_than_two = []
            for x in sync_dict.keys() :
                for y in sync_dict[x].keys() :
                    val = 0
                    for z in sync_dict[x][y] :
                        val += 1

                    if val > 1 :
                        more_than_two.append(f'{x}_{y}')
                    else :
                        pass
            if len(more_than_two) > 0 :
                m_box.showwarning ( '¯\_(ツ)_/¯',
                                "Mianhamnida !!\nTo reverse head, please make sure that all of your head have a different name !"
                                        )
            else :
                self.table_data_final_dict = sync_dict.copy()
                self.file_sync(4)

                head_00 = list(self.table_data_final_dict.keys())[0]
                self.reverse_file_head = []
                for x in self.table_data_final_dict[head_00].keys() :
                    self.reverse_file_head.append(x)

                self.head_sync(file = True, reverse = True)

        else :
            self.table_data_final_dict = sync_dict.copy()
            self.file_sync(4)


    def file_sync(self, command) :
        for widget in self.inside_canvas.winfo_children():
            widget.destroy()

        if command == 1 : #read_file
            cmd = 1
        elif command == 2 : #add
            cmd = 2
        elif command == 3 : #del
            cmd = 3
        else : #head_sync
            cmd = 4

        current = self.two_phase_ipr.get()

        if current == 'Fetkovich - Two Phase' :
            self.fetkovich_two_phase(cmd)
        elif current == 'Data Test' :
            self.data_test(cmd)
        elif current == 'Composite IPR' :
            self.composite_ipr(cmd)


    def entry_btn(self):
        self.r_outer_frm += 1
        btn = ttk.Button(self.outer_frm,
                        text = 'Enter',
                            command = lambda : self.controller.enter_click(self)
                                )
        btn.grid(column = 0, row = self.r_outer_frm, sticky = 'e', pady = 10)


class Windows_PopUp(tk.Tk) :
    def __init__(self, title, data_dict) :
        super().__init__()
        self.title(title)
        self.overrideredirect(True)

        self.sub_master_frame()
        layer, cb, var = self.main_function(data_dict)

    def sub_master_frame(self) :
        self.master_popup       = ttk.Frame(self)
        self.master_popup.pack()


    def done_cmd(self) :
        self.withdraw()


    def main_function(self, data_dict) :
        self.main_func_frame    = ttk.Frame(self.master_popup)
        self.main_func_frame.pack()

        frame = self.main_func_frame

        list_layer = []

        layer_count = 0
        for x in data_dict.keys():
            layer_count += 1
            list_layer.append(x)

        cb_group = {}
        var_group = {}

        col = 0
        row = 0

        row_cb = 1
        for i in range(1, layer_count+1) :
            unify_layer = ttk.Button(frame, state = 'disabled', text = f'Layer Group {i}')
            unify_layer.grid(column = col, row = row, columnspan = 2)

            key = f'Group_{i}'

            cb_group[key] = []
            var_group[key] = []

            for j in list_layer :
                i_var = tk.BooleanVar()

                cb_layer = ttk.Checkbutton(frame, text = f'Layer {j}', textvariable = i_var)
                cb_layer.grid(column = col, row = row_cb)

                # if row_cb == 1 :
                #     i_var.set(True)
                # else :
                #     i_var.set(False)

                cb_layer_text = ttk.Label(frame, text = f'{j}')
                cb_layer_text.grid(column = (col+1), row = row_cb, sticky = 'ew')

                cb_group[key].append(cb_layer)
                var_group[key].append(i_var)

                row_cb += 1

            row_cb = 1
            col += 2

        self.done_btn           = ttk.Button(self.master_popup, text = 'DONE', command = self.done_cmd)
        self.done_btn.pack()

        return list_layer, cb_group, var_group



class Plot_PopUp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title ('Plot')
        self.main_frame()

        for_who = 'Isni'

        if for_who == 'Isni' :
            self.location_directory = r'C:\Users\windows 10\Documents\MY PYTHON NOTE\Phyton Tutorial'
        elif for_who == 'User' :
            self.location_directory = r"C:"

    def main_frame(self):
        self.main_frm2      =   ttk.Frame(self  )
        self.main_frm2.grid(    padx    = 10,
                                pady    = 10,
                                column  = 0,
                                row     = 0     )

    def multiple_plot_show(self, plot_x, plot_y, well_name, s_dict, one_pack = False) :
        data = 0
        for x in s_dict.keys() :
            data  += 1

        data_loop = ''
        if one_pack == True :
            data_loop = 1
            max_data = data

        else :
            max_data = 9 #COMBINATION MAX_DATA vs MAX_COL = MAX GRID
            loop = data/max_data

            if loop > 1 :
                for n in str(loop) :
                    if n == '.' :
                        break
                    else :
                        data_loop = int(f'{data_loop}{n}')
                data_loop = data_loop + 1
            else :
                data_loop = 1

        start = 0
        end = max_data

        for z in range(0, data_loop) :
            s = {}
            for x in range(start, end) :
                try :
                    y = list(s_dict.keys())[x]
                    s[y] = s_dict[y].copy()
                except IndexError :
                    pass

            if one_pack == False :
                if data_loop == 1 :
                    self.execute_multiple_plot_show(plot_x, plot_y, well_name, s)
                elif data_loop > 1 :
                    PopUp().execute_multiple_plot_show(plot_x, plot_y, well_name, s)
            elif one_pack == True :
                self.execute_multiple_plot_show(plot_x, plot_y, well_name, s, one_pack = True)

            start = end
            end += max_data

    def execute_multiple_plot_show(self, plot_x, plot_y, well_name, s_dict, one_pack = False) :
        submain_frm = ttk.Frame(self.main_frm2)
        submain_frm.pack()

        data = 0
        for x in s_dict.keys() :
            data  += 1

        max_col = 3 #COMBINATION MAX_DATA vs MAX_COL = MAX GRID
        for j in range(1, 100) : #max only for 30 layer --> if not (plot will be so bad looking)
            if j*3 >= data : #3 is max row
                if j <= max_col :
                    l = max_col #max normal length of column
                else :
                    l = j #length of column (it can be more than 3)
                break

            else :
                continue

        empty_plot = []
        row = ''
        mul = data/l
        if mul > 1 :
            for n in str(mul) :
                if n == '.' :
                    break
                else :
                    row = int(f'{row}{n}')
                    col = l
            row = row+1
        else :
            row = 1
            col = data

        if one_pack == True :
            row = 1
            col = 1
        else :
            pass

        my_dpi = 80
        fig, axes = plt.subplots(   nrows   = row,
                                    ncols   = col,
                                    figsize = (14,7),
                                    dpi     = my_dpi
                                            )
        #title of entire fig
        fig.suptitle(well_name, fontsize = 15)

        comp_xmin = 0
        comp_xmax = 0
        comp_ymin = 0
        comp_ymax = 0

        c = 0
        r = 0
        for x in s_dict.keys() :
            layer_name = x
            for y in s_dict[x].keys() :
                if y == plot_x :
                    arg1 = s_dict[x][y]
                elif y == plot_y :
                    arg2 = s_dict[x][y]

            if one_pack == False :
                x_min = np.amin(arg1)
                x_max = np.amax(arg1)

                y_min = np.amin(arg2)
                y_max = np.amax(arg2)

            elif one_pack == True :
                for i in arg1 :
                    if i <= comp_xmin :
                        comp_xmin = i
                    if i >= comp_xmax :
                        comp_xmax = i

                for k in arg2 :
                    if k <= comp_ymin :
                        comp_ymin = k
                    if k >= comp_ymax :
                        comp_ymax = k

                x_min = comp_xmin
                x_max = comp_xmax

                y_min = comp_ymin
                y_max = comp_ymax

                x_split = x.split('\n') #AFTER SPLIT --> LIST
                x = x_split[0]

                layer_name = 'Composite IPR'

            x_lbl = f'{plot_x} (bbl/day)'
            y_lbl = f'{plot_y} (psi)'

            try :
                axes[r,c].plot(arg1, arg2) #more than 1 row
                axes[r,c].set_title (layer_name, fontsize = 10)
                axes[r,c].set_xlabel(x_lbl, fontsize = 7)
                axes[r,c].set_ylabel(y_lbl, fontsize = 7)
                axes[r,c].grid(True)

                axes[r,c].set_xlim(x_min, x_max)
                axes[r,c].set_ylim(y_min, y_max)

            except IndexError : #1 row
                axes[c].plot(arg1, arg2)
                axes[c].set_title (layer_name, fontsize = 10)
                axes[c].set_xlabel(x_lbl, fontsize = 7)
                axes[c].set_ylabel(y_lbl, fontsize = 7)
                axes[c].grid(True)

                axes[c].set_xlim(x_min, x_max)
                axes[c].set_ylim(y_min, y_max)

            except TypeError : #AxesSubPlot obj isnot subscriptable #1 obj, no row/no col
                axes.plot(arg1, arg2, label = x)
                axes.set_title (layer_name, fontsize = 12)
                axes.set_xlabel(x_lbl, fontsize = 10)
                axes.set_ylabel(y_lbl, fontsize = 10)
                axes.grid(True)
                axes.legend(loc = 'upper right')

                axes.set_xlim(x_min, x_max)
                axes.set_ylim(y_min, y_max)

            c += 1
            if c == l :
                r += 1
                c = 0
            else :
                pass

        #check empty plot and remove
        r = 0
        c = 0
        dt = 1
        for x in range(0, row*col) :
            if dt > data :
                try :
                    axes[r,c].set_axis_off()
                except IndexError :
                    axes[c].set_axis_off()
                except TypeError :
                    axes.set_axis_off()
            else :
                pass

            c += 1
            if c == l :
                r += 1
                c = 0
            else :
                pass

            dt += 1

        fig.tight_layout()

        figCanvas = FigureCanvasTkAgg(fig, master = submain_frm)
        figCanvas.get_tk_widget().pack(pady = 5, padx = 5)
        figCanvas.draw()

        btn_frame = ttk.Frame(submain_frm)
        btn_frame.pack()

        dwld_img = ttk.Button(btn_frame,
                            text    = 'Export Image',
                            command = lambda : self.download_comp(
                                                                s_dict,
                                                                source  = 1,
                                                                fig     = fig)
                                            )
        dwld_img.pack(side = 'left')

        dwld_tbl = ttk.Button(btn_frame,
                                text    = 'Export Table',
                                command = lambda : self.download_comp(
                                                                    s_dict,
                                                                    source  = 2)
                                            )
        dwld_tbl.pack(side = 'left')

    def download_comp(self, s_dict, source, fig = None) :
        # try :
        if source == 1 :
            d = '.jpg'
            ftype = [('JPEG', ('*.jpg', '*jpeg' ))]

        elif source == 2 :
            d = '.xlsx'
            ftype = [('Excel Files', '*.xlsx'), ('All files', '*.*')]


        file = filedialog.asksaveasfilename(
                        initialdir          = self.location_directory,
                        defaultextension    = d,
                        filetypes           = ftype
                                            )

        if not file :
            pass

        else :
            if source == 1 :
                fig.savefig(file)

            elif source == 2 :
                writer = pd.ExcelWriter(file)

                for s in s_dict.keys() :
                    sn = s.split('\n')
                    s_name = sn[0]
                    for y in s_dict[s].keys() :
                        if y == 'Q' :
                            arg1 = s_dict[s][y]
                        elif y == 'Pwf' :
                            arg2 = s_dict[s][y]

                    data = {'Q'     : arg1,
                            'Pwf'   : arg2}

                    df = pd.DataFrame(data)
                    try :
                        df.to_excel(writer,
                                    index       = False,
                                    sheet_name  = s_name
                                            )
                    except ValueError :
                        df.to_excel(writer,
                                    index       = False,
                                    sheet_name  = f'copy_{s_name}'
                                            )

                writer.save()


if __name__ == '__main__':
    controller = Controller()
    controller.main()
