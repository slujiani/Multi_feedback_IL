import math

def angle(nums,label):
    if label != 1:
        index = 5 - label
        num = nums[index]
        delta = -5*10**(-10)*num**3 + 9*10**(-7)*num**2 - 0.0018*num + 1.4191
        angle1 = math.radians(173.95) - delta
        angle1_A = math.degrees(angle1)
        angle2_A = 1.0843 * angle1_A - 8.2534
        angle2 = math.radians(angle2_A)
        # 四指弯曲主动、从动
        return angle1,angle2
    
    else:
        index = 5
        num = nums[index]
        delta = -0.0012*num + 1.1641
        angle1 = math.radians(164.95) - delta
        
        index = 4
        num = nums[index]
        delta = 8*10**(-11)*num**3 -4*10**(-8)*num**2 - 0.0006*num + 0.5869
        angle2 = math.radians(55.9) - delta
        angle2_A = math.degrees(angle2)
        angle3_A = 0.8024*angle2_A + 138.97
        angle3 = math.radians(angle3_A)

        angle4_A = 0.9487*angle3_A + 3.5511
        angle4 = math.radians(angle4_A)
        angle2_A = 180 - angle2_A
        angle2 = math.radians(angle2_A)

        return angle2,angle3,angle4,angle1
        

if __name__ == "__main__":
    nums = [0,0,0,0,1000,1000]
    label = 1
    angle1,angle2,angle3,angle4 = angle(nums,label)
    print(math.degrees(angle1), math.degrees(angle2), math.degrees(angle3), math.degrees(angle4))