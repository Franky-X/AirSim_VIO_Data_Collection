# In settings.json first activate computer vision mode: 
# https://github.com/Microsoft/AirSim/blob/main/docs/image_apis.md#computer-vision-mode

import setup_path 
import airsim

import pprint
import tempfile
import os
import time

pp = pprint.PrettyPrinter(indent=4)

client = airsim.VehicleClient()

airsim.wait_key('Press any key to get camera parameters')
for camera_id in range(2):
    camera_info = client.simGetCameraInfo(str(camera_id))
    print("CameraInfo %d: %s" % (camera_id, pp.pprint(camera_info)))

airsim.wait_key('Press any key to get images')
tmp_dir = os.path.join(tempfile.gettempdir(), "airsim_drone")
print ("Saving images to %s" % tmp_dir)
try:
    for n in range(3):
        os.makedirs(os.path.join(tmp_dir, str(n)))
except OSError:
    if not os.path.isdir(tmp_dir):
        raise

# GT TUM FORMAT FILE
path = "../car/ground_truth_Car_10m_s_turn.txt"
file = open(path,"r")
# my_str = file.readline()
# my_str = file.readline()
# my_str = file.readline()
# my_str = file.readline()

# count means the pose you want to capture picture
count = 5856 

# save to /tmp/airsim_drone
for x in range(count): # do few times
    #xn = 1 + x*5  # some random number
    my_str = file.readline()
    if x % 10 == 0:
    # if x >= 0 :
        str_list = my_str.split()
        float_list = [float(x) for x in str_list]
        print(float_list)
        pose = airsim.Pose(airsim.Vector3r(float_list[1], float_list[2], float_list[3]), airsim.Quaternionr(float_list[4], float_list[5], float_list[6], float_list[7]))
        client.simSetVehiclePose(pose, True)
        time.sleep(0.001)
        # client.simSetDistortionParam("1","K1",-0.3751)
        # client.simSetDistortionParam("1","K2",-0.1204)
        # client.simSetDistortionParam("2","K1",-0.3751)
        # client.simSetDistortionParam("2","K2",-0.1204)
        responses = client.simGetImages([
            airsim.ImageRequest("0", airsim.ImageType.Scene),
            airsim.ImageRequest("1", airsim.ImageType.Scene),
            airsim.ImageRequest("2", airsim.ImageType.Scene)])

        for i, response in enumerate(responses):
            if response.pixels_as_float:
                print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_float), pprint.pformat(response.camera_position)))
                airsim.write_pfm(os.path.normpath(os.path.join(tmp_dir, str(x) + "_" + str(i) + '.pfm')), airsim.get_pfm_array(response))
            else:
                print("Type %d, size %d, pos %s" % (response.image_type, len(response.image_data_uint8), pprint.pformat(response.camera_position)))
                airsim.write_file(os.path.normpath(os.path.join(tmp_dir, str(i), str(x) + "_" + str(i) + '.png')), response.image_data_uint8)

        #time.sleep(1)

# currently reset() doesn't work in CV mode. Below is the workaround
client.simSetVehiclePose(airsim.Pose(airsim.Vector3r(0, 0, 0), airsim.to_quaternion(0, 0, 0)), True)
