class Utils:

    def calculate_volume(self, weight):
        if weight >= 450 and weight <= 550:
            volume = 0.5 
        else:
            volume = 1
        return volume
    
    def calculate_cost(self, milktype, volume):
        if milktype == 'NandiniBlue':
            cost = 18
        elif milktype == 'NandiniOrange':
            cost = 20
        elif milktype == 'NandiniGreen':
            cost = 21
        elif milktype == 'NandiniGoodLife':
            cost = 23
        elif milktype == 'NandiniSlim':
            cost = 25
        else:
            cost = 0
        return cost*volume*2