import RPi.GPIO as GPIO
import time
import keyboard  # 用于键盘映射

GPIO.setmode(GPIO.BCM)

# 定义引脚
CONTROL_PIN = 18
OUTPUT_PINS = [15, 24, 7, 21, 5]
MONITOR_PINS = [14, 23, 8, 20, 6]
KEY_MAPPING = ['left', 'q', 'm', 'right', 'return']  # 按钮对应的键盘按键

# 设置引脚模式
GPIO.setup(CONTROL_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in OUTPUT_PINS:
    GPIO.setup(pin, GPIO.OUT)

for pin in MONITOR_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# 初始化状态
control_state = GPIO.LOW
last_control_state = GPIO.LOW

# 读取初始状态，避免启动时错误触发
initial_states = [GPIO.input(pin) for pin in MONITOR_PINS]

try:
    while True:
        control_state = GPIO.input(CONTROL_PIN)

        # 检测 CONTROL_PIN 状态变化
        if control_state != last_control_state:
            if control_state == GPIO.LOW:
                # CONTROL_PIN 按下
                keyboard.press_and_release('p')  # 映射键盘P键
                print("Control pin activated: P key pressed.")

                # 关闭所有其他按钮的供电
                for pin in OUTPUT_PINS:
                    GPIO.output(pin, GPIO.LOW)
                
                time.sleep(0.2)
                print("All output pins deactivated.")
            else:
                # CONTROL_PIN 松开
                keyboard.press_and_release('p')  # 再次映射键盘P键以恢复播放
                print("Control pin deactivated: P key pressed.")

                # 恢复其他按钮的供电
                for pin in OUTPUT_PINS:
                    GPIO.output(pin, GPIO.HIGH)
                    
                time.sleep(0.2)
                print("All output pins reactivated.")

            last_control_state = control_state

        # 如果 CONTROL_PIN 为 HIGH，检查其他按钮状态
        if control_state == GPIO.HIGH:
            for i, monitor_pin in enumerate(MONITOR_PINS):
                current_state = GPIO.input(monitor_pin)

                # 仅当按钮从未按下状态变为按下状态时触发
                if current_state == GPIO.LOW and initial_states[i] == GPIO.HIGH:
                    # 独立映射键盘按键
                    keyboard.press_and_release(KEY_MAPPING[i])
                    print(f"Button {i+1} pressed, mapped to {KEY_MAPPING[i].upper()}")
                    while GPIO.input(monitor_pin) == GPIO.HIGH:
                        pass  # 等待按键释放

                # 更新按钮的初始状态
                initial_states[i] = current_state

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
