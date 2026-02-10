import streamlit as st
import pandas as pd

# =========================
# LOAD DATASET
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("Dataset_Protein.xlsx")

    # Hapus kolom No jika ada
    if "No" in df.columns:
        df = df.drop(columns=["No"])

    return df


# =========================
# HITUNG EFISIENSI
# =========================
def hitung_efisiensi(data):
    for item in data:
        item["Harga/protein"] = item["Harga"] / item["Protein"]
    return data


# =========================
# SORTING MANUAL (ASC)
# =========================
def sort_manual(data):
    n = len(data)
    for i in range(n):
        for j in range(i + 1, n):
            if data[j]["Harga/protein"] < data[i]["Harga/protein"]:
                data[i], data[j] = data[j], data[i]
    return data


# =========================
# GREEDY
# =========================
def greedy_protein(data, kebutuhan):
    solusi = []
    total_protein = 0
    total_harga = 0

    for item in data:
        if total_protein < kebutuhan:
            solusi.append(item)
            total_protein += item["Protein"]
            total_harga += item["Harga"]
        else:
            break

    return solusi, total_protein, total_harga


# =========================
# MAIN APP
# =========================
def main():
    st.set_page_config(page_title="Algoritma Greedy", layout="wide")

    # =========================
    # SIDEBAR
    # =========================
    st.sidebar.markdown(
        """
        <div style="font-size:28px; font-weight:700;">
            🧠 Algoritma Greedy
        </div>
        <div style="font-size:14px; opacity:0.6; margin-top:6px;">
            kombinasi sumber pangan protein tinggi<br>
            dengan budget minimum
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.divider()

    if "menu" not in st.session_state:
        st.session_state.menu = "Operasi Greedy"

    if st.sidebar.button("🍽️ Operasi Greedy", use_container_width=True):
        st.session_state.menu = "Operasi Greedy"

    if st.sidebar.button("📊 Dataset", use_container_width=True):
        st.session_state.menu = "Dataset"

    # =========================
    # LOAD DATA
    # =========================
    df = load_data()

    # =========================
    # MENU OPERASI GREEDY
    # =========================
    if st.session_state.menu == "Operasi Greedy":

        st.markdown("## 🍽️ Operasi Greedy")

        # ===== INPUT BOX (MODEL CARI TEMPAT) =====
        with st.container():
            st.markdown("#### 🗂️ Pilih kategori & atur kebutuhan protein")

            kategori_opsi = ["Semua"] + sorted(df["Kategori"].unique().tolist())
            kategori_pilihan = st.selectbox(
                "Kategori sumber protein",
                kategori_opsi
            )

            kebutuhan_input = st.text_input(
                "Kebutuhan protein harian (gram)",
                value="70",
                placeholder="Contoh: 70",
                help="Tekan Enter untuk menerapkan nilai"
            )

        try:
            kebutuhan = int(kebutuhan_input)
        except ValueError:
            st.warning("Masukkan angka kebutuhan protein yang valid.")
            return

        # ===== FILTER DATASET =====
        df_filter = df.copy()
        if kategori_pilihan != "Semua":
            df_filter = df_filter[df_filter["Kategori"] == kategori_pilihan]

        data = df_filter.to_dict(orient="records")

        # ===== TAHAP 1 =====
        st.markdown("### 📐 Tahap 1: Perhitungan Fungsi Efisiensi Harga")
        st.latex(r"\text{Harga/protein} = \frac{\text{Harga (Rp)}}{\text{Protein (gram)}}")

        data = hitung_efisiensi(data)
        st.dataframe(pd.DataFrame(data), use_container_width=True)

        # ===== TAHAP 2 =====
        st.markdown("### 🔃 Tahap 2: Sorting Berdasarkan Harga/Protein (Ascending)")
        data_sorted = sort_manual(data.copy())
        st.dataframe(pd.DataFrame(data_sorted), use_container_width=True)

        # ===== TAHAP 3 =====
        st.markdown("### 🧩 Tahap 3: Himpunan Solusi")
        solusi, total_protein, total_harga = greedy_protein(data_sorted, kebutuhan)

        if solusi:
            df_solusi = pd.DataFrame(solusi)
            st.dataframe(df_solusi, use_container_width=True)

            nama_solusi = [item["Nama_pangan"] for item in solusi]
            himpunan_solusi = "{ " + ", ".join(nama_solusi) + " }"

            st.markdown("### 📌 Himpunan Solusi (Notasi Himpunan)")
            st.code(f"Himpunan Solusi = {himpunan_solusi}")
        else:
            st.warning("Tidak ada kombinasi yang memenuhi kebutuhan protein.")

        # ===== RINGKASAN =====
        st.markdown("### 📊 Ringkasan Hasil")
        st.write(f"**Kategori Aktif** : {kategori_pilihan}")
        st.write(f"**Kebutuhan Protein** : {kebutuhan} gram")
        st.write(f"**Total Protein Didapat** : {total_protein:.2f} gram")
        st.write(f"**Total Harga** : Rp {total_harga:,.0f}")

    # =========================
    # MENU DATASET
    # =========================
    elif st.session_state.menu == "Dataset":

        st.markdown("## 📊 Dataset Utama")

        st.markdown("### ℹ️ Rincian Attribute Dataset")
        st.markdown("""
        - **Protein** : gram protein per 100 gram bahan pangan  
        - **Harga** : harga (Rp) per 100 gram bahan pangan  
        - **Kategori** : jenis sumber protein
        """) 

        st.markdown("### 📋 Dataset")
        st.dataframe(df, use_container_width=True)
        
        # ===== DOWNLOAD DATASET =====
        import io

        buffer = io.BytesIO()
        df.to_excel(buffer, index=False)
        buffer.seek(0)

        st.download_button(
            label="⬇️ Unduh Dataset (Excel)",
            data=buffer,
            file_name="Dataset_Protein.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

if __name__ == "__main__":
    main()