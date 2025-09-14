from collections import deque

class IMSI_POOL:

    def __init__(self):
    
        self.imsi_pool = deque()
        self.imsi_pool= deque([999991000000087, \
        999991000000088, 999991000000089, 999991000000090, \
        999991000000091, 999991000000092, 999991000000093, \
        999991000000094, 999991000000095, 999991000000096, \
        999991000000097, 999991000000098, 999991000000099 \
            ])   
    
    def get_imsi(self):
        imsi = self.imsi_pool.popleft()           
        return (imsi)  
    
    def get_pool_info(self):
        return(len(self.imsi_pool))
