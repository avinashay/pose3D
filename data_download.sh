wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_label_2.zip -P ./data/
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_2.zip -P ./data/
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_image_3.zip -P ./data/
wget https://s3.eu-central-1.amazonaws.com/avg-kitti/data_object_calib.zip -P ./data/

#unzip files
unzip ./data/data_object_label_2.zip -d ./data/
unzip ./data/data_object_image_2.zip -d ./data/
unzip ./data/data_object_image_3.zip -d ./data/
unzip ./data/data_object_calib.zip -d ./data/

#delete zip files
rm ./data/data_object_label_2.zip
rm ./data/data_object_image_2.zip
rm ./data/data_object_image_3.zip
rm ./data/data_object_calib.zip