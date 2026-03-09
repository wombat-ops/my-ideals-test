import os
import json

# ================= 配置区域 =================
# 映射表建议保持在脚本中，作为你的“数据库”
MEMBER_MAP = {
    "1": ["takai-rika", "高井俐香"],
    "2": ["ota-mitsuki", "大田美月"],
    "3": ["kamimura-hinano", "上村ひなの"]
}

POSE_MAP = {
    "1": ["yori", "より"],
    "2": ["chuu", "チュウ"],
    "3": ["hiki", "ヒキ"],
    "4": ["suwari", "スワリ"],
    "5": ["yori-b", "より-B"],
    "6": ["chuu-b", "チュウ-B"],
    "7": ["hiki-b", "ヒキ-B"],
    "8": ["suwari-b", "スワリ-B"]
}

JSON_FILE = "hinatazaka46.json" # 你要维护的唯一主文件
ROOT_URL = "https://raw.githubusercontent.com/wombat-ops/my-ideals-test/main/resources/"
# ==========================================

def update_task():
    # 1. 读取/初始化 JSON 结构
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {"magic": "my-ideals-template", "members": [], "collections": [], 
                "imageBaseUrl": {"root": ROOT_URL, "format": "webp"}}

    # 2. 获取系列信息
    series_id = input("请输入系列ID (如 2025-santa): ").strip()
    series_name = input("请输入系列名称 (如 2025圣诞): ").strip()
    m_input = input("请输入成员编号 (如 1,2): ").strip()
    selected_nums = [n.strip() for n in m_input.split(",")]

    new_items = []
    target_dir = os.path.join("resources", series_id)
    os.makedirs(target_dir, exist_ok=True)

    print("\n[开始扫描并处理图片...]")

    for num in selected_nums:
        if num in MEMBER_MAP:
            m_en, m_cn = MEMBER_MAP[num]
            
            # 更新全局 members 列表
            if not any(m['id'] == m_en for m in data['members']):
                data['members'].append({"id": m_en, "name": m_cn})
            
            # 动态探测：只处理 images 文件夹中实际存在的图片
            for p_num, p_info in POSE_MAP.items():
                p_en, p_cn = p_info
                old_name = f"{num}-{p_num}.webp"
                old_path = os.path.join("images", old_name)
                
                # 只有文件存在时，才生成 JSON 条目并移动文件
                if os.path.exists(old_path):
                    # 构造 ID：为了方便管理，建议保留系列前缀，或根据你之前的要求只留 ID
                    item_id = f"{m_en}-{p_en}" 
                    
                    new_items.append({
                        "id": item_id,
                        "member": m_en,
                        "name": f"{m_cn} {p_cn}"
                    })
                    
                    # 移动并重命名图片到指定文件夹
                    new_path = os.path.join(target_dir, f"{m_en}-{p_en}.webp")
                    os.rename(old_path, new_path)
                    print(f"✅ 处理成功: {old_name} -> {new_path}")

    # 3. 更新 Collection
    col = next((c for c in data["collections"] if c["id"] == series_id), None)
    if col:
        col["items"] = new_items
        col["name"] = series_name
    else:
        data["collections"].append({"id": series_id, "name": series_name, "items": new_items})

    # 4. 保存 JSON
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n[任务完成] JSON 已更新，图片已转移至 resources/{series_id}")

if __name__ == "__main__":
    update_task()