#### 一. 缘起
  因为最近疫情的原因，待在家里实在无聊就又玩起了wow怀旧服，wow是一款非常经典的游戏，里面有一个专业技能叫做钓鱼。因为钓鱼本身比较枯燥，且重复度很高，所以作为一名资深程序员，我决定用代码的方式来解决这个问题。
#### 二. 历程
  最开始的时候，在b站上找了一个wow钓鱼的介绍视频，看了一下大概思路，但是没什么用，里面用的是按键精灵且系统为windows.
  ```
  https://www.bilibili.com/video/av90618144?t=426
  ```
  于是我决定用python实现，因为我比较熟悉python和javascript，而明显这种需求python会更合适,google找代码，最后参考了github上的python2实现的方法
  ```
  https://github.com/kioltk/wow-fishipy
  ```
  进行改造成python3

#### 三. 困难
  1. 觉得大多数的代码都是在windows上的实现的，mac上比较少，但是找到以上跨平台的这段代码就比较容易了。
  2. 安装环境也有一点麻烦，安装pyaudio的时候需要先brew 安装一个环境
  3. 之前用autopy进行的一部分交互，改成了用pyUserInterface
  4. 匹配钓鱼坐标的时候，遇到了问题，cv2.matchTemplate参数进行了改造和调试，这部分还需要优化
  5. 当地点和钓鱼时间切换的石斛，可以用以下代码进行调试
  ```
    # 在原图上画矩形
    cv2.rectangle(img_rgb, top_left, bottom_right, (0, 0, 255), 2)
    # 显示原图和处理后的图像,
    cv2.imshow("template", template)
    cv2.imshow("processed", img_rgb)
    cv2.waitKey()
  ```

#### 四. 总结
  目前，需要换地点的时候，包括白天黑夜环境的切换会影响找到鱼漂的坐标的问题，需要进行截图替换，重新调试，但是总体可以实现，以下是我的代码。
  ```
  https://github.com/codingories/mywowfishing
  ```
#### 最后,个人微信,欢迎交流！
![wechat0.jpg](https://i.loli.net/2020/01/30/mbV7Q3XqxedsJKP.jpg)