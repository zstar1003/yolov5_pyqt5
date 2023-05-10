## yolov5_pyqt5

这是一个使用pyqt5搭建YOLOv5目标检测可视化程序。

项目采用了极简设计，以便读者可以基于此界面进行二次开发。

主要功能：加载单图/选择模型/图像检测/视频检测

项目界面：

![image-20220821211811729](Assets/show.png)

# 使用方式
1.安装Cuda、Cudnn

根据自己设备GPU型号选择合适版本进行安装。

2.安装torch、torchvision

- torch版本：1.7.1
- torchvision版本：0.8.2

在[此处](https://download.pytorch.org/whl/torch_stable.html)根据Cuda版本选择合适的文件下载安装

3.安装剩余模块其它依赖

```
pip install -r requriements.txt
```

4.运行main.py即可看到显示界面
 
## Star History

如果此项目对你有所帮助，请给项目点个star

如果有任何问题，均可在此仓库中提出issue

![Stargazers over time](https://starchart.cc/zstar1003/yolov5_pyqt5.svg)
