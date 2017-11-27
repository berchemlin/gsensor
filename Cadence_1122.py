import json
import math
import numpy as np

class step_calc:
    '''
    following Cadence_1107.py
    cosider pause situation
    and replace time counter (index) with time stamp
    '''
    def __init__(self):
        ''' initial attributes '''
        self.tminus = 0      # t[n-1]
        self.tstamp = 0      # t[n]
        self.PSNR = 1.3      # default of PSNR ratio
        self.step_count = 0  # total steps

        self.datan0 = 0
        self.datan1 = 0
        self.datan2 = 0
        self.peak = 0
        self.peak_frame = 0
        self.max_PSNR_value = -1
        self.PSNR_peak = 0
        self.PSNR_peak_frame = 0
        self.PSNR_rate = [0 for x in range(3)]
        self.cadN = [0 for x in range(3)]
        self.CAD = 0
        self.real_peak_frame = 0
        self.pause = 0

    def update_x_y_z(self, x, y, z, tstamp):
        '''
        input:
               x      (float)
               y      (float)
               z      (float)
               index  (int)
        output:
               self.get_step_count  (int)
               self.get_step_CAD    (list_float...cad/time)
        '''
        try:
            x = float(x)
            y = float(y)
            z = float(z)
            # assert type(index) == int
        except:
            print('Input type error')

        if tstamp < 0:
            print('Error time stamp')

        self.datan0 = self.datan1
        self.datan1 = self.datan2
        self.datan2 = math.sqrt(x**2 + y**2 + z**2) if not all(i==0.0 for i in (x,y,z)) else 0.01
        self.tminus = self.tstamp
        self.tstamp = tstamp

        if max(self.datan2, self.datan1, self.datan0) == self.datan1:
            if float(self.tminus-self.peak_frame) >= 0.25 or self.datan1 > self.peak:
                self.peak = self.datan1
                self.peak_frame = self.tminus
        # updata PSNR value                                       #|
        if self.max_PSNR_value < self.peak/self.datan2:           #|
            self.max_PSNR_value = self.peak/self.datan2           #|
        # get max PSNR rate every second                          #|
        if int(self.tstamp) > int(self.tminus):                             #|  PSNR exam
            self.PSNR_rate[int(self.tstamp)%3] = self.max_PSNR_value   #|
            self.max_PSNR_value = 1                               #|                            #|
        # re-calculate PSNR rate every 3 second                   #|
        if int(self.tstamp)%3 == 0: # 3 sec                            #|
            if np.mean(self.PSNR_rate) > 4:                       #|
                self.PSNR = 1.8	# running                         #|
            else:                                                 #|
                self.PSNR = 1.3	# walking                         #|
        # select the real peak
        if (self.peak/self.datan2) > self.PSNR:
            if float(self.peak_frame-self.PSNR_peak_frame) <= 0.2 and self.peak < self.PSNR_peak:
                pass
            elif float(self.peak_frame-self.PSNR_peak_frame) > 0.2:
                self.step_count += 1
                self.real_peak_frame = self.PSNR_peak_frame
                self.cadN[self.step_count%len(self.cadN)] = round(60/(self.peak_frame-self.real_peak_frame))
                self.PSNR_peak = self.peak
                self.PSNR_peak_frame = self.peak_frame
            else:
                self.PSNR_peak = self.peak
                self.PSNR_peak_frame = self.peak_frame
                
        if np.mean(self.PSNR_rate)<1.3:
            self.pause += 1
        else:
            self.pause = 0

        if self.step_count >= len(self.cadN) and int(self.tstamp) > int(self.tminus):
            if self.CAD == 0:
                self.CAD = round(np.mean(self.cadN))
            else:
                self.CAD = round(self.CAD*0.8+round(np.mean(self.cadN))*0.2)
            if self.pause>=1:
                self.CAD = 0

    def get_step_count(self):
        return self.step_count

    def get_step_CAD(self):
        return self.CAD
