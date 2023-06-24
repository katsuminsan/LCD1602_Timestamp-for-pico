from ViewContents import view_contents


class Timepicker:
    def __init__(self):
        
        self.vc_tp = (
                view_contents(
                        content='',
                        spliter=' ',
                        title=''
                )
        )
        self.vc_tp.fstr(modal=False, mode=5)
        self.hh_up = 8
        self.mm_up = 0
        
        self._tp_t = f'{self.hh}:{self.mm}'
        self.tp_sel = 0
        
        for i in range(3):
            if i == self.tp_sel:
                self.vc_tp.select_objects[i].selected = True
            else:
                self.vc_tp.select_objects[i].selected = False
        
        self.vc_yn = (
                view_contents(
                        content='Save?',
                        spliter=' ',
                        title=''
                )
        )
        self.vc_yn.fstr(modal=False, mode=4)

        self.yn_sel = 0

        for i in range(2):
            if i == self.yn_sel:
                self.vc_yn.select_objects[i].selected = True
            else:
                self.vc_yn.select_objects[i].selected = False

        self.PAGEMODEL = {
                'ShowContents':
                        self.vc_tp.fstr(modal=True, mode=5),
                'OutTexts': ''
        }
        
        self.step = 0
        
    @property
    def hh(self):
        _h = self.vc_tp.cnt_obj['tp_h'].text
        return f'{_h: >2}'
        
    @hh.setter
    def hh_up(self, count_up=1):
        self.vc_tp.cnt_obj['tp_h'].counter = count_up
        
    @property
    def mm(self):
        _m = self.vc_tp.cnt_obj['tp_m'].text
        return f'{_m:0>2}'
        
    @mm.setter
    def mm_up(self, count_up=1):
        self.vc_tp.cnt_obj['tp_m'].counter = count_up
        
    @property
    def tp_time(self):
        return f'{self.hh}:{self.mm}'
        
    def yesno(self):
        
        self.PAGEMODEL['ShowContents'] = self.vc_yn.fstr(modal=True, mode=4)
        return self.PAGEMODEL
        
    def timepicker(self):
        
        self.PAGEMODEL['ShowContents'] = self.vc_tp.fstr(modal=True, mode=5)
        return self.PAGEMODEL
        
    def Clicked_Select(self):
        if self.step == 0 or self.step == 1:
            # step-0 set hh
            # step-1 set mm
            self.tp_sel += 1
            self.tp_sel = self.tp_sel % 3
            for i in range(3):
                if i == self.tp_sel:
                    self.vc_tp.select_objects[i].selected = True
                else:
                    self.vc_tp.select_objects[i].selected = False

            self.PAGEMODEL = self.timepicker()
            
        elif self.step == 2:
            # step-2 select yes_no
            self.yn_sel += 1
            self.yn_sel = self.yn_sel % 2
            for i in range(2):
                if i == self.yn_sel:
                    self.vc_yn.select_objects[i].selected = True
                else:
                    self.vc_yn.select_objects[i].selected = False
            self.PAGEMODEL = self.yesno()
        
        
    def Clicked_Enter(self):
        if self.step == 0:
            # step-0 set hh
            if self.vc_tp.select_objects[0].selected == True:
                self.hh_up = 1
                
            elif self.vc_tp.select_objects[1].selected == True:
                self.hh_up = -1
                
            elif self.vc_tp.select_objects[2].selected == True:
                self.step = 1
                
            self.PAGEMODEL = self.timepicker()
            
        elif self.step == 1:
            # step-1 set mm
            if self.vc_tp.select_objects[0].selected == True:
                self.mm_up = 1
                
            elif self.vc_tp.select_objects[1].selected == True:
                self.mm_up = -1
                
            elif self.vc_tp.select_objects[2].selected == True:
                self.step = 2
                
            if self.step == 2:
                self.PAGEMODEL = self.yesno()
            else:
                self.PAGEMODEL = self.timepicker()
            
        elif self.step == 2:
            # step-2 select yes_no
            if self.vc_yn.select_objects[0].selected == True:
                self.step = -1
                self.PAGEMODEL['OutTexts'] =  self.tp_time
                
            elif self.vc_yn.select_objects[1].selected == True:
                self.step = 0
                self.PAGEMODEL = self.timepicker()
        elif self.step == -1:
            # step-(-1) exit timepick flag
            print('exit tp')


if __name__ == '__main__':
    pick = Timepicker()
    pick_tp = pick.timepicker()
    pick.hh_up = 8
    # pick.vc.cnt_obj['tp_h'].count = int(8)
    print(pick.timepicker())
    print(pick_tp)
    print(pick.tp_time)

