# CyberStick-ESP32
ESP32-based portable security audit tool featuring 433MHz RF analysis (CC1101), WiFi penetration testing modules, and BLE/IR capabilities. Developed in MicroPython

# RU
# CyberStick: Portable Security Audit Tool (ESP32)

CyberStick — это портативное многофункциональное устройство для аудита безопасности и тестирования беспроводных сетей, построенное на базе ESP32 и MicroPython.

## 🚀 
 Возможности
- **WiFi**: Сканирование сетей, Beacon Spam, создание Evil Portal для тестирования фишинга, сетевой сканер (IP/Port).
- **RF (433MHz)**: Анализатор спектра на базе CC1101 (мониторинг RSSI в реальном времени).
- **Bluetooth (BLE)**: Сканирование устройств и имитация рекламных пакетов (Target Spam).
- **IR**: Прием и анализ инфракрасных сигналов.
- **Data Logging**: Сохранение результатов сканирования на SD-карту.
- **Дополнительно**: Интегрированные мини-игры (Snake, Flappy Bird) для проверки работы дисплея и кнопок.

## 🛠 Аппаратная часть
- **MCU**: ESP32-D0WD-V3
- **Display**: OLED SSD1306 (128x64 I2C)
- **Radio**: CC1101 (SPI)
- **Storage**: MicroSD Card Module (SPI)
- **Peripheral**: IR Receiver, 3x Buttons

## 🔧 
 Установка
1. Прошейте ESP32 актуальной версией MicroPython.
2. Загрузите содержимое папки `/src` на устройство с помощью Thonny или ampy.
3. Отредактируйте `boot.py` для настройки подключения к WiFi.
