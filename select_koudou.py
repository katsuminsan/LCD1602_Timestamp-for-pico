from ViewContents import view_contents

class select_koudou():
    text = 'syukkin gaisyutu toutyaku syuppatu kityaku'
    
    def __init__(self):
        # self.btn_Select.action = self.Clicked_Select
        # self.btn_Enter.action = self.Clicked_Enter
        self.vc = (
                view_contents(
                        content=select_koudou.text,
                        spliter=' ',
                        title=''
                )
        )

        # self.v['show_contents'].text = self.vc._text
        self.SelectCnt = 99
        self.EnterCnt = 99

        self.PAGEMODEL = {
                'ShowContents':
                        self.vc.fstr(modal=False, mode=3),
                'OutTexts': ''
        }
        
    @property
    def EnterCnt_counter(self):
        if self.EnterCnt == 99:
            self.EnterCnt = 0
        return self.EnterCnt

    @EnterCnt_counter.setter
    def EnterCnt_countup(self, countup):
        if countup <= 9:
            _cntup = countup
        else:
            _cntup = 9
        self.EnterCnt += 1
        for i in range(1, _cntup + 1):
            if self.EnterCnt == 4 or self.EnterCnt >= 99:
                self.EnterCnt = 0
        
    @property
    def SelectCnt_counter(self):
        if self.SelectCnt == 99:
            self.SelectCnt = -1
        return self.SelectCnt
        
    @SelectCnt_counter.setter
    def SelectCnt_countup(self, countup):
        # _cntup is countup step of number.
        if countup <= 9:
            _cntup = countup
        else:
            _cntup = 9
        # countup loop by before set _cntup values
        if self.SelectCnt >= 99:
            self.SelectCnt = 0
        else:

            if (self.vc.max_row * 2) < self.SelectCnt:
                card_num = self.vc.max_row * 2
            else:
                card_num = len(self.vc.select_objects)


            self.SelectCnt += countup
            self.SelectCnt = self.SelectCnt % card_num
        
    def Clicked_Select(self):
        self.SelectCnt_countup = 1
        p_num = 0
        for i in range(len(self.vc.select_objects)):
            if self.SelectCnt_counter == i:
                self.vc.select_objects[i].selected = True
            else:
                self.vc.select_objects[i].selected = False
        p_num = self.SelectCnt // (self.vc.max_row * 2)
        self.PAGEMODEL['ShowContents'] = (
                self.vc.fstr(
                        modal=True, mode=3, page=p_num
                )
        )
        
    def Clicked_Enter(self):
        if self.SelectCnt_counter != -1:
            self.PAGEMODEL['OutTexts'] = (
                    self.vc.select_objects[
                            self.SelectCnt_counter
                    ].source
            )
        else:
            self.PAGEMODEL['OutTexts'] = 'not selected'

