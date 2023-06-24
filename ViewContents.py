from  lcd1602 import LCD
import machine
import time


# items = ['出勤', '外出', '帰着', '退勤']


class lcdControl(LCD):
    def __init__(self):
        super().__init__()
        
        self.KEY_SELECT = machine.Pin(8)
        self.KEY_ENTER = machine.Pin(9)
        self._msg = ''
        
    def update(self,PageModel):
        if self.message != PageModel['ShowContents']['text']:
            self.message = PageModel['ShowContents']['text']
        else:
            self.message = self._msg
        
    @property
    def message(self):
        return self._msg
        
    @message.setter
    def message(self, text):
        self.clear()
        super().message(text)
        self._msg = text
        
    def Clicked_Select(self):
        pass
        
    def Clicked_Enter(self):
        pass


class view_contents():
    # horizontal displays viewer
    class select_item_card():
        def __init__(self, source, max_length=-1, before_dot=True):
            self.source = source
            self._slctd = False
            self._before_dot = bool(before_dot)
            if max_length >= 1:
                self._max_len = int(max_length)
            else:
                self._max_len = 1
            self._txt = self.__ftext(self.source, self._max_len, self._before_dot)
            
        def __str__(self):
            return (self._txt, self.sourse, self._slctd)
            
        def __ftext(self, t, ln, bf_d):
            ln -= 1
            
            if self._slctd:
                t = ' o' + t
            else:
                if bf_d:
                    t = ' -' + t
                else:
                    t = '  ' + t
            if isinstance(t, str):
                if len(t) > ln:
                    if ln >= 1:
                        if len(t) >= 1:
                            rtn = t[:ln] + '_'
                        else:
                            rtn = t[:2]
                    else:
                        rtn = t
                else:
                    rtn = t
                    
            else:
                raise TypeError(f't is not type of strings.\n "{t}"')
            return rtn
            
        @property
        def text(self):
            self._txt = self.__ftext(self.source, self._max_len, self._before_dot)
            return self._txt
            
        @property
        def selected(self):
            return self._slctd
            
        @selected.setter
        def selected(self, _bol):
            self._slctd = bool(_bol)
            
    class num_counter_card():
        end_behavior_modelist =('cut', 'round')
        
        def __init__(self, def_num=0,start_num=None, end_num=None, end_behavior='cut'):
            if start_num == None:
                self.start_num = def_num
            else:
                self.start_num = start_num
            
            self.end_num = end_num
            self.end_behavior = end_behavior
            if isinstance(def_num, (int, float)):
                self.def_num = int(def_num)
            self._cnt = self.def_num
            
        @property
        def counter(self):
            return self._cnt
            
        @counter.setter
        def counter(self, cnt):
            if isinstance(cnt, int):
                self._cnt += cnt
                if self.end_behavior == 'cut':
                    if self._cnt >= self.end_num:
                        self._cnt = self.end_num
                elif self.end_behavior == 'round':
                    self._cnt = self._cnt % self.end_num
                else:
                    raise ValueError(f'end_behavior only set in {num_counter_card.end_behavior_modelist}')
            else:
                raise TypeError(f'An {type(cnt)} value was passed to count')
            
        @property
        def text(self):
            _txt = str(self.counter)
            return _txt
    
    _type_list = ['list', 'dict']
    
    def __init__(self, content, spliter=' ', title=''):
        self.spliter = spliter
        self.sel_obj = []
        self.cnt_obj = {}
        self.title = title
        self.__contents = content
        self._obj_grps = {}
        self._text = ''
        self.modal = False
        self.mode = None
        self._max_len = 16
        self.max_row = 2
        self.type = view_contents._type_list[0]
        
    def __str__(self):
        return str(self._content)
        
    @property
    def max_len(self):
        return self._max_len
        
    @max_len.setter
    def max_len(self, max_len):
        self.modal = False
        self._max_len = max_len
        
    @property
    def __contents(self):
        return self._content
        
    @__contents.setter
    def __contents(self, cont):
        if isinstance(cont, (list, tuple)):
            self._content = cont
        elif isinstance(cont, str) and self.spliter != '':
            self._content = cont.split(self.spliter)
        else:
            self._content = str(cont)
        
    @property
    def select_objects(self):
        if self.mode == 3 or self.mode == 4 or self.mode == 5:
            return self.sel_obj
        else:
            raise TypeError('please set mode-(3, 4, 5) before acsess to select_objects')
        
    @select_objects.setter
    def select_objects(self, sel_obj):
        if isinstance(sel_obj, self.select_item_card):
            self.sel_obj.append(sel_obj)
        else:
            raise TypeError('Must pass the type of select_item_card to this function')
        
    @property
    def __object_group(self):
        return self._obj_grps
        
    @__object_group.setter
    def __object_group(self, obj_no):
        _title = self.title
        if isinstance(obj_no, int):
            if obj_no == 1:
                self.mode = 1
                self._obj_grps = self.long_sentence_indence(_title)
            elif obj_no == 2:
                self.mode = 2
                self._obj_grps = self.split_sentence_indence(_title)
            elif obj_no == 3:
                self.mode = 3
                self._obj_grps = self.selection_sentence_indence(_title)
            elif obj_no == 4:
                self.mode = 4
                self._obj_grps = self.yes_no_sentence(_title)
            elif obj_no == 5:
                self.mode = 5
                self._obj_grps = self.timepicker_sentence(_title)
            else:
                self.mode = 0
                self.modal = False
                self._obj_grps = {'title': None, 'contents': [None]}
        
    def long_sentence_indence(self, title='', type='dict'):
        # title   sentssentss
        #         entssents
        if not (self.modal):
            n = self.spliter.join(self._content)
            sents = []
            sents_append = sents.append
            for i in range(0, len(n), self._max_len * self.max_row):
                s = n[i:]
                sents_append(
                        [
                                s[
                                        i:i+self._max_len
                                ] for i in range(
                                        0,
                                        self._max_len*self.max_row,
                                        self._max_len
                                        )
                        ]
                )
            if type == 'list':
                # debug used
                lsi = sents
            elif type == 'dict':
                lsi = {'title': title, 'contents': sents}
            return lsi
        
    def split_sentence_indence(self, title='', type='dict'):
        # title   sents
        #         sents
        #
        #
        if not (self.modal):
            cont = self._content
            sents = []
            xxx = []
            xxx_append = xxx.append
            for x in cont:
                if len(x) <= self.max_len:
                    xxx_append(x)
                else:
                    xxx_append(x[:self.max_len])
                    xxx_append(x[self.max_len:])
            sents = [xxx[i:i+self.max_row] for i in range(0, len(xxx), self.max_row)]
            if type == 'list':
                # debug used
                splt_si = sents
            elif type == 'dict':
                splt_si = {'title': title, 'contents': sents}
            return splt_si
        
    def selection_sentence_indence(self, title='', type='dict'):
        # title   •sl_1 •sl_2
        #         •sl_3 •sl_4
        
        if not (self.modal):
            self.sel_obj = []
            tc = []
            card_len = int(self._max_len / 2)
            
            for x in self._content:
                self.select_objects = self.select_item_card(x, card_len, True)
        gg = ''.join(
                [
                        f'{g.text}\n' if i % 2 == 1 and i + 1 != len(self.sel_obj) else f'{g.text}'
                        for i, g
                        in enumerate(self.sel_obj)
                ]
        )
        tc = gg.split('\n')
        selects = [tc[i:i+2] for i in range(0, len(tc), 2)]
        if type == 'list':
            # debug used
            slct_si = selects
        elif type == 'dict':
            slct_si = {'title': title, 'contents': selects}
        return slct_si
        
    def yes_no_sentence(self, title='', type='dict'):
        # title   •yes •no
        con = self.spliter.join(self._content)
        if not (self.modal):
            y = 'yes'
            n = 'no'
            self.sel_obj = []
            if self.max_row <= 1:
                card_len = 1
            else:
                card_len = int(self._max_len / 2)
            y_card = self.select_item_card(y, card_len, False)
            n_card = self.select_item_card(n, card_len, False)
            self.select_objects = y_card
            self.select_objects = n_card
        selects = []
        selects_append = selects.append
        x = []
        x_append = x.append
        
        if len(title) >= self.max_len:
            x_append(f'{con[:self.max_len - 1]}…')
        else:
            x_append(f'{con[:self.max_len]}')
        
        gg = ''.join(
                [
                        f'{g.text}' for g in self.sel_obj
                ]
        )
        
        x_append(f'{gg: >{self.max_len}}')
        selects_append(x)
        
        if type == 'list':
            # debug used
            slct_si = selects
        elif type == 'dict':
            slct_si = {'title': title, 'contents': selects}
        return slct_si
        
    def timepicker_sentence(self, title='', type='dict'):
        # title  Time hh:mm
        #            u/d/nx
        #
        if not (self.modal):
            self.cnt_obj = {}
            self.cnt_obj['tp_h'] = (
                    self.num_counter_card(
                            def_num=0,
                            start_num=0,
                            end_num=24,
                            end_behavior='round'
                    )
            )
            self.cnt_obj['tp_m'] = (
                    self.num_counter_card(
                            def_num=0,
                            start_num=0,
                            end_num=60,
                            end_behavior='round'
                    )
            )
            self.sel_obj = []
            u_card = self.select_item_card('u', 1, False)
            d_card = self.select_item_card('d', 1, False)
            E_card = self.select_item_card('E', 1, False)
            self.select_objects = u_card
            self.select_objects = d_card
            self.select_objects = E_card
        
        __X = lambda tl, hr, mn: f'{tl} {hr}:{mn:0>2}'
        selects = []
        selects_append = selects.append
        x = []
        x_append = x.append
        x_append(
                __X(
                        'Time',
                        self.cnt_obj['tp_h'].text,
                        self.cnt_obj['tp_m'].text
                )
        )
        
        x_append(
                ''.join(
                        [
                                f'{g.text}' for g in self.select_objects
                        ]
                )
        )
        
        selects_append(x)
        
        if type == 'list':
            # debug used
            slct_si = selects
        elif type == 'dict':
            slct_si = {'title': title, 'contents': selects}
        return slct_si
        
    def fstr(self, modal, mode, page=0):
        _title = ''
        _page_num = page
        self.modal = modal
        if isinstance(mode, int):
            self.mode = mode
            self.__object_group = self.mode
            
            con1 = self.__object_group
            con2 = '\n'.join(con1['contents'][_page_num])
            con = con2
            if con1['title'] != '':
                _title = con1['title'] + ('\n' * self.max_row)
            padding = ' '
            ln = self._max_len
            self._text = f'{con:{padding}>{ln}}'
        else:
            raise ValueError(f'mode requires a raw integer\n"{mode}"')
        
        return {'title': _title, 'text': self._text}



if __name__ == '__main__':
    # text = 'syukkin gaisyutu toutyaku syuppatu kityaku'
    text = 'save?'
    # text = text + ' ' + text
    #
    v_c = view_contents(content=text, spliter=' ', title='')
    
    # x = v_c.split_sentence_indence()
    # v_c.mode = 1
    #
    
    if True:
        print(v_c.fstr(modal=False, mode=5)['text'])
        v_c.select_objects[0].selected = True
        
        print(v_c.fstr(modal=True, mode=5)['text'])

