import os
import torch
# import torchvision
from torch.autograd import Variable
# import torch.nn as nn
# import torch.nn.functional as F
from torch.utils.data import DataLoader
from torchvision import transforms #, utils
# import torch.optim as optim

import glob

from U2Net.data_loader import RescaleT
from U2Net.data_loader import ToTensorLab
from U2Net.data_loader import SalObjDataset

from U2Net.model import U2NET # full size version 173.6 MB

# For Mac
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

# normalize the predicted SOD probability map
def normPRED(d):
    ma = torch.max(d)
    mi = torch.min(d)

    dn = (d-mi)/(ma-mi)

    return dn


def get_inference_from_images(model_name, images_dir):
    model_dir = os.path.join("U2Net/saved_models/", model_name)
    img_name_list = glob.glob(images_dir + '*')
    prediction = []

# #   --------- 2. dataloader ---------
    test_salobj_dataset = SalObjDataset(img_name_list = img_name_list,
                                        lbl_name_list = [],
                                        transform=transforms.Compose([RescaleT(320),
                                                                      ToTensorLab(flag=0)])
                                        )
    test_salobj_dataloader = DataLoader(test_salobj_dataset,
                                            batch_size=1,
                                            shuffle=False,
                                            num_workers=0)

    if model_name == 'u2net.pth':
        net = U2NET(3, 1)

    net.load_state_dict(torch.load(model_dir, map_location=torch.device('cpu')))
    if torch.cuda.is_available():
        net.cuda()
    net.eval()

    for i_test, data_test in enumerate(test_salobj_dataloader):
        print("Inferencing: ", img_name_list[i_test].split("/")[-1])

        inputs_test = data_test['image']
        inputs_test = inputs_test.type(torch.FloatTensor)

        if torch.cuda.is_available():
            inputs_test = Variable(inputs_test.cuda())
        else:
            inputs_test = Variable(inputs_test)

        d1, d2, d3, d4, d5, d6, d7 = net(inputs_test)

        # normalization
        pred = d1[:,0,:,:]
        pred = normPRED(pred)

        # save results to test_results folder
        #save_output(img_name_list[i_test], pred, prediction_dir)
        prediction.append((img_name_list[i_test], pred))

        del d1,d2,d3,d4,d5,d6,d7
    return prediction