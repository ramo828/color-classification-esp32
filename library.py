from machine import Pin, PWM, ADC
import os

class Utility:
    def __init__(self):
        self.smooth_value = False
        self.sm_value = 0
        self.ref_data = 0
        self.temp_val = []
        self.rgb_colors = {
            "white":[255,255,255], # white
            "gold":[246,224,201], # iphone 7 gold
            "cyan":[0,255,255],   # cyan
            "red":[255,0,0],     # red
            "purple":[128, 0, 128],  # purple
            "pink":[255, 192, 203],  # pink
            "orange":[255, 165, 0],  # orange
            "yellow":[255, 255, 0],  # yellow
            }

        # Eğer CSV dosyası yoksa, başlıkları ekleyin
        self.dosya_adi = "color_dataset.csv"
        if self.dosya_adi not in os.listdir():
            with open(self.dosya_adi, 'w') as dosya:
                self.data_yaz(['value', 'r', 'g', 'b'], self.dosya_adi)
    
    def unique_data(self, veri_listesi):
        benzersiz_veriler = []
        for veri in veri_listesi:
            if veri not in benzersiz_veriler:
                benzersiz_veriler.append(veri)
        return benzersiz_veriler

    # CSV faylina data yazma funksiyasi
    def data_yaz(self, data, filename):
        with open(filename, 'a') as file:
            file.write(','.join(map(str, data)) + '\n')
            
    def get_color(self, color_name):
        return self.rgb_colors[color_name]
    
    def get_colors(self):
        return self.rgb_colors
    
    def clean_smoth(self, val=False):
        self.smooth_value = val
        
        
    def smooth(self, value):
        self.temp_val.append(value)
        
        if len(self.temp_val) > 100:
            for i in self.temp_val:
                self.ref_data += i
                
            self.sm_value = self.ref_data / len(self.temp_val)
            self.temp_val = []
            
        return self.sm_value

    def check_unique(self, value, data_list=[]):
        if value in data_list:
            return False
        else:
            data_list.append(value)
            return True

class Electronics:
    def __init__(self):
        # LED'lerin bağlı olduğu GPIO pin numaralarını belirtin
        self.red_pin_num = 13
        self.green_pin_num = 12
        self.blue_pin_num = 14
        self.ldr_pin = 27  # Örnek olarak GPIO pin 27
        # PWM nesnelerini oluşturun
        self.red_pwm = PWM(Pin(self.red_pin_num), freq=1000)  # Frekans 1000 Hz olarak ayarlandı
        self.green_pwm = PWM(Pin(self.green_pin_num), freq=1000)
        self.blue_pwm = PWM(Pin(self.blue_pin_num), freq=1000)
        # ADC nesnesini oluştur
        self.adc = ADC(Pin(self.ldr_pin))
        # ADC çözünürlüğünü ayarla (1-12 arasında, 12 en yüksek çözünürlüktür)
        self.adc.width(ADC.WIDTH_12BIT)  # Örnek olarak 10 bit çözünürlük
        # Giriş gerilim aralığını ayarla (0-1.1V, 0-1.5V, 0-2.2V, 0-3.3V arasında)
        self.adc.atten(ADC.ATTN_11DB)  # ESP32'de varsayılan referans gerilimi 3.3V'dir
        self.util = Utility()

    def set_color(self, r, g, b):
        # Duty cycle değerlerini hesapla (0 - 1023 arasında)
        r_duty = int((r / 255) * 1023)
        g_duty = int((g / 255) * 1023)
        b_duty = int((b / 255) * 1023)
        
        # Duty cycle değerlerini PWM sinyallerine uygula
        self.red_pwm.duty(r_duty)
        self.green_pwm.duty(g_duty)
        self.blue_pwm.duty(b_duty)
        
    def read_ldr(self, stat = False):
        if(stat):
            return self.adc.read()  # ADC ile LDR değerini oku
        else:
            return self.util.smooth(self.adc.read())  # ADC ile LDR değerini oku




