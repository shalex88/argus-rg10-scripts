# argus-rg10-scripts

Generate file or configure camera to output RG10 RGGB

Colors: red, green, blue, white, black, magenta, yellow, grey/gray

## RUN

For binary mode:

```bash
./set_rg10_rggb_by_color.py binary <color> <width> <height>
```

For camera mode:

```bash
./set_rg10_rggb_by_color.py camera <color>
```

692x520

MPSOC
./ultrazed_channel_config.sh 0 5 30 15 1 3
./tp_solid_config.sh 0x80 0x80 0x80
gst-launch-1.0 nvarguscamera sensor_id=0 sensor_mode=5 ! nv3dsink
./set_camera.sh -d3 -r

nvargus_nvraw --lps
nvargus_nvraw --c 0 --mode 5 --file test --format raw
nvargus_nvraw --c 0 --mode 5 --file test --format jpg
