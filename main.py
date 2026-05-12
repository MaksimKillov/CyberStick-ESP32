import time
from core import *
import app_rf
import app_wifi
import app_games
import app_misc

def splash():
    cls()
    txt("CYBERSTICK", 24, 20)
    
    rect(14, 40, 100, 8, 1) 
    show()
    
    for i in range(1, 101, 2):
        fill_rect(14, 40, i, 8, 1)
        show()
        time.sleep_ms(15)
        
    time.sleep_ms(300)

def run_menu(title, items):
    idx = 0
    offset = 0
    while True:
        cls()
        txt(f"== {title} ==", 0, 0)
        hline(0, 10, 128, 1)
        
        visible = items[offset:offset+4]
        for i, item in enumerate(visible):
            y = 13 + i * 12
            real_i = offset + i
            if real_i == idx:
                fill_rect(0, y-1, 128, 11, 1)
                txt(item[:15], 2, y, 0)
            else:
                txt(item[:15], 2, y)
                
        hline(0, 61, 128, 1)

        if len(items) > 4:
            pos = int(idx / (len(items)-1) * 120)
            fill_rect(pos, 62, 8, 2, 1)
            
        show()
        
        time.sleep_ms(80)
        if btn_pressed(btn_left):
            idx = (idx - 1) % len(items)
            if idx < offset: 
                offset = max(0, offset - 1)
            if idx == len(items) - 1: 
                offset = max(0, len(items) - 4)
                
        elif btn_pressed(btn_right):
            idx = (idx + 1) % len(items)
            if idx >= offset + 4: 
                offset = min(len(items)-4, offset+1)
            if idx == 0: 
                offset = 0
                
        elif btn_pressed(btn_ok):
            return items[idx]

def main_loop():
    main_items = ["Tools", "Games", "Settings", "About"]
    tool_items = ["Beacon Spam", "RF Analyzer", "WiFi Scan", "Evil Portal", "Net Scanner", "SD Logger", "IR Receiver", "BT Scan", "< Back"]
    game_items = ["Snake", "Flappy Bird", "Dino Run", "< Back"]
    set_items  = ["In progress...", "< Back"] 

    while True:
        sel = run_menu("MAIN MENU", main_items)
        
        if sel == "Tools":
            while True:
                t = run_menu("TOOLS", tool_items)
                if t == "< Back": break
                elif t == "Beacon Spam": app_wifi.beacon_spam()
                elif t == "RF Analyzer": app_rf.rf_analyzer()
                elif t == "WiFi Scan":   app_wifi.wifi_scan()
                elif t == "Evil Portal": app_wifi.evil_portal()
                elif t == "Net Scanner": app_wifi.net_scanner()
                elif t == "SD Logger":   app_wifi.sd_logger()
                elif t == "IR Receiver": app_misc.ir_receiver()
                elif t == "BT Scan":     app_misc.bt_scan()
                
        elif sel == "Games":
            while True:
                g = run_menu("GAMES", game_items)
                if g == "< Back": break
                elif g == "Snake":       app_games.snake_game()
                elif g == "Flappy Bird": app_games.flappy_bird()
                elif g == "Dino Run":    app_games.dino_game()
                
        elif sel == "Settings":
            while True:
                s = run_menu("SETTINGS", set_items)
                if s == "< Back": break
                
        elif sel == "About":
            app_misc.about()

splash()
main_loop()
