import cv2
import streamlit as st
import time
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Veri saklamak için global bir DataFrame
if "video_data" not in st.session_state:
    st.session_state.video_data = []

def main():
    st.title("Canlı Video ile Süre Analizi ve Standart Sapma Hesaplama")

    # Video Akışı
    run_video = st.checkbox("Canlı Videoyu Başlat")
    stop_video = st.checkbox("Videoyu Durdur")
    calculate_time = st.button("Süreyi Başlat ve Durdur")

    cap = None
    start_time = None
    end_time = None

    if run_video:
        cap = cv2.VideoCapture(0)
        st.warning("Canlı video başlatıldı. Süreyi başlat/durdur için butonu kullanın.")

        while run_video and not stop_video:
            ret, frame = cap.read()
            if not ret:
                st.error("Kamera akışı açılamıyor.")
                break

            # OpenCV ile çerçeveleme
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            st.image(frame, channels="RGB", caption="Canlı Video Akışı", use_column_width=True)

            # Süre Hesaplama
            if calculate_time:
                if start_time is None:
                    start_time = datetime.now()
                    st.success(f"Başlangıç zamanı: {start_time.strftime('%H:%M:%S')}")
                else:
                    end_time = datetime.now()
                    duration = (end_time - start_time).seconds
                    st.success(f"Süre hesaplandı: {duration} saniye")

                    # Veriyi kaydet
                    st.session_state.video_data.append({
                        "Çalışan": "Anonim",
                        "Başlangıç": start_time,
                        "Bitiş": end_time,
                        "Süre (saniye)": duration
                    })
                    start_time = None  # Sıfırla
                    end_time = None  # Sıfırla
                    break

    if stop_video and cap is not None:
        cap.release()
        st.warning("Video akışı durduruldu.")

    # Analiz Bölümü
    st.header("Hesaplanan Sürelerin Analizi")

    if st.session_state.video_data:
        df = pd.DataFrame(st.session_state.video_data)

        # Verileri Göster
        st.subheader("Toplanan Veriler")
        st.dataframe(df)

        # Ortalama ve Standart Sapma Hesaplama
        st.subheader("İstatistiksel Analiz")
        mean_duration = df["Süre (saniye)"].mean()
        std_dev_duration = df["Süre (saniye)"].std()
        st.write(f"Ortalama Süre: {mean_duration:.2f} saniye")
        st.write(f"Standart Sapma: {std_dev_duration:.2f} saniye")

        # Standart Sapma Grafiği
        st.subheader("Standart Sapma Grafiği")
        fig, ax = plt.subplots()
        df["Süre (saniye)"].plot(kind="bar", ax=ax, color="skyblue")
        ax.set_title("Çalışan Süreleri")
        ax.set_xlabel("Kayıtlar")
        ax.set_ylabel("Süre (saniye)")
        st.pyplot(fig)

if __name__ == "__main__":
    main()
