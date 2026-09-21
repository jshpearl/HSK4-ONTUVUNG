import streamlit as st
import random
import requests
import datetime

# --- CẤU HÌNH TRANG STREAMLIT ---
st.set_page_config(
    page_title="ÔN TẬP TỪ VỰNG HSK4",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- ẨN HEADER / MENU / LOGO KHÔNG CẦN THIẾT ---
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    .stAppDeployButton { display: none !important; }
    
    /* Responsive Layout */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px !important;
    }
    
    /* Clean, Simple Header */
    .clean-title {
        text-align: center;
        color: #1E293B;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .clean-subtitle {
        text-align: center;
        color: #475569;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    
    /* Question Text Style - Dark Pastel Bold */
    .q-text {
        color: #2C3E50;
        font-weight: 700;
        font-size: 1.05rem;
        margin-bottom: 0.4rem;
        line-height: 1.5;
    }
    
    /* Flashcard CSS with Hover Flip Effect */
    .flashcard-box {
        perspective: 1000px;
        height: 150px;
        margin-bottom: 15px;
    }
    .flashcard-inner {
        position: relative;
        width: 100%;
        height: 100%;
        text-align: center;
        transition: transform 0.6s;
        transform-style: preserve-3d;
        box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        border-radius: 12px;
        cursor: pointer;
    }
    .flashcard-box:hover .flashcard-inner {
        transform: rotateY(180deg);
    }
    .flashcard-front, .flashcard-back {
        position: absolute;
        width: 100%;
        height: 100%;
        -webkit-backface-visibility: hidden;
        backface-visibility: hidden;
        border-radius: 12px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 12px;
        box-sizing: border-box;
    }
    .flashcard-front {
        background: linear-gradient(135deg, #F8FAFC 0%, #EDF2F7 100%);
        color: #1E293B;
        border: 2px solid #CBD5E1;
    }
    .flashcard-back {
        background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
        color: #78350F;
        border: 2px solid #FCD34D;
        transform: rotateY(180deg);
    }
    .fc-hanzi {
        font-size: 2.1rem;
        font-weight: 800;
        color: #1E3A8A;
    }
    .fc-pinyin {
        font-size: 1.15rem;
        font-weight: 700;
        color: #475569;
        margin-top: 2px;
    }
    .fc-meaning {
        font-size: 1.1rem;
        font-weight: 700;
        color: #92400E;
    }
    .fc-hint {
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 6px;
    }

    /* Result Banners */
    .result-banner-8 {
        background-color: #D1FAE5;
        border-left: 5px solid #10B981;
        color: #065F46;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .result-banner-5 {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        color: #92400E;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .result-banner-0 {
        background-color: #FEE2E2;
        border-left: 5px solid #EF4444;
        color: #991B1B;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    .teacher-footer {
        text-align: center;
        color: #64748B;
        font-size: 1.2rem;
        font-weight: 700;
        margin-top: 3rem;
        margin-bottom: 2rem;
        padding-top: 1rem;
        border-top: 1px dashed #CBD5E1;
    }
</style>
""", unsafe_allow_html=True)

# --- GOOGLE SHEETS API URL ---
GSHEET_URL = "https://script.google.com/macros/s/AKfycbzsGpC84ZYruRCamTzv3pnY3eHcibMa9sVLT73S5zpX_OfAKRYwmMDgZElfUeWbA7Km/exec"

def post_to_gsheet(student_name, test_name, score_str):
    try:
        payload = {
            "sheet": "Từ vựng HSK",
            "name": student_name,
            "test": test_name,
            "score": score_str,
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        resp = requests.post(GSHEET_URL, json=payload, timeout=5)
        return True
    except Exception:
        return False

# --- HEADER (ĐƠN GIẢN, KHÔNG MÀU MÈ CẦU KỲ) ---
st.markdown('<div class="clean-title">ÔN TẬP TỪ VỰNG HSK4</div>', unsafe_allow_html=True)
st.markdown('<div class="clean-subtitle">Chúc cả lớp ôn tập tốt nha, cảm ơn vì đã chăm chỉ!</div>', unsafe_allow_html=True)

# --- FLASHCARD 600 TỪ VỰNG HSK4 (NGẪU NHIÊN KHI MỞ / TẢI LẠI TRANG) ---

PASTEL_PALETTES = [
    {"front_bg": "linear-gradient(135deg, #FFF0F5 0%, #FFE4E1 100%)", "front_border": "#FBCFE8", "front_text": "#9D174D",
     "back_bg": "linear-gradient(135deg, #FCE7F3 0%, #FBCFE8 100%)", "back_border": "#F472B6", "back_text": "#831843"},
    {"front_bg": "linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%)", "front_border": "#7DD3FC", "front_text": "#0369A1",
     "back_bg": "linear-gradient(135deg, #BAE6FD 0%, #93C5FD 100%)", "back_border": "#60A5FA", "back_text": "#1E3A8A"},
    {"front_bg": "linear-gradient(135deg, #E6F4EA 0%, #D1E7DD 100%)", "front_border": "#A3E635", "front_text": "#15803D",
     "back_bg": "linear-gradient(135deg, #DCFCE7 0%, #BBF7D0 100%)", "back_border": "#86EFAC", "back_text": "#14532D"},
    {"front_bg": "linear-gradient(135deg, #F3E8FF 0%, #E9D5FF 100%)", "front_border": "#D8B4FE", "front_text": "#6B21A8",
     "back_bg": "linear-gradient(135deg, #EDE9FE 0%, #DDD6FE 100%)", "back_border": "#C4B5FD", "back_text": "#581C87"},
    {"front_bg": "linear-gradient(135deg, #FEF9C3 0%, #FEF08A 100%)", "front_border": "#FDE047", "front_text": "#854D0E",
     "back_bg": "linear-gradient(135deg, #FFEDD5 0%, #FED7AA 100%)", "back_border": "#FDBA74", "back_text": "#9A3412"},
    {"front_bg": "linear-gradient(135deg, #E0F2F1 0%, #B2DFDB 100%)", "front_border": "#80CBC4", "front_text": "#00695C",
     "back_bg": "linear-gradient(135deg, #CCFBF1 0%, #99F6E4 100%)", "back_border": "#5EEAD4", "back_text": "#115E59"}
]

VOCAB_600 = [
    {"hanzi": "爱情", "pinyin": "àiqíng", "meaning": "tình yêu"},
    {"hanzi": "按照", "pinyin": "ànzhào", "meaning": "dựa vào, theo"},
    {"hanzi": "按时", "pinyin": "ànshí", "meaning": "đúng hạn"},
    {"hanzi": "安排", "pinyin": "ānpái", "meaning": "sắp xếp"},
    {"hanzi": "安全", "pinyin": "ānquán", "meaning": "an toàn"},
    {"hanzi": "百分之", "pinyin": "bǎi fēn zhī", "meaning": "phần trăm (%)"},
    {"hanzi": "饼干", "pinyin": "bǐnggān", "meaning": "bánh"},
    {"hanzi": "部分", "pinyin": "bùfèn", "meaning": "bộ phận, phần"},
    {"hanzi": "遍", "pinyin": "biàn", "meaning": "lần, lượt"},
    {"hanzi": "表示", "pinyin": "biǎoshì", "meaning": "biểu thị, cho thấy"},
    {"hanzi": "表演", "pinyin": "biǎoyǎn", "meaning": "biểu diễn"},
    {"hanzi": "表格", "pinyin": "biǎogé", "meaning": "bảng biểu"},
    {"hanzi": "表扬", "pinyin": "biǎoyáng", "meaning": "tuyên dương"},
    {"hanzi": "笨", "pinyin": "bèn", "meaning": "ngốc nghếch"},
    {"hanzi": "毕业", "pinyin": "bìyè", "meaning": "tốt nghiệp"},
    {"hanzi": "比如", "pinyin": "bǐrú", "meaning": "ví dụ như"},
    {"hanzi": "棒", "pinyin": "bàng", "meaning": "cây gậy"},
    {"hanzi": "标准", "pinyin": "biāozhǔn", "meaning": "tiêu chuẩn"},
    {"hanzi": "本来", "pinyin": "běnlái", "meaning": "vốn có"},
    {"hanzi": "抱歉", "pinyin": "bàoqiàn", "meaning": "xin lỗi"},
    {"hanzi": "抱", "pinyin": "bào", "meaning": "ôm"},
    {"hanzi": "报名", "pinyin": "bàomíng", "meaning": "đăng kí"},
    {"hanzi": "并且", "pinyin": "bìngqiě", "meaning": "đồng thời"},
    {"hanzi": "博士", "pinyin": "bóshì", "meaning": "tiến sĩ"},
    {"hanzi": "包子", "pinyin": "bāozi", "meaning": "bánh bao"},
    {"hanzi": "倍", "pinyin": "bèi", "meaning": "lần"},
    {"hanzi": "保证", "pinyin": "bǎozhèng", "meaning": "đảm bảo, cam đoan"},
    {"hanzi": "保护", "pinyin": "bǎohù", "meaning": "che chở, bảo vệ"},
    {"hanzi": "不过", "pinyin": "bùguò", "meaning": "nhưng"},
    {"hanzi": "不管", "pinyin": "bùguǎn", "meaning": "bất kể"},
    {"hanzi": "不得不", "pinyin": "bù dé bù", "meaning": "đành"},
    {"hanzi": "不仅", "pinyin": "bùjǐn", "meaning": "không những"},
    {"hanzi": "擦", "pinyin": "cā", "meaning": "lau"},
    {"hanzi": "餐厅", "pinyin": "cāntīng", "meaning": "căng tin, nhà ăn"},
    {"hanzi": "长江", "pinyin": "chángjiāng", "meaning": "Trường Giang"},
    {"hanzi": "长城", "pinyin": "chángchéng", "meaning": "Trường Thành"},
    {"hanzi": "错误", "pinyin": "cuòwù", "meaning": "sai lầm"},
    {"hanzi": "重新", "pinyin": "chóngxīn", "meaning": "làm lại"},
    {"hanzi": "超过", "pinyin": "chāoguò", "meaning": "vượt trên"},
    {"hanzi": "诚实", "pinyin": "chéngshí", "meaning": "trung thực"},
    {"hanzi": "词语", "pinyin": "cíyǔ", "meaning": "từ ngữ"},
    {"hanzi": "粗心", "pinyin": "cūxīn", "meaning": "thô lỗ, cẩu thả"},
    {"hanzi": "窗户", "pinyin": "chuānghù", "meaning": "cửa sổ"},
    {"hanzi": "猜", "pinyin": "cāi", "meaning": "đoán"},
    {"hanzi": "材料", "pinyin": "cáiliào", "meaning": "tài liệu"},
    {"hanzi": "抽烟", "pinyin": "chōuyān", "meaning": "hút thuốc"},
    {"hanzi": "成功", "pinyin": "chénggōng", "meaning": "thành công"},
    {"hanzi": "成为", "pinyin": "chéngwéi", "meaning": "trở thành"},
    {"hanzi": "差不多", "pinyin": "chàbuduō", "meaning": "gần như"},
    {"hanzi": "尝", "pinyin": "cháng", "meaning": "nếm thử"},
    {"hanzi": "存", "pinyin": "cún", "meaning": "giữ, tiết kiệm, tồn"},
    {"hanzi": "场", "pinyin": "chǎng", "meaning": "trận, suất"},
    {"hanzi": "吃惊", "pinyin": "chījīng", "meaning": "ngạc nhiên"},
    {"hanzi": "参观", "pinyin": "cānguān", "meaning": "tham quan"},
    {"hanzi": "厨房", "pinyin": "chúfáng", "meaning": "phòng bếp"},
    {"hanzi": "厕所", "pinyin": "cèsuǒ", "meaning": "phòng vệ sinh"},
    {"hanzi": "出生", "pinyin": "chūshēng", "meaning": "ra đời"},
    {"hanzi": "出现", "pinyin": "chūxiàn", "meaning": "xuất hiện"},
    {"hanzi": "出差", "pinyin": "chūchāi", "meaning": "đi công tác"},
    {"hanzi": "出发", "pinyin": "chūfā", "meaning": "xuất phát"},
    {"hanzi": "传真", "pinyin": "chuánzhēn", "meaning": "fax, bản fax"},
    {"hanzi": "从来", "pinyin": "cónglái", "meaning": "từ trước đến nay"},
    {"hanzi": "乘坐", "pinyin": "chéngzuò", "meaning": "ngồi xe"},
    {"hanzi": "答案", "pinyin": "dá’àn", "meaning": "đáp án"},
    {"hanzi": "道歉", "pinyin": "dàoqiàn", "meaning": "xin lỗi"},
    {"hanzi": "调查", "pinyin": "diàochá", "meaning": "điều tra"},
    {"hanzi": "肚子", "pinyin": "dùzi", "meaning": "bụng"},
    {"hanzi": "等", "pinyin": "děng", "meaning": "vân vân"},
    {"hanzi": "短信", "pinyin": "duǎnxìn", "meaning": "tin nhắn"},
    {"hanzi": "登机牌", "pinyin": "dēngjīpái", "meaning": "thẻ lên tàu"},
    {"hanzi": "掉", "pinyin": "diào", "meaning": "rơi"},
    {"hanzi": "打针", "pinyin": "dǎzhēn", "meaning": "tiêm"},
    {"hanzi": "打招呼", "pinyin": "dǎ zhāohū", "meaning": "chào hỏi"},
    {"hanzi": "打折", "pinyin": "dǎzhé", "meaning": "giảm giá"},
    {"hanzi": "打扰", "pinyin": "dǎrǎo", "meaning": "làm phiền"},
    {"hanzi": "打扮", "pinyin": "dǎbàn", "meaning": "trau chuốt, trang điểm"},
    {"hanzi": "打印", "pinyin": "dǎyìn", "meaning": "in ấn"},
    {"hanzi": "戴", "pinyin": "dài", "meaning": "đeo"},
    {"hanzi": "得意", "pinyin": "déyì", "meaning": "đắc ý"},
    {"hanzi": "得", "pinyin": "de", "meaning": "trợ từ"},
    {"hanzi": "当时", "pinyin": "dāngshí", "meaning": "lúc đó"},
    {"hanzi": "当", "pinyin": "dāng", "meaning": "làm"},
    {"hanzi": "底", "pinyin": "dǐ", "meaning": "đáy"},
    {"hanzi": "导游", "pinyin": "dǎoyóu", "meaning": "hướng dẫn viên du lịch"},
    {"hanzi": "符合", "pinyin": "fúhé", "meaning": "phù hợp"},
    {"hanzi": "父亲", "pinyin": "fùqīn", "meaning": "bố"},
    {"hanzi": "烦恼", "pinyin": "fánnǎo", "meaning": "phiền脑 (phiền não)"},
    {"hanzi": "法律", "pinyin": "fǎlǜ", "meaning": "pháp luật"},
    {"hanzi": "方面", "pinyin": "fāngmiàn", "meaning": "phương diện"},
    {"hanzi": "方法", "pinyin": "fāngfǎ", "meaning": "phương pháp"},
    {"hanzi": "方向", "pinyin": "fāngxiàng", "meaning": "phương hướng"},
    {"hanzi": "放松", "pinyin": "fàngsōng", "meaning": "thư giãn"},
    {"hanzi": "放暑假", "pinyin": "fàngshǔjià", "meaning": "nghỉ hè"},
    {"hanzi": "放弃", "pinyin": "fàngqì", "meaning": "vứt bỏ, từ bỏ"},
    {"hanzi": "房东", "pinyin": "fángdōng", "meaning": "chủ nhà"},
    {"hanzi": "富", "pinyin": "fù", "meaning": "giàu"},
    {"hanzi": "复杂", "pinyin": "fùzá", "meaning": "phức tạp"},
    {"hanzi": "复印", "pinyin": "fùyìn", "meaning": "phô tô"},
    {"hanzi": "否则", "pinyin": "fǒuzé", "meaning": "nếu không thì"},
    {"hanzi": "发展", "pinyin": "fāzhǎn", "meaning": "phát triển"},
    {"hanzi": "反对", "pinyin": "fǎnduì", "meaning": "phản đối"},
    {"hanzi": "份", "pinyin": "fèn", "meaning": "phần"},
    {"hanzi": "付款", "pinyin": "fùkuǎn", "meaning": "thanh toán"},
    {"hanzi": "丰富", "pinyin": "fēngfù", "meaning": "phong phú"},
    {"hanzi": "改变", "pinyin": "gǎibiàn", "meaning": "thay đổi"},
    {"hanzi": "鼓励", "pinyin": "gǔlì", "meaning": "cổ vũ"},
    {"hanzi": "高速公路", "pinyin": "gāosù gōng lù", "meaning": "đường cao tốc"},
    {"hanzi": "顾客", "pinyin": "gùkè", "meaning": "khách hàng"},
    {"hanzi": "逛", "pinyin": "guàng", "meaning": "đi dạo"},
    {"hanzi": "过程", "pinyin": "guòchéng", "meaning": "quá trình"},
    {"hanzi": "赶", "pinyin": "gǎn", "meaning": "đuổi theo"},
    {"hanzi": "购物", "pinyin": "gòuwù", "meaning": "mua sắm"},
    {"hanzi": "规定", "pinyin": "guīdìng", "meaning": "qui định"},
    {"hanzi": "观众", "pinyin": "guānzhòng", "meaning": "khán giả"},
    {"hanzi": "胳膊", "pinyin": "gēbo", "meaning": "cánh tay"},
    {"hanzi": "管理", "pinyin": "guǎnlǐ", "meaning": "quản lý"},
    {"hanzi": "果汁", "pinyin": "guǒzhī", "meaning": "nước hoa quả"},
    {"hanzi": "敢", "pinyin": "gǎn", "meaning": "dám"},
    {"hanzi": "故意", "pinyin": "gùyì", "meaning": "cố ý"},
    {"hanzi": "挂", "pinyin": "guà", "meaning": "treo"},
    {"hanzi": "感谢", "pinyin": "gǎnxiè", "meaning": "cảm ơn"},
    {"hanzi": "感觉", "pinyin": "gǎnjué", "meaning": "cảm giác"},
    {"hanzi": "感情", "pinyin": "gǎnqíng", "meaning": "tình cảm"},
    {"hanzi": "感动", "pinyin": "gǎndòng", "meaning": "cảm động"},
    {"hanzi": "广播", "pinyin": "guǎngbō", "meaning": "phát thanh"},
    {"hanzi": "广告", "pinyin": "guǎnggào", "meaning": "quảng cáo"},
    {"hanzi": "干杯", "pinyin": "gānbēi", "meaning": "cạn ly"},
    {"hanzi": "计划", "pinyin": "jìhuà", "meaning": "kế hoạch"},
    {"hanzi": "警察", "pinyin": "jǐngchá", "meaning": "cảnh sát"},
    {"hanzi": "解释", "pinyin": "jiěshì", "meaning": "giải thích"},
    {"hanzi": "节约", "pinyin": "jiéyuē", "meaning": "tiết kiệm"},
    {"hanzi": "节", "pinyin": "jié", "meaning": "tiết"},
    {"hanzi": "聚会", "pinyin": "jùhuì", "meaning": "tụ tập"},
    {"hanzi": "继续", "pinyin": "jìxù", "meaning": "tiếp tục"},
    {"hanzi": "结果", "pinyin": "jiéguǒ", "meaning": "kết quả"},
    {"hanzi": "经验", "pinyin": "jīngyàn", "meaning": "kinh nghiệm"},
    {"hanzi": "经济", "pinyin": "jīngjì", "meaning": "kinh tế"},
    {"hanzi": "经历", "pinyin": "jīnglì", "meaning": "trải qua, kinh qua"},
    {"hanzi": "紧张", "pinyin": "jǐnzhāng", "meaning": "căng thẳng"},
    {"hanzi": "精彩", "pinyin": "jīngcǎi", "meaning": "hấp dẫn"},
    {"hanzi": "竟然", "pinyin": "jìngrán", "meaning": "mà lại"},
    {"hanzi": "竞争", "pinyin": "jìngzhēng", "meaning": "cạnh tranh"},
    {"hanzi": "究竟", "pinyin": "jiūjìng", "meaning": "rốt cuộc"},
    {"hanzi": "积累", "pinyin": "jīlěi", "meaning": "tích lũy"},
    {"hanzi": "禁止", "pinyin": "jìnzhǐ", "meaning": "cấm"},
    {"hanzi": "激动", "pinyin": "jīdòng", "meaning": "xúc động"},
    {"hanzi": "景色", "pinyin": "jǐngsè", "meaning": "cảnh sắc"},
    {"hanzi": "既然", "pinyin": "jìrán", "meaning": "đã…."},
    {"hanzi": "教育", "pinyin": "jiàoyù", "meaning": "giáo dục"},
    {"hanzi": "教授", "pinyin": "jiàoshòu", "meaning": "giáo sư"},
    {"hanzi": "接着", "pinyin": "jiēzhe", "meaning": "tiếp theo"},
    {"hanzi": "接受", "pinyin": "jiēshòu", "meaning": "tiếp nhận"},
    {"hanzi": "拒绝", "pinyin": "jùjué", "meaning": "từ chối"},
    {"hanzi": "技术", "pinyin": "jìshù", "meaning": "kỹ thuật"},
    {"hanzi": "建议", "pinyin": "jiànyì", "meaning": "kiến nghị"},
    {"hanzi": "尽管", "pinyin": "jǐnguǎn", "meaning": "tuy rằng"},
    {"hanzi": "将来", "pinyin": "jiānglái", "meaning": "tương lai"},
    {"hanzi": "寄", "pinyin": "jì", "meaning": "gửi"},
    {"hanzi": "家具", "pinyin": "jiājù", "meaning": "đồ gia dụng"},
    {"hanzi": "奖金", "pinyin": "jiǎngjīn", "meaning": "học bổng"},
    {"hanzi": "基础", "pinyin": "jīchǔ", "meaning": "cơ sở, căn bản"},
    {"hanzi": "坚持", "pinyin": "jiānchí", "meaning": "kiên trì"},
    {"hanzi": "及时", "pinyin": "jíshí", "meaning": "kịp thời"},
    {"hanzi": "即使", "pinyin": "jíshǐ", "meaning": "cho dù"},
    {"hanzi": "加班", "pinyin": "jiābān", "meaning": "tăng ca"},
    {"hanzi": "加油站", "pinyin": "jiāyóuzhàn", "meaning": "cây xăng"},
    {"hanzi": "减肥", "pinyin": "jiǎnféi", "meaning": "giảm béo"},
    {"hanzi": "减少", "pinyin": "jiǎnshǎo", "meaning": "cắt giảm"},
    {"hanzi": "假", "pinyin": "jiǎ", "meaning": "giả"},
    {"hanzi": "价格", "pinyin": "jiàgé", "meaning": "giá cả"},
    {"hanzi": "京剧", "pinyin": "jīngjù", "meaning": "kinh kịch"},
    {"hanzi": "交通", "pinyin": "jiāotōng", "meaning": "giao thông"},
    {"hanzi": "交流", "pinyin": "jiāoliú", "meaning": "giao lưu"},
    {"hanzi": "交", "pinyin": "jiāo", "meaning": "giao"},
    {"hanzi": "举行", "pinyin": "jǔxíng", "meaning": "tổ chức"},
    {"hanzi": "举办", "pinyin": "jǔbàn", "meaning": "tổ chức"},
    {"hanzi": "举", "pinyin": "jǔ", "meaning": "giơ, nâng"},
    {"hanzi": "开玩笑", "pinyin": "kāi wánxiào", "meaning": "đùa"},
    {"hanzi": "苦", "pinyin": "kǔ", "meaning": "khổ, đắng"},
    {"hanzi": "肯定", "pinyin": "kěndìng", "meaning": "khẳng định"},
    {"hanzi": "考虑", "pinyin": "kǎolǜ", "meaning": "suy nghĩ"},
    {"hanzi": "空气", "pinyin": "kōngqì", "meaning": "không khí"},
    {"hanzi": "空", "pinyin": "kōng", "meaning": "trống rỗng"},
    {"hanzi": "科学", "pinyin": "kēxué", "meaning": "khoa học"},
    {"hanzi": "矿泉水", "pinyin": "kuàngquánshuǐ", "meaning": "nước khoáng"},
    {"hanzi": "看法", "pinyin": "kànfǎ", "meaning": "quan điểm"},
    {"hanzi": "烤鸭", "pinyin": "kǎoyā", "meaning": "vịt quay"},
    {"hanzi": "棵", "pinyin": "kē", "meaning": "lượng từ cho cây"},
    {"hanzi": "恐怕", "pinyin": "kǒngpà", "meaning": "e rằng"},
    {"hanzi": "开心", "pinyin": "kāixīn", "meaning": "vui vẻ"},
    {"hanzi": "客厅", "pinyin": "kètīng", "meaning": "phòng khách"},
    {"hanzi": "困难", "pinyin": "kùnnán", "meaning": "khó khăn"},
    {"hanzi": "困", "pinyin": "kùn", "meaning": "buồn ngủ"},
    {"hanzi": "咳嗽", "pinyin": "késou", "meaning": "ho"},
    {"hanzi": "可是", "pinyin": "kěshì", "meaning": "nhưng"},
    {"hanzi": "可惜", "pinyin": "kěxī", "meaning": "đáng tiếc"},
    {"hanzi": "可怜", "pinyin": "kělián", "meaning": "đáng thương"},
    {"hanzi": "垃圾桶", "pinyin": "lājī tǒng", "meaning": "thùng rác"},
    {"hanzi": "零钱", "pinyin": "língqián", "meaning": "tiền lẻ"},
    {"hanzi": "连", "pinyin": "lián", "meaning": "liên kết, nối"},
    {"hanzi": "辣", "pinyin": "là", "meaning": "cay"},
    {"hanzi": "联系", "pinyin": "liánxì", "meaning": "liên hệ"},
    {"hanzi": "老虎", "pinyin": "lǎohǔ", "meaning": "hổ"},
    {"hanzi": "礼貌", "pinyin": "lǐmào", "meaning": "lễ phép, lịch sự"},
    {"hanzi": "礼拜天", "pinyin": "lǐbàitiān", "meaning": "chủ nhật"},
    {"hanzi": "留", "pinyin": "liú", "meaning": "lưu lại, ở lại"},
    {"hanzi": "理解", "pinyin": "lǐjiě", "meaning": "lý giải, hiểu"},
    {"hanzi": "理想", "pinyin": "lǐxiǎng", "meaning": "lý tưởng"},
    {"hanzi": "理发", "pinyin": "lǐfà", "meaning": "cắt tóc"},
    {"hanzi": "浪费", "pinyin": "làngfèi", "meaning": "lãng phí"},
    {"hanzi": "浪漫", "pinyin": "làngmàn", "meaning": "lãng mạn"},
    {"hanzi": "流行", "pinyin": "liúxíng", "meaning": "thịnh hành"},
    {"hanzi": "破", "pinyin": "pò", "meaning": "rách, nổ"},
    {"hanzi": "皮肤", "pinyin": "pífū", "meaning": "da"},
    {"hanzi": "普遍", "pinyin": "pǔbiàn", "meaning": "phổ biến"},
    {"hanzi": "普通话", "pinyin": "pǔtōnghuà", "meaning": "tiếng phổ thông"},
    {"hanzi": "排列", "pinyin": "páiliè", "meaning": "liệt kê"},
    {"hanzi": "批评", "pinyin": "pīpíng", "meaning": "phê bình"},
    {"hanzi": "平时", "pinyin": "píngshí", "meaning": "bình thường"},
    {"hanzi": "判断", "pinyin": "pànduàn", "meaning": "phán đoán"},
    {"hanzi": "乒乓球", "pinyin": "pīngpāngqiú", "meaning": "bóng bàn"},
    {"hanzi": "其次", "pinyin": "qícì", "meaning": "tiếp theo"},
    {"hanzi": "轻松", "pinyin": "qīngsōng", "meaning": "thoải mái"},
    {"hanzi": "轻", "pinyin": "qīng", "meaning": "nhẹ"},
    {"hanzi": "缺点", "pinyin": "quēdiǎn", "meaning": "khuyết điểm"},
    {"hanzi": "缺少", "pinyin": "quēshǎo", "meaning": "thiếu"},
    {"hanzi": "签证", "pinyin": "qiānzhèng", "meaning": "visa"},
    {"hanzi": "穷", "pinyin": "qióng", "meaning": "nghèo"},
    {"hanzi": "确实", "pinyin": "quèshí", "meaning": "thật sự"},
    {"hanzi": "气候", "pinyin": "qìhòu", "meaning": "khí hậu"},
    {"hanzi": "桥", "pinyin": "qiáo", "meaning": "cầu"},
    {"hanzi": "敲", "pinyin": "qiāo", "meaning": "gõ"},
    {"hanzi": "情况", "pinyin": "qíngkuàng", "meaning": "tình hình"},
    {"hanzi": "巧克力", "pinyin": "qiǎokèlì", "meaning": "sô cô la"},
    {"hanzi": "取", "pinyin": "qǔ", "meaning": "lấy"},
    {"hanzi": "却", "pinyin": "què", "meaning": "lại"},
    {"hanzi": "千万", "pinyin": "qiānwàn", "meaning": "nhất thiết"},
    {"hanzi": "区别", "pinyin": "qūbié", "meaning": "khác biệt"},
    {"hanzi": "其中", "pinyin": "qízhōng", "meaning": "trong đó"},
    {"hanzi": "全部", "pinyin": "quánbù", "meaning": "toàn bộ"},
    {"hanzi": "亲戚", "pinyin": "qīnqi", "meaning": "họ hàng"},
    {"hanzi": "然而", "pinyin": "rán’ér", "meaning": "vậy mà"},
    {"hanzi": "热闹", "pinyin": "rènào", "meaning": "náo nhiệt"},
    {"hanzi": "日记", "pinyin": "rìjì", "meaning": "nhật kí"},
    {"hanzi": "扔", "pinyin": "rēng", "meaning": "ném"},
    {"hanzi": "入口", "pinyin": "rùkǒu", "meaning": "cửa vào"},
    {"hanzi": "任务", "pinyin": "rènwù", "meaning": "nhiệm vụ"},
    {"hanzi": "任何", "pinyin": "rènhé", "meaning": "bất kì"},
    {"hanzi": "仍然", "pinyin": "réngrán", "meaning": "vẫn"},
    {"hanzi": "散步", "pinyin": "sànbù", "meaning": "tản bộ"},
    {"hanzi": "首都", "pinyin": "shǒudū", "meaning": "thủ đô"},
    {"hanzi": "首先", "pinyin": "shǒuxiān", "meaning": "đầu tiên"},
    {"hanzi": "顺序", "pinyin": "shùnxù", "meaning": "thứ tự"},
    {"hanzi": "顺利", "pinyin": "shùnlì", "meaning": "thuận lợi"},
    {"hanzi": "顺便", "pinyin": "shùnbiàn", "meaning": "nhân tiện"},
    {"hanzi": "随着", "pinyin": "suízhe", "meaning": "cùng với"},
    {"hanzi": "随便", "pinyin": "suíbiàn", "meaning": "tùy tiện, tự nhiên"},
    {"hanzi": "小说", "pinyin": "xiǎoshuō", "meaning": "tiểu thuyết"},
    {"hanzi": "小吃", "pinyin": "xiǎochī", "meaning": "đồ ăn vặt"},
    {"hanzi": "小伙子", "pinyin": "xiǎohuǒzi", "meaning": "anh chàng"},
    {"hanzi": "学期", "pinyin": "xuéqī", "meaning": "học kì"},
    {"hanzi": "响", "pinyin": "xiǎng", "meaning": "kêu"},
    {"hanzi": "咸", "pinyin": "xián", "meaning": "mặn"},
    {"hanzi": "吸引", "pinyin": "xīyǐn", "meaning": "thu hút"},
    {"hanzi": "兴奋", "pinyin": "xīngfèn", "meaning": "hưng phấn, hứng khởi"},
    {"hanzi": "修理", "pinyin": "xiūlǐ", "meaning": "sửa chữa"},
    {"hanzi": "信息", "pinyin": "xìnxī", "meaning": "thông tin"},
    {"hanzi": "信心", "pinyin": "xìnxīn", "meaning": "niềm tin"},
    {"hanzi": "信封", "pinyin": "xìnfēng", "meaning": "bức thư"},
    {"hanzi": "压力", "pinyin": "yālì", "meaning": "áp lực"},
    {"hanzi": "预习", "pinyin": "yùxí", "meaning": "chuẩn bị trước"},
    {"hanzi": "页", "pinyin": "yè", "meaning": "trang mạng"},
    {"hanzi": "阳光", "pinyin": "yángguāng", "meaning": "ánh nắng"},
    {"hanzi": "阅读", "pinyin": "yuèdú", "meaning": "đọc hiểu"},
    {"hanzi": "钥匙", "pinyin": "yàoshi", "meaning": "chìa khóa"},
    {"hanzi": "邮局", "pinyin": "yóujú", "meaning": "bưu điện"},
    {"hanzi": "邀请", "pinyin": "yāoqǐng", "meaning": "mời"},
    {"hanzi": "赢", "pinyin": "yíng", "meaning": "thắng"},
    {"hanzi": "语言", "pinyin": "yǔyán", "meaning": "ngôn ngữ"},
    {"hanzi": "语法", "pinyin": "yǔfǎ", "meaning": "ngữ pháp"},
    {"hanzi": "要是", "pinyin": "yàoshi", "meaning": "nếu"},
    {"hanzi": "艺术", "pinyin": "yìshù", "meaning": "nghệ thuật"},
    {"hanzi": "羽毛球", "pinyin": "yǔmáoqiú", "meaning": "cầu lông"},
    {"hanzi": "约会", "pinyin": "yuēhuì", "meaning": "hẹn, cuộc hẹn"},
    {"hanzi": "研究", "pinyin": "yánjiū", "meaning": "nghiên cứu"},
    {"hanzi": "眼镜", "pinyin": "yǎnjìng", "meaning": "kính mắt"},
    {"hanzi": "盐", "pinyin": "yán", "meaning": "muối"},
    {"hanzi": "由于", "pinyin": "yóuyú", "meaning": "do"},
    {"hanzi": "由", "pinyin": "yóu", "meaning": "do"},
    {"hanzi": "牙膏", "pinyin": "yágāo", "meaning": "kem đánh răng"},
    {"hanzi": "演员", "pinyin": "yǎnyuán", "meaning": "diễn viên"},
    {"hanzi": "演出", "pinyin": "yǎnchū", "meaning": "buổi diễn"},
    {"hanzi": "永远", "pinyin": "yǒngyuǎn", "meaning": "mãi mãi"},
    {"hanzi": "样子", "pinyin": "yàngzi", "meaning": "dáng ngoài, bề ngoài"},
    {"hanzi": "有趣", "pinyin": "yǒuqù", "meaning": "hứng thú"},
    {"hanzi": "意见", "pinyin": "yìjiàn", "meaning": "ý kiến"},
    {"hanzi": "愉快", "pinyin": "yúkuài", "meaning": "vui vẻ"},
    {"hanzi": "引起", "pinyin": "yǐnqǐ", "meaning": "dẫn đến, gây ra"},
    {"hanzi": "应聘", "pinyin": "yìngpìn", "meaning": "ứng tuyển"},
    {"hanzi": "只要", "pinyin": "zhǐyào", "meaning": "chỉ cần"},
    {"hanzi": "只好", "pinyin": "zhǐhǎo", "meaning": "đành"},
    {"hanzi": "占线", "pinyin": "zhànxiàn", "meaning": "máy bận"},
    {"hanzi": "准确", "pinyin": "zhǔnquè", "meaning": "chính xác"},
    {"hanzi": "准时", "pinyin": "zhǔnshí", "meaning": "đúng giờ"},
    {"hanzi": "值得", "pinyin": "zhídé", "meaning": "đáng"},
    {"hanzi": "作者", "pinyin": "zuòzhě", "meaning": "tác gia"},
    {"hanzi": "作用", "pinyin": "zuòyòng", "meaning": "tác dụng"},
    {"hanzi": "作家", "pinyin": "zuòjiā", "meaning": "tác gia"},
    {"hanzi": "仔细", "pinyin": "zǐxì", "meaning": "cẩn thận"},
    {"hanzi": "之", "pinyin": "zhī", "meaning": "chi"},
    {"hanzi": "主意", "pinyin": "zhǔyì", "meaning": "chủ ý"},
    {"hanzi": "专门", "pinyin": "zhuānmén", "meaning": "chuyên môn"},
    {"hanzi": "专业", "pinyin": "zhuānyè", "meaning": "chuyên ngành"}
]

# Random sample of 6 cards stored in session_state or recalculated
if "fc_sample" not in st.session_state:
    st.session_state["fc_sample"] = random.sample(VOCAB_600, 6)

with st.expander("🎴 **FLASHCARD TỪ VỰNG HSK4**", expanded=True):
    col_fc_btn, _ = st.columns([1, 3])
    with col_fc_btn:
        if st.button("🔀 Đổi thẻ ngẫu nhiên"):
            st.session_state["fc_sample"] = random.sample(VOCAB_600, 6)
            st.rerun()
            
    cols = st.columns(3)
    for idx, card in enumerate(st.session_state["fc_sample"]):
        with cols[idx % 3]:
            palette = PASTEL_PALETTES[idx % len(PASTEL_PALETTES)]
            card_html = f"""
            <div class="flashcard-box">
                <div class="flashcard-inner">
                    <div class="flashcard-front" style="background: {palette['front_bg']}; border: 2px solid {palette['front_border']};">
                        <div class="fc-hanzi" style="color: {palette['front_text']};">{card['hanzi']}</div>
                    </div>
                    <div class="flashcard-back" style="background: {palette['back_bg']}; border: 2px solid {palette['back_border']};">
                        <div class="fc-pinyin" style="color: {palette['back_text']}; margin-bottom: 6px;">{card['pinyin']}</div>
                        <div class="fc-meaning" style="color: {palette['back_text']};">{card['meaning']}</div>
                    </div>
                </div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

st.markdown("---")

# --- BẢNG NHẬP HỌ TÊN HỌC VIÊN NẰM TRỰC TIẾP TRÊN TRANG MAIN ---
st.markdown("### 📝 Thông tin học viên")
student_name = st.text_input("Họ và tên học viên (bắt buộc trước khi làm bài):", key="global_student_name", placeholder="Ví dụ: Nguyễn Văn A").strip()

if student_name:
    st.success(f"Chào mừng **{student_name}**! Hãy chọn bộ đề bên dưới để bắt đầu làm bài.")

TEST_DATA = [
    {
        "id": "01-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Ví dụ 1",
        "questions": [
            {"num": 1, "text": "王老师对学生的要求很高，要得到他的_______很不容易。", "options": ["A. 表扬", "B. 得意", "C. 从来", "D. 确实", "E. 理想"], "ans": "A. 表扬", "key": "A"},
            {"num": 2, "text": "听说老张的儿子找到了一个好工作，你看他那_______的样子。", "options": ["A. 表扬", "B. 得意", "C. 从来", "D. 确实", "E. 理想"], "ans": "B. 得意", "key": "B"},
            {"num": 3, "text": "他学习很努力，_______不会因为生病就不来上课。", "options": ["A. 表扬", "B. 得意", "C. 从来", "D. 确实", "E. 理想"], "ans": "C. 从来", "key": "C"},
            {"num": 4, "text": "父母常常告诉孩子，要为自己的_______而努力。", "options": ["A. 表扬", "B. 得意", "C. 从来", "D. 确实", "E. 理想"], "ans": "E. 理想", "key": "E"},
            {"num": 5, "text": "我们已经调查过了，这笔钱_______不是她拿的。", "options": ["A. 表扬", "B. 得意", "C. 从来", "D. 确实", "E. 理想"], "ans": "D. 确实", "key": "D"},
            {"num": 6, "text": "A: 你明天去开会吗？\n\nB: 当然要去啊，_______就要被经理批评了。", "options": ["A. 吸引", "B. 顺便", "C. 千万", "D. 否则", "E. 烦恼"], "ans": "D. 否则", "key": "D"},
            {"num": 7, "text": "A: 哎呀，我把数字填错了。\n\nB: _______要仔细啊，这个表格是非常重要的。", "options": ["A. 吸引", "B. 顺便", "C. 千万", "D. 否则", "E. 烦恼"], "ans": "C. 千万", "key": "C"},
            {"num": 8, "text": "A: 老师，最近我女儿很爱哭，我问她怎么了，她又不说。\n\nB: 别太担心了，让我去问问她有什么_______。", "options": ["A. 吸引", "B. 顺便", "C. 千万", "D. 否则", "E. 烦恼"], "ans": "E. 烦恼", "key": "E"},
            {"num": 9, "text": "A: 我要去书店，你去吗？\n\nB: 我现在没空儿，你_______帮我买一本汉英词典吧。", "options": ["A. 吸引", "B. 顺便", "C. 千万", "D. 否则", "E. 烦恼"], "ans": "B. 顺便", "key": "B"},
            {"num": 10, "text": "A: 到底是什么这么_______你啊？看得那么认真，我叫你，你都没听见。\n\nB: 我在看小说，这本小说特别意思。", "options": ["A. 吸引", "B. 顺便", "C. 千万", "D. 否则", "E. 烦恼"], "ans": "A. 吸引", "key": "A"}
        ]
    },
    {
        "id": "02-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 1",
        "questions": [
            {"num": 1, "text": "这条河很深，为了保证各位的_______，请大家不要在河边游玩。", "options": ["A. 方向", "B. 安全", "C. 规定", "D. 风景", "E. 世纪"], "ans": "B. 安全", "key": "B"},
            {"num": 2, "text": "为顾客提供更好的服务，一直是我们努力的_______。", "options": ["A. 方向", "B. 安全", "C. 规定", "D. 风景", "E. 世纪"], "ans": "A. 方向", "key": "A"},
            {"num": 3, "text": "我们家门前的那条马路是 1920 年修的，到现在都快一个_______了。", "options": ["A. 方向", "B. 安全", "C. 规定", "D. 风景", "E. 世纪"], "ans": "E. 世纪", "key": "E"},
            {"num": 4, "text": "那座山上的_______特别美，我们在那儿照了很多照片。", "options": ["A. 方向", "B. 安全", "C. 规定", "D. 风景", "E. 世纪"], "ans": "D. 风景", "key": "D"},
            {"num": 5, "text": "抱歉，先生，按照_______，每位乘客最多只能带两件行李。", "options": ["A. 方向", "B. 安全", "C. 规定", "D. 风景", "E. 世纪"], "ans": "C. 规定", "key": "C"},
            {"num": 6, "text": "A: 你周末经常去参加社会活动？\n\nB: 对，我觉得光学习书本_______是不够的，还要多积累社会经验。", "options": ["A. 沙发", "B. 公里", "C. 力气", "D. 演员", "E. 知识"], "ans": "E. 知识", "key": "E"},
            {"num": 7, "text": "A: 你看来看去，到底想买哪一个呀？\n\nB: 这两个_______我都喜欢，真是太难做决定了。", "options": ["A. 沙发", "B. 公里", "C. 力气", "D. 演员", "E. 知识"], "ans": "A. 沙发", "key": "A"},
            {"num": 8, "text": "A: 听说这次活动会邀请许多著名_______，是真的吗？\n\nB: 我也不太清楚，这次活动是小张负责的，你可以去问问他。", "options": ["A. 沙发", "B. 公里", "C. 力气", "D. 演员", "E. 知识"], "ans": "D. 演员", "key": "D"},
            {"num": 9, "text": "A: 你怎么了？胳膊疼吗？\n\nB: 不是，我刚才搬了一箱矿泉水上 7 楼，现在没_______了。", "options": ["A. 沙发", "B. 公里", "C. 力气", "D. 演员", "E. 知识"], "ans": "C. 力气", "key": "C"},
            {"num": 10, "text": "A: 真的吗？可是这辆车看起来还像是新的一样。\n\nB: 我都开了 10000 多_______了。", "options": ["A. 沙发", "B. 公里", "C. 力气", "D. 演员", "E. 知识"], "ans": "B. 公里", "key": "B"}
        ]
    },
    {
        "id": "03-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 2",
        "questions": [
            {"num": 1, "text": "以我们现在的技术的_______，解决这个问题还有点儿困难。", "options": ["A. 号码", "B. 全部", "C. 条件", "D. 叶子", "E. 语言"], "ans": "C. 条件", "key": "C"},
            {"num": 2, "text": "哥，你快来看看，这是什么植物呀？_______怎么这么宽？", "options": ["A. 号码", "B. 全部", "C. 条件", "D. 叶子", "E. 语言"], "ans": "D. 叶子", "key": "D"},
            {"num": 3, "text": "爱一个人就应该爱他的_______，包括他的优点和缺点。", "options": ["A. 号码", "B. 全部", "C. 条件", "D. 叶子", "E. 语言"], "ans": "B. 全部", "key": "B"},
            {"num": 4, "text": "在中国，手机_______一般由 11 个数字组成。", "options": ["A. 号码", "B. 全部", "C. 条件", "D. 叶子", "E. 语言"], "ans": "A. 号码", "key": "A"},
            {"num": 5, "text": "这篇报道我中午就要用，你帮我看看_______还有没有问题。", "options": ["A. 号码", "B. 全部", "C. 条件", "D. 叶子", "E. 语言"], "ans": "E. 语言", "key": "E"},
            {"num": 6, "text": "A: 我在网上买电影票吧，你要坐第几排？\n\nB: 我想要中间的_______。", "options": ["A. 签证", "B. 温度", "C. 座位", "D. 毛巾", "E. 密码"], "ans": "C. 座位", "key": "C"},
            {"num": 7, "text": "A: 小高，听说你出国的时间推迟了？\n\nB: 是的，我的_______还没有办好，大概 10 月底才能走。", "options": ["A. 签证", "B. 温度", "C. 座位", "D. 毛巾", "E. 密码"], "ans": "A. 签证", "key": "A"},
            {"num": 8, "text": "A: 妈，帮我拿条_______，外面雨真大啊。\n\nB: 又忘记带伞了吧？头发都湿了，先把头发擦干，别感冒了。", "options": ["A. 签证", "B. 温度", "C. 座位", "D. 毛巾", "E. 密码"], "ans": "D. 毛巾", "key": "D"},
            {"num": 9, "text": "A: 今天真冷啊，好像白天最高_______才 2℃。\n\nB: 刚才电视里说明天更冷。", "options": ["A. 签证", "B. 温度", "C. 座位", "D. 毛巾", "E. 密码"], "ans": "B. 温度", "key": "B"},
            {"num": 10, "text": "A: 行李箱的_______是多少？\n\nB: 你试试 1158，不对的话再试试 1185，应该是其中的一个。", "options": ["A. 签证", "B. 温度", "C. 座位", "D. 毛巾", "E. 密码"], "ans": "E. 密码", "key": "E"}
        ]
    },
    {
        "id": "04-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 3",
        "questions": [
            {"num": 1, "text": "真抱歉，我晚上要_______，不能和你们去逛街了。", "options": ["A. 禁止", "B. 举", "C. 引起", "D. 回忆", "E. 加班"], "ans": "E. 加班", "key": "E"},
            {"num": 2, "text": "飞机上_______使用手机，飞行过程中手机也要关上。", "options": ["A. 禁止", "B. 举", "C. 引起", "D. 回忆", "E. 加班"], "ans": "A. 禁止", "key": "A"},
            {"num": 3, "text": "这次演出非常顺利，感谢大家的努力。来，让我们共同_______杯！", "options": ["A. 禁止", "B. 举", "C. 引起", "D. 回忆", "E. 加班"], "ans": "B. 举", "key": "B"},
            {"num": 4, "text": "最近 10 年这个省经济增长很快，_______了很多人的关注。", "options": ["A. 禁止", "B. 举", "C. 引起", "D. 回忆", "E. 加班"], "ans": "C. 引起", "key": "C"},
            {"num": 5, "text": "爷爷常说，人年龄越大，越爱_______过去的事情。", "options": ["A. 禁止", "B. 举", "C. 引起", "D. 回忆", "E. 加班"], "ans": "D. 回忆", "key": "D"},
            {"num": 6, "text": "A: 你有没有李律师的电话号码？我想问他几个法律方面的问题。\n\nB: 有，我发到你手机上，你直接跟他_______就行。", "options": ["A. 联系", "B. 堵车", "C. 当", "D. 考虑", "E. 扔"], "ans": "A. 联系", "key": "A"},
            {"num": 7, "text": "A: 弟弟，你怎么把葡萄_______垃圾桶里了？\n\nB: 买回来好几天了，都不新鲜了，会吃坏肚子的。", "options": ["A. 联系", "B. 堵车", "C. 当", "D. 考虑", "E. 扔"], "ans": "E. 扔", "key": "E"},
            {"num": 8, "text": "A: 我_______了很久，还是决定离开现在的公司。\n\nB: 既然这样，那我们尊重你的选择。", "options": ["A. 联系", "B. 堵车", "C. 当", "D. 考虑", "E. 扔"], "ans": "D. 考虑", "key": "D"},
            {"num": 9, "text": "A: 男性也可以_______护士吗？\n\nB: 当然。只要做事认真、有耐心就行。", "options": ["A. 联系", "B. 堵车", "C. 当", "D. 考虑", "E. 扔"], "ans": "C. 当", "key": "C"},
            {"num": 10, "text": "A: 路上_______，恐怕我要晚一点儿才能到。\n\nB: 没事，不用着急，我也刚落地铁。", "options": ["A. 联系", "B. 堵车", "C. 当", "D. 考虑", "E. 扔"], "ans": "B. 堵车", "key": "B"}
        ]
    },
    {
        "id": "05-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 4",
        "questions": [
            {"num": 1, "text": "你希望感冒快点儿好的话，最好_______，吃药好得比较慢。", "options": ["A. 参观", "B. 打针", "C. 陪", "D. 调查", "E. 复印"], "ans": "B. 打针", "key": "B"},
            {"num": 2, "text": "根据_______，我们发现现在城市的离婚率越来越高。", "options": ["A. 参观", "B. 打针", "C. 陪", "D. 调查", "E. 复印"], "ans": "D. 调查", "key": "D"},
            {"num": 3, "text": "明天我们去_______博物馆，请大家做好准备。", "options": ["A. 参观", "B. 打针", "C. 陪", "D. 调查", "E. 复印"], "ans": "A. 参观", "key": "A"},
            {"num": 4, "text": "有时候，吃完晚饭，爸爸会_______着爷爷奶奶去附近的公园走走。", "options": ["A. 参观", "B. 打针", "C. 陪", "D. 调查", "E. 复印"], "ans": "C. 陪", "key": "C"},
            {"num": 5, "text": "我花了半个小时，才把这本书_______完。", "options": ["A. 参观", "B. 打针", "C. 陪", "D. 调查", "E. 复印"], "ans": "E. 复印", "key": "E"},
            {"num": 6, "text": "A: 你收拾行李要去哪儿？\n\nB: 我要去上海_______。", "options": ["A. 来得及", "B. 打折", "C. 出差", "D. 赚", "E. 逛"], "ans": "C. 出差", "key": "C"},
            {"num": 7, "text": "A: 喂，你现在在哪儿呢？\n\nB: 我和同事在外面_______街呢，马上就回去。", "options": ["A. 来得及", "B. 打折", "C. 出差", "D. 赚", "E. 逛"], "ans": "E. 逛", "key": "E"},
            {"num": 8, "text": "A: 对不起，这个问题我还要再考虑一下，明天告诉你晚不晚？\n\nB: 好的，没问题，_______。", "options": ["A. 来得及", "B. 打折", "C. 出差", "D. 赚", "E. 逛"], "ans": "A. 来得及", "key": "A"},
            {"num": 9, "text": "A: 他这几年做生意肯定_______了不少。\n\nB: 下次让他请客。", "options": ["A. 来得及", "B. 打折", "C. 出差", "D. 赚", "E. 逛"], "ans": "D. 赚", "key": "D"},
            {"num": 10, "text": "A: 商场的衣服最近都在_______，挺便宜的。我们明天去看看吧？\n\nB: 好啊，明天我们一起去。", "options": ["A. 来得及", "B. 打折", "C. 出差", "D. 赚", "E. 逛"], "ans": "B. 打折", "key": "B"}
        ]
    },
    {
        "id": "06-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 5",
        "questions": [
            {"num": 1, "text": "这两份材料，一份给王经理，_______一份给林主任。", "options": ["A. 任何", "B. 另外", "C. 咱们", "D. 各", "E. 一切"], "ans": "B. 另外", "key": "B"},
            {"num": 2, "text": "他是一名很优秀的学生，_______方面的表现都很出色。", "options": ["A. 任何", "B. 另外", "C. 咱们", "D. 各", "E. 一切"], "ans": "D. 各", "key": "D"},
            {"num": 3, "text": "明天_______一起去博物馆，好吗？", "options": ["A. 任何", "B. 另外", "C. 咱们", "D. 各", "E. 一切"], "ans": "C. 咱们", "key": "C"},
            {"num": 4, "text": "这个孩子特别聪明，_______字只要看过一遍，他都会写。", "options": ["A. 任何", "B. 另外", "C. 咱们", "D. 各", "E. 一切"], "ans": "A. 任何", "key": "A"},
            {"num": 5, "text": "这次活动的_______事务都由小李安排。", "options": ["A. 任何", "B. 另外", "C. 咱们", "D. 各", "E. 一切"], "ans": "E. 一切", "key": "E"},
            {"num": 6, "text": "A: 希望我们的工作能让您满意。\n\nB: 我非常满意，_______都安排得很好，谢谢你们。", "options": ["A. 一切", "B. 另外", "C. 咱们", "D. 各", "E. 任何"], "ans": "A. 一切", "key": "A"},
            {"num": 7, "text": "A: 今天商店打折，下班后_______去逛商店吧？\n\nB: 好啊。", "options": ["A. 一切", "B. 另外", "C. 咱们", "D. 各", "E. 任何"], "ans": "C. 咱们", "key": "C"},
            {"num": 8, "text": "A: 你怎么这么喜欢去旅行啊？\n\nB: 去旅行能了解_______个地方的风俗习惯、人文景观。", "options": ["A. 一切", "B. 另外", "C. 咱们", "D. 各", "E. 任何"], "ans": "D. 各", "key": "D"},
            {"num": 9, "text": "A: 他怎么了？\n\nB: 他只能在自己家里才能很快入睡，换了别的_______一个地方，他都睡不好。", "options": ["A. 一切", "B. 另外", "C. 咱们", "D. 各", "E. 任何"], "ans": "E. 任何", "key": "E"},
            {"num": 10, "text": "A: 你觉得留学生生活给你最大的影响是什么？\n\nB: 发现_______的一个世界。", "options": ["A. 一切", "B. 另外", "C. 咱们", "D. 各", "E. 任何"], "ans": "B. 另外", "key": "B"}
        ]
    },
    {
        "id": "07-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 6",
        "questions": [
            {"num": 1, "text": "这个歌特别好听，最近很_______，你竟然没听过？", "options": ["A. 安全", "B. 流行", "C. 重", "D. 顺利", "E. 辛苦"], "ans": "B. 流行", "key": "B"},
            {"num": 2, "text": "谢谢，不用了，这个行李箱一点儿都不_______，里面都是衣服。", "options": ["A. 安全", "B. 流行", "C. 重", "D. 顺利", "E. 辛苦"], "ans": "C. 重", "key": "C"},
            {"num": 3, "text": "这条河很深，为了保证各位的_______，请大家不要在河边游玩。", "options": ["A. 安全", "B. 流行", "C. 重", "D. 顺利", "E. 辛苦"], "ans": "A. 安全", "key": "A"},
            {"num": 4, "text": "这次演出非常_______，感谢大家的努力。来，让我们共同举杯！", "options": ["A. 安全", "B. 流行", "C. 重", "D. 顺利", "E. 辛苦"], "ans": "D. 顺利", "key": "D"},
            {"num": 5, "text": "今天的演出非常精彩，大家都_______了，早点儿回去休息吧。", "options": ["A. 安全", "B. 流行", "C. 重", "D. 顺利", "E. 辛苦"], "ans": "E. 辛苦", "key": "E"},
            {"num": 6, "text": "A: 小张，你的衣服是不是穿反了？\n\nB: 啊？对，我太_______了，竟然没发现。", "options": ["A. 符合", "B. 适合", "C. 乱", "D. 整齐", "E. 粗心"], "ans": "E. 粗心", "key": "E"},
            {"num": 7, "text": "A: 没想到你的房间这么_______。\n\nB: 知道你要来，我专门打扫了一上午。", "options": ["A. 符合", "B. 适合", "C. 乱", "D. 整齐", "E. 粗心"], "ans": "D. 整齐", "key": "D"},
            {"num": 8, "text": "A: 你写的作文内容不错，可是不太_______作文比赛的要求。\n\nB: 那我再改一下吧。", "options": ["A. 符合", "B. 适合", "C. 乱", "D. 整齐", "E. 粗心"], "ans": "A. 符合", "key": "A"},
            {"num": 9, "text": "A: 周末爬山怎么样？\n\nB: 好主意，这个季节很_______到外面运动。", "options": ["A. 符合", "B. 适合", "C. 乱", "D. 整齐", "E. 粗心"], "ans": "B. 适合", "key": "B"},
            {"num": 10, "text": "A: 你的头发长了，看上去有些_______。\n\nB: 是啊，我正准备下午去理发呢。", "options": ["A. 符合", "B. 适合", "C. 乱", "D. 整齐", "E. 粗心"], "ans": "C. 乱", "key": "C"}
        ]
    },
    {
        "id": "08-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 7",
        "questions": [
            {"num": 1, "text": "和同龄人相比，他看上去更_______一些。", "options": ["A. 成熟", "B. 轻松", "C. 复杂", "D. 害羞", "E. 活泼"], "ans": "A. 成熟", "key": "A"},
            {"num": 2, "text": "她的性格就像个孩子，_______又天真。", "options": ["A. 成熟", "B. 轻松", "C. 复杂", "D. 害羞", "E. 活泼"], "ans": "E. 活泼", "key": "E"},
            {"num": 3, "text": "昨天的乒乓球比赛他赢得很非常_______。", "options": ["A. 成熟", "B. 轻松", "C. 复杂", "D. 害羞", "E. 活泼"], "ans": "B. 轻松", "key": "B"},
            {"num": 4, "text": "这其实是一件很简单的事情，不要把它弄_______了。", "options": ["A. 成熟", "B. 轻松", "C. 复杂", "D. 害羞", "E. 活泼"], "ans": "C. 复杂", "key": "C"},
            {"num": 5, "text": "都这么大的人了，还_______呢？这有什么不好意思的？", "options": ["A. 成熟", "B. 轻松", "C. 复杂", "D. 害羞", "E. 活泼"], "ans": "D. 害羞", "key": "D"},
            {"num": 6, "text": "A: 小张，你有什么意见？\n\nB: 按照现在的速度，想要在规定时间内完成计划，好像有点儿_______。", "options": ["A. 粗心", "B. 成功", "C. 困难", "D. 厉害", "E. 浪费"], "ans": "C. 困难", "key": "C"},
            {"num": 7, "text": "A: 剩下这么多菜没吃完，太_______了。\n\nB: 让服务员拿几个盒子来，我们都带回家吧。", "options": ["A. 粗心", "B. 成功", "C. 困难", "D. 厉害", "E. 浪费"], "ans": "E. 浪费", "key": "E"},
            {"num": 8, "text": "A: 你真_______，刚买的手机又弄丢了。\n\nB: 刚刚还在的，肯定是被偷走了。", "options": ["A. 粗心", "B. 成功", "C. 困难", "D. 厉害", "E. 浪费"], "ans": "A. 粗心", "key": "A"},
            {"num": 9, "text": "A: 周末爬山怎么样？\n\nB: 好主意，这个季节很_______到外面运动。", "options": ["A. 粗心", "B. 成功", "C. 困难", "D. 厉害", "E. 浪费"], "ans": "D. 厉害", "key": "D"},
            {"num": 10, "text": "A: 明天就要开始比赛了，心里有点儿紧张。\n\nB: 我相信你的能力，祝你_______！", "options": ["A. 粗心", "B. 成功", "C. 困难", "D. 厉害", "E. 浪费"], "ans": "B. 成功", "key": "B"}
        ]
    },
    {
        "id": "09-CƠ BẢN - Bộ đề 10",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 10",
        "questions": [
            {"num": 1, "text": "其实许多事情_______很简单，只是我们想得太复杂了。", "options": ["A. 恐怕", "B. 仍然", "C. 却", "D. 大约", "E. 本来"], "ans": "E. 本来", "key": "E"},
            {"num": 2, "text": "这次报名的人中，_______有三分之二是硕士研究生。", "options": ["A. 恐怕", "B. 仍然", "C. 却", "D. 大约", "E. 本来"], "ans": "D. 大约", "key": "D"},
            {"num": 3, "text": "真奇怪，我从来没有来过这儿，_______对这里有种熟悉的感觉。", "options": ["A. 恐怕", "B. 仍然", "C. 却", "D. 大约", "E. 本来"], "ans": "C. 却", "key": "C"},
            {"num": 4, "text": "孙小姐来北京都快 4 年了，_______不习惯北方的气候。", "options": ["A. 恐怕", "B. 仍然", "C. 却", "D. 大约", "E. 本来"], "ans": "B. 仍然", "key": "B"},
            {"num": 5, "text": "这本语法书这么厚，我一个星期_______看不完。", "options": ["A. 恐怕", "B. 仍然", "C. 却", "D. 大约", "E. 本来"], "ans": "A. 恐怕", "key": "A"},
            {"num": 6, "text": "A: 下午考试，_______别忘了带准考证！\n\nB: 放心吧，我检查过了，该带的东西都在书包里。", "options": ["A. 千万", "B. 到底", "C. 刚刚", "D. 按时", "E. 顺便"], "ans": "A. 千万", "key": "A"},
            {"num": 7, "text": "A: 等会儿去散步的时候，_______去超市买个牙膏。\n\nB: 好，还买现在用的这种吧，我觉得挺好用的。", "options": ["A. 千万", "B. 到底", "C. 刚刚", "D. 按时", "E. 顺便"], "ans": "E. 顺便", "key": "E"},
            {"num": 8, "text": "A: 喂，你_______什么时候到啊？\n\nB: 马上。刚刚车没油了，好不容易才找到加油站。", "options": ["A. 千万", "B. 到底", "C. 刚刚", "D. 按时", "E. 顺便"], "ans": "B. 到底", "key": "B"},
            {"num": 9, "text": "A: 你看见小李了吗？我的车钥匙还在他那里。\n\nB: 他_______离开这儿，应该还没走远。", "options": ["A. 千万", "B. 到底", "C. 刚刚", "D. 按时", "E. 顺便"], "ans": "C. 刚刚", "key": "C"},
            {"num": 10, "text": "A: 即使下大雨，你们也一定要_______出发。\n\nB: 放心，我都已经安排好了。", "options": ["A. 千万", "B. 到底", "C. 刚刚", "D. 按时", "E. 顺便"], "ans": "D. 按时", "key": "D"}
        ]
    },
    {
        "id": "10-CƠ BẢN - Bộ đề 11",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 11",
        "questions": [
            {"num": 1, "text": "他_______都不迟到，是一个很准时的人。", "options": ["A. 极其", "B. 挺", "C. 从来", "D. 忽然", "E. 竟然"], "ans": "C. 从来", "key": "C"},
            {"num": 2, "text": "刚才还出太阳呢，怎么现在_______下起了雨呢？", "options": ["A. 极其", "B. 挺", "C. 从来", "D. 忽然", "E. 竟然"], "ans": "D. 忽然", "key": "D"},
            {"num": 3, "text": "他长得_______帅的，就是眼睛小了点儿。", "options": ["A. 极其", "B. 挺", "C. 从来", "D. 忽然", "E. 竟然"], "ans": "B. 挺", "key": "B"},
            {"num": 4, "text": "你真勇敢，_______敢从这么高的地方往下跳。", "options": ["A. 极其", "B. 挺", "C. 从来", "D. 忽然", "E. 竟然"], "ans": "E. 竟然", "key": "E"},
            {"num": 5, "text": "知道这件事后，她_______吃惊。", "options": ["A. 极其", "B. 挺", "C. 从来", "D. 忽然", "E. 竟然"], "ans": "A. 极其", "key": "A"},
            {"num": 6, "text": "A: 这次旅行需要多长时间？\n\nB: _______一个多星期吧。", "options": ["A. 挺", "B. 大概", "C. 千万", "D. 竟然", "E. 稍微"], "ans": "B. 大概", "key": "B"},
            {"num": 7, "text": "A: 明天我们八点去机场行吗？\n\nB: 还是_______早一点儿吧，我怕路上堵车。", "options": ["A. 挺", "B. 大概", "C. 千万", "D. 竟然", "E. 稍微"], "ans": "E. 稍微", "key": "E"},
            {"num": 8, "text": "A: 你接受那份工作了吗？他们公司工资好像不太高。\n\nB: 先干一段时间吧，奖金还_______多的。", "options": ["A. 挺", "B. 大概", "C. 千万", "D. 竟然", "E. 稍微"], "ans": "A. 挺", "key": "A"},
            {"num": 9, "text": "A: 你刚学会开车，开车的时候_______要小心。\n\nB: 知道了，我会注意的。", "options": ["A. 挺", "B. 大概", "C. 千万", "D. 竟然", "E. 稍微"], "ans": "C. 千万", "key": "C"},
            {"num": 10, "text": "A: 他才学了一年，_______能说这么流利的汉语。\n\nB: 他的汉语确实很流利。", "options": ["A. 挺", "B. 大概", "C. 千万", "D. 竟然", "E. 稍微"], "ans": "D. 竟然", "key": "D"}
        ]
    },
    {
        "id": "11-CƠ BẢN - Bộ đề 12",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 12",
        "questions": [
            {"num": 1, "text": "这次招聘会_______他安排和负责。", "options": ["A. 由", "B. 往", "C. 通过", "D. 按照", "E. 随着"], "ans": "A. 由", "key": "A"},
            {"num": 2, "text": "从这儿_______左再走 100 米，你就会看见一个饭馆儿。", "options": ["A. 由", "B. 往", "C. 通过", "D. 按照", "E. 随着"], "ans": "B. 往", "key": "B"},
            {"num": 3, "text": "_______调查，人们逐渐认识到海洋对气候有着直接的影响。", "options": ["A. 由", "B. 往", "C. 通过", "D. 按照", "E. 随着"], "ans": "C. 通过", "key": "C"},
            {"num": 4, "text": "_______人口的增长，城市住宅显得越来越紧缺了。", "options": ["A. 由", "B. 往", "C. 通过", "D. 按照", "E. 随着"], "ans": "E. 随着", "key": "E"},
            {"num": 5, "text": "_______现在的情况，想要在规定的时间内完成计划，恐怕有点儿困难。", "options": ["A. 由", "B. 往", "C. 通过", "D. 按照", "E. 随着"], "ans": "D. 按照", "key": "D"},
            {"num": 6, "text": "A: 这几年人民的生活水平得到了改善。\n\nB: 是啊，_______经济的发展，人民的生活水平也提高了不少。", "options": ["A. 按照", "B. 以", "C. 由", "D. 随着", "E. 对于"], "ans": "D. 随着", "key": "D"},
            {"num": 7, "text": "A: _______这个问题，你有什么解决办法？\n\nB: 我看，要解决这个问题得从技术方面入手。", "options": ["A. 按照", "B. 以", "C. 由", "D. 随着", "E. 对于"], "ans": "E. 对于", "key": "E"},
            {"num": 8, "text": "A: 不知道办理去中国的旅游签证都要准备哪些材料？\n\nB: 大使馆的网站上应该有，你可以_______要求来准备。", "options": ["A. 按照", "B. 以", "C. 由", "D. 随着", "E. 对于"], "ans": "A. 按照", "key": "A"},
            {"num": 9, "text": "A: 小马，上次的工作你做得很好，所以想再交给你一个任务，希望你能完成。\n\nB: 请您放心，我一定_______最高的标准要求自己，把它做好。", "options": ["A. 按照", "B. 以", "C. 由", "D. 随着", "E. 对于"], "ans": "B. 以", "key": "B"},
            {"num": 10, "text": "A: 老师，这个“卡”字怎么写啊？\n\nB: 你看，这个字_______两个部分组成，先写“上”，后写“下”。", "options": ["A. 按照", "B. 以", "C. 由", "D. 随着", "E. 对于"], "ans": "C. 由", "key": "C"}
        ]
    },
    {
        "id": "12-cơ bản",
        "source": "ĐỌC 1 (CƠ BẢN)",
        "name": "Bộ đề 13",
        "questions": [
            {"num": 1, "text": "这种花开的时间不长，一般只有两到三个小时，_______只在晚上开花。", "options": ["A. 然而", "B. 既然", "C. 并且", "D. 而", "E. 但是"], "ans": "C. 并且", "key": "C"},
            {"num": 2, "text": "笨人总是把简单的问题说复杂，_______，聪明人却能把复杂的问题解释得简单、清楚。", "options": ["A. 然而", "B. 既然", "C. 并且", "D. 而", "E. 但是"], "ans": "D. 而", "key": "D"},
            {"num": 3, "text": "事情_______已经发生，我们现在要做的是静下来，想办法解决。", "options": ["A. 然而", "B. 既然", "C. 并且", "D. 而", "E. 但是"], "ans": "B. 既然", "key": "B"},
            {"num": 4, "text": "这种苹果大_______不甜。", "options": ["A. 然而", "B. 既然", "C. 并且", "D. 而", "E. 但是"], "ans": "E. 但是", "key": "E"},
            {"num": 5, "text": "这台电脑很不错，_______价钱也不便宜。", "options": ["A. 然而", "B. 既然", "C. 并且", "D. 而", "E. 但是"], "ans": "A. 然而", "key": "A"},
            {"num": 6, "text": "A: 你看过这本书了吗？\n\nB: 尽管大家都说这本书值得一读，_______我都没有时间。", "options": ["A. 然而", "B. 而", "C. 不过", "D. 并且", "E. 既然"], "ans": "A. 然而", "key": "A"},
            {"num": 7, "text": "A: 我报名参加汉语歌曲唱歌比赛了，可是又担心自己到时候唱得不好。\n\nB: _______报了名，就去试试吧。", "options": ["A. 然而", "B. 而", "C. 不过", "D. 并且", "E. 既然"], "ans": "E. 既然", "key": "E"},
            {"num": 8, "text": "A: 你们学校有那么多外国学生来学习啊？\n\nB: 是啊，他们都是为学好汉语_______来到中国的。", "options": ["A. 然而", "B. 而", "C. 不过", "D. 并且", "E. 既然"], "ans": "B. 而", "key": "B"},
            {"num": 9, "text": "A: 小林最近怎么样了？\n\nB: 几年没见，他个子高了，身体壮了，_______性格也开朗多了。", "options": ["A. 然而", "B. 而", "C. 不过", "D. 并且", "E. 既然"], "ans": "D. 并且", "key": "D"},
            {"num": 10, "text": "A: 你是不是喜欢这样的衣服吗？怎么不买？\n\nB: 这件衣服款式不错，_______颜色太深，我不太喜欢。", "options": ["A. 然而", "B. 而", "C. 不过", "D. 并且", "E. 既然"], "ans": "C. 不过", "key": "C"}
        ]
    },
    {
        "id": "13-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 14",
        "questions": [
            {"num": 1, "text": "医生这个职业需要很强的_______知识。", "options": ["A. 安全", "B. 提前", "C. 邀请", "D. 专业", "E. 敲"], "ans": "D. 专业", "key": "D"},
            {"num": 2, "text": "你怎么不_______门就进来了？", "options": ["A. 安全", "B. 提前", "C. 邀请", "D. 专业", "E. 敲"], "ans": "E. 敲", "key": "E"},
            {"num": 3, "text": "在网上，可以_______一个月购买火车票。", "options": ["A. 安全", "B. 提前", "C. 邀请", "D. 专业", "E. 敲"], "ans": "B. 提前", "key": "B"},
            {"num": 4, "text": "下雨天站在大树底下是非常不_______的。", "options": ["A. 安全", "B. 提前", "C. 邀请", "D. 专业", "E. 敲"], "ans": "A. 安全", "key": "A"},
            {"num": 5, "text": "谢谢您的_______，明天的会议我一定参加。", "options": ["A. 安全", "B. 提前", "C. 邀请", "D. 专业", "E. 敲"], "ans": "C. 邀请", "key": "C"},
            {"num": 6, "text": "A: 我想开车去郊区玩儿，但对那儿的_______情况不太了解。\n\nB: 我告诉你怎么走，我上星期刚去过。", "options": ["A. 严重", "B. 可惜", "C. 交通", "D. 剩", "E. 管理"], "ans": "C. 交通", "key": "C"},
            {"num": 7, "text": "A: 我连着几个星期每天只能睡两三个小时。\n\nB: 如果你继续这样，一定会引起_______的健康问题。", "options": ["A. 严重", "B. 可惜", "C. 交通", "D. 剩", "E. 管理"], "ans": "A. 严重", "key": "A"},
            {"num": 8, "text": "A: 这节课还_______十分钟，有问题的同学现在可以提问。\n\nB: 老师，我有一个问题！", "options": ["A. 严重", "B. 可惜", "C. 交通", "D. 剩", "E. 管理"], "ans": "D. 剩", "key": "D"},
            {"num": 9, "text": "A: 现在的海水还太凉，不能下去游泳，你来早了一个月。\n\nB: 早知道我晚点儿再来了，太_______了。", "options": ["A. 严重", "B. 可惜", "C. 交通", "D. 剩", "E. 管理"], "ans": "B. 可惜", "key": "B"},
            {"num": 10, "text": "A: 他那么年轻，能_______好这么大的公司吗？\n\nB: 我也很怀疑。", "options": ["A. 严重", "B. 可惜", "C. 交通", "D. 剩", "E. 管理"], "ans": "E. 管理", "key": "E"}
        ]
    },
    {
        "id": "14-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 15",
        "questions": [
            {"num": 1, "text": "一听到有可能不能毕业的消息，他完全没了_______。", "options": ["A. 主意", "B. 差不多", "C. 积累", "D. 接着", "E. 发现"], "ans": "A. 主意", "key": "A"},
            {"num": 2, "text": "在一次次参加比赛的过程中，我也_______了很多经验。", "options": ["A. 主意", "B. 差不多", "C. 积累", "D. 接着", "E. 发现"], "ans": "C. 积累", "key": "C"},
            {"num": 3, "text": "生活中不是缺少美，而是缺少_______美的眼睛。", "options": ["A. 主意", "B. 差不多", "C. 积累", "D. 接着", "E. 发现"], "ans": "E. 发现", "key": "E"},
            {"num": 4, "text": "她唱完歌后又_______跳了一段舞。", "options": ["A. 主意", "B. 差不多", "C. 积累", "D. 接着", "E. 发现"], "ans": "D. 接着", "key": "D"},
            {"num": 5, "text": "这个手机看起来和那个_______，可价格却便宜不少。", "options": ["A. 主意", "B. 差不多", "C. 积累", "D. 接着", "E. 发现"], "ans": "B. 差不多", "key": "B"},
            {"num": 6, "text": "A: 我的电脑每次用了半个小时后就变得特别热。\n\nB: 那你最好找个懂_______的来检查一下。", "options": ["A. 推迟", "B. 联系", "C. 技术", "D. 顺便", "E. 优秀"], "ans": "C. 技术", "key": "C"},
            {"num": 7, "text": "A: 听说他_______了结婚的时间。\n\nB: 发生什么事儿了？", "options": ["A. 推迟", "B. 联系", "C. 技术", "D. 顺便", "E. 优秀"], "ans": "A. 推迟", "key": "A"},
            {"num": 8, "text": "A: 听说有个亲戚是律师，你能帮我_______一下他吗？\n\nB: 你遇到什么麻烦了？", "options": ["A. 推迟", "B. 联系", "C. 技术", "D. 顺便", "E. 优秀"], "ans": "B. 联系", "key": "B"},
            {"num": 9, "text": "A: 他的成绩不是最_______的，为什么他应聘成功了呢？\n\nB: 因为他以前有工作的经历。", "options": ["A. 推迟", "B. 联系", "C. 技术", "D. 顺便", "E. 优秀"], "ans": "E. 优秀", "key": "E"},
            {"num": 10, "text": "A: 既然已经到北京了，不_______去参观一下长城就太可惜了。\n\nB: 我下午就得坐火车回去，下次再说吧。", "options": ["A. 推迟", "B. 联系", "C. 技术", "D. 顺便", "E. 优秀"], "ans": "D. 顺便", "key": "D"}
        ]
    },
    {
        "id": "15-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 16",
        "questions": [
            {"num": 1, "text": "坚持发展经济是解决一切问题的_______。", "options": ["A. 商量", "B. 保证", "C. 关键", "D. 掉", "E. 改变"], "ans": "C. 关键", "key": "C"},
            {"num": 2, "text": "如果你决定买这辆自行车，价格可以再_______。", "options": ["A. 商量", "B. 保证", "C. 关键", "D. 掉", "E. 改变"], "ans": "A. 商量", "key": "A"},
            {"num": 3, "text": "想_______我爸爸的想法不是一件容易的事情。", "options": ["A. 商量", "B. 保证", "C. 关键", "D. 掉", "E. 改变"], "ans": "E. 改变", "key": "E"},
            {"num": 4, "text": "这个法律是为了_______每一个孩子都能接受教育。", "options": ["A. 商量", "B. 保证", "C. 关键", "D. 掉", "E. 改变"], "ans": "B. 保证", "key": "B"},
            {"num": 5, "text": "这场比赛我们一共输_______了 6 分！", "options": ["A. 商量", "B. 保证", "C. 关键", "D. 掉", "E. 改变"], "ans": "D. 掉", "key": "D"},
            {"num": 6, "text": "A: 老师要求在上课的时候只能说汉语。\n\nB: 这样可以为大家_______一个说汉语的环境，让我们进步得更快。", "options": ["A. 梦", "B. 邀请", "C. 提供", "D. 超过", "E. 安排"], "ans": "C. 提供", "key": "C"},
            {"num": 7, "text": "A: 周末一定到我家来吃饭，别忘了。\n\nB: 谢谢您热情的_______，我一定去。", "options": ["A. 梦", "B. 邀请", "C. 提供", "D. 超过", "E. 安排"], "ans": "B. 邀请", "key": "B"},
            {"num": 8, "text": "A: 我想让小王和她一起表演一个节目。\n\nB: 这么_______不太合适吧？", "options": ["A. 梦", "B. 邀请", "C. 提供", "D. 超过", "E. 安排"], "ans": "E. 安排", "key": "E"},
            {"num": 9, "text": "A: 经理，我想继续请一个星期假。\n\nB: 如果请假_______十天，你这个月的奖金就没了。", "options": ["A. 梦", "B. 邀请", "C. 提供", "D. 超过", "E. 安排"], "ans": "D. 超过", "key": "D"},
            {"num": 10, "text": "A: 你看起来很困，是不是昨天晚上没休息好？\n\nB: 我做了一晚上的_______。", "options": ["A. 梦", "B. 邀请", "C. 提供", "D. 超过", "E. 安排"], "ans": "A. 梦", "key": "A"}
        ]
    },
    {
        "id": "16-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 17",
        "questions": [
            {"num": 1, "text": "这段在中国学习汉语的_______，给我留下了很深的印象。", "options": ["A. 总结", "B. 经历", "C. 羡慕", "D. 相同", "E. 弄"], "ans": "B. 经历", "key": "B"},
            {"num": 2, "text": "这条小狗真可爱，你是从哪儿_______来的？", "options": ["A. 总结", "B. 经历", "C. 羡慕", "D. 相同", "E. 弄"], "ans": "E. 弄", "key": "E"},
            {"num": 3, "text": "在会议开始前，我先来_______一下这个月中出现的问题。", "options": ["A. 总结", "B. 经历", "C. 羡慕", "D. 相同", "E. 弄"], "ans": "A. 总结", "key": "A"},
            {"num": 4, "text": "每个老师教学生的方法都不_______。", "options": ["A. 总结", "B. 经历", "C. 羡慕", "D. 相同", "E. 弄"], "ans": "D. 相同", "key": "D"},
            {"num": 5, "text": "她怎么吃都不胖，真让人_______。", "options": ["A. 总结", "B. 经历", "C. 羡慕", "D. 相同", "E. 弄"], "ans": "C. 羡慕", "key": "C"},
            {"num": 6, "text": "A: 虽然做医生又累又_______，但也给我带来了很多快乐。\n\nB: 是啊，特别是病人对你说“谢谢”的时候。", "options": ["A. 付款", "B. 辛苦", "C. 估计", "D. 负责", "E. 提醒"], "ans": "B. 辛苦", "key": "B"},
            {"num": 7, "text": "A: 我先把东西寄给你，你可以收到以后再_______。\n\nB: 如果能这样就太好了！", "options": ["A. 付款", "B. 辛苦", "C. 估计", "D. 负责", "E. 提醒"], "ans": "A. 付款", "key": "A"},
            {"num": 8, "text": "A: 明天出发的时间是上午 8 点。\n\nB: 好的，谢谢您的_______。", "options": ["A. 付款", "B. 辛苦", "C. 估计", "D. 负责", "E. 提醒"], "ans": "E. 提醒", "key": "E"},
            {"num": 9, "text": "A: 你放心，这件事情我会_______到底。\n\nB: 谢谢您的支持和帮助！", "options": ["A. 付款", "B. 辛苦", "C. 估计", "D. 负责", "E. 提醒"], "ans": "D. 负责", "key": "D"},
            {"num": 10, "text": "A: 你_______我们还有多长时间才能到宾馆？\n\nB: 大概二十分钟吧。", "options": ["A. 付款", "B. 辛苦", "C. 估计", "D. 负责", "E. 提醒"], "ans": "C. 估计", "key": "C"}
        ]
    },
    {
        "id": "17-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 18",
        "questions": [
            {"num": 1, "text": "_______你真的没有感觉到我对你的爱吗？", "options": ["A. 互相", "B. 各", "C. 难道", "D. 千万", "E. 左右"], "ans": "C. 难道", "key": "C"},
            {"num": 2, "text": "我们是同班同学，应该_______帮助！", "options": ["A. 互相", "B. 各", "C. 难道", "D. 千万", "E. 左右"], "ans": "A. 互相", "key": "A"},
            {"num": 3, "text": "他看起来 40 岁_______。", "options": ["A. 互相", "B. 各", "C. 难道", "D. 千万", "E. 左右"], "ans": "E. 左右", "key": "E"},
            {"num": 4, "text": "美食节上你可以尝到全国_______地的美食。", "options": ["A. 互相", "B. 各", "C. 难道", "D. 千万", "E. 左右"], "ans": "B. 各", "key": "B"},
            {"num": 5, "text": "要是你在森林里迷了路，_______别紧张。", "options": ["A. 互相", "B. 各", "C. 难道", "D. 千万", "E. 左右"], "ans": "D. 千万", "key": "D"},
            {"num": 6, "text": "A: 你暑假去北京旅游，感觉怎么样？\n\nB: 非常不错，_______最吸引我的是北京的小吃。", "options": ["A. 重新", "B. 其中", "C. 趟", "D. 偶尔", "E. 恐怕"], "ans": "B. 其中", "key": "B"},
            {"num": 7, "text": "A: 第一天上班感觉怎么样？\n\nB: 这_______是我最难忘的一天了！", "options": ["A. 重新", "B. 其中", "C. 趟", "D. 偶尔", "E. 恐怕"], "ans": "E. 恐怕", "key": "E"},
            {"num": 8, "text": "A: 我今天去找小王，可他不在家。\n\nB: 看来你今天是白跑一_______。", "options": ["A. 重新", "B. 其中", "C. 趟", "D. 偶尔", "E. 恐怕"], "ans": "C. 趟", "key": "C"},
            {"num": 9, "text": "A: 这件衣服不适合我。\n\nB: 没关系，我再帮您_______拿一件，您再试试。", "options": ["A. 重新", "B. 其中", "C. 趟", "D. 偶尔", "E. 恐怕"], "ans": "A. 重新", "key": "A"},
            {"num": 10, "text": "A: 换了工作以后，你现在还经常出差吗？\n\nB: 不，现在一年_______会出一两次，出差的时间也不长。", "options": ["A. 重新", "B. 其中", "C. 趟", "D. 偶尔", "E. 恐怕"], "ans": "D. 偶尔", "key": "D"}
        ]
    },
    {
        "id": "18-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 19",
        "questions": [
            {"num": 1, "text": "过新年的时候_______是孩子们最开心的时候。", "options": ["A. 仍然", "B. 座", "C. 往往", "D. 从来", "E. 随着"], "ans": "C. 往往", "key": "C"},
            {"num": 2, "text": "学习就像是在爬一_______山，只有坚持才能成功。", "options": ["A. 仍然", "B. 座", "C. 往往", "D. 从来", "E. 随着"], "ans": "B. 座", "key": "B"},
            {"num": 3, "text": "他下班后也不休息，_______在考虑工作中的问题。", "options": ["A. 仍然", "B. 座", "C. 往往", "D. 从来", "E. 随着"], "ans": "A. 仍然", "key": "A"},
            {"num": 4, "text": "很多植物叶子的颜色都会_______季节的变化而改变。", "options": ["A. 仍然", "B. 座", "C. 往往", "D. 从来", "E. 随着"], "ans": "E. 随着", "key": "E"},
            {"num": 5, "text": "我_______都没有说过这样的话。", "options": ["A. 仍然", "B. 座", "C. 往往", "D. 从来", "E. 随着"], "ans": "D. 从来", "key": "D"},
            {"num": 6, "text": "A: _______这件事情我们花了很大力气，可还是没成功。\n\nB: 没关系的，失败很正常，相信下次一定会成功！", "options": ["A. 对于", "B. 否则", "C. 按时", "D. 光", "E. 尽管"], "ans": "E. 尽管", "key": "E"},
            {"num": 7, "text": "A: 我想报名参加跑步比赛，你知道有什么条件吗？\n\nB: 我听说参赛者需要在 18 岁以下，_______不能参加比赛。", "options": ["A. 对于", "B. 否则", "C. 按时", "D. 光", "E. 尽管"], "ans": "B. 否则", "key": "B"},
            {"num": 8, "text": "A: _______您刚才说到的这件事情，我不太了解实际的情况。\n\nB: 对不起，打扰您了！", "options": ["A. 对于", "B. 否则", "C. 按时", "D. 光", "E. 尽管"], "ans": "A. 对于", "key": "A"},
            {"num": 9, "text": "A: 还有不到一个星期的时间，这个工作你来得及完成吗？\n\nB: 放心，我一定_______完成。", "options": ["A. 对于", "B. 否则", "C. 按时", "D. 光", "E. 尽管"], "ans": "C. 按时", "key": "C"},
            {"num": 10, "text": "A: 你能和我们说说你学习汉语的经验吗？\n\nB: 多讲、多练，很多词_______会读不行，还得知道怎么用。", "options": ["A. 对于", "B. 否则", "C. 按时", "D. 光", "E. 尽管"], "ans": "D. 光", "key": "D"}
        ]
    },
    {
        "id": "19-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 20",
        "questions": [
            {"num": 1, "text": "你误会我了，这件事情_______不是我说的。", "options": ["A. 确实", "B. 倍", "C. 是否", "D. 百分之", "E. 要是"], "ans": "A. 确实", "key": "A"},
            {"num": 2, "text": "只要有成功的希望，我就要做_______百的努力。", "options": ["A. 确实", "B. 倍", "C. 是否", "D. 百分之", "E. 要是"], "ans": "D. 百分之", "key": "D"},
            {"num": 3, "text": "无论他_______同意，我都会这样做。", "options": ["A. 确实", "B. 倍", "C. 是否", "D. 百分之", "E. 要是"], "ans": "C. 是否", "key": "C"},
            {"num": 4, "text": "鸡肉的价格比过去高了一_______。", "options": ["A. 确实", "B. 倍", "C. 是否", "D. 百分之", "E. 要是"], "ans": "B. 倍", "key": "B"},
            {"num": 5, "text": "_______你联系不上他，可以给我打电话。", "options": ["A. 确实", "B. 倍", "C. 是否", "D. 百分之", "E. 要是"], "ans": "E. 要是", "key": "E"},
            {"num": 6, "text": "A: 尝尝我做的西红柿鸡蛋汤味道怎么样。\n\nB: 挺好喝的，就是_______有点儿咸。", "options": ["A. 任何", "B. 由", "C. 只好", "D. 稍微", "E. 最好"], "ans": "D. 稍微", "key": "D"},
            {"num": 7, "text": "A: 根据我之前的经验，这个地方你_______再检查一下。\n\nB: 好的，我马上就做！", "options": ["A. 任何", "B. 由", "C. 只好", "D. 稍微", "E. 最好"], "ans": "E. 最好", "key": "E"},
            {"num": 8, "text": "A: 这本小说好看吗？\n\nB: 好看，我觉得到现在没有_______一本小说能超过它。", "options": ["A. 任何", "B. 由", "C. 只好", "D. 稍微", "E. 最好"], "ans": "A. 任何", "key": "A"},
            {"num": 9, "text": "A: 这个工作就_______你负责，你看怎么样？\n\nB: 好的，你决定就好。", "options": ["A. 任何", "B. 由", "C. 只好", "D. 稍微", "E. 最好"], "ans": "B. 由", "key": "B"},
            {"num": 10, "text": "A: 你昨晚看球赛了吗？\n\nB: 没有，我家突然停电了，我_______上床睡觉了。", "options": ["A. 任何", "B. 由", "C. 只好", "D. 稍微", "E. 最好"], "ans": "C. 只好", "key": "C"}
        ]
    },
    {
        "id": "20-cường hóa",
        "source": "Cường hóa",
        "name": "Bộ đề 21",
        "questions": [
            {"num": 1, "text": "这件事情我是_______他的要求来做的。", "options": ["A. 由于", "B. 篇", "C. 按照", "D. 既然", "E. 而"], "ans": "C. 按照", "key": "C"},
            {"num": 2, "text": "_______堵车，星期一上午的课我们全都迟到了。", "options": ["A. 由于", "B. 篇", "C. 按照", "D. 既然", "E. 而"], "ans": "A. 由于", "key": "A"},
            {"num": 3, "text": "姐姐喜欢喝茶，_______妹妹却喜欢喝咖啡。", "options": ["A. 由于", "B. 篇", "C. 按照", "D. 既然", "E. 而"], "ans": "E. 而", "key": "E"},
            {"num": 4, "text": "她_______已经认识到错误了，我们就原谅她吧。", "options": ["A. 由于", "B. 篇", "C. 按照", "D. 既然", "E. 而"], "ans": "D. 既然", "key": "D"},
            {"num": 5, "text": "这_______文章我一点儿也没看懂。", "options": ["A. 由于", "B. 篇", "C. 按照", "D. 既然", "E. 而"], "ans": "B. 篇", "key": "B"},
            {"num": 6, "text": "A: 你昨天去看京剧表演了吗？感觉怎么样？\n\nB: 太精彩了，_______连我妈妈这个对表演从来不感兴趣的人，都立刻喜欢上了京剧。", "options": ["A. 刚", "B. 甚至", "C. 到处", "D. 实在", "E. 到底"], "ans": "B. 甚至", "key": "B"},
            {"num": 7, "text": "A: 再坚持一下，我们就快到了！\n\nB: 我_______是太累了，你让我休息五分钟吧。", "options": ["A. 刚", "B. 甚至", "C. 到处", "D. 实在", "E. 到底"], "ans": "D. 实在", "key": "D"},
            {"num": 8, "text": "A: 明天的晚会你_______去不去？\n\nB: 我还没想好。", "options": ["A. 刚", "B. 甚至", "C. 到处", "D. 实在", "E. 到底"], "ans": "E. 到底", "key": "E"},
            {"num": 9, "text": "A: 太热了，帮我把空调打开吧。\n\nB: 没想到_______过五月，天气就已经这么热了。", "options": ["A. 刚", "B. 甚至", "C. 到处", "D. 实在", "E. 到底"], "ans": "A. 刚", "key": "A"},
            {"num": 10, "text": "A: 放暑假的时候去海边玩儿吗？\n\nB: 不去，_______都是人，我不喜欢人多的地方。", "options": ["A. 刚", "B. 甚至", "C. 到处", "D. 实在", "E. 到底"], "ans": "C. 到处", "key": "C"}
        ]
    },
    {
        "id": "21-xanh lá",
        "source": "Xanh lá",
        "name": "Bộ đề 22",
        "questions": [
            {"num": 1, "text": "刚才小丽打电话来叫我去她家一_______，说是有急事找我。", "options": ["A. 趟", "B. 赶", "C. 把", "D. 作用", "E. 过", "F. 坚持"], "ans": "A. 趟", "key": "A"},
            {"num": 2, "text": "情人节，许多男孩儿都_______红玫瑰当作礼物送给心爱的女孩儿。", "options": ["A. 趟", "B. 赶", "C. 把", "D. 作用", "E. 过", "F. 坚持"], "ans": "C. 把", "key": "C"},
            {"num": 3, "text": "你必须在半个小时之内_______到火车站，不然就来不及了。", "options": ["A. 趟", "B. 赶", "C. 把", "D. 作用", "E. 过", "F. 坚持"], "ans": "B. 赶", "key": "B"},
            {"num": 4, "text": "这种药我吃过，对我的病没有什么_______。", "options": ["A. 趟", "B. 赶", "C. 把", "D. 作用", "E. 过", "F. 坚持"], "ans": "D. 作用", "key": "D"},
            {"num": 5, "text": "看_______这部小说的人，都会被女主角的坚强勇敢所感动。", "options": ["A. 趟", "B. 赶", "C. 把", "D. 作用", "E. 过", "F. 坚持"], "ans": "E. 过", "key": "E"},
            {"num": 6, "text": "A: 山本，不好意思，刚才把你的书碰到地上，弄脏了。\n\nB: _______，我擦擦就行了。", "options": ["A. 经常", "B. 害羞", "C. 不要紧", "D. 温度", "E. 语法", "F. 考虑"], "ans": "C. 不要紧", "key": "C"},
            {"num": 7, "text": "A: 老师，我觉得汉语的_______太难了，你说我该怎么办呢？\n\nB: 别着急，只要你多学多练，一定会弄懂的。", "options": ["A. 经常", "B. 害羞", "C. 不要紧", "D. 温度", "E. 语法", "F. 考虑"], "ans": "E. 语法", "key": "E"},
            {"num": 8, "text": "A: 你已经是个大小伙子了，怎么还这么_______呢？\n\nB: 其实我只是不知道该说什么好。", "options": ["A. 经常", "B. 害羞", "C. 不要紧", "D. 温度", "E. 语法", "F. 考虑"], "ans": "B. 害羞", "key": "B"},
            {"num": 9, "text": "A: 现在这个公司的待遇是不错，可是太累了！_______加班。\n\nB: 不行就换个工作吧，不管怎么说身体是最重要的啊！", "options": ["A. 经常", "B. 害羞", "C. 不要紧", "D. 温度", "E. 语法", "F. 考虑"], "ans": "A. 经常", "key": "A"},
            {"num": 10, "text": "A: 我还是希望你能再_______一下，万一赔钱呢？\n\nB: 你放心吧，不会的。", "options": ["A. 经常", "B. 害羞", "C. 不要紧", "D. 温度", "E. 语法", "F. 考虑"], "ans": "F. 考虑", "key": "F"}
        ]
    },
    {
        "id": "22-xanh lá",
        "source": "Xanh lá",
        "name": "Bộ đề 23",
        "questions": [
            {"num": 1, "text": "她_______外向性格，爱唱爱跳，喜欢热闹，不喜欢安静。", "options": ["A. 来自", "B. 顺序", "C. 坚持", "D. 对于", "E. 不断", "F. 属于"], "ans": "F. 属于", "key": "F"},
            {"num": 2, "text": "_______吸烟的危害，虽然大家比较了解，但真正能把烟戒掉的人却不多。", "options": ["A. 来自", "B. 顺序", "C. 坚持", "D. 对于", "E. 不断", "F. 属于"], "ans": "D. 对于", "key": "D"},
            {"num": 3, "text": "经过大家_______的努力，我们公司终于完成了这个项目。", "options": ["A. 来自", "B. 顺序", "C. 坚持", "D. 对于", "E. 不断", "F. 属于"], "ans": "E. 不断", "key": "E"},
            {"num": 4, "text": "导游让大家一点在宾馆门口排队，然后按先后_______上车。", "options": ["A. 来自", "B. 顺序", "C. 坚持", "D. 对于", "E. 不断", "F. 属于"], "ans": "B. 顺序", "key": "B"},
            {"num": 5, "text": "这次运动会，有_______一百多个国家的运动员参加。", "options": ["A. 来自", "B. 顺序", "C. 坚持", "D. 对于", "E. 不断", "F. 属于"], "ans": "A. 来自", "key": "A"},
            {"num": 6, "text": "A: 前几天看的眼镜，你买了吗？\n\nB: _______打折，否则我不会考虑的。", "options": ["A. 任何", "B. 占线", "C. 安排", "D. 忍不住", "E. 除非", "F. 温度"], "ans": "E. 除非", "key": "E"},
            {"num": 7, "text": "A: 昨天你怎么醉成那样儿？\n\nB: 我们同学聚会，大家玩得很高兴，我_______多喝了几杯。", "options": ["A. 任何", "B. 占线", "C. 安排", "D. 忍不住", "E. 除非", "F. 温度"], "ans": "D. 忍不住", "key": "D"},
            {"num": 8, "text": "A: 你给小张打电话了吗？\n\nB: 打了，可是他的电话一直_______。", "options": ["A. 任何", "B. 占线", "C. 安排", "D. 忍不住", "E. 除非", "F. 温度"], "ans": "B. 占线", "key": "B"},
            {"num": 9, "text": "A: 下午你要是没什么_______就跟我去健身房吧，我有免费的票。\n\nB: 真不巧，我得去机场接朋友。", "options": ["A. 任何", "B. 占线", "C. 安排", "D. 忍不住", "E. 除非", "F. 温度"], "ans": "C. 安排", "key": "C"},
            {"num": 10, "text": "A: 教练，这次比赛不在我们本地举行，想赢不太容易呀！\n\nB: 我觉得只要我们队员团结起来，_______困难都能克服。", "options": ["A. 任何", "B. 占线", "C. 安排", "D. 忍不住", "E. 除非", "F. 温度"], "ans": "A. 任何", "key": "A"}
        ]
    },
    {
        "id": "23-xanh lá",
        "source": "Xanh lá",
        "name": "Bộ đề 24",
        "questions": [
            {"num": 1, "text": "其实我还是挺_______的，不该花的钱我从来不乱花。", "options": ["A. 尽管", "B. 所", "C. 节约", "D. 离", "E. 坚持", "F. 家具"], "ans": "C. 节约", "key": "C"},
            {"num": 2, "text": "这套_______是我很久以前就想买的，今天终于可以买回家了。", "options": ["A. 尽管", "B. 所", "C. 节约", "D. 离", "E. 坚持", "F. 家具"], "ans": "F. 家具", "key": "F"},
            {"num": 3, "text": "_______考试结束还有十分钟，请同学们抓紧时间答题。", "options": ["A. 尽管", "B. 所", "C. 节约", "D. 离", "E. 坚持", "F. 家具"], "ans": "D. 离", "key": "D"},
            {"num": 4, "text": "政府计划在两年内再建十_______希望小学。", "options": ["A. 尽管", "B. 所", "C. 节约", "D. 离", "E. 坚持", "F. 家具"], "ans": "B. 所", "key": "B"},
            {"num": 5, "text": "_______这件事我们没有告诉她，她还是知道了。", "options": ["A. 尽管", "B. 所", "C. 节约", "D. 离", "E. 坚持", "F. 家具"], "ans": "A. 尽管", "key": "A"},
            {"num": 6, "text": "A: 妈，我去同学家玩儿一会儿。\n\nB: 好，下楼的时候顺便把垃圾_______下去！", "options": ["A. 恐怕", "B. 带", "C. 恢复", "D. 精彩", "E. 温度", "F. 往"], "ans": "B. 带", "key": "B"},
            {"num": 7, "text": "A: 于飞的胳膊现在怎么样了？\n\nB: 他这次摔得可不轻，估计得过一段时间才能_______。", "options": ["A. 恐怕", "B. 带", "C. 恢复", "D. 精彩", "E. 温度", "F. 往"], "ans": "C. 恢复", "key": "C"},
            {"num": 8, "text": "A: 这么晚了，小王_______不能来了。\n\nB: 那可怎么办呀？我的资料还在他那儿呢！", "options": ["A. 恐怕", "B. 带", "C. 恢复", "D. 精彩", "E. 温度", "F. 往"], "ans": "A. 恐怕", "key": "A"},
            {"num": 9, "text": "A: 先生，您能不能再_______前动一动，我这儿太挤了。\n\nB: 不好意思，这车人太多，前边也没地方了。", "options": ["A. 恐怕", "B. 带", "C. 恢复", "D. 精彩", "E. 温度", "F. 往"], "ans": "F. 往", "key": "F"},
            {"num": 10, "text": "A: 昨天的演出太_______了，你没看真可惜。\n\nB: 没事儿，我还能弄到票。", "options": ["A. 恐怕", "B. 带", "C. 恢复", "D. 精彩", "E. 温度", "F. 往"], "ans": "D. 精彩", "key": "D"}
        ]
    },
    {
        "id": "24-xanh lá",
        "source": "Xanh lá",
        "name": "Bộ đề 25",
        "questions": [
            {"num": 1, "text": "这个活动很_______，经理对我们非常满意。", "options": ["A. 提", "B. 坚持", "C. 而且", "D. 再", "E. 成功", "F. 跟"], "ans": "E. 成功", "key": "E"},
            {"num": 2, "text": "她的化妆方法是_______着电视学的，虽然不太专业，但是还是挺漂亮的。", "options": ["A. 提", "B. 坚持", "C. 而且", "D. 再", "E. 成功", "F. 跟"], "ans": "F. 跟", "key": "F"},
            {"num": 3, "text": "王姐她们家想等儿子大学毕业以后_______搬到南方去。", "options": ["A. 提", "B. 坚持", "C. 而且", "D. 再", "E. 成功", "F. 跟"], "ans": "D. 再", "key": "D"},
            {"num": 4, "text": "今天是我第一次讲课，你一定要给我_______点儿建议。", "options": ["A. 提", "B. 坚持", "C. 而且", "D. 再", "E. 成功", "F. 跟"], "ans": "A. 提", "key": "A"},
            {"num": 5, "text": "小明喜欢去网吧，这不仅浪费了很多钱，_______也影响了学习成绩。", "options": ["A. 提", "B. 坚持", "C. 而且", "D. 再", "E. 成功", "F. 跟"], "ans": "C. 而且", "key": "C"},
            {"num": 6, "text": "A: _______女人来说，事业重要还是家庭重要呢？\n\nB: 关于这个问题，不同的人会有不同的看法。", "options": ["A. 绝对", "B. 目标", "C. 单调", "D. 幅", "E. 温度", "F. 对于"], "ans": "F. 对于", "key": "F"},
            {"num": 7, "text": "A: 这种手机的质量怎么样啊？我以前没见过这个牌子。\n\nB: 放心吧，_______没问题。", "options": ["A. 绝对", "B. 目标", "C. 单调", "D. 幅", "E. 温度", "F. 对于"], "ans": "A. 绝对", "key": "A"},
            {"num": 8, "text": "A: 客厅里除了几件旧家具，什么也没有，不好看。\n\nB: 买两_______画儿挂上不就行了。", "options": ["A. 绝对", "B. 目标", "C. 单调", "D. 幅", "E. 温度", "F. 对于"], "ans": "D. 幅", "key": "D"},
            {"num": 9, "text": "A: 我觉得自己现在的生活太_______了，上班、回家、上网，每天都一样。\n\nB: 要不你也来参加我们的俱乐部吧。", "options": ["A. 绝对", "B. 目标", "C. 单调", "D. 幅", "E. 温度", "F. 对于"], "ans": "C. 单调", "key": "C"},
            {"num": 10, "text": "A: 马上就要毕业了，打算找个什么样的工作啊？有_______了吗？\n\nB: 别提了，我正为这事发愁呢！", "options": ["A. 绝对", "B. 目标", "C. 单调", "D. 幅", "E. 温度", "F. 对于"], "ans": "B. 目标", "key": "B"}
        ]
    },
    {
        "id": "25-xanh lá",
        "source": "Xanh lá",
        "name": "Bộ đề 26",
        "questions": [
            {"num": 1, "text": "她今天表演得很好，跳舞时非常有_______。", "options": ["A. 准时", "B. 坚持", "C. 自信", "D. 害羞", "E. 符合", "F. 道歉"], "ans": "C. 自信", "key": "C"},
            {"num": 2, "text": "因为小李昨天的作业不_______老师的要求，所以今天必须重新写。", "options": ["A. 准时", "B. 坚持", "C. 自信", "D. 害羞", "E. 符合", "F. 道歉"], "ans": "E. 符合", "key": "E"},
            {"num": 3, "text": "他从小就很_______，一和女生说话脸就红。", "options": ["A. 准时", "B. 坚持", "C. 自信", "D. 害羞", "E. 符合", "F. 道歉"], "ans": "D. 害羞", "key": "D"},
            {"num": 4, "text": "玛丽上班一直很_______，从来不会迟到。", "options": ["A. 准时", "B. 坚持", "C. 自信", "D. 害羞", "E. 符合", "F. 道歉"], "ans": "A. 准时", "key": "A"},
            {"num": 5, "text": "昨天王志对他女朋友发脾气了，现在去向她_______。", "options": ["A. 准时", "B. 坚持", "C. 自信", "D. 害羞", "E. 符合", "F. 道歉"], "ans": "F. 道歉", "key": "F"},
            {"num": 6, "text": "A: 你能告诉我这两台电脑有什么_______吗？\n\nB: 很抱歉，我不太懂电脑。", "options": ["A. 由于", "B. 尊重", "C. 严重", "D. 小吃", "E. 区别", "F. 温度"], "ans": "E. 区别", "key": "E"},
            {"num": 7, "text": "A: 听说小王病了，现在怎么样了？\n\nB: 不用担心，他病得不_______。", "options": ["A. 由于", "B. 尊重", "C. 严重", "D. 小吃", "E. 区别", "F. 温度"], "ans": "C. 严重", "key": "C"},
            {"num": 8, "text": "A: 你的小学老师是位非常善良的人。\n\nB: 是啊，我一直都很_______她。", "options": ["A. 由于", "B. 尊重", "C. 严重", "D. 小吃", "E. 区别", "F. 温度"], "ans": "B. 尊重", "key": "B"},
            {"num": 9, "text": "A: _______今天天气不好，校长坐的飞机不能按时起飞。\n\nB: 好的，我告诉王老师一声。", "options": ["A. 由于", "B. 尊重", "C. 严重", "D. 小吃", "E. 区别", "F. 温度"], "ans": "A. 由于", "key": "A"},
            {"num": 10, "text": "A: 你为什么这么喜欢四川？\n\nB: 因为那里有特别多我喜欢吃的_______！", "options": ["A. 由于", "B. 尊重", "C. 严重", "D. 小吃", "E. 区别", "F. 温度"], "ans": "D. 小吃", "key": "D"}
        ]
    },
    {
        "id": "26-xanh lá",
        "source": "Xanh lá",
        "name": "Bộ đề 27",
        "questions": [
            {"num": 1, "text": "对不起，_______一下，请问，中国银行怎么走？", "options": ["A. 印象", "B. 得到", "C. 质量", "D. 打扰", "E. 占线", "F. 坚持"], "ans": "D. 打扰", "key": "D"},
            {"num": 2, "text": "她今天的精彩表演给大家留下了很好的_______。", "options": ["A. 印象", "B. 得到", "C. 质量", "D. 打扰", "E. 占线", "F. 坚持"], "ans": "A. 印象", "key": "A"},
            {"num": 3, "text": "这件衣服的颜色、样式都很合适，就是_______不太好。", "options": ["A. 印象", "B. 得到", "C. 质量", "D. 打扰", "E. 占线", "F. 坚持"], "ans": "C. 质量", "key": "C"},
            {"num": 4, "text": "那家公司生产的巧克力_______很多人的好评。", "options": ["A. 印象", "B. 得到", "C. 质量", "D. 打扰", "E. 占线", "F. 坚持"], "ans": "B. 得到", "key": "B"},
            {"num": 5, "text": "我打了一个上午电话了，总是_______。", "options": ["A. 印象", "B. 得到", "C. 质量", "D. 打扰", "E. 占线", "F. 坚持"], "ans": "E. 占线", "key": "E"},
            {"num": 6, "text": "A: 你常常来这儿喝茶吗？\n\nB: 不常来，_______会跟同事们来一次。", "options": ["A. 温度", "B. 偶尔", "C. 可惜", "D. 能力", "E. 解释", "F. 只要"], "ans": "B. 偶尔", "key": "B"},
            {"num": 7, "text": "A: 他差两分就通过考试了，真_______！\n\nB: 没关系，下次继续努力。", "options": ["A. 温度", "B. 偶尔", "C. 可惜", "D. 能力", "E. 解释", "F. 只要"], "ans": "C. 可惜", "key": "C"},
            {"num": 8, "text": "A: 老师，您能给我_______一下这个汉字的意思吗？\n\nB: 哪个？让我看看。", "options": ["A. 温度", "B. 偶尔", "C. 可惜", "D. 能力", "E. 解释", "F. 只要"], "ans": "E. 解释", "key": "E"},
            {"num": 9, "text": "A: 明天就要去面试了，我有点儿担心。\n\nB: 别担心，要相信自己的_______。", "options": ["A. 温度", "B. 偶尔", "C. 可惜", "D. 能力", "E. 解释", "F. 只要"], "ans": "D. 能力", "key": "D"},
            {"num": 10, "text": "A: 老师，这次考试难吗？\n\nB: 不难，_______你认真复习，就一定能考好。", "options": ["A. 温度", "B. 偶尔", "C. 可惜", "D. 能力", "E. 解释", "F. 只要"], "ans": "F. 只要", "key": "F"}
        ]
    }
]

# --- RENDER TABS ---
tab_names = [t["id"] for t in TEST_DATA]
tabs = st.tabs(tab_names)

for index, tab in enumerate(tabs):
    test_info = TEST_DATA[index]
    with tab:
        
        st.markdown("Chọn đáp án đúng nhất cho từng câu hỏi dưới đây:")
        
        # Form for answering questions
        with st.form(key=f"form_{test_info['id']}"):
            user_answers = {}
            for q in test_info["questions"]:
                st.markdown(f"**Câu {q['num']}:** {q['text'].replace('\\n', '<br>')}", unsafe_allow_html=True)
                selected = st.radio(
                    f"Chọn đáp án cho câu {q['num']}:",
                    options=q["options"],
                    key=f"radio_{test_info['id']}_{q['num']}",
                    index=None
                )
                user_answers[q["num"]] = selected
                st.markdown("---")
            
            submit_btn = st.form_submit_button("🚀 Nộp bài & Xem điểm", type="primary")
        
        if submit_btn:
            if not student_name:
                st.error("❌ Bạn chưa nhập **Họ và tên học viên** ở sidebar (thanh bên trái). Vui lòng nhập họ tên để ghi nhận điểm!")
            else:
                score = 0
                total = len(test_info["questions"])
                results_detail = []
                
                for q in test_info["questions"]:
                    user_ans = user_answers.get(q["num"])
                    is_correct = (user_ans == q["ans"])
                    if is_correct:
                        score += 1
                    results_detail.append({
                        "num": q["num"],
                        "text": q["text"],
                        "user_ans": user_ans,
                        "correct_ans": q["ans"],
                        "is_correct": is_correct
                    })
                
                score_str = f"{score}/{total}"
                
                # Dynamic Feedback message based on score
                st.markdown(f"### 🎉 Chúc mừng "**{student_name}**" hoàn thành **{test_info['id']}**. Điểm số của bạn là **{score}/{total}**")
                
                if score >= 8:
                    st.markdown('<div class="result-banner-8">🌟 <b>Ai mà giỏi quá ta, tiếp tục phát huy nha.</b></div>', unsafe_allow_html=True)
                elif score >= 5:
                    st.markdown('<div class="result-banner-5">👍 <b>Ok cũng được đó, tiếp tục cố gắng nha!</b></div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="result-banner-0">💪 <b>Hơi tiếc một chút, bạn nhớ kỹ lại từ vựng nhé!</b></div>', unsafe_allow_html=True)
                
                # Send result to Google Sheet
                sent = post_to_gsheet(student_name, test_info["id"], score_str)
                if sent:
                    st.success("✅ Đã tự động gửi kết quả điểm về Google Sheet cho cô Bảo Ngọc!")
                else:
                    st.warning("⚠️ Không thể kết nối với Google Sheet, nhưng điểm số của bạn đã được hiển thị bên trên.")
                
                # Review mistakes
                st.markdown("### 🔍 Chi tiết kết quả & Xem lại câu sai:")
                for item in results_detail:
                    if item["is_correct"]:
                        st.markdown(f"**Câu {item['num']}:** ✅ Đúng! ({item['correct_ans']})")
                    else:
                        st.markdown(f"**Câu {item['num']}:** ❌ Sai.")
                        st.markdown(f"- Bạn chọn: `{item['user_ans'] if item['user_ans'] else 'Chưa chọn'}`")
                        st.markdown(f"- Đáp án đúng: **{item['correct_ans']}**")
# --- FOOTER ---
st.markdown('<div class="teacher-footer">黄宝玉老师</div>', unsafe_allow_html=True)
