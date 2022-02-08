# toolDeleteDuplicate 重复文件删除脚本

能删除完全相同的文件和内容重复但画质较差的视频的Python脚本。

A Python script which can delete duplicate files, and videos with same content but lower image quality.

## 依赖 Dependency 

Python 3.5+

pyopencv

## 用法 Usage

toolDeleteDuplicate.py：拖入文件夹，即会删除该文件夹下的重复文件和重复但低画质的视频。

toolDeleteInDifferentFolder.py：拖入数个文件夹，按指示输入要保留的文件所在的文件夹编号，即可跨文件夹删除重复文件和重复但低画质的视频。对于有些相似的视频，该脚本会输出警告，但不会做任何操作。

toolDeleteDuplicate.py : Drag and drop a folder into the script, which will delete duplicate files and duplicate but low-quality videos in that folder.

toolDeleteInDifferentFolder.py : Drag and drop several folders into the script, and follow the instructions to enter the folder number of the folder which contains files you want to keep, this script will delete duplicate files and duplicate but low-quality videos across folders.For some similar videos, the script will output a warning, but will do nothing.

## 原理 Principles

删除相同文件：首先判断大小是否相同，然后判断哈希值是否相同。

删除内容重复但画质较差的视频：首先判断视频时长是否相同，然后用OpenCV截取视频的几帧，获取直方图相似度，大于0.99的则判为相同视频，然后删除文件大小较小的视频。

Delete the same file: First determine whether the size is the same, then determine whether their hash values are the same. 

Delete videos with duplicate content but lower image quality: First determine whether the length of video is the same, then use OpenCV to capture some frames of the video to obtain the similarity of the histogram. Videos whose similarity larger than 0.99 will be judged as the same video, and then delete the video with smaller file size.

## 删除顺序 Delete which?

删除相同文件：

1. toolDeleteDuplicate.py：

   对于 abcdefg.mp4 和 abcdefg(1).mp4类型，即一个文件的文件名包含在另一个文件的文件名中，删除abcdefg(1).mp4，即文件名较长的文件。对于其他情况，删除文件名较短的文件。

2. toolDeleteInDifferentFolder.py：

   若文件不在需要保留的文件夹下，则删除之。若在，则删除另一个文件。如果两个文件都在需要保留的文件夹下，则按toolDeleteDuplicate.py的方法删除。

删除内容重复但画质较差的视频：

1. toolDeleteDuplicate.py：

   删除文件较小的视频。

2. toolDeleteInDifferentFolder.py：

   删除文件较小的视频。若文件不在需要保留的文件夹下，则删除之。若在，则删除之，并把另一个文件移动到需要保留的文件夹下。

Delete the same file：

 1. toolDeleteDuplicate.py：

    For "abcdefg.mp4 and abcdefg(1).mp4" case, which the file name of one file is included in the file name of another file, delete abcdefg(1). mp4, that is, delete the file with the longer file name. For the other cases, delete the file with the shorter file name.

 2. toolDeleteInDifferentFolder.py：

    If the file is not in the folder that needs to be kept, delete it. If it is, delete another file. If both files are in the folder that needs to be kept, use toolDeleteDuplicate. py's method to delete. 

 Delete videos with duplicate content but lower image quality：

 1. toolDeleteDuplicate.py：

    Delete videos with smaller file sizes. 

 2. toolDeleteInDifferentFolder.py：

    Delete videos with smaller file sizes. If the file is not in the folder that needs to be kept, delete it. If it is, delete it and move another file to the folder that needs to be kept.

## 参数 Parameters 

MAX_HASH_SIZE = 100: 计算哈希值的最大大小。单位为MB. 由于大文件读取耗时较久，所以只读取文件的一部分即可（有可能出问题，但概率极小）。 

DELETE_VIDEO_WITH_SAME_CONTENT = True: 若为真，则删除同样内容但画质较差的视频。

MAX_HASH_SIZE = 100: The maximum size of file to calculate  the hash value. The unit is MB.  Since it takes a long time to read large files, only read a part of the file would be better (This may go wrong, but the probability is very small).   DELETE_VIDEO_WITH_SAME_CONTENT = True: If true, delete videos with the same content but lower image quality.

## License

The project is released under MIT License.
