from ViewContents import view_contents, lcdControl
import select_koudou, timepicker


class tpui_title(lcdControl):
    text = 'Welcome to timestamp'
    
    def __init__(self):
        self._init()
        self._SDmem = []
        self.toSDdata = ''
        super().__init__()
        
    def _init(self):
        self.vc = (
                view_contents(
                        content=tpui_title.text,
                        spliter='',
                        title=''
                )
        )
        self._PAGEMODEL = {
                'ShowContents':
                        self.vc.fstr(modal=False, mode=1),
                'OutTexts': ''
        }
        
        self.page_ID = 'p0'
        sel_k = select_koudou.select_koudou()
        time_p = timepicker.Timepicker()
        self.page = {
                'p0': self,
                'p1': sel_k,
                'p2': time_p,
        }
        
        
    @property
    def SDmem(self):
        return '\n'.join(self._SDmem)
        
    @SDmem.setter
    def SDmem(self, strData):
        self._SDmem.append(strData)
        
    @property
    def PAGEMODEL(self):
        return self._PAGEMODEL
        
    @PAGEMODEL.setter
    def PAGEMODEL(self, p_obj):
        self._PAGEMODEL = p_obj
        
    def Clicked_Select(self):
        pID = self.page_ID

        pg = self.page[pID]
        if pID == 'p0':
            self._PAGEMODEL['OutTexts'] = self.SDmem
            print('SDmem:')
            print(self.SDmem)
            
        elif pID == 'p1':
            self.page[self.page_ID].Clicked_Select()

        elif pID == 'p2':
            self.page[self.page_ID].Clicked_Select()
        
        self.PAGEMODEL = self.page[self.page_ID].PAGEMODEL
        self.update(self.PAGEMODEL)
        
    def Clicked_Enter(self):
        pID = self.page_ID
        
        pg = self.page[pID]
        if pID == 'p0':
            self.page_ID = 'p1'
            
        elif self.page_ID == 'p1':
            self.page[self.page_ID].Clicked_Enter()
            
            if self.page[self.page_ID].PAGEMODEL['OutTexts'] != 'not selected':
                self.toSDdata = self.page[self.page_ID].PAGEMODEL["OutTexts"]
                
                self.page_ID = 'p2'
            
        elif self.page_ID == 'p2':
            for obj in self.page[self.page_ID].vc_tp.select_objects:
                if obj.selected == True:
                    self.page[self.page_ID].Clicked_Enter()
                    
                    if self.page[self.page_ID].step == -1:
                        self.toSDdata += self.page[self.page_ID].tp_time
                        
                        self.SDmem = self.toSDdata
                        self._init()
        
        self.PAGEMODEL = self.page[self.page_ID].PAGEMODEL
        self.update(self.PAGEMODEL)

if __name__ == '__main__':
    tss = tpui_title()
    KEY_SELECT = machine.Pin(8, machine.Pin.IN)
    KEY_ENTER = machine.Pin(9, machine.Pin.IN)
    
    while True:
        tss.update(tss.PAGEMODEL)
        if KEY_SELECT.value() == 1 and KEY_ENTER.value() == 0:
            tss.Clicked_Select()
        if KEY_SELECT.value() == 1 and KEY_ENTER.value() == 0:
            tss.Clicked_Enter()
        time.sleep_ms(200)
