from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENTS = ROOT / "hardware" / "components"


FILES = {
    "sensors/proximity/e18_d80nk.yaml": """
identity:
  id: e18_d80nk
  name: E18-D80NK
  manufacturer: Generic / Omron-style photoelectric sensor family
  part_number: E18-D80NK
  description: Adjustable infrared diffuse-reflective photoelectric proximity sensor.

classification:
  category: sensor
  subcategory: proximity

capabilities:
  - proximity_detection
  - obstacle_detection
  - digital_object_detection

interfaces:
  - gpio

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: OUT
    type: gpio
    direction: output
    required: true

electrical:
  voltage:
    min: 6.0
    typical: 12.0
    max: 36.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: read_detection
      description: Read the digital detection state from the sensor.

constraints:
  - Exact electrical characteristics depend on the specific E18-D80NK module variant.
  - Output interface type and polarity must be verified on the physical module.
  - The sensor is intended for object/proximity detection rather than precision distance measurement.

safety:
  - Do not exceed the supply voltage of the exact module.
  - Verify output voltage compatibility before connecting the output directly to an ESP32 GPIO.
""",

    "sensors/distance/hc_sr04.yaml": """
identity:
  id: hc_sr04
  name: HC-SR04
  manufacturer: HC-SR04 module family
  part_number: HC-SR04
  description: Ultrasonic ranging module for non-contact distance measurement.

classification:
  category: sensor
  subcategory: distance

capabilities:
  - distance_measurement
  - obstacle_detection
  - ultrasonic_ranging

interfaces:
  - gpio

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: TRIG
    type: control
    direction: input
    required: true

  - name: ECHO
    type: gpio
    direction: output
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

electrical:
  voltage:
    min: 5.0
    typical: 5.0
    max: 5.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: trigger_measurement
      description: Generate a trigger pulse to start ultrasonic ranging.

    - name: read_echo_time
      description: Measure the echo pulse duration returned by the module.

    - name: read_distance
      description: Convert echo timing into target distance.

constraints:
  - Typical measurement range is approximately 2 cm to 400 cm.
  - Trigger input requires a short digital pulse.
  - Echo output voltage must be checked for compatibility with the selected controller.
  - Measurement timing must allow sufficient recovery time between ranging cycles.

safety:
  - Do not expose ESP32 GPIOs to incompatible logic voltage.
  - Do not exceed the module supply voltage.
""",

    "sensors/environment/dht22.yaml": """
identity:
  id: dht22
  name: DHT22
  manufacturer: Aosong Electronics
  part_number: AM2302 / DHT22
  description: Digital temperature and relative humidity sensor.

classification:
  category: sensor
  subcategory: environmental

capabilities:
  - temperature_measurement
  - humidity_measurement

interfaces:
  - digital

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: DATA
    type: gpio
    direction: bidirectional
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

electrical:
  voltage:
    min: 3.3
    typical: 3.3
    max: 5.5
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - DHT sensor library
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: read_temperature
      description: Read ambient temperature.

    - name: read_humidity
      description: Read relative humidity.

constraints:
  - Communication uses a single digital data line.
  - A suitable pull-up configuration is required.
  - Exact measurement accuracy and timing depend on the sensor variant.

safety:
  - Do not exceed the specified supply voltage.
  - Do not connect the data line to incompatible voltage levels.
""",

    "displays/oled_0_9_ssd1306.yaml": """
identity:
  id: oled_0_9_ssd1306
  name: 0.9-inch OLED SSD1306
  manufacturer: Generic module
  part_number: SSD1306-based 0.9-inch OLED
  description: Small monochrome OLED display module using an SSD1306-compatible controller.

classification:
  category: display
  subcategory: oled

capabilities:
  - text_display
  - graphics_display
  - monochrome_display

interfaces:
  - i2c

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: SDA
    type: i2c_data
    direction: bidirectional
    required: true

  - name: SCL
    type: i2c_clock
    direction: input
    required: true

electrical:
  voltage:
    min: 3.3
    typical: 3.3
    max: 5.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - Adafruit SSD1306
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: initialize_display
      description: Initialize the OLED controller.

    - name: clear_display
      description: Clear the display buffer.

    - name: draw_text
      description: Render text onto the display.

    - name: update_display
      description: Transfer the display buffer to the OLED.

constraints:
  - Exact module voltage tolerance and controller configuration depend on the physical breakout board.
  - Display resolution and I2C address must be confirmed for the selected module.
  - The SSD1306 controller and module wiring must be compatible with the generated driver configuration.

safety:
  - Do not exceed the electrical limits of the specific OLED module.
""",

    "outputs/ws2812b.yaml": """
identity:
  id: ws2812b
  name: WS2812B
  manufacturer: Worldsemi
  part_number: WS2812B
  description: Individually addressable RGB LED with integrated constant-current driver.

classification:
  category: output
  subcategory: addressable_led

capabilities:
  - rgb_output
  - individually_addressable_led
  - programmable_light_output

interfaces:
  - digital

pins:
  - name: VDD
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: DIN
    type: gpio
    direction: input
    required: true

  - name: DOUT
    type: gpio
    direction: output
    required: false

electrical:
  voltage:
    min: 3.5
    typical: 5.0
    max: 5.3
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - Adafruit NeoPixel
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: set_pixel
      description: Set the RGB value of an individual LED.

    - name: show
      description: Transmit the LED data stream.

constraints:
  - Logic-level compatibility between ESP32 output and LED data input must be considered.
  - Power consumption increases with LED count and brightness.
  - Long LED chains may require distributed power injection.
  - Exact electrical limits depend on the WS2812B revision.

safety:
  - Do not exceed the LED supply voltage.
  - Size the power supply for the total LED current.
""",

    "outputs/active_buzzer.yaml": """
identity:
  id: active_buzzer
  name: Active Buzzer
  manufacturer: Generic
  part_number: Active Buzzer Module
  description: Electrically driven buzzer producing an audible tone when enabled.

classification:
  category: output
  subcategory: buzzer

capabilities:
  - audible_alert
  - status_notification

interfaces:
  - gpio

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: SIGNAL
    type: control
    direction: input
    required: true

electrical:
  voltage:
    min: 3.3
    typical: 5.0
    max: 5.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: buzzer_on
      description: Enable the buzzer.

    - name: buzzer_off
      description: Disable the buzzer.

constraints:
  - Exact module trigger voltage and current depend on the selected buzzer module.
  - A transistor driver may be required for modules exceeding GPIO drive capability.

safety:
  - Do not exceed the module supply voltage.
  - Do not drive a high-current buzzer directly from a GPIO unless its current requirement is within GPIO limits.
""",

    "outputs/led.yaml": """
identity:
  id: led
  name: LED
  manufacturer: Generic
  part_number: Standard 5mm LED
  description: Discrete light-emitting diode for visual indication.

classification:
  category: output
  subcategory: indicator_led

capabilities:
  - visual_indicator
  - status_indicator

interfaces:
  - gpio

pins:
  - name: ANODE
    type: gpio
    direction: input
    required: true

  - name: CATHODE
    type: ground
    direction: power
    required: true

electrical:
  voltage:
    min: 1.8
    typical: 2.0
    max: 3.3
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: led_on
      description: Turn the indicator LED on.

    - name: led_off
      description: Turn the indicator LED off.

constraints:
  - A current-limiting resistor is required.
  - Forward voltage depends on LED color and construction.
  - Exact current rating depends on the selected LED.

safety:
  - Never connect the LED directly across a power source without current limiting.
  - Keep LED current within the selected component rating.
""",

    "inputs/push_button.yaml": """
identity:
  id: push_button
  name: Push Button
  manufacturer: Generic
  part_number: Momentary Push Button
  description: Momentary mechanical switch for digital user input.

classification:
  category: input
  subcategory: button

capabilities:
  - digital_input
  - user_input
  - momentary_switch

interfaces:
  - gpio

pins:
  - name: CONTACT_A
    type: gpio
    direction: bidirectional
    required: true

  - name: CONTACT_B
    type: gpio
    direction: bidirectional
    required: true

electrical:
  voltage:
    typical: 3.3
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: read_button
      description: Read the current button state.

constraints:
  - Mechanical switch bounce must be handled by hardware or software debouncing.
  - Pull-up or pull-down biasing is required for a stable logic state.

safety:
  - Do not exceed the switch electrical rating.
""",

    "inputs/potentiometer.yaml": """
identity:
  id: potentiometer
  name: Potentiometer
  manufacturer: Generic
  part_number: 10k Linear Potentiometer
  description: Three-terminal variable resistor suitable for analog user input.

classification:
  category: input
  subcategory: analog_control

capabilities:
  - analog_input
  - user_control
  - variable_resistance

interfaces:
  - adc
  - analog

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: WIPER
    type: analog
    direction: output
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

electrical:
  voltage:
    typical: 3.3
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: read_value
      description: Read the potentiometer position through an ADC input.

constraints:
  - Wiper voltage must remain within the selected ESP32 ADC input range.
  - Exact resistance value depends on the selected potentiometer.
  - ADC attenuation and calibration may affect measured values.

safety:
  - Do not apply a voltage above the ADC input limit.
""",

    "actuators/sg90.yaml": """
identity:
  id: sg90
  name: SG90
  manufacturer: Generic / TowerPro-style servo
  part_number: SG90
  description: Small positional hobby servo motor controlled by a PWM-style servo signal.

classification:
  category: actuator
  subcategory: servo

capabilities:
  - angular_position
  - servo_motion

interfaces:
  - pwm

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: SIGNAL
    type: pwm
    direction: input
    required: true

electrical:
  voltage:
    typical: 5.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - ESP32Servo
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: set_angle
      description: Command the servo to a target angular position.

constraints:
  - Exact voltage, current, torque, and angular range depend on the servo variant.
  - Servo power should normally be supplied separately from the ESP32 GPIO.
  - Servo ground must share an appropriate reference with the controller.

safety:
  - Do not power the servo directly from an ESP32 GPIO.
  - Provide adequate current capacity for servo startup and stall conditions.
""",

    "actuators/mg90s.yaml": """
identity:
  id: mg90s
  name: MG90S
  manufacturer: Generic / Metal-gear servo family
  part_number: MG90S
  description: Small metal-gear positional hobby servo controlled by a PWM-style servo signal.

classification:
  category: actuator
  subcategory: servo

capabilities:
  - angular_position
  - servo_motion

interfaces:
  - pwm

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: SIGNAL
    type: pwm
    direction: input
    required: true

electrical:
  voltage:
    typical: 5.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - ESP32Servo
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: set_angle
      description: Command the servo to a target angular position.

constraints:
  - Exact voltage, current, torque, and angular range depend on the servo variant.
  - Servo power should normally be supplied separately from the ESP32 GPIO.
  - Servo ground must share an appropriate reference with the controller.

safety:
  - Do not power the servo directly from an ESP32 GPIO.
  - Provide adequate current capacity for servo startup and stall conditions.
""",

    "actuators/nema17.yaml": """
identity:
  id: nema17
  name: NEMA 17 Stepper Motor
  manufacturer: Generic
  part_number: NEMA 17
  description: Bipolar hybrid stepper motor in the NEMA 17 mechanical frame size.

classification:
  category: actuator
  subcategory: stepper_motor

capabilities:
  - rotational_motion
  - precise_positioning
  - step_motion

interfaces:
  - digital

pins:
  - name: A1
    type: motor
    direction: output
    required: true

  - name: A2
    type: motor
    direction: output
    required: true

  - name: B1
    type: motor
    direction: output
    required: true

  - name: B2
    type: motor
    direction: output
    required: true

electrical:
  voltage:
    typical: 4.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - AccelStepper
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: step
      description: Command one or more motor steps through a compatible driver.

    - name: set_direction
      description: Set the commanded direction of rotation through a compatible driver.

constraints:
  - NEMA 17 defines a mechanical frame size and does not uniquely define electrical characteristics.
  - A dedicated stepper driver is required.
  - Current, resistance, inductance, torque, and rated voltage must be verified for the selected motor.
  - The motor must not be driven directly from ESP32 GPIO pins.

safety:
  - Never drive the motor coils directly from the ESP32.
  - Use a suitable current-controlled stepper driver.
""",

    "drivers/a4988.yaml": """
identity:
  id: a4988
  name: A4988
  manufacturer: Allegro MicroSystems
  part_number: A4988
  description: Microstepping bipolar stepper motor driver IC/module.

classification:
  category: driver
  subcategory: stepper_driver

capabilities:
  - stepper_motor_drive
  - current_control
  - microstepping
  - direction_control

interfaces:
  - gpio

pins:
  - name: VMOT
    type: power
    direction: power
    required: true

  - name: VDD
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: STEP
    type: control
    direction: input
    required: true

  - name: DIR
    type: control
    direction: input
    required: true

  - name: ENABLE
    type: control
    direction: input
    required: false

  - name: MS1
    type: control
    direction: input
    required: false

  - name: MS2
    type: control
    direction: input
    required: false

  - name: MS3
    type: control
    direction: input
    required: false

  - name: A1
    type: motor
    direction: output
    required: true

  - name: A2
    type: motor
    direction: output
    required: true

  - name: B1
    type: motor
    direction: output
    required: true

  - name: B2
    type: motor
    direction: output
    required: true

electrical:
  voltage:
    min: 8.0
    typical: 12.0
    max: 35.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries:
    - AccelStepper
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: step_motor
      description: Generate STEP pulses to advance the motor.

    - name: set_direction
      description: Set the motor direction.

    - name: set_microstep_mode
      description: Configure the microstepping mode using MS1, MS2, and MS3.

constraints:
  - Logic input voltage must be compatible with the selected controller.
  - Motor current must be configured according to the selected motor and carrier implementation.
  - Adequate cooling may be required at higher currents.
  - VMOT must remain within the driver operating range.
  - Appropriate bulk capacitance is required near the motor supply.

safety:
  - Do not exceed the driver voltage or current limits.
  - Do not connect or disconnect the motor while the driver is powered.
""",

    "actuators/dc_geared_motor.yaml": """
identity:
  id: dc_geared_motor
  name: DC Geared Motor
  manufacturer: Generic
  part_number: Brushed DC Geared Motor
  description: Brushed DC motor with an integrated gearbox for reduced speed and increased output torque.

classification:
  category: actuator
  subcategory: dc_motor

capabilities:
  - rotational_motion
  - speed_control
  - direction_control

interfaces:
  - pwm

pins:
  - name: MOTOR_A
    type: motor
    direction: output
    required: true

  - name: MOTOR_B
    type: motor
    direction: output
    required: true

electrical:
  voltage:
    typical: 6.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: set_speed
      description: Command motor speed through a compatible motor driver.

    - name: set_direction
      description: Command motor direction through a compatible motor driver.

constraints:
  - A motor driver is required.
  - Exact voltage, current, gearbox ratio, speed, and torque depend on the selected motor.
  - Stall current must be considered when sizing the driver and power supply.

safety:
  - Never drive the motor directly from ESP32 GPIO pins.
  - Use a suitable motor driver and power supply.
""",

    "drivers/tb6612fng.yaml": """
identity:
  id: tb6612fng
  name: TB6612FNG
  manufacturer: Toshiba
  part_number: TB6612FNG
  description: Dual full-bridge brushed DC motor driver for controlling up to two DC motors.

classification:
  category: driver
  subcategory: dc_motor_driver

capabilities:
  - dc_motor_drive
  - direction_control
  - pwm_speed_control
  - braking
  - standby_control

interfaces:
  - gpio
  - pwm

pins:
  - name: VM
    type: power
    direction: power
    required: true

  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: AIN1
    type: control
    direction: input
    required: true

  - name: AIN2
    type: control
    direction: input
    required: true

  - name: PWMA
    type: pwm
    direction: input
    required: true

  - name: BIN1
    type: control
    direction: input
    required: true

  - name: BIN2
    type: control
    direction: input
    required: true

  - name: PWMB
    type: pwm
    direction: input
    required: true

  - name: STBY
    type: control
    direction: input
    required: true

  - name: AO1
    type: motor
    direction: output
    required: true

  - name: AO2
    type: motor
    direction: output
    required: true

  - name: BO1
    type: motor
    direction: output
    required: true

  - name: BO2
    type: motor
    direction: output
    required: true

electrical:
  voltage:
    typical: 5.0
    max: 15.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: set_motor_a
      description: Control direction and PWM of motor channel A.

    - name: set_motor_b
      description: Control direction and PWM of motor channel B.

    - name: standby
      description: Put the motor driver into standby mode.

constraints:
  - Motor supply and logic supply are separate rails.
  - Output current depends on thermal conditions and operating conditions.
  - Motor stall current must remain within driver limits.
  - STBY must be asserted appropriately for operation.

safety:
  - Do not exceed the driver supply and output-current limits.
  - Provide adequate decoupling near the driver.
""",

    "outputs/relay_5v.yaml": """
identity:
  id: relay_5v
  name: 5V Relay Module
  manufacturer: Generic
  part_number: SRD-05VDC-SL-C based module
  description: Single-channel 5V electromechanical relay module for switching an external load.

classification:
  category: output
  subcategory: relay

capabilities:
  - on_off_switching
  - isolated_load_switching

interfaces:
  - gpio

pins:
  - name: VCC
    type: power
    direction: power
    required: true

  - name: GND
    type: ground
    direction: power
    required: true

  - name: IN
    type: control
    direction: input
    required: true

  - name: COM
    type: control
    direction: bidirectional
    required: true

  - name: NO
    type: control
    direction: bidirectional
    required: true

  - name: NC
    type: control
    direction: bidirectional
    required: true

electrical:
  voltage:
    min: 5.0
    typical: 5.0
    max: 5.0
    unit: V

compatibility:
  controllers:
    - esp32
  frameworks:
    - arduino

software:
  libraries: []
  frameworks:
    - Arduino
  languages:
    - C++

hal:
  operations:
    - name: relay_on
      description: Energize the relay through the module control input.

    - name: relay_off
      description: De-energize the relay.

constraints:
  - Exact trigger polarity depends on the relay module implementation.
  - The relay coil must be powered from the module supply, not directly from an ESP32 GPIO.
  - Contact voltage and current ratings depend on the relay used on the module.
  - AC mains switching requires appropriate electrical safety practices.

safety:
  - Never route mains voltage through an ESP32 or breadboard.
  - Respect the relay contact voltage and current ratings.
  - Use appropriate enclosure, insulation, fusing, and wiring for hazardous voltages.
"""
}


def main():
    created = 0

    for relative_path, content in FILES.items():
        path = COMPONENTS / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)

        path.write_text(
            content.strip() + "\n",
            encoding="utf-8",
        )

        print(f"Created: {path.relative_to(ROOT)}")
        created += 1

    print()
    print(f"Created {created} component files.")


if __name__ == "__main__":
    main()