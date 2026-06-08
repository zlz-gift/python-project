"""种子数据脚本 —— 初始化商品、管理员和测试用户（异步版本）"""
import asyncio

from sqlalchemy import select

from app.db.database import engine, Base, AsyncSessionLocal
from app.models.product import Product
from app.models.user import User
from app.core.security import hash_password


async def seed():
    # 创建表
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        # ===================== 用户 =====================
        result = await db.execute(select(User))
        if not result.scalars().first():
            db.add_all([
                User(
                    username="admin",
                    password=hash_password("admin123"),
                    nickname="管理员",
                    role="admin",
                ),
                User(
                    username="test",
                    password=hash_password("test123"),
                    nickname="测试用户",
                    role="user",
                ),
            ])
            await db.commit()
            print("[OK] 用户数据已创建")
        else:
            print("[SKIP] 用户数据已存在，跳过")

        # ===================== 商品 =====================
        result = await db.execute(select(Product))
        if not result.scalars().first():
            products = [
                # ---- 手机数码 ----
                Product(name="iPhone 16 Pro Max 256GB", price=8999.00, stock=120,
                        category="手机数码", image="https://picsum.photos/id/1/400/400",
                        description="6.9英寸 OLED 屏幕 | A18 Pro 芯片 | 钛金属边框 | 4800万像素三摄 | 支持卫星通信"),
                Product(name="华为 Mate 70 Pro", price=6999.00, stock=85,
                        category="手机数码", image="https://picsum.photos/id/2/400/400",
                        description="麒麟 9100 芯片 | 6.8英寸 LTPO 屏幕 | 鸿蒙 NEXT 系统 | 卫星通话 | 星环影像"),
                Product(name="小米 15 Ultra", price=5999.00, stock=200,
                        category="手机数码", image="https://picsum.photos/id/3/400/400",
                        description="骁龙 8 Gen4 | 徕卡光学四摄 | 2K 微曲屏 | 120W 秒充 | 钛金属特别版"),
                Product(name="iPad Air M4 11英寸", price=4799.00, stock=60,
                        category="手机数码", image="https://picsum.photos/id/4/400/400",
                        description="M4 芯片 | Liquid Retina 显示屏 | 支持 Apple Pencil Pro | 全天续航"),
                # ---- 电脑办公 ----
                Product(name="MacBook Pro 16 M4 Max", price=19999.00, stock=45,
                        category="电脑办公", image="https://picsum.photos/id/5/400/400",
                        description="M4 Max 芯片 | 16核 CPU 40核 GPU | 36GB 统一内存 | Liquid Retina XDR | 22小时续航"),
                Product(name="ThinkPad X1 Carbon Gen 12", price=12999.00, stock=30,
                        category="电脑办公", image="https://picsum.photos/id/6/400/400",
                        description="酷睿 Ultra 9 | 14英寸 2.8K OLED | 980克轻至 | 军规级耐用 | 4G LTE 全时互联"),
                Product(name="戴尔 U3224KB 32寸 6K显示器", price=15999.00, stock=15,
                        category="电脑办公", image="https://picsum.photos/id/7/400/400",
                        description="6K分辨率 IPS Black | Thunderbolt 4 | 内置4K摄像头 | 专业级色准"),
                # ---- 家用电器 ----
                Product(name="戴森 V16 无线吸尘器", price=4990.00, stock=100,
                        category="家用电器", image="https://picsum.photos/id/8/400/400",
                        description="激光探测微尘 | 240AW 强劲吸力 | 60分钟续航 | 整机HEPA过滤"),
                Product(name="小米空气净化器 4 Pro", price=1999.00, stock=150,
                        category="家用电器", image="https://picsum.photos/id/9/400/400",
                        description="CADR 500m³/h | 适用60㎡ | OLED触控屏 | 智能联动"),
                Product(name="美的 3匹 新一级变频空调", price=5999.00, stock=80,
                        category="家用电器", image="https://picsum.photos/id/10/400/400",
                        description="新一级能效 | 全直流变频 | 智能WiFi | 高温自清洁"),
                # ---- 服饰鞋包 ----
                Product(name="Nike Air Max Pulse 运动鞋", price=1099.00, stock=300,
                        category="服饰鞋包", image="https://picsum.photos/id/11/400/400",
                        description="Air Max 气垫 | 织物+合成革鞋面 | 耐磨橡胶外底"),
                Product(name="北面 1996 经典羽绒服", price=2998.00, stock=120,
                        category="服饰鞋包", image="https://picsum.photos/id/12/400/400",
                        description="700蓬鹅绒 | 防风防水 | 经典复古款 | RDS认证"),
                Product(name="Coach 经典标志帆布托特包", price=3500.00, stock=40,
                        category="服饰鞋包", image="https://picsum.photos/id/13/400/400",
                        description="经典C标印花 | 牛皮饰边 | 大容量 | 日常通勤"),
                # ---- 食品生鲜 ----
                Product(name="三只松鼠 坚果大礼包 2kg", price=168.00, stock=999,
                        category="食品生鲜", image="https://picsum.photos/id/14/400/400",
                        description="6种坚果组合 | 开心果/巴旦木/腰果/夏威夷果 | 年货送礼"),
                Product(name="阳澄湖大闸蟹礼券 8只装", price=588.00, stock=500,
                        category="食品生鲜", image="https://picsum.photos/id/15/400/400",
                        description="4公4母 | 公蟹≥4两 母蟹≥3两 | 产地直发 | 顺丰冷链"),
                Product(name="蒙牛 特仑苏纯牛奶 250ml*24盒", price=79.90, stock=2000,
                        category="食品生鲜", image="https://picsum.photos/id/16/400/400",
                        description="3.8g优质蛋白/100ml | 限定牧场 | 超高温灭菌"),
                # ---- 美妆个护 ----
                Product(name="雅诗兰黛 小棕瓶精华 50ml", price=960.00, stock=200,
                        category="美妆个护", image="https://picsum.photos/id/17/400/400",
                        description="第七代修护精华 | 夜间深层修护 | 淡化细纹"),
                Product(name="SK-II 神仙水 230ml", price=1370.00, stock=150,
                        category="美妆个护", image="https://picsum.photos/id/18/400/400",
                        description="超过90% PITERA™精华 | 改善毛孔 | 提亮肤色"),
                Product(name="飞利浦 电动牙刷 HX9352", price=799.00, stock=250,
                        category="美妆个护", image="https://picsum.photos/id/19/400/400",
                        description="声波震动 31000次/分 | 5种模式 | 智能计时"),
                # ---- 运动户外 ----
                Product(name="迪卡侬 山地自行车 ST100", price=1299.00, stock=60,
                        category="运动户外", image="https://picsum.photos/id/20/400/400",
                        description="27.5英寸 | 铝合金车架 | 21速变速 | 液压碟刹"),
                Product(name="尤尼克斯 天斧100ZZ 羽毛球拍", price=1680.00, stock=80,
                        category="运动户外", image="https://picsum.photos/id/21/400/400",
                        description="安赛龙同款 | 超级薄拍框 | 增强甜区 | 重头进攻型"),
                Product(name="牧高笛 户外露营帐篷 3-4人", price=899.00, stock=100,
                        category="运动户外", image="https://picsum.photos/id/22/400/400",
                        description="一帐多用 | 防风防雨 | 速开设计 | UPF50+"),
                # ---- 家居家装 ----
                Product(name="网易严选 乳胶床垫 1.8m*2m", price=2599.00, stock=50,
                        category="家居家装", image="https://picsum.photos/id/23/400/400",
                        description="泰国进口天然乳胶 | 7区独立弹簧 | 透气抗菌"),
                Product(name="小米智能门锁 2 Pro", price=1799.00, stock=180,
                        category="家居家装", image="https://picsum.photos/id/24/400/400",
                        description="3D结构光人脸识别 | AI猫眼 | 门铃可视通话"),
            ]
            db.add_all(products)
            await db.commit()
            print(f"[OK] {len(products)} 件商品已创建")
        else:
            print("[SKIP] 商品数据已存在，跳过")

    print("\n种子数据初始化完成!")
    print("   管理员账号: admin / admin123")
    print("   测试账号:   test  / test123")


if __name__ == "__main__":
    asyncio.run(seed())
