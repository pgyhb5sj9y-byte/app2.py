import streamlit as st
import pandas as pd

st.set_page_config(page_title="TCST Reefer Risk Control", page_icon="🚢", layout="wide")
st.title("🚢 HỆ THỐNG SMART GATE - ĐỐI CHIẾU CONTAINER LẠNH")

# 1. Khởi tạo Database tạm thời (Session State) để tự lưu dữ liệu Master Data khi nhập
if 'master_data' not in st.session_state:
    st.session_state.master_data = {
        "TCNU1234567": {"Booking": "BK-2026-01", "Temp": -18.0, "Vent": 0, "Line": "ONE"},
        "MSKU9876543": {"Booking": "BK-2026-02", "Temp": -5.0, "Vent": 15, "Line": "Maersk"}
    }

col_db, col_check = st.columns([1, 1.2])

with col_db:
    st.subheader("📥 1. NẠP MASTER DATA TỪ HÃNG TÀU")
    st.write("Bộ phận Thương vụ/Kế hoạch tự động nạp thông số chuẩn vào hệ thống trước khi xe đến.")
    
    new_cont = st.text_input("Số Container (VD: CMAU1122334):").upper()
    new_line = st.text_input("Hãng tàu:")
    new_temp = st.number_input("Nhiệt độ chuẩn (°C):", value=-18.0, step=0.5)
    new_vent = st.number_input("Thông gió chuẩn (CBM/h):", value=0, step=5)
    
    if st.button("➕ Thêm vào Cơ sở dữ liệu Cảng"):
        if new_cont:
            st.session_state.master_data[new_cont] = {
                "Booking": "Auto-Gen", 
                "Temp": new_temp, 
                "Vent": new_vent, 
                "Line": new_line
            }
            st.success(f"Đã lưu Master Data cho container {new_cont}!")
        else:
            st.warning("Vui lòng nhập số Container.")
            
    st.markdown("---")
    st.write("📚 **Danh sách Master Data hiện tại:**")
    st.dataframe(pd.DataFrame.from_dict(st.session_state.master_data, orient='index'))

with col_check:
    st.subheader("🔍 2. ĐỐI CHIẾU TẠI CỔNG (GATE IN)")
    st.write("Nhân viên Gate đối chiếu khai báo của tài xế với hệ thống.")
    
    check_cont = st.text_input("Ghi số Container tài xế chở đến:").upper()
    driver_temp = st.number_input("Nhiệt độ tài xế khai báo (°C):", value=0.0, step=0.5)
    driver_vent = st.number_input("Thông gió tài xế khai báo (CBM/h):", value=0, step=5)
    
    if st.button("🚀 KIỂM TRA & DUYỆT LỆNH", type="primary"):
        if not check_cont:
            st.error("Vui lòng nhập số container để kiểm tra.")
        elif check_cont not in st.session_state.master_data:
            st.error("🚨 KHÔNG TÌM THẤY! Container này chưa được Hãng tàu gửi dữ liệu Master Data.")
        else:
            target = st.session_state.master_data[check_cont]
            st.write(f"**Thông số chuẩn của Hãng {target['Line']}:** Nhiệt độ `{target['Temp']}°C` | Thông gió `{target['Vent']} CBM/h`")
            
            if driver_temp == target['Temp'] and driver_vent == target['Vent']:
                st.success("✅ KHỚP DỮ LIỆU. Cho phép cấp phiếu giao nhận hạ bãi.")
            else:
                st.error("❌ SAI LỆCH KHAI BÁO! Cổng tự động khóa lệnh.")
                if driver_temp != target['Temp']:
                    st.warning(f"Lệch nhiệt độ: Tài xế báo {driver_temp}°C (Chuẩn phải là {target['Temp']}°C)")
                if driver_vent != target['Vent']:
                    st.warning(f"Lệch thông gió: Tài xế báo {driver_vent} (Chuẩn phải là {target['Vent']})")