# import matplotlib.pyplot as plt
import numpy as np
# from sklearn.cluster import KMeans
# from sklearn.utils import shuffle

class Quantizer():
    def __init__(self, Ys, Crs, Cbs, n_intensity):
        self.Ys = Ys
        self.Crs = Crs
        self.Cbs = Cbs
        
        self.qYs = []
        self.qCrs = []
        self.qCbs = []
        
        self.dqYs = []
        self.dqCrs = []
        self.dqCbs = []
        
        self.n_intensity = n_intensity
        self.table = np.zeros(256)
        self.reverseTable = np.zeros(8)
    
    def quantization(self):
        all_value = np.array([])
        for i in range(len(self.Ys)):
            Y_flatten = self.Ys[i].flatten()
            Cr_flatten = self.Crs[i].flatten()
            Cb_flatten = self.Cbs[i].flatten()
            all_value = np.concatenate((all_value, Y_flatten, Cr_flatten, Cb_flatten))
        
        offset = 256 / self.n_intensity
        for i in range(self.n_intensity):
            self.reverseTable[i] = i*offset+int(offset/2)
            for j in range(int(i*offset), int(i*offset+offset)):
                self.table[j] = i
        
        self.table = self.table.astype(int)
        self.reverseTable = self.reverseTable.astype(np.uint8)
        
        
        for y in self.Ys:
            h, w = y.shape[:2]
            cy = np.copy(y)
            for i in range(h):
                for j in range(w):
                    cy[i, j] = self.table[int(cy[i, j])]
            self.qYs.append(cy)
        for i in range(len(self.qYs)):
            self.qYs[i] = self.qYs[i].astype(int)
            
        for cr in self.Crs:
            h, w = cr.shape[:2]
            ccr = np.copy(cr)
            for i in range(h):
                for j in range(w):
                    ccr[i, j] = self.table[int(ccr[i, j])]
            self.qCrs.append(ccr)
        for i in range(len(self.qCbs)):
            self.qCrs[i] = self.qCrs[i].astype(int)
            
        for cb in self.Cbs:
            h, w = cb.shape[:2]
            ccb = np.copy(cb)
            for i in range(h):
                for j in range(w):
                    ccb[i, j] = self.table[int(ccb[i, j])]
            self.qCbs.append(ccb)
        for i in range(len(self.qCbs)):
            self.qCbs[i] = self.qCbs[i].astype(int)

    def dequantization(self):
        for y in self.qYs:
            h, w = y.shape[:2]
            cy = np.copy(y)
            for i in range(h):
                for j in range(w):
                    cy[i, j] = self.reverseTable[int(cy[i, j])]
            self.dqYs.append(cy)
            
        for cr in self.qCrs:
            h, w = cr.shape[:2]
            ccr = np.copy(cr)
            for i in range(h):
                for j in range(w):
                    ccr[i, j] = self.reverseTable[int(ccr[i, j])]
            self.dqCrs.append(ccr)
            
        for cb in self.qCbs:
            h, w = cb.shape[:2]
            ccb = np.copy(cb)
            for i in range(h):
                for j in range(w):
                    ccb[i, j] = self.reverseTable[int(ccb[i, j])]
            self.dqCbs.append(ccb)
        
    def setQs(self, nYs, nCrs, nCbs):
        self.qYs = nYs
        self.qCrs = nCrs
        self.qCbs = nCbs
        
    def getQ(self):
        return self.qYs, self.qCrs, self.qCbs
    
    def getDQ(self):
        return self.dqYs, self.dqCrs, self.dqCbs
        
        # all_intensity = np.zeros(256, dtype=int)
        # for i in all_value:
        #     all_intensity[int(i)] += 1
        
        # print(self.table)
        # print(self.reverseTable)
            
        # total = int(len(all_value)/self.n_intensity)
        # now = 0
        # id = 0
        # for i in range(256):
        #     now += all_intensity[int(i)]
        #     if now >= total:
        #         self.table[id] = i
        #         now = 0
        #         id += 1
        #     elif i == 255:
        #         for j in range(id, self.n_intensity):
        #             self.table[j] = i
            

        
        # print(all_intensity)
        
        # hist = np.histogram(all_value, bins=np.arange(0, 256))
        # print(hist)
        # plt.figure(2)
        # plt.clf()
        # plt.title('Histogram')
        # plt.hist(all_value)
        # plt.show()
        # plt.plot(hist[1][:-1], hist[0], lw=2)
