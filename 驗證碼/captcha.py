#!/usr/bin/env python
# coding: utf-8

import cv2
import numpy as np
import torch
import torch.nn as nn
from matplotlib import pyplot as plt

import torch._utils
try:
    torch._utils._rebuild_tensor_v2
except AttributeError:
    def _rebuild_tensor_v2(storage, storage_offset, size, stride, requires_grad, backward_hooks):
        tensor = torch._utils._rebuild_tensor(storage, storage_offset, size, stride)
        tensor.requires_grad = requires_grad
        tensor._backward_hooks = backward_hooks
        return tensor
    torch._utils._rebuild_tensor_v2 = _rebuild_tensor_v2



class CNN(nn.Module):
    def __init__(self):
        super(CNN, self).__init__()
        self.conv1 = nn.Sequential(         # input shape (1, 28, 28)
            nn.Conv2d(
                in_channels=3,              # input height
                out_channels=16,            # n_filters
                kernel_size=5,              # filter size
                stride=1,                   # filter movement/step
                padding=2,                  # if want same width and length of this image after Conv2d, padding=(kernel_size-1)/2 if stride=1
            ),                              # output shape (16, 28, 28)
            nn.ReLU(),                      # activation
            nn.MaxPool2d(kernel_size=2),    # choose max value in 2x2 area, output shape (16, 14, 14)
        )
        self.conv2 = nn.Sequential(         # input shape (16, 14, 14)
            nn.Conv2d(16, 32, 5, 1, 2),     # output shape (32, 14, 14)
            nn.ReLU(),                      # activation
            nn.MaxPool2d(2),                # output shape (32, 7, 7)
        )
        self.out = nn.Linear(32 * 7 * 7, 36)   # fully connected layer, output 10 classes

    def forward(self, x):
        x = self.conv1(x)
        x = self.conv2(x)
        x = x.view(x.size(0), -1)           # flatten the output of conv2 to (batch_size, 32 * 7 * 7)
        output = self.out(x)
        return output # return x for visualization

class CAPTCHA():
    def __init__(self, img_file , model_path = './hack.pth'):
        # input image
        #self.file_name = file_name
        self.img = img_file
        # declare DNN model
        self.model = CNN()
        self.model.load_state_dict(torch.load(model_path,map_location='cpu'))
        #self.model = torch.load(model_path)

        # label to class decoder
        self.decoder = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,                   'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',                   'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',                   's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        
        self.img_array = None
        self.gray = None
        
        self.get_img()
        self.rects = self.seperate_letter()
        
    def get_img(self):
        # read image
        #file_name = 'captcha1.jpg'
        #self.img = cv2.imread(self.file_name)

        black = np.asarray([0, 0, 0])
        white = np.asarray([255, 255, 255])

        (row, col, chn) = self.img.shape
        self.img_array = np.array(self.img)

        # remove noise using color threshold
        for r in range(row):
            for c in range(col):
                px = self.img[r][c]
                #0~100, 50~143, 180~255
                if px[0] >= 0 or px[0] <= 100:
                    if px[1] >= 50 and px[1] <= 150:
                        if px[2] >= 180 and px[2] <= 255:
                            self.img_array[r][c] = black
                        else:
                            self.img_array[r][c] = white
                    else:
                        self.img_array[r][c] = white
                else:
                    self.img_array[r][c] = white
        self.gray = cv2.cvtColor(self.img_array, cv2.COLOR_BGR2GRAY)

        
    def seperate_letter(self):
        backup = self.gray.copy()   #taking backup of the input image
        backup = 255 - backup       #color inversion
        #draw_img = self.img_array.copy()
        _, contours, _ = cv2.findContours(backup, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        cts = []
        for i, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            if w*h < 100:
                continue
            cts.append([x, y, x + w, y + h])

        rects = self.check_rec(cts)
        if len(rects) != 5:
            print('Letter detector goes wrong!!!!!!')
        return rects
        
    def is_intersect(self, rect, rect1):
            if rect[0] >= rect1[2] or rect[2] <= rect1[0]:
                return False
            if rect[1] >= rect1[3] or rect[3] <= rect1[1]:
                return False
            return True

    def compare(self, x):
            return x[0]
        
    def check_rec(self, rects):
        letters = []
        for rect in rects:
            intersect = False
            for rect1 in rects:
                if rect == rect1:
                    #if rect not in letters:
                    #    letters.append(rect)
                    continue
                if self.is_intersect(rect, rect1):
                    rect_size = (rect[2] - rect[0])*(rect[3] - rect[1])
                    rect1_size = (rect1[2] - rect1[0])*(rect1[3] - rect1[1])
                    if rect_size > rect1_size:
                        if rect not in letters:
                            letters.append(rect)
                    elif rect_size < rect1_size:
                        if rect1 not in letters:
                            letters.append(rect1)
                    intersect = True
            if not intersect:
                if rect not in letters:
                    letters.append(rect)
        
        letters.sort(key=self.compare)
        return letters

    def classification(self):
        count = 0
        prediction = []
        for rect in self.rects:
            cv2.rectangle(self.img, (rect[0], rect[1]), (rect[2], rect[3]), (0, 0, 255), 2)
            crop_img = self.gray[rect[1]:rect[3], rect[0]:rect[2]]
            row, col= crop_img.shape[:2]
            bottom= crop_img[row-2:row, 0:col]
            mean= cv2.mean(bottom)[0]

            bordersize = 6
            border=cv2.copyMakeBorder(crop_img, bordersize, bordersize, bordersize, bordersize, cv2.BORDER_CONSTANT, value=[255, 255, 255])

            #border = abs(border - 255)
            crop_img = cv2.resize(border, (28, 28))

            crop_img = cv2.cvtColor(crop_img,cv2.COLOR_GRAY2RGB)
            crop_img = np.transpose(crop_img, (2, 0, 1))
            crop_img = np.expand_dims(crop_img, axis=0)
            x = torch.tensor(crop_img).type('torch.FloatTensor')
            output = self.model(x)
            pred_y = torch.max(output, 1)[1].cpu().data.numpy()
            prediction.append(self.decoder[int(pred_y)])
            count = count + 1
        #plt.imshow(cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB))
        #plt.title('image')
        #plt.show()
        return prediction

#captcha = CAPTCHA(file_name = 'captcha2.jpg')

#prediction = captcha.classification()
#print('Prediction: ', prediction)
