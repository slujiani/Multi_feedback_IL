import math
from angle import angle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class FourFingerKinematics:
    def __init__(self, B, C, D, label):
        """
        AB: AB段长度
        B, C, D: 三个点的坐标，格式为[x, y, z]
        label: 整型，2~5，表示食指到小指
        """
        self.AB = B[1]
        self.B = B
        self.C = C
        self.D = D
        self.label = label
        # 计算BC和CD长度
        self.BC = math.sqrt((C[0]-B[0])**2 + (C[1]-B[1])**2 + (C[2]-B[2])**2)
        self.CD = math.sqrt((D[0]-C[0])**2 + (D[1]-C[1])**2 + (D[2]-C[2])**2)

    def getPosition(self, nums):
        """
        angle_B: B点处的弯折角度（弧度）
        angle_C: C点处的弯折角度（弧度）
        返回：B, C, D三点的坐标，格式为[[x, y, z], [x, y, z], [x, y, z]]
        """
        angle_B,angle_C = angle(nums,self.label)
        # B点
        B = self.B
        # C点
        x_C = B[0]
        y_C = B[1] + self.BC * math.cos(math.pi - angle_B)
        z_C = B[2] + self.BC * math.sin(math.pi - angle_B)
        C = [x_C, y_C, z_C]
        # D点
        x_D = x_C
        y_D = y_C + self.CD * math.cos(2 * math.pi - angle_B - angle_C)
        z_D = z_C + self.CD * math.sin(2 * math.pi - angle_B - angle_C)
        D = [x_D, y_D, z_D]
        return [B, C, D]

class ThumbKinematics:
    def __init__(self, E, F, G, H, I):
        """
        E, F, G, H, I: 五个点的坐标 [x, y, z]
        """
        self.label = 1
        self.E = E
        self.F = F
        # 计算各段长度
        self.EF = math.sqrt((F[0]-E[0])**2 + (F[1]-E[1])**2 + (F[2]-E[2])**2)
        self.FG = math.sqrt((G[0]-F[0])**2 + (G[1]-F[1])**2 + (G[2]-F[2])**2)
        self.GH = math.sqrt((H[0]-G[0])**2 + (H[1]-G[1])**2 + (H[2]-G[2])**2)
        self.HI = math.sqrt((I[0]-H[0])**2 + (I[1]-H[1])**2 + (I[2]-H[2])**2)

    def getPosition(self, nums):
        """
        nums: 输入的数值列表
        角度通过angle(nums, self.label)获取
        """
        # 获取四个角度
        angle_F, angle_G, angle_H, angle_E = angle(nums, self.label)
        E = self.E
        F = self.F
        # F点
        YF = F[1]
        XF = E[0] - self.EF * math.cos(angle_E)
        ZF = E[2] + self.EF * math.sin(angle_E)
        F = [XF, YF, ZF]
        # G点
        YG = YF + self.FG * math.cos(math.pi - angle_F)
        GverticalFJ = self.FG * math.sin(math.pi - angle_F)
        XG = XF - GverticalFJ * math.cos(angle_E)
        ZG = ZF + GverticalFJ * math.sin(angle_E)
        G = [XG, YG, ZG]
        # H点
        YH = YG + self.GH * math.cos(angle_G - angle_F)
        HverticalFJ = GverticalFJ + self.GH * math.sin(angle_G - angle_F)
        XH = XF - HverticalFJ * math.cos(angle_E)
        ZH = ZF + HverticalFJ * math.sin(angle_E)
        H = [XH, YH, ZH]
        # I点
        YI = YH + self.HI * math.cos(angle_H + angle_G - angle_F - math.pi)
        IverticalFJ = HverticalFJ + self.HI * math.sin(angle_H + angle_G - angle_F - math.pi)
        XI = XF - IverticalFJ * math.cos(angle_E)
        ZI = ZF + IverticalFJ * math.sin(angle_E)
        I = [XI, YI, ZI]
        return [E, F, G, H, I]
    
class HandKinematics:
    def __init__(self, fingers, thumb):
        """
        fingers: 四指对象列表（FourFingerKinematics实例列表）
        thumb: 拇指对象（ThumbKinematics实例）
        """
        self.fingers = fingers
        self.thumb = thumb

    def getAllPositions(self, nums):
        """
        nums: 输入的数值列表
        返回所有手指（含拇指）的关键点坐标，格式为字典
        """
        result = {}
        result['finger_1'] = self.thumb.getPosition(nums)
        for i, finger in enumerate(self.fingers, start=2):
            result[f'finger_{i}'] = finger.getPosition(nums)
        
        return result

def plot_hand(hand_points_dict):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # 绘制所有五指
    for i in range(1, 6):
        key = f'finger_{i}'
        points = hand_points_dict[key]
        xs, ys, zs = zip(*points)
        ax.plot(xs, ys, zs, marker='o', label=key)

    # 手掌连线：E1E2,E2E3,E3E4,E4E5,E5O,E1O
    E1 = hand_points_dict['finger_1'][0]
    E2 = hand_points_dict['finger_2'][0]
    E3 = hand_points_dict['finger_3'][0]
    E4 = hand_points_dict['finger_4'][0]
    E5 = hand_points_dict['finger_5'][0]
    O = [0, 0, 0]
    palm_points = [E1, E2, E3, E4, E5, O, E1]
    xs, ys, zs = zip(*palm_points)
    ax.plot(xs, ys, zs, color='red', marker='x', label='palm')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.legend()

    # 设置3D坐标轴等比例
    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()
    x_range = abs(x_limits[1] - x_limits[0])
    y_range = abs(y_limits[1] - y_limits[0])
    z_range = abs(z_limits[1] - z_limits[0])
    max_range = max(x_range, y_range, z_range)
    x_middle = sum(x_limits) / 2
    y_middle = sum(y_limits) / 2
    z_middle = sum(z_limits) / 2
    ax.set_xlim3d([x_middle - max_range/2, x_middle + max_range/2])
    ax.set_ylim3d([y_middle - max_range/2, y_middle + max_range/2])
    ax.set_zlim3d([z_middle - max_range/2, z_middle + max_range/2])

    plt.show()

def inspire_hand_fk(nums):
    fingers = [
        FourFingerKinematics(
            B=[32.15, 156.63, 0.56],  # E2
            C=[32.15, 189.65, 3.71],  # F2
            D=[32.15, 241.4, 12.34],  # G2
            label=2
        ),
        FourFingerKinematics(
            B=[10.45, 157, 0.56],     # E3
            C=[10.45, 189.65, 3.41],  # F3
            D=[10.45, 245.4, 13.36], # G3
            label=3
        ),
        FourFingerKinematics(
            B=[-11.08, 156.49, 0.56], # E4
            C=[-11.08, 189.07, 3.71], # F4
            D=[-11.08, 241.18, 12.34],# G4
            label=4
        ),
        FourFingerKinematics(
            B=[-32.53, 152.96, 0.56], # E5
            C=[-32.53, 185.4, 3.72],  # F5
            D=[-32.53, 227.53, 10.31],# G5
            label=5
        )
    ]

    # 拇指初始化
    thumb = ThumbKinematics(
        E=[26.9, 68.9, 21.01],       # E1
        F=[29.87, 72.1, 30.56],      # F1
        G=[38.59, 100.66, 58.59],    # G1
        H=[42.06, 119.44, 69.75],    # H1
        I=[44.06, 151.26, 76.16]     # I1
    )

    # 手的整体初始化
    hand = HandKinematics(fingers, thumb)
    return hand.getAllPositions(nums)

if __name__ == '__main__':
    # from FK import FourFingerKinematics, ThumbKinematics, HandKinematics

    # 四指初始化
    fingers = [
        FourFingerKinematics(
            B=[32.15, 156.63, 0.56],  # E2
            C=[32.15, 189.65, 3.71],  # F2
            D=[32.15, 241.4, 12.34],  # G2
            label=2
        ),
        FourFingerKinematics(
            B=[10.45, 157, 0.56],     # E3
            C=[10.45, 189.65, 3.41],  # F3
            D=[10.45, 245.4, 13.36], # G3
            label=3
        ),
        FourFingerKinematics(
            B=[-11.08, 156.49, 0.56], # E4
            C=[-11.08, 189.07, 3.71], # F4
            D=[-11.08, 241.18, 12.34],# G4
            label=4
        ),
        FourFingerKinematics(
            B=[-32.53, 152.96, 0.56], # E5
            C=[-32.53, 185.4, 3.72],  # F5
            D=[-32.53, 227.53, 10.31],# G5
            label=5
        )
    ]

    # 拇指初始化
    thumb = ThumbKinematics(
        E=[26.9, 68.9, 21.01],       # E1
        F=[29.87, 72.1, 30.56],      # F1
        G=[38.59, 100.66, 58.59],    # G1
        H=[42.06, 119.44, 69.75],    # H1
        I=[44.06, 151.26, 76.16]     # I1
    )

    # 手的整体初始化
    hand = HandKinematics(fingers, thumb)
    plot_hand(hand.getAllPositions([1000]*6))