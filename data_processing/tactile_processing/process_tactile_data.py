import os
import numpy as np
from pathlib import Path
import sys

# 添加项目根目录到系统路径
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))  # 只需要向上两级目录
print(project_root)
sys.path.append(project_root)

from Inspire_Hand_FK.FK import inspire_hand_fk

def validate_data(tactile_data, pose_data):
    """
    验证输入数据的有效性
    
    Args:
        tactile_data (numpy.ndarray): 触觉数据
        pose_data (numpy.ndarray): 姿态数据
    
    Raises:
        ValueError: 当数据无效时抛出
    """
    # 检查数据维度
    if tactile_data.shape[1] != 581:
        raise ValueError(f"触觉数据维度错误，应为(x, 581)，当前为{tactile_data.shape}")
    
    if pose_data.shape[1] < 6:
        raise ValueError(f"姿态数据维度不足，需要至少6列，当前为{pose_data.shape[1]}")
    
    # 检查数据帧数匹配
    if tactile_data.shape[0] != pose_data.shape[0]:
        raise ValueError(f"触觉数据和姿态数据的帧数不匹配: {tactile_data.shape[0]} vs {pose_data.shape[0]}")
    
    # 检查数据是否包含无效值
    if np.isnan(tactile_data).any():
        raise ValueError("触觉数据包含NaN值")
    if np.isnan(pose_data).any():
        raise ValueError("姿态数据包含NaN值")

def get_tactile_positions():
    """
    获取触觉传感器阵列的位置信息
    返回一个字典，包含每个触觉像素的位置信息
    """
    # 注意：这些尺寸需要与实际触觉传感器阵列的尺寸完全匹配
    positions = {
        'middle': {
            'tip': (3, 3),      # 3x3
            'finger': (12, 8),  # 12x8
            'palm': (10, 8)     # 10x8
        },
        'index': {
            'tip': (3, 3),      # 3x3
            'finger': (12, 8),  # 12x8
            'palm': (10, 8)     # 10x8
        },
        'thumb': {
            'tip': (3, 3),      # 3x3
            'finger': (12, 8),  # 12x8
            'middle': (3, 3),   # 3x3
            'palm': (12, 8)     # 12x8
        }
    }
    
    # 验证总像素数
    total_pixels = sum(rows * cols for finger in positions.values() 
                      for rows, cols in finger.values())
    if total_pixels != 580:
        raise ValueError(f"触觉传感器阵列总像素数不匹配，应为580，当前为{total_pixels}")
    
    return positions

def get_3d_position(fk_result, finger, part):
    """
    根据FK结果获取指定手指部位的3D坐标
    
    Args:
        fk_result (dict): FK计算的结果
        finger (str): 手指名称 ('middle', 'index', 'thumb')
        part (str): 部位名称 ('tip', 'finger', 'palm', 'middle')
    
    Returns:
        tuple: (x, y, z) 坐标
    """
    try:
        if finger == 'middle':
            finger_points = fk_result['finger_3']  # 中指是finger_3
            if part == 'tip':
                return finger_points[2]  # D点
            elif part == 'finger':
                return (np.array(finger_points[1]) + np.array(finger_points[2])) / 2  # C和D的中点
            elif part == 'palm':
                return (np.array(finger_points[0]) + np.array(finger_points[1])) / 2  # B和C的中点
        elif finger == 'index':
            finger_points = fk_result['finger_2']  # 食指是finger_2
            if part == 'tip':
                return finger_points[2]  # D点
            elif part == 'finger':
                return (np.array(finger_points[1]) + np.array(finger_points[2])) / 2  # C和D的中点
            elif part == 'palm':
                return (np.array(finger_points[0]) + np.array(finger_points[1])) / 2  # B和C的中点
        elif finger == 'thumb':
            thumb_points = fk_result['finger_1']  # 拇指是finger_1
            if part == 'tip':
                return thumb_points[4]  # I点
            elif part == 'finger':
                return (np.array(thumb_points[3]) + np.array(thumb_points[4])) / 2  # H和I的中点
            elif part == 'middle':
                return (np.array(thumb_points[2]) + np.array(thumb_points[3])) / 2  # G和H的中点
            elif part == 'palm':
                return (np.array(thumb_points[1]) + np.array(thumb_points[2])) / 2  # F和G的中点
    except (KeyError, IndexError) as e:
        raise ValueError(f"获取3D位置时出错: {e}")
    return None

def process_tactile_data(tactile_file, pose_file):
    """
    处理触觉数据
    
    Args:
        tactile_file (str): 触觉数据文件路径
        pose_file (str): 姿态数据文件路径
    
    Returns:
        numpy.ndarray: 处理后的数据，形状为 (x, 580, 6)
    """
    # 加载数据
    tactile_data = np.load(tactile_file)
    pose_data = np.load(pose_file)
    
    # 验证数据
    validate_data(tactile_data, pose_data)
    
    num_frames = tactile_data.shape[0]
    
    # 初始化输出数组
    output_data = np.zeros((num_frames, 580, 6))
    
    # 获取触觉传感器位置信息
    positions = get_tactile_positions()
    
    # 处理每一帧数据
    for frame_idx in range(num_frames):
        try:
            # 获取当前帧的触觉数据（不包括时间戳）
            current_tactile = tactile_data[frame_idx, 1:]
            
            # 获取第一帧的触觉数据作为基准
            base_data = tactile_data[0, 1:]
            
            # 计算触觉值（与第一帧的差分）
            tactile_values = current_tactile - base_data
            
            # 获取FK结果（使用pose.npy的后6位数据）
            fk_result = inspire_hand_fk(pose_data[frame_idx, -6:])
            
            # 处理每个触觉像素
            pixel_idx = 0
            for finger in ['middle', 'index', 'thumb']:
                for part, (rows, cols) in positions[finger].items():
                    # 获取3D位置
                    pos_3d = get_3d_position(fk_result, finger, part)
                    if pos_3d is None:
                        raise ValueError(f"无法获取{finger}的{part}部位3D位置")
                    
                    # 处理该部位的所有触觉像素
                    for row in range(rows):
                        for col in range(cols):
                            # T值（触觉值）
                            output_data[frame_idx, pixel_idx, 0] = tactile_values[pixel_idx]
                            
                            # P值（3D位置）
                            output_data[frame_idx, pixel_idx, 1:4] = pos_3d
                            
                            # K值（2D位置）
                            output_data[frame_idx, pixel_idx, 4] = row
                            output_data[frame_idx, pixel_idx, 5] = col
                            
                            pixel_idx += 1
        except Exception as e:
            raise ValueError(f"处理第{frame_idx}帧数据时出错: {e}")
    
    return output_data

def main():
    # 创建输出目录
    output_dir = os.path.join(project_root, "data_processing", "out")
    os.makedirs(output_dir, exist_ok=True)
    
    # 处理所有tactile.npy文件
    data_dir = os.path.join(project_root, "data_processing", "data")
    all_processed = []
    for root, _, files in os.walk(data_dir):
        if "tactile.npy" in files and "pose.npy" in files:
            tactile_path = os.path.join(root, "tactile.npy")
            pose_path = os.path.join(root, "pose.npy")
            print(f"处理文件: {tactile_path}")
            try:
                # 处理数据
                processed_data = process_tactile_data(tactile_path, pose_path)
                all_processed.append(processed_data)
            except Exception as e:
                print(f"处理文件时出错: {e}")
    if all_processed:
        merged = np.concatenate(all_processed, axis=0)
        output_path = os.path.join(output_dir, "tactile.npy")
        np.save(output_path, merged)
        print(f"所有数据已合并并保存到: {output_path}")
    else:
        print("未找到任何可处理的数据文件。")

if __name__ == "__main__":
    main() 