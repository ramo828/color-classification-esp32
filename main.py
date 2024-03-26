from library import Utility, Electronics
from time import time as tm
import time
import os

util = Utility()
elec = Electronics()

def make_data(color="red", minus = 0, plus = 0):
    u_data = []
    color_index = 0
    if(color=='white'):
        color_index = 0
    elif(color=='gold'):
        color_index = (1-minus+plus)
    elif(color=='cyan'):
        color_index = (2-minus+plus)
    elif(color=='red'):
        color_index = (3-minus+plus)
    elif(color=='purple'):
        color_index = (4-minus+plus)
    elif(color=='pink'):
        color_index = (5-minus+plus)
    elif(color=='orange'):
        color_index = (6-minus+plus)
    elif(color=='yellow'):
        color_index = (7-minus+plus)
    rgb = util.get_color(color)    # R.G.B
    elec.set_color(rgb[0], rgb[1], rgb[2])
    begin = tm()
    while True:
        if len(util.unique_data(u_data)) == 100:
            for u_d in util.unique_data(u_data):
                util.data_yaz([u_d, color_index],'color_dataset.csv')
            break
        else:
            print("Farklı veri sayısı:", len(util.unique_data(u_data)))
        
        time.sleep(1)
        ldr_value = elec.read_ldr(True)  # ADC ile LDR değerini oku

        if ldr_value != 0:
            print("LDR Değeri:", ldr_value)  # Değeri ekrana yazdır
            u_data.append(ldr_value)
    end = tm()
    print(f"{rgb[0]},{rgb[1]},{rgb[2]}")
    print("Dataset yazıldı: ", (end-begin)/60)
    
def test_data():
    counter = 0
    counter_colors = 0
    colors = util.get_colors()
    temp_ldr = 0.0
    while True:
        color = list(colors.keys())[counter_colors]
        if(counter_colors == len(list(colors.keys()))-1):
            break
            time.sleep(1/100)
            temp_ldr += elec.read_ldr()
        ldr = temp_ldr/1000
        while True:
            ldr = elec.read_ldr()
            time.sleep(1)
            if(ldr == 0):
                print("LDR Hazirlanir: ",counter)
                counter+=1
                continue
            else:
                break
        time.sleep(1)
        if util.check_unique(ldr):
            pass
        else:
            continue
        print(color,ldr, sep="-")
        r,g,b = util.get_color(color)
        elec.set_color(r,g,b)
        
        counter_colors+=1
    print("Test bitdi")


make_data("white",plus=7)
