#!/usr/bin/python3
# -*- coding: UTF-8 -*-

# Created by Mario Chen, 04.01.2021, Shenzhen
# My Github site: https://github.com/Mario-Hero

import sys
import os
import hashlib
# import datefinder

try:
    import cv2
except ImportError:
    os.system('pip install opencv-python')
    import cv2

import numpy as np


# you can edit this >>>>>>
MAX_HASH_SIZE = 100  # MB. Set it to 0 to disable MAX_HASH_SIZE.
DELETE_VIDEO_WITH_SAME_CONTENT = True
# <<<<<< you can edit this


MAX_HASH_TIME = MAX_HASH_SIZE * 128

SHOULD_NOT_DELETE = ['.ini', '.dll', '.exe']
VIDEO_SUPPORT = ['mp4', 'webm', 'avi', 'mov', '.mkv', '.wmv', '.m3u8', '.3g2', '.3gp', '.3gp2', '.3gpp', '.amv', '.asf',
                 '.bik','.divx', '.drc', '.dv', '.f4v', '.flv', '.gvi', '.gxf', '.m1v', '.m2v', '.m2t', '.m2ts',
                 '.m4v', '.mp2', '.mp4v', '.mpe', '.mpeg', '.mpeg1', '.mpeg2', '.mpeg4', '.mpg', '.mpv2', '.mts',
                 '.mxf', '.mxg', '.nsv', '.nuv', '.ogg', '.ogm', '.ogv', '.ps', '.rec', '.rm', '.rmvb', '.rpl', '.thp',
                 '.tod', '.ts', '.tts', '.txd', '.vob', '.vro', '.wm', '.wtv', '.xesc']
VIDEO_CUTTIME = 3


def canDelete(fileName):
    for keepStr in SHOULD_NOT_DELETE:
        if fileName.endswith(keepStr):
            return False
    return True


def getVidLength(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num = cap.get(7)
        duration = frame_num / rate
        return duration
    return -1


def captureFrame(vidPath):
    vidCapture = cv2.VideoCapture(vidPath)
    if vidCapture.isOpened():
        frameNumber = vidCapture.get(7)
    else:
        return False
    frames = []
    for i in range(1, VIDEO_CUTTIME + 1):
        vidCapture.set(cv2.CAP_PROP_POS_MSEC, int((frameNumber / VIDEO_CUTTIME + 1) * i))
        # print("f: "+str(int((frameNumber/cutTime)*i)))
        success, image = vidCapture.read()
        if success:
            resized = cv2.resize(image, (150, 150), interpolation=cv2.INTER_NEAREST)
            # resized = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
            frames.append(resized)
        else:
            return ''
    return frames


def create_rgb_hist(image):
    h, w, c = image.shape
    # 创建一个（16*16*16,1）的初始矩阵，作为直方图矩阵
    # 16*16*16的意思为三通道每通道有16个bins
    rgbhist = np.zeros([16 * 16 * 16, 1], np.float32)
    bsize = 256 / 16
    for row in range(h):
        for col in range(w):
            b = image[row, col, 0]
            g = image[row, col, 1]
            r = image[row, col, 2]
            index = int(b / bsize) * 16 * 16 + int(g / bsize) * 16 + int(r / bsize)
            rgbhist[int(index), 0] += 1
    return rgbhist


class videoStruct:
    def __init__(self, fileName='', path=''):
        self.name = fileName  # name without extension
        self.path = path  # complete path
        self.date = None  # date in the name of file
        self.size = 0
        self.md5: str = ''
        self.length: float = 0.0
        self.frames = None

    def updateNormal(self):
        '''
        self.size = os.path.getsize(self.path)
        try:
            dateMatches = list(datefinder.find_dates(self.name))
            if len(dateMatches) > 0:
                self.date = dateMatches[0]
        except:
            pass
            '''
        self.length = getVidLength(self.path)

    def printInfo(self):
        print('Name: ' + self.name)
        print('Date: ' + str(self.date))
        print('Size: ' + str(self.size))
        print('Length: ' + str(self.length))


def isVid(fileName: str):
    for ext in VIDEO_SUPPORT:
        if fileName.endswith(ext):
            return True
    return False


def videoFrameCompare(vid1: videoStruct, vid2: videoStruct) -> float:
    if not vid1.frames:
        vid1.frames = captureFrame(vid1.path)
    if not vid2.frames:
        vid2.frames = captureFrame(vid2.path)
    result: float = 0.0
    if vid1.frames and vid2.frames:
        for i in range(len(vid1.frames)):
            hist1 = create_rgb_hist(vid1.frames[i])
            hist2 = create_rgb_hist(vid2.frames[i])
            oneResult = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
            if oneResult < 0.9:
                return oneResult
            # print(oneResult)
            result += oneResult
    result = result / VIDEO_CUTTIME
    return result


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    hashI = 0
    while hashI < MAX_HASH_TIME or MAX_HASH_TIME <= 0:
        b = f.read(8192)
        if not b:
            break
        myhash.update(b)
        hashI += 1
    f.close()
    return myhash.hexdigest()


def lengthClose(a, b):
    return abs(a - b) < 0.4


def sizeShow(size):
    SIZE_STR = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    i = 0
    while size > 1024:
        size /= 1024
        i += 1
    return '(' + str(round(size,1)) + SIZE_STR[i] + ')'


def deleteDuplicate(folder):
    sizeList = []
    fileList = os.listdir(folder)
    fileI = 0
    fileListLength = len(fileList)
    while fileI < fileListLength:
        if os.path.isdir(os.path.join(folder, fileList[fileI])):
            deleteDuplicate(os.path.join(folder, fileList[fileI]))
            fileList.pop(fileI)
            fileListLength = fileListLength - 1
        else:
            sizeList.append(os.path.getsize(os.path.join(folder, fileList[fileI])))
            fileI = fileI + 1
    print(folder)
    print('Size testing...')
    i = 0
    while i < fileListLength - 1:
        j = i + 1
        while j < fileListLength:
            if sizeList[i] == sizeList[j]:
                if canDelete(os.path.join(folder, fileList[i])) and canDelete(os.path.join(folder, fileList[j])):
                    if GetFileMd5(os.path.join(folder, fileList[i])) == GetFileMd5(os.path.join(folder, fileList[j])):
                        name1 = os.path.splitext(fileList[i])[0]
                        name2 = os.path.splitext(fileList[j])[0]
                        if name1.startswith(name2):
                            removeJ = False
                        elif name2.startswith(name1):
                            removeJ = True
                        else:
                            removeJ = len(name1) < len(name2)
                        fileListLength = fileListLength - 1
                        if removeJ:
                            os.remove(os.path.join(folder, fileList[j]))
                            print("Keep: " + fileList[i])
                            print("Remove same: " + fileList[j] + '\n')
                            fileList.pop(j)
                            sizeList.pop(j)
                            continue
                        else:
                            os.remove(os.path.join(folder, fileList[i]))
                            print("Keep: " + fileList[j])
                            print("Remove same: " + fileList[i] + '\n')
                            fileList.pop(i)
                            sizeList.pop(i)
                            i -= 1
                            break
            j += 1
        i += 1
    if DELETE_VIDEO_WITH_SAME_CONTENT:
        fileList = os.listdir(folder)
        videoList: list[videoStruct] = []
        for file in fileList:
            if isVid(file):
                videoList.append(videoStruct(os.path.splitext(file)[0], os.path.join(folder, file)))
        for struct in videoList:
            struct.updateNormal()
            # struct.printInfo()
        print('Video Content testing...')
        fileListLength = len(videoList)
        i = 0
        while i < fileListLength - 1:
            j = i + 1
            while j < fileListLength:
                if lengthClose(videoList[i].length, videoList[j].length):
                    #print('\nCompare:')
                    #print(videoList[i].name)
                    #print(videoList[j].name)
                    result = videoFrameCompare(videoList[i], videoList[j])
                    if 0.5 < result < 0.99:
                        print('Warning:')
                        print(videoList[i].name + '\n' + videoList[j].name)
                        print('Similarity: ' + str(result) + '\n')
                    elif result > 0.99:
                        if videoList[i].size == 0:
                            videoList[i].size = os.path.getsize(videoList[i].path)
                        if videoList[j].size == 0:
                            videoList[j].size = os.path.getsize(videoList[j].path)
                        removeJ = videoList[i].size > videoList[j].size  # Keep the bigger video.
                        fileListLength -= 1
                        if removeJ:
                            os.remove(videoList[j].path)
                            print('Keep   ' + sizeShow(videoList[i].size) + ': ' + videoList[i].name)
                            print('Remove ' + sizeShow(videoList[j].size) + ': ' + videoList[j].name + '\n')
                            videoList.pop(j)
                            continue
                        else:
                            os.remove(videoList[i].path)
                            print('Keep   ' + sizeShow(videoList[j].size) + ': ' + videoList[j].name)
                            print('Remove ' + sizeShow(videoList[i].size) + ': ' + videoList[i].name + '\n')
                            videoList.pop(i)
                            i -= 1
                            break
                j += 1
            i += 1


if __name__ == '__main__':
    for inputFolder in sys.argv[1:]:
        deleteDuplicate(inputFolder)
    os.system("pause")
