[1mdiff --git a/hardware/components/sensors/bno085.yaml b/hardware/components/sensors/bno085.yaml[m
[1mindex e769d72..c661b16 100644[m
[1m--- a/hardware/components/sensors/bno085.yaml[m
[1m+++ b/hardware/components/sensors/bno085.yaml[m
[36m@@ -1,20 +1,24 @@[m
 identity:[m
   id: bno085[m
   name: BNO085[m
[31m-  manufacturer: Hillcrest Laboratories[m
[32m+[m[32m  manufacturer: CEVA / Hillcrest Labs[m
   part_number: BNO085[m
[31m-  description: 9-axis absolute orientation sensor with integrated sensor fusion.[m
[32m+[m[32m  description: 9-axis sensor hub System in Package with integrated accelerometer, gyroscope, magnetometer, sensor fusion, and embedded processing.[m
 [m
 classification:[m
   category: sensor[m
   subcategory: imu[m
 [m
 capabilities:[m
[31m-  - orientation[m
   - acceleration[m
   - angular_velocity[m
[31m-  - rotation[m
[31m-  - imu[m
[32m+[m[32m  - magnetic_field[m
[32m+[m[32m  - orientation[m
[32m+[m[32m  - rotation_vector[m
[32m+[m[32m  - gravity[m
[32m+[m[32m  - linear_acceleration[m
[32m+[m[32m  - sensor_fusion[m
[32m+[m[32m  - activity_classification[m
 [m
 interfaces:[m
   - i2c[m
[36m@@ -22,7 +26,12 @@[m [minterfaces:[m
   - uart[m
 [m
 pins:[m
[31m-  - name: VIN[m
[32m+[m[32m  - name: VDD[m
[32m+[m[32m    type: power[m
[32m+[m[32m    direction: power[m
[32m+[m[32m    required: true[m
[32m+[m
[32m+[m[32m  - name: VDDIO[m
     type: power[m
     direction: power[m
     required: true[m
[36m@@ -32,19 +41,44 @@[m [mpins:[m
     direction: power[m
     required: true[m
 [m
[31m-  - name: SDA[m
[32m+[m[32m  - name: HOST_SDA[m
     type: i2c_data[m
     direction: bidirectional[m
[31m-    required: true[m
[32m+[m[32m    required: false[m
 [m
[31m-  - name: SCL[m
[32m+[m[32m  - name: HOST_SCL[m
     type: i2c_clock[m
[32m+[m[32m    direction: bidirectional[m
[32m+[m[32m    required: false[m
[32m+[m
[32m+[m[32m  - name: HOST_INTN[m
[32m+[m[32m    type: interrupt[m
[32m+[m[32m    direction: output[m
[32m+[m[32m    required: false[m
[32m+[m
[32m+[m[32m  - name: RSTN[m
[32m+[m[32m    type: control[m
     direction: input[m
     required: true[m
 [m
[32m+[m[32m  - name: BOOTN[m
[32m+[m[32m    type: control[m
[32m+[m[32m    direction: input[m
[32m+[m[32m    required: false[m
[32m+[m
[32m+[m[32m  - name: PS1[m
[32m+[m[32m    type: control[m
[32m+[m[32m    direction: input[m
[32m+[m[32m    required: false[m
[32m+[m
[32m+[m[32m  - name: PS0[m
[32m+[m[32m    type: control[m
[32m+[m[32m    direction: input[m
[32m+[m[32m    required: false[m
[32m+[m
 electrical:[m
   voltage:[m
[31m-    min: 3.0[m
[32m+[m[32m    min: 2.4[m
     typical: 3.3[m
     max: 3.6[m
     unit: V[m
[36m@@ -69,14 +103,26 @@[m [mhal:[m
       description: Read fused orientation data.[m
 [m
     - name: read_acceleration[m
[31m-      description: Read linear acceleration data.[m
[32m+[m[32m      description: Read acceleration data.[m
 [m
     - name: read_angular_velocity[m
[31m-      description: Read angular velocity data.[m
[32m+[m[32m      description: Read gyroscope angular velocity data.[m
[32m+[m
[32m+[m[32m    - name: read_magnetic_field[m
[32m+[m[32m      description: Read magnetic field data.[m
[32m+[m
[32m+[m[32m    - name: read_linear_acceleration[m
[32m+[m[32m      description: Read linear acceleration data.[m
 [m
 constraints:[m
[31m-  - Requires an appropriate hardware interface configuration.[m
[31m-  - I2C address and bus configuration must be compatible with the selected breakout/module.[m
[32m+[m[32m  - Host communication can use I2C, SPI, or UART depending on protocol-selection configuration.[m
[32m+[m[32m  - Protocol selection pins are sampled at reset.[m
[32m+[m[32m  - VDD must remain within the specified 2.4 V to 3.6 V range.[m
[32m+[m[32m  - VDDIO must remain within the specified 1.65 V to 3.6 V range.[m
[32m+[m[32m  - Exact host pin configuration depends on the selected communication protocol.[m
[32m+[m[32m  - The 32.768 kHz crystal requirement applies to the BNO085 device-level design.[m
[32m+[m[32m  - A suitable hardware interface configuration is required before firmware generation.[m
 [m
 safety:[m
[31m-  - Do not exceed the specified supply voltage.[m
\ No newline at end of file[m
[32m+[m[32m  - Do not exceed the specified VDD or VDDIO voltage limits.[m
[32m+[m[32m  - Do not connect incompatible host-interface voltage levels.[m
\ No newline at end of file[m
