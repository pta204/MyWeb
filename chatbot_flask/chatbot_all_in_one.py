from flask import Flask, request, jsonify, Response

# Khởi tạo ứng dụng Flask
app = Flask(__name__)

import os # Thêm thư viện os

#====================================================================
# PHẦN 0: CẤU HÌNH BẢO MẬT
#====================================================================
# NEW: Lấy API Key từ biến môi trường.
# Nếu không tìm thấy, nó sẽ dùng key mặc định (chỉ dành cho lúc chạy ở máy bạn).
SECRET_API_KEY = os.environ.get('SECRET_API_KEY', 'local-secret-key-for-testing')
#====================================================================
# PHẦN 0: CẤU HÌNH BẢO MẬT
SECRET_API_KEY = "MySuperSecretChatbotKey123!@#"


#====================================================================
# PHẦN 1: DỮ LIỆU THỰC ĐƠN (ĐÃ CẬP NHẬT HƯỚNG DẪN NẤU ĂN)
#====================================================================
THUC_DON_MAU = {
    "giảm cân": {
        "mô tả": "Thực đơn này tập trung vào việc giảm calo nhưng vẫn đảm bảo đủ chất, giàu protein và chất xơ để bạn no lâu hơn.",
        "calo_ước_tính": "1500-1700 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "2 trứng luộc và 1 quả táo. (250 kcal)", "Trưa": "Ức gà luộc (150g) với salad rau xanh. (400 kcal)", "Tối": "Cá diêu hồng hấp gừng (200g) và rau củ luộc. (500 kcal)", "Hướng dẫn": "<b>Trứng luộc:</b> Luộc sôi trong 8-10 phút. <b>Ức gà luộc:</b> Luộc với vài lát gừng cho thơm. <b>Cá hấp gừng:</b> Khứa nhẹ cá, hấp với gừng thái sợi, hành lá và một chút nước tương."},
            "Thứ Ba": {"Sáng": "Yến mạch (40g) nấu với sữa tươi không đường và chuối. (350 kcal)", "Trưa": "Thịt bò xào bông cải xanh (100g thịt). (450 kcal)", "Tối": "Canh bí đao nấu tôm (100g tôm) và cơm gạo lứt. (400 kcal)", "Hướng dẫn": "<b>Yến mạch:</b> Cho yến mạch và sữa vào nồi, đun nhỏ lửa 5 phút đến khi đặc lại. <b>Bò xào:</b> Ướp bò với tỏi, xào nhanh trên lửa lớn rồi cho bông cải xanh đã luộc sơ vào đảo đều."},
            "Thứ Tư": {"Sáng": "Sữa chua không đường với các loại hạt và quả mọng. (300 kcal)", "Trưa": "Cơm gạo lứt, đậu phụ nhồi thịt sốt cà chua. (500 kcal)", "Tối": "Salad cá ngừ và rau củ. (450 kcal)", "Hướng dẫn": "<b>Đậu phụ nhồi thịt:</b> Trộn thịt băm với mộc nhĩ, nhồi vào đậu phụ rồi đem hấp hoặc chiên bằng nồi chiên không dầu. Sốt cà chua phi thơm, cho đậu vào rim nhỏ lửa."},
            "Thứ Năm": {"Sáng": "Phở gà (ít bánh, nhiều thịt và rau). (400 kcal)", "Trưa": "Thịt heo luộc (150g) cuốn bánh tráng rau sống. (500 kcal)", "Tối": "Súp lơ trắng nấu ức gà. (400 kcal)", "Hướng dẫn": "<b>Thịt heo luộc:</b> Luộc thịt ba chỉ với một ít hành khô cho thơm. <b>Súp lơ nấu gà:</b> Xào gà cho săn, đổ nước vào đun sôi rồi cho súp lơ vào nấu chín tới."},
            "Thứ Sáu": {"Sáng": "Bánh mì đen kẹp trứng ốp la và rau. (350 kcal)", "Trưa": "Cá basa kho tộ (150g) và canh rau. (550 kcal)", "Tối": "Mực hấp gừng và salad dưa chuột. (450 kcal)", "Hướng dẫn": "<b>Cá kho tộ:</b> Ướp cá với nước mắm, tiêu, hành. Thắng một ít nước màu rồi cho cá vào kho nhỏ lửa. <b>Mực hấp:</b> Mực làm sạch, cắt khoanh, hấp với gừng thái sợi khoảng 7-10 phút."},
            "Thứ Bảy": {"Sáng": "Sinh tố bơ và cải bó xôi (không đường). (300 kcal)", "Trưa": "Bún thịt nướng (hạn chế bún, nhiều rau). (500 kcal)", "Tối": "Đậu hũ non hấp trứng và tôm. (400 kcal)", "Hướng dẫn": "<b>Thịt nướng:</b> Thịt nạc vai thái mỏng, ướp sả, tỏi, nước mắm rồi nướng. <b>Đậu hũ hấp:</b> Đánh tan trứng, nêm gia vị, cho tôm và đậu hũ non vào rồi đem hấp cách thủy 15 phút."},
            "Chủ Nhật": {"Sáng": "Cháo yến mạch nấu với trứng và nấm. (350 kcal)", "Trưa": "Lẩu nấm ăn kèm bún và thịt bò. (600 kcal)", "Tối": "Ăn nhẹ với salad trái cây và sữa chua. (300 kcal)", "Hướng dẫn": "<b>Cháo yến mạch:</b> Nấu yến mạch với nước cho nở, sau đó cho nấm đã xào và trứng đã đánh tan vào khuấy đều."}
        }
    },
    "tăng cân lành mạnh": {
        "mô tả": "Thực đơn này tập trung vào việc tạo ra thặng dư calo từ các nguồn thực phẩm bổ dưỡng, giàu năng lượng để giúp bạn tăng cân một cách khỏe mạnh.",
        "calo_ước_tính": "2800-3200 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Yến mạch (80g) nấu sữa nguyên kem, chuối, hạt óc chó, mật ong. (700 kcal)", "Trưa": "Cơm trắng (2 chén), thịt kho trứng (2 quả, 100g thịt). (850 kcal)", "Tối": "Cơm (1.5 chén), đùi gà chiên mắm (200g). (800 kcal)", "Phụ": "Sinh tố bơ chuối và bơ đậu phộng. (500 kcal)", "Hướng dẫn": "<b>Thịt kho trứng:</b> Thắng nước màu, cho thịt ba chỉ vào xào săn, thêm nước mắm, đường, nước dừa và trứng luộc, kho nhỏ lửa. <b>Gà chiên mắm:</b> Chiên vàng gà, vớt ra. Pha sốt mắm tỏi ớt đường rồi cho gà vào đảo đều."},
            "Thứ Ba": {"Sáng": "Phở bò tô lớn, thêm trứng chần. (650 kcal)", "Trưa": "Cơm tấm sườn bì chả. (750 kcal)", "Tối": "Mì Ý sốt bò bằm phô mai (150g thịt). (700 kcal)", "Phụ": "2 hũ sữa chua Hy Lạp và hạt điều. (450 kcal)", "Hướng dẫn": "<b>Mì Ý sốt bò bằm:</b> Phi thơm hành tỏi, cho cà chua và thịt bò bằm vào xào, nêm gia vị, đun nhỏ lửa 15 phút. Luộc mì rồi trộn với sốt."},
            "Thứ Tư": {"Sáng": "Bánh mì bò kho và 1 ly sữa béo. (700 kcal)", "Trưa": "Cơm (2 chén), cá hồi áp chảo sốt bơ tỏi. (800 kcal)", "Tối": "Xôi gà và gỏi. (750 kcal)", "Phụ": "Trái cây sấy và các loại hạt. (400 kcal)", "Hướng dẫn": "<b>Bò kho:</b> Ướp bò với gia vị bò kho, sả, tỏi. Xào săn rồi cho nước dừa, cà rốt, khoai tây vào hầm mềm. <b>Cá hồi áp chảo:</b> Áp chảo vàng 2 mặt cá hồi. Phi thơm bơ tỏi rồi rưới lên cá."},
            "Thứ Năm": {"Sáng": "Cơm tấm sườn trứng. (700 kcal)", "Trưa": "Bún bò Huế tô lớn. (650 kcal)", "Tối": "Vịt quay, cơm và canh. (850 kcal)", "Phụ": "Bánh flan và sinh tố sapoche. (500 kcal)", "Hướng dẫn": "<b>Sườn cơm tấm:</b> Ướp sườn cốt lết với tỏi, mật ong, nước mắm rồi nướng cho vàng đều hai mặt."},
            "Thứ Sáu": {"Sáng": "Hủ tiếu Nam Vang. (600 kcal)", "Trưa": "Cơm (2 chén), sườn xào chua ngọt, canh. (800 kcal)", "Tối": "Pizza hải sản (2-3 miếng). (750 kcal)", "Phụ": "1 ly ngũ cốc dinh dưỡng và chuối. (450 kcal)", "Hướng dẫn": "<b>Sườn xào chua ngọt:</b> Chiên vàng sườn. Pha sốt gồm mắm, đường, giấm, tương cà. Phi thơm hành tỏi, cho sườn và rau củ (thơm, ớt chuông) vào xào, cuối cùng rưới sốt."},
            "Thứ Bảy": {"Sáng": "Bò né và bánh mì. (750 kcal)", "Trưa": "Lẩu Thái hải sản, ăn với mì. (900 kcal)", "Tối": "Cơm chiên dương châu. (700 kcal)", "Phụ": "Chè và trái cây. (400 kcal)", "Hướng dẫn": "<b>Bò né:</b> Làm nóng chảo gang với bơ, cho hành tây, thịt bò, trứng, pate vào và nấu tái theo sở thích."},
            "Chủ Nhật": {"Sáng": "Bún chả Hà Nội. (650 kcal)", "Trưa": "Gà nướng nguyên con, xôi và gỏi. (950 kcal)", "Tối": "Ăn nhẹ với súp cua và bánh mì. (600 kcal)", "Phụ": "Sữa tươi và các loại hạt. (400 kcal)", "Hướng dẫn": "<b>Bún chả:</b> Thịt ba chỉ và thịt băm viên ướp gia vị rồi nướng trên than hoa. Pha nước mắm chua ngọt với đu đủ xanh."}
        }
    },
    "tăng cơ": {
        "mô tả": "Thực đơn này giàu protein và carb phức hợp để cung cấp năng lượng cho việc tập luyện và phục hồi cơ bắp.",
        "calo_ước_tính": "2500-2800 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "3 trứng ốp la, 2 lát bánh mì nguyên cám, 1 ly sữa. (500 kcal)", "Trưa": "Cơm gạo lứt (1.5 chén), ức gà áp chảo (200g). (700 kcal)", "Tối": "Bò bít tết (200g) với khoai lang nghiền. (800 kcal)", "Phụ": "Sinh tố whey protein. (300 kcal)", "Hướng dẫn": "<b>Ức gà áp chảo:</b> Ướp ức gà với muối, tiêu, tỏi. Áp chảo mỗi mặt 5-7 phút. <b>Bò bít tết:</b> Áp chảo miếng thăn bò dày 2-3cm trên chảo gang nóng với bơ và tỏi."},
            "Thứ Ba": {"Sáng": "Yến mạch (80g) với whey protein và chuối. (600 kcal)", "Trưa": "Phở bò (nhiều thịt, ít bánh). (650 kcal)", "Tối": "Cá hồi nướng măng tây (200g cá) và cơm. (750 kcal)", "Phụ": "Sữa chua Hy Lạp. (200 kcal)", "Hướng dẫn": "<b>Cá hồi nướng:</b> Ướp cá hồi với muối, tiêu, dầu oliu. Nướng cùng măng tây ở 200°C trong 12-15 phút."},
            "Thứ Tư": {"Sáng": "Bò lúc lắc (150g) và khoai tây. (600 kcal)", "Trưa": "Cơm gạo lứt, ức gà xào nấm (200g). (700 kcal)", "Tối": "Hải sản hấp (tôm, mực - 250g). (650 kcal)", "Phụ": "Các loại hạt và chuối. (300 kcal)", "Hướng dẫn": "<b>Bò lúc lắc:</b> Bò thái vuông, ướp dầu hào, tỏi. Xào nhanh trên lửa lớn với hành tây, ớt chuông."},
            "Thứ Năm": {"Sáng": "Trứng bác (3 quả) với thịt nguội và rau. (550 kcal)", "Trưa": "Bún chả cá (nhiều chả cá). (600 kcal)", "Tối": "Sườn heo nướng (200g) và salad. (750 kcal)", "Phụ": "Phô mai cottage và trái cây. (250 kcal)", "Hướng dẫn": "<b>Sườn nướng:</b> Ướp sườn với sốt BBQ hoặc mật ong, tỏi, mắm. Nướng ở 180°C trong 20-25 phút."},
            "Thứ Sáu": {"Sáng": "Sinh tố bơ, chuối, whey protein. (600 kcal)", "Trưa": "Cơm, cá diêu hồng chiên, canh. (750 kcal)", "Tối": "Thịt thăn heo áp chảo (200g), rau bina xào. (700 kcal)", "Phụ": "Trứng luộc (2 quả). (160 kcal)", "Hướng dẫn": "<b>Thăn heo áp chảo:</b> Ướp thăn heo với muối, tiêu. Áp chảo mỗi mặt 4-5 phút cho chín tới."},
            "Thứ Bảy": {"Sáng": "Bò bít tết và trứng. (700 kcal)", "Trưa": "Cơm gà xối mỡ (chọn phần ức). (750 kcal)", "Tối": "Lẩu hải sản (tập trung ăn hải sản và rau). (800 kcal)", "Phụ": "Sữa chua và hạt. (250 kcal)", "Hướng dẫn": "<b>Cơm gà xối mỡ:</b> Luộc gà, lấy nước luộc nấu cơm. Gà để nguội rồi xối dầu nóng cho da giòn."},
            "Chủ Nhật": {"Sáng": "Yến mạch và trứng. (550 kcal)", "Trưa": "Gà quay, bánh mì và salad. (800 kcal)", "Tối": "Ăn nhẹ với salad ức gà (200g). (600 kcal)", "Phụ": "Whey protein. (300 kcal)", "Hướng dẫn": "Chuẩn bị bữa ăn cho tuần tiếp theo."}
        }
    },
    "ăn chay": {
        "mô tả": "Thực đơn chay đảm bảo cung cấp đủ protein từ thực vật, vitamin và khoáng chất cần thiết.",
        "calo_ước_tính": "1800-2000 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Bún riêu chay với nấm và đậu hũ. (400 kcal)", "Trưa": "Cơm, đậu hũ sốt cà chua, canh rau đay. (550 kcal)", "Tối": "Nấm xào thập cẩm và salad đậu gà. (500 kcal)", "Hướng dẫn": "<b>Riêu chay:</b> Xay đậu hũ với cà chua, nấm để làm riêu. Nấu nước dùng từ rau củ. <b>Đậu hũ sốt cà:</b> Chiên vàng đậu, sốt với cà chua băm nhuyễn."},
            "Thứ Ba": {"Sáng": "Bánh mì ốp la chay. (350 kcal)", "Trưa": "Cơm, canh chua chay, nấm kho tiêu. (600 kcal)", "Tối": "Đậu lăng hầm rau củ. (500 kcal)", "Hướng dẫn": "<b>Nấm kho tiêu:</b> Ướp nấm với nước tương, tiêu, đường. Kho nhỏ lửa đến khi keo lại. <b>Đậu lăng hầm:</b> Hầm đậu lăng với cà rốt, khoai tây, cần tây cho mềm nhừ."},
            "Thứ Tư": {"Sáng": "Xôi nếp cẩm và muối vừng. (400 kcal)", "Trưa": "Cơm, khổ qua xào trứng chay, canh bí đỏ. (550 kcal)", "Tối": "Bún xào chay với rau củ và đậu hũ. (500 kcal)", "Hướng dẫn": "<b>Khổ qua xào trứng chay:</b> Khổ qua thái mỏng, xào chín tới rồi cho trứng chay (từ bột hoặc đậu hũ) vào đảo đều."},
            "Thứ Năm": {"Sáng": "Phở nấm chay. (450 kcal)", "Trưa": "Cơm, cà ri chay với khoai lang và đậu gà. (600 kcal)", "Tối": "Salad diêm mạch (quinoa) với rau củ nướng. (450 kcal)", "Hướng dẫn": "<b>Cà ri chay:</b> Xào thơm bột cà ri, cho nước cốt dừa, khoai lang, cà rốt vào hầm. Khi gần chín cho đậu gà vào."},
            "Thứ Sáu": {"Sáng": "Cháo yến mạch với các loại hạt. (350 kcal)", "Trưa": "Cơm, đậu hũ chiên sả ớt, canh rong biển. (600 kcal)", "Tối": "Gỏi cuốn chay chấm tương đậu phộng. (500 kcal)", "Hướng dẫn": "<b>Đậu hũ chiên sả ớt:</b> Đậu hũ cắt miếng, chiên vàng giòn rồi xốc với sả, ớt băm nhuyễn."},
            "Thứ Bảy": {"Sáng": "Hủ tiếu chay. (450 kcal)", "Trưa": "Lẩu nấm chay. (700 kcal)", "Tối": "Pizza rau củ và phô mai chay. (550 kcal)", "Hướng dẫn": "<b>Lẩu nấm:</b> Nấu nước dùng từ các loại rau củ (củ cải, cà rốt, su su) và các loại nấm để có vị ngọt tự nhiên."},
            "Chủ Nhật": {"Sáng": "Bánh bao chay. (300 kcal)", "Trưa": "Cơm gia đình chay với nhiều món. (750 kcal)", "Tối": "Súp ngô và nấm. (400 kcal)", "Hướng dẫn": "<b>Súp ngô nấm:</b> Xào nấm, cho ngô ngọt và nước dùng rau củ vào nấu. Thêm ít bột năng để tạo độ sánh."}
        }
    },
    "eat clean": {
        "mô tả": "Thực đơn Eat Clean tập trung vào thực phẩm toàn phần, không qua chế biến sâu, hạn chế tối đa đường và chất béo không lành mạnh.",
        "calo_ước_tính": "1800-2000 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Khoai lang luộc, ức gà luộc xé (100g). (400 kcal)", "Trưa": "Cơm gạo lứt, cá hồi áp chảo, măng tây nướng. (600 kcal)", "Tối": "Salad tôm và bơ với sốt chanh leo. (500 kcal)", "Hướng dẫn": "<b>Cá hồi áp chảo:</b> Áp chảo mặt da trước cho giòn, không cần nhiều dầu. Nướng măng tây với ít dầu oliu và muối tiêu."},
            "Thứ Ba": {"Sáng": "Sinh tố cải bó xôi, chuối, hạt chia. (350 kcal)", "Trưa": "Diêm mạch (quinoa) xào rau củ và đậu gà. (550 kcal)", "Tối": "Thịt bò lúc lắc (150g) với ớt chuông. (600 kcal)", "Hướng dẫn": "<b>Nấu diêm mạch:</b> Vo sạch, nấu với tỉ lệ 1 diêm mạch : 2 nước. <b>Bò lúc lắc:</b> Ướp bò với ít xì dầu, tỏi. Xào lửa lớn rất nhanh để bò không bị dai."},
            "Thứ Tư": {"Sáng": "Trứng luộc (2 quả) và yến mạch. (400 kcal)", "Trưa": "Cơm gạo lứt, ức gà nướng mật ong. (600 kcal)", "Tối": "Canh bí đỏ nấu tôm. (500 kcal)", "Hướng dẫn": "<b>Gà nướng mật ong:</b> Ướp gà với 1 muỗng mật ong, tỏi, muối, tiêu. Nướng 180°C trong 20 phút."},
            "Thứ Năm": {"Sáng": "Sữa chua không đường, granola nhà làm. (450 kcal)", "Trưa": "Cá diêu hồng hấp xì dầu, cơm gạo lứt. (550 kcal)", "Tối": "Bò bít tết áp chảo, salad rau rocket. (600 kcal)", "Hướng dẫn": "<b>Cá hấp xì dầu:</b> Hấp cá với gừng, hành. Pha sốt: xì dầu, một chút dầu hào, dầu mè rồi rưới lên cá khi gần chín."},
            "Thứ Sáu": {"Sáng": "Bánh mì nguyên cám kẹp bơ và trứng. (400 kcal)", "Trưa": "Mực xào cần tỏi tây. (500 kcal)", "Tối": "Gà hầm nấm và rau củ. (550 kcal)", "Hướng dẫn": "<b>Mực xào:</b> Xào mực trên lửa lớn để không bị ra nước. <b>Gà hầm:</b> Hầm gà với các loại củ như cà rốt, khoai tây cho mềm và ngọt nước."},
            "Thứ Bảy": {"Sáng": "Pancake yến mạch với trái cây tươi. (500 kcal)", "Trưa": "Bún gạo lứt trộn ức gà và rau thơm. (600 kcal)", "Tối": "Hải sản nướng (tôm, cá, mực). (650 kcal)", "Hướng dẫn": "<b>Pancake yến mạch:</b> Xay nhuyễn yến mạch, trứng, chuối, sữa chua rồi áp chảo. <b>Hải sản nướng:</b> Ướp với muối, tiêu, ớt bột và ít dầu oliu rồi nướng."},
            "Chủ Nhật": {"Sáng": "Trứng bác và bơ trên bánh mì lúa mạch. (450 kcal)", "Trưa": "Bò cuộn nấm kim châm nướng. (650 kcal)", "Tối": "Súp rau củ và ức gà. (500 kcal)", "Hướng dẫn": "<b>Bò cuộn nấm:</b> Trải thịt bò mỏng, đặt nấm kim châm vào cuộn lại, nướng hoặc áp chảo nhanh."}
        }
    },
    "keto": {
        "mô tả": "Chế độ ăn Keto có hàm lượng carb rất thấp, protein vừa phải và chất béo cao để đưa cơ thể vào trạng thái Ketosis.",
        "calo_ước_tính": "1600-1800 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Trứng chiên bơ (2 quả), ba chỉ xông khói, nửa quả bơ. (500 kcal)", "Trưa": "Salad ức gà với sốt mayonnaise không đường. (550 kcal)", "Tối": "Thịt bò xay xào nấm, bông cải xanh luộc. (600 kcal)", "Hướng dẫn": "<b>Bò xào nấm:</b> Xào bò xay với bơ và tỏi, sau đó cho nấm vào xào cùng. Nêm muối và tiêu."},
            "Thứ Ba": {"Sáng": "Pudding hạt chia làm bằng nước cốt dừa. (400 kcal)", "Trưa": "Cá diêu hồng chiên bơ tỏi, rau chân vịt xào. (600 kcal)", "Tối": "Canh sườn non nấu bí đao (chỉ ăn sườn và nước). (500 kcal)", "Hướng dẫn": "<b>Pudding chia:</b> Ngâm hạt chia trong nước cốt dừa qua đêm trong tủ lạnh. <b>Cá chiên bơ tỏi:</b> Chiên cá vàng giòn, sau đó phi thơm bơ tỏi và rưới lên."},
            "Thứ Tư": {"Sáng": "Trứng cuộn phô mai và thịt nguội. (450 kcal)", "Trưa": "Ba chỉ heo quay và dưa chuột. (650 kcal)", "Tối": "Thịt gà xào sả ớt với dầu dừa. (550 kcal)", "Hướng dẫn": "<b>Ba chỉ heo quay:</b> Khứa da, ướp gia vị mặt thịt. Quay bằng nồi chiên không dầu cho da nổ giòn. <b>Gà xào sả ớt:</b> Xào gà với dầu dừa, sả và ớt băm."},
            "Thứ Năm": {"Sáng": "Sinh tố bơ, rau xanh và whey protein isolate. (400 kcal)", "Trưa": "Bò lúc lắc xào với ớt chuông. (600 kcal)", "Tối": "Cá hồi nướng măng tây. (550 kcal)", "Hướng dẫn": "<b>Cá hồi nướng:</b> Ướp cá hồi với muối, tiêu, dầu oliu. Nướng cùng măng tây ở 200°C trong 12-15 phút."},
            "Thứ Sáu": {"Sáng": "Trứng luộc và bơ. (350 kcal)", "Trưa": "Cánh gà chiên nước mắm (dùng đường ăn kiêng). (600 kcal)", "Tối": "Thịt viên sốt cà chua (sốt tự làm, không đường). (550 kcal)", "Hướng dẫn": "<b>Gà chiên mắm keto:</b> Chiên vàng gà. Pha sốt: nước mắm, đường ăn kiêng, tỏi, ớt. Cho gà vào đảo đều."},
            "Thứ Bảy": {"Sáng": "Trứng ốp la và xúc xích. (500 kcal)", "Trưa": "Lẩu Thái (chỉ ăn thịt, hải sản, nấm, rau keto). (700 kcal)", "Tối": "Bò bít tết và salad. (650 kcal)", "Hướng dẫn": "<b>Lưu ý khi ăn lẩu:</b> Tránh các loại viên thả lẩu (thường có tinh bột) và không dùng nước chấm có đường."},
            "Chủ Nhật": {"Sáng": "Phô mai và các loại hạt. (400 kcal)", "Trưa": "Gà nướng và salad. (700 kcal)", "Tối": "Súp xương hầm rau củ keto. (500 kcal)", "Hướng dẫn": "<b>Gà nướng:</b> Ướp gà với muối, tiêu, thảo mộc khô và bơ. Nướng cho đến khi chín vàng."}
        }
    },
    "tiểu đường": {
        "mô tả": "Thực đơn giúp kiểm soát đường huyết ổn định, ưu tiên thực phẩm có chỉ số đường huyết (GI) thấp, giàu chất xơ.",
        "calo_ước_tính": "1500-1700 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Cháo yến mạch nguyên hạt (30g) nấu loãng. (250 kcal)", "Trưa": "Cơm gạo lứt (nửa chén), cá nục kho, canh khổ qua nhồi thịt. (500 kcal)", "Tối": "Miến dong nấu ức gà (100g) và rau củ. (450 kcal)", "Hướng dẫn": "<b>Cá kho:</b> Kho cá với nước mắm và gia vị, hạn chế tối đa đường. <b>Canh khổ qua:</b> Dồn thịt băm vào khổ qua rồi hầm mềm."},
            "Thứ Ba": {"Sáng": "1 quả trứng luộc, 1 ly sữa không đường. (200 kcal)", "Trưa": "Bún gạo lứt (ít bún), chả cá thác lác. (550 kcal)", "Tối": "Thịt ba chỉ luộc, rau củ luộc chấm kho quẹt (không đường). (500 kcal)", "Hướng dẫn": "<b>Chả cá:</b> Quết cá thác lác với thì là, tiêu. Hấp hoặc chiên ít dầu. <b>Kho quẹt:</b> Kho thịt ba chỉ với nước mắm, tiêu cho keo lại, không dùng đường."},
            "Thứ Tư": {"Sáng": "Khoai lang luộc (1 củ nhỏ). (200 kcal)", "Trưa": "Cơm gạo lứt, ức gà áp chảo, salad. (500 kcal)", "Tối": "Canh rong biển nấu đậu hũ non. (400 kcal)", "Hướng dẫn": "<b>Ức gà áp chảo:</b> Ướp gà với muối, tiêu, tỏi. Áp chảo mỗi mặt 5-7 phút."},
            "Thứ Năm": {"Sáng": "Sữa chua không đường và hạt chia. (250 kcal)", "Trưa": "Cá diêu hồng hấp, cơm gạo lứt. (550 kcal)", "Tối": "Thịt bò xào mướp đắng. (450 kcal)", "Hướng dẫn": "<b>Thịt bò xào mướp đắng:</b> Xào bò tái rồi vớt ra. Xào mướp đắng chín tới rồi cho bò vào đảo lại."},
            "Thứ Sáu": {"Sáng": "Phở gạo lứt (ít bánh). (400 kcal)", "Trưa": "Đậu hũ dồn thịt sốt cà, canh rau. (500 kcal)", "Tối": "Tôm hấp và bông cải xanh luộc. (400 kcal)", "Hướng dẫn": "<b>Đậu hũ dồn thịt:</b> Hấp hoặc chiên ít dầu. Sốt cà chua không cho đường."},
            "Thứ Bảy": {"Sáng": "Bánh mì nguyên cám và trứng. (350 kcal)", "Trưa": "Gỏi cuốn tôm thịt. (450 kcal)", "Tối": "Lẩu nấm, ăn với miến dong. (550 kcal)", "Hướng dẫn": "<b>Gỏi cuốn:</b> Luộc thịt và tôm, cuốn với bún và nhiều rau. Nước chấm pha từ tương, không dùng đường."},
            "Chủ Nhật": {"Sáng": "Cháo cá lóc. (300 kcal)", "Trưa": "Gà luộc lá chanh, cơm gạo lứt. (550 kcal)", "Tối": "Súp rau củ. (350 kcal)", "Hướng dẫn": "<b>Cháo cá:</b> Nấu cháo từ gạo lứt, cá luộc gỡ xương rồi cho vào cháo. Nêm nếm thanh đạm."}
        }
    },
    "bận rộn": {
        "mô tả": "Thực đơn dành cho người có ít thời gian, tập trung vào các món nhanh gọn, dễ chuẩn bị và có thể chuẩn bị trước.",
        "calo_ước_tính": "1600-1900 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Sinh tố chuối, yến mạch, sữa chua (xay 2 phút). (350 kcal)", "Trưa": "Salad ức gà và rau củ (chuẩn bị sẵn). (500 kcal)", "Tối": "Trứng đúc thịt và rau củ (cắt sẵn). (600 kcal)", "Hướng dẫn": "<b>Meal prep:</b> Luộc sẵn ức gà, trứng, cắt sẵn rau củ vào hộp và bảo quản trong tủ lạnh cho 2-3 ngày."},
            "Thứ Ba": {"Sáng": "Bánh mì đen kẹp bơ đậu phộng và chuối. (400 kcal)", "Trưa": "Cơm văn phòng (đặt ngoài hoặc mang hộp cơm). (600 kcal)", "Tối": "Ức gà áp chảo (ướp sẵn) và salad trộn nhanh. (550 kcal)", "Hướng dẫn": "<b>Ướp sẵn:</b> Ướp thịt gà, bò, heo với các loại gia vị khác nhau, chia túi zip và cấp đông."},
            "Thứ Tư": {"Sáng": "Yến mạch ngâm qua đêm (overnight oats). (350 kcal)", "Trưa": "Cơm cuộn (mua sẵn hoặc làm từ tối qua). (500 kcal)", "Tối": "Cá hồi áp chảo (10 phút) và măng tây. (600 kcal)", "Hướng dẫn": "<b>Overnight oats:</b> Trộn yến mạch, sữa chua, sữa, hạt chia vào hũ, để tủ lạnh qua đêm, sáng ra chỉ việc ăn."},
            "Thứ Năm": {"Sáng": "Sữa chua và granola. (400 kcal)", "Trưa": "Thịt bò xào nhanh với hành tây (ướp sẵn). (550 kcal)", "Tối": "Canh gói nấu với trứng và rau. (450 kcal)", "Hướng dẫn": "<b>Nấu nhanh:</b> Luôn có sẵn các loại rau củ đông lạnh để xào hoặc nấu súp."},
            "Thứ Sáu": {"Sáng": "Trứng luộc (2 quả, đã luộc sẵn). (160 kcal)", "Trưa": "Đặt đồ ăn ngoài (chọn món lành mạnh). (600 kcal)", "Tối": "Tôm hấp sả (15 phút). (500 kcal)", "Hướng dẫn": "<b>Tôm hấp sả:</b> Rửa sạch tôm, cho vào nồi cùng sả đập dập, hấp 10-15 phút là chín."},
            "Thứ Bảy": {"Sáng": "Ăn sáng bên ngoài (phở, bún). (500 kcal)", "Trưa": "Ăn trưa cùng bạn bè, gia đình. (700 kcal)", "Tối": "Mì ý sốt cà chua thịt bằm (sốt làm sẵn). (600 kcal)", "Hướng dẫn": "<b>Làm sẵn sốt:</b> Nấu một nồi sốt mì Ý lớn, chia nhỏ và cấp đông để dùng dần."},
            "Chủ Nhật": {"Sáng": "Pancake đơn giản. (450 kcal)", "Trưa": "Đi chợ và chuẩn bị đồ ăn cho cả tuần. (650 kcal)", "Tối": "Thử một công thức nấu ăn mới. (600 kcal)", "Hướng dẫn": "Dành 2 tiếng Chủ Nhật để sơ chế thực phẩm sẽ tiết kiệm rất nhiều thời gian trong tuần."}
        }
    },
    "tốt cho tim mạch": {
        "mô tả": "Dựa trên chế độ ăn DASH và Địa Trung Hải, thực đơn này tập trung vào rau củ, trái cây, ngũ cốc nguyên hạt, protein nạc và chất béo lành mạnh.",
        "calo_ước_tính": "1800-2100 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Yến mạch, quả mọng, hạt óc chó. (400 kcal)", "Trưa": "Salad cá hồi nướng, sốt dầu oliu. (600 kcal)", "Tối": "Ức gà nướng thảo mộc, diêm mạch (quinoa). (550 kcal)", "Hướng dẫn": "<b>Gà nướng:</b> Ướp gà với dầu oliu, lá hương thảo, muối, tiêu rồi nướng. <b>Sốt salad:</b> Trộn dầu oliu, nước cốt chanh, ít mật ong."},
            "Thứ Ba": {"Sáng": "Sữa chua Hy Lạp, hạt lanh, đào. (350 kcal)", "Trưa": "Súp đậu lăng, bánh mì nguyên cám. (500 kcal)", "Tối": "Cá tuyết đút lò với cà chua, oliu, cơm gạo lứt. (600 kcal)", "Hướng dẫn": "<b>Súp đậu lăng:</b> Hầm đậu lăng với cà rốt, cần tây, hành tây cho mềm. <b>Cá đút lò:</b> Xếp cà chua bi, oliu, cá vào khay, rưới dầu oliu và nướng."},
            "Thứ Tư": {"Sáng": "Sinh tố rau bina, táo, gừng. (300 kcal)", "Trưa": "Gà xào hạt điều, rau củ, cơm gạo lứt. (650 kcal)", "Tối": "Salad đậu gà với rau xanh và bơ. (500 kcal)", "Hướng dẫn": "<b>Gà xào hạt điều:</b> Xào gà trước, sau đó cho rau củ và hạt điều vào xào cùng. Dùng ít dầu và nước tương."},
            "Thứ Năm": {"Sáng": "Trứng luộc, bơ cắt lát, bánh mì nguyên cám. (400 kcal)", "Trưa": "Tôm xào tỏi và bông cải xanh. (550 kcal)", "Tối": "Canh chua cá basa (nấu nhạt). (500 kcal)", "Hướng dẫn": "<b>Canh chua:</b> Dùng vị chua tự nhiên từ me, cà chua, thơm. Hạn chế đường và bột ngọt."},
            "Thứ Sáu": {"Sáng": "Yến mạch và chuối. (350 kcal)", "Trưa": "Cá ngừ trộn salad (tự làm sốt). (500 kcal)", "Tối": "Bò bít tết (phần thăn, 120g), khoai lang nướng. (600 kcal)", "Hướng dẫn": "<b>Bít tết:</b> Chỉ cần ướp muối và tiêu. Áp chảo nhanh với một ít dầu oliu. Ăn phần nhỏ thịt đỏ."},
            "Thứ Bảy": {"Sáng": "Pancake ngũ cốc nguyên hạt với dâu. (450 kcal)", "Trưa": "Gỏi cuốn tôm thịt. (500 kcal)", "Tối": "Gà nướng rau củ. (650 kcal)", "Hướng dẫn": "<b>Gà nướng rau củ:</b> Cho gà và các loại rau củ (ớt chuông, bí ngòi, hành tây) vào khay, ướp với dầu oliu, thảo mộc rồi nướng."},
            "Chủ Nhật": {"Sáng": "Trứng bác với cà chua và hành tây. (350 kcal)", "Trưa": "Cá diêu hồng chưng tương. (550 kcal)", "Tối": "Súp gà và rau củ. (450 kcal)", "Hướng dẫn": "<b>Cá chưng tương:</b> Hấp cá với tương hột, nấm mèo, bún tàu. Hạn chế gia vị mặn."}
        }
    },
    "tăng cường trí não": {
        "mô tả": "Chế độ ăn MIND, tập trung vào các loại thực phẩm đã được chứng minh là hỗ trợ sức khỏe não bộ.",
        "calo_ước_tính": "1700-2000 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Trứng bác với rau bina và nấm. (350 kcal)", "Trưa": "Salad gà với rau xanh đậm, quả óc chó, dâu tây. (550 kcal)", "Tối": "Cá hồi nướng, khoai lang nướng, măng tây. (600 kcal)", "Phụ": "Một nắm quả việt quất. (80 kcal)", "Hướng dẫn": "<b>Trứng bác:</b> Xào nấm trước, sau đó cho rau bina vào đảo sơ rồi mới cho trứng đã đánh tan vào."},
            "Thứ Ba": {"Sáng": "Yến mạch, quả việt quất, hạt lanh. (400 kcal)", "Trưa": "Súp đậu lăng. (500 kcal)", "Tối": "Gà nướng với dầu oliu và hương thảo. (550 kcal)", "Phụ": "Một nắm hạt hạnh nhân. (150 kcal)", "Hướng dẫn": "<b>Súp đậu lăng:</b> Hầm đậu lăng với các loại rau củ, xay nhuyễn một phần để tạo độ sánh."},
            "Thứ Tư": {"Sáng": "Sữa chua Hy Lạp với quả óc chó. (350 kcal)", "Trưa": "Salad cá ngừ với nhiều rau xanh. (500 kcal)", "Tối": "Đậu hũ xào rau củ với nghệ. (500 kcal)", "Phụ": "Trà xanh và một quả táo. (100 kcal)", "Hướng dẫn": "<b>Đậu hũ xào nghệ:</b> Chiên sơ đậu hũ, sau đó xào với rau củ và một muỗng cà phê bột nghệ."},
            "Thứ Năm": {"Sáng": "Sinh tố quả mọng và rau bina. (300 kcal)", "Trưa": "Cơm gạo lứt và cá thu kho. (600 kcal)", "Tối": "Thịt gà luộc và salad. (500 kcal)", "Phụ": "Sô cô la đen (>70% cacao). (150 kcal)", "Hướng dẫn": "<b>Cá kho:</b> Ưu tiên kho nhạt, dùng các loại gia vị tự nhiên."},
            "Thứ Sáu": {"Sáng": "Trứng luộc và bơ. (350 kcal)", "Trưa": "Salad diêm mạch với đậu gà và rau. (550 kcal)", "Tối": "Tôm xào bông cải xanh. (500 kcal)", "Phụ": "Rượu vang đỏ (1 ly nhỏ, nếu có). (120 kcal)", "Hướng dẫn": "<b>Nấu diêm mạch:</b> Vo sạch, nấu với tỉ lệ 1 diêm mạch : 2 nước trong khoảng 15 phút."},
            "Thứ Bảy": {"Sáng": "Yến mạch và các loại hạt. (400 kcal)", "Trưa": "Cá nướng và salad. (600 kcal)", "Tối": "Ăn ngoài, chọn món có cá và rau. (650 kcal)", "Phụ": "Các loại quả mọng. (100 kcal)", "Hướng dẫn": "<b>Cá nướng:</b> Có thể nướng giấy bạc với các loại rau thơm và chanh để giữ độ ẩm."},
            "Chủ Nhật": {"Sáng": "Trứng ốp la và cà chua. (350 kcal)", "Trưa": "Gà nướng nguyên con. (700 kcal)", "Tối": "Súp rau củ. (400 kcal)", "Phụ": "Quả óc chó. (180 kcal)", "Hướng dẫn": "<b>Súp rau củ:</b> Hầm các loại rau củ với nước dùng gà hoặc rau củ cho đến khi mềm."}
        }
    },
    "cải thiện tiêu hóa": {
        "mô tả": "Thực đơn này giàu chất xơ, probiotics (lợi khuẩn) và prebiotics (thức ăn cho lợi khuẩn) để thúc đẩy một hệ đường ruột khỏe mạnh.",
        "calo_ước_tính": "1600-1900 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Sữa chua sống (live yogurt), hạt chia, chuối. (400 kcal)", "Trưa": "Gà xào rau củ với tỏi, gừng; cơm gạo lứt. (550 kcal)", "Tối": "Súp đậu đen. (450 kcal)", "Hướng dẫn": "<b>Gà xào:</b> Gừng và tỏi rất tốt cho tiêu hóa. <b>Súp đậu đen:</b> Hầm đậu đen đã ngâm cho mềm nhừ."},
            "Thứ Ba": {"Sáng": "Sinh tố kefir, dâu và yến mạch. (350 kcal)", "Trưa": "Cá hấp gừng, canh khoai mỡ. (500 kcal)", "Tối": "Canh xương hầm rau củ (cà rốt, khoai tây). (500 kcal)", "Hướng dẫn": "<b>Kefir:</b> Là một loại sữa lên men chứa nhiều lợi khuẩn. <b>Canh xương hầm:</b> Nước hầm xương giàu gelatin tốt cho niêm mạc ruột."},
            "Thứ Tư": {"Sáng": "Táo và bơ hạnh nhân. (300 kcal)", "Trưa": "Cơm gạo lứt, tempeh kho. (550 kcal)", "Tối": "Salad gà với nhiều rau xanh. (450 kcal)", "Hướng dẫn": "<b>Tempeh:</b> Là đậu nành lên men, vừa cung cấp protein vừa tốt cho tiêu hóa."},
            "Thứ Năm": {"Sáng": "Cháo yến mạch với hạt lanh. (350 kcal)", "Trưa": "Canh chua cá lóc. (500 kcal)", "Tối": "Đậu lăng hầm. (450 kcal)", "Hướng dẫn": "<b>Hạt lanh:</b> Giàu chất xơ hòa tan, giúp hỗ trợ nhu động ruột."},
            "Thứ Sáu": {"Sáng": "Trà kombucha và một quả chuối. (250 kcal)", "Trưa": "Kim chi xào thịt heo, cơm. (600 kcal)", "Tối": "Gà luộc và súp lơ luộc. (450 kcal)", "Hướng dẫn": "<b>Kombucha và Kim chi:</b> Là những thực phẩm lên men (fermented foods) cung cấp nhiều probiotics."},
            "Thứ Bảy": {"Sáng": "Sữa chua và đu đủ. (300 kcal)", "Trưa": "Gỏi cuốn. (450 kcal)", "Tối": "Lẩu mắm (ăn nhiều rau). (650 kcal)", "Hướng dẫn": "<b>Đu đủ:</b> Chứa enzyme papain giúp tiêu hóa protein. <b>Rau thơm:</b> Các loại rau trong gỏi cuốn cũng rất tốt cho tiêu hóa."},
            "Chủ Nhật": {"Sáng": "Khoai lang luộc. (250 kcal)", "Trưa": "Cá diêu hồng nướng giấy bạc. (550 kcal)", "Tối": "Súp gà hầm. (450 kcal)", "Hướng dẫn": "<b>Ăn chậm, nhai kỹ:</b> Đây là bước quan trọng nhất để hệ tiêu hóa hoạt động tốt."}
        }
    },
    "chống viêm": {
        "mô tả": "Giảm viêm trong cơ thể bằng cách tập trung vào thực phẩm giàu chất chống oxy hóa. Hạn chế thực phẩm chế biến sẵn và đường.",
        "calo_ước_tính": "1700-2000 kcal/ngày",
        "chi_tiết": {
            "Thứ Hai": {"Sáng": "Sinh tố cải bó xôi, dứa, gừng, nước cốt dừa. (350 kcal)", "Trưa": "Salad lớn với cá ngừ, bơ, cà chua, sốt dầu oliu. (550 kcal)", "Tối": "Cà ri gà với nghệ, rau củ, gạo lứt. (600 kcal)", "Hướng dẫn": "<b>Cà ri nghệ:</b> Nghệ chứa curcumin là chất chống viêm cực mạnh. Luôn dùng kèm một ít tiêu đen để tăng hấp thu."},
            "Thứ Ba": {"Sáng": "Yến mạch, quả mọng, hạt óc chó. (400 kcal)", "Trưa": "Cá hồi áp chảo, măng tây. (600 kcal)", "Tối": "Súp bông cải xanh. (450 kcal)", "Hướng dẫn": "<b>Cá hồi và hạt óc chó:</b> Cực kỳ giàu Omega-3, một axit béo có tác dụng chống viêm hiệu quả."},
            "Thứ Tư": {"Sáng": "Sữa chua, hạt chia, dâu tây. (350 kcal)", "Trưa": "Gà nướng với rau củ nhiều màu. (600 kcal)", "Tối": "Salad đậu đen và bơ. (500 kcal)", "Hướng dẫn": "<b>Quả mọng và rau củ nhiều màu:</b> Chứa nhiều chất chống oxy hóa và polyphenol."},
            "Thứ Năm": {"Sáng": "Trà xanh và một nắm hạnh nhân. (250 kcal)", "Trưa": "Tôm xào nấm và ớt chuông. (550 kcal)", "Tối": "Canh cải bó xôi nấu thịt bằm. (450 kcal)", "Hướng dẫn": "<b>Trà xanh:</b> Chứa EGCG, một chất chống oxy hóa mạnh mẽ. <b>Cải bó xôi:</b> Rau lá xanh đậm rất tốt để chống viêm."},
            "Thứ Sáu": {"Sáng": "Sinh tố cherry và cacao. (400 kcal)", "Trưa": "Cơm gạo lứt, cá thu sốt cà. (600 kcal)", "Tối": "Thịt bò xào bông cải xanh. (550 kcal)", "Hướng dẫn": "<b>Cherry:</b> Đặc biệt tốt trong việc giảm các dấu hiệu viêm nhiễm."},
            "Thứ Bảy": {"Sáng": "Trứng bác với nghệ. (350 kcal)", "Trưa": "Salad gà và các loại hạt. (600 kcal)", "Tối": "Ăn ngoài, ưu tiên món hấp, nướng. (650 kcal)", "Hướng dẫn": "<b>Hạn chế thực phẩm chế biến sẵn:</b> Đường, bột mì trắng và dầu ăn tinh luyện là những tác nhân gây viêm hàng đầu."},
            "Chủ Nhật": {"Sáng": "Yến mạch và quả việt quất. (400 kcal)", "Trưa": "Gà hầm nấm. (650 kcal)", "Tối": "Súp cà chua. (400 kcal)", "Hướng dẫn": "<b>Cà chua nấu chín:</b> Giải phóng nhiều lycopene, một chất chống oxy hóa mạnh."}
        }
    }
}


#====================================================================
# PHẦN 2: LOGIC PYTHON VÀ NỘI DUNG GIAO DIỆN
#====================================================================

def tao_thuc_don(muc_tieu):
    muc_tieu = muc_tieu.lower().strip()
    if muc_tieu in THUC_DON_MAU:
        return THUC_DON_MAU[muc_tieu]
    else:
        return None

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <title>Chatbot Thực Đơn Dinh Dưỡng</title>
    <link rel="stylesheet" href="/style.css">
</head>
<body>
    <div class="chat-container">
        <div class="chat-header">
            <h2>AI Tư Vấn Dinh Dưỡng</h2>
        </div>
        <div class="chat-messages" id="chat-messages">
             <div class="message bot-message">
                Xin chào! Mục tiêu của bạn là gì? (vd: giảm cân, tăng cân, tăng cơ, ăn chay, eat clean, keto, tiểu đường, bận rộn, tim mạch, trí não, tiêu hóa, chống viêm...)
            </div>
        </div>
        <form class="chat-input-form" id="chat-form">
            <input type="text" id="user-input" placeholder="Nhập mục tiêu của bạn...">
            <button type="submit">Gửi</button>
        </form>
    </div>
    <script src="/script.js"></script>
</body>
</html>
"""

CSS_CONTENT = """
body { font-family: Arial, sans-serif; background-color: #f4f4f4; }
.chat-container { max-width: 600px; margin: 50px auto; border: 1px solid #ccc; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
.chat-header { background-color: #4CAF50; color: white; padding: 15px; text-align: center; }
.chat-messages { padding: 20px; height: 400px; overflow-y: auto; background-color: #fff; }
.message { margin-bottom: 15px; padding: 10px 15px; border-radius: 18px; line-height: 1.5; max-width: 80%; }
.user-message { background-color: #DCF8C6; text-align: left; margin-left: auto; }
.bot-message { background-color: #f1f0f0; text-align: left; }
.chat-input-form { display: flex; padding: 10px; border-top: 1px solid #ccc; background-color: #f9f9f9; }
#user-input { flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 20px; }
button { padding: 10px 15px; border: none; background-color: #4CAF50; color: white; border-radius: 20px; cursor: pointer; margin-left: 10px; }
h3 { color: #4CAF50; }
h4 { margin-bottom: 5px; }
ul { padding-left: 20px; margin-top: 5px; }
li > em { color: #555; font-size: 0.9em; }
"""

JS_CONTENT = """
document.getElementById('chat-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const API_KEY = "MySuperSecretChatbotKey123!@#";
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    if (message === "") return;
    const chatMessages = document.getElementById('chat-messages');
    const userMessageElem = document.createElement('div');
    userMessageElem.className = 'message user-message';
    userMessageElem.textContent = message;
    chatMessages.appendChild(userMessageElem);
    userInput.value = '';
    chatMessages.scrollTop = chatMessages.scrollHeight;
    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': API_KEY
        },
        body: JSON.stringify({ message: message })
    });
    if (response.status === 401) {
        const botMessageElem = document.createElement('div');
        botMessageElem.className = 'message bot-message';
        botMessageElem.innerHTML = "Lỗi: API Key không hợp lệ. Vui lòng kiểm tra lại.";
        chatMessages.appendChild(botMessageElem);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        return;
    }
    const data = await response.json();
    const botMessageElem = document.createElement('div');
    botMessageElem.className = 'message bot-message';
    botMessageElem.innerHTML = data.reply;
    chatMessages.appendChild(botMessageElem);
    chatMessages.scrollTop = chatMessages.scrollHeight;
});
"""

#====================================================================
# PHẦN 3: CÁC ROUTE CỦA FLASK
#====================================================================

@app.route("/")
def index():
    return HTML_CONTENT

@app.route("/style.css")
def style():
    return Response(CSS_CONTENT, mimetype='text/css')

@app.route("/script.js")
def script():
    return Response(JS_CONTENT, mimetype='application/javascript')

@app.route("/chat", methods=["POST"])
def chat():
    client_api_key = request.headers.get('X-API-Key')
    if not client_api_key or client_api_key != SECRET_API_KEY:
        return jsonify({"error": "Unauthorized"}), 401
    user_message = request.json.get("message").lower()
    if not user_message:
        return jsonify({"reply": "Vui lòng nhập mục tiêu của bạn."})
    muc_tieu_tim_thay = None
    if "giảm cân" in user_message: muc_tieu_tim_thay = "giảm cân"
    elif "tăng cơ" in user_message: muc_tieu_tim_thay = "tăng cơ"
    elif "tăng cân" in user_message: muc_tieu_tim_thay = "tăng cân lành mạnh"
    elif "ăn chay" in user_message: muc_tieu_tim_thay = "ăn chay"
    elif "eat clean" in user_message or "lành mạnh" in user_message: muc_tieu_tim_thay = "eat clean"
    elif "keto" in user_message: muc_tieu_tim_thay = "keto"
    elif "tiểu đường" in user_message: muc_tieu_tim_thay = "tiểu đường"
    elif "bận rộn" in user_message or "nhanh" in user_message: muc_tieu_tim_thay = "bận rộn"
    elif "tim mạch" in user_message: muc_tieu_tim_thay = "tốt cho tim mạch"
    elif "trí não" in user_message or "minh mẫn" in user_message: muc_tieu_tim_thay = "tăng cường trí não"
    elif "tiêu hóa" in user_message: muc_tieu_tim_thay = "cải thiện tiêu hóa"
    elif "chống viêm" in user_message or "đề kháng" in user_message: muc_tieu_tim_thay = "chống viêm"
    if muc_tieu_tim_thay:
        thuc_don = tao_thuc_don(muc_tieu_tim_thay)
        reply_text = f"<h3>Thực đơn gợi ý cho mục tiêu '{muc_tieu_tim_thay.upper()}'</h3>"
        reply_text += f"<p><em>{thuc_don['mô tả']}</em></p>"
        reply_text += f"<p><strong>Lượng calo ước tính:</strong> {thuc_don['calo_ước_tính']}</p>"
        for ngay, bua_an in thuc_don['chi_tiết'].items():
            reply_text += f"<h4>{ngay}</h4><ul>"
            for bua, mon in bua_an.items():
                if bua != "Hướng dẫn":
                    reply_text += f"<li><strong>{bua}:</strong> {mon}</li>"
            reply_text += f"<li><em>Hướng dẫn: {bua_an['Hướng dẫn']}</em></li>"
            reply_text += "</ul>"
    else:
        reply_text = "Xin lỗi, tôi chưa có thực đơn cho mục tiêu này. Bạn vui lòng thử lại với các từ khóa được gợi ý."
    return jsonify({"reply": reply_text})

if __name__ == "__main__":
    app.run(debug=True)