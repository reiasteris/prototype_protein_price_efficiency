import streamlit as st
import pandas as pd

# =========================
# LOAD DATASET
# =========================
@st.cache_data
def load_data():
    df = pd.read_excel("Dataset_Protein.xlsx")
    return df


# =========================
# HITUNG EFISIENSI (MANUAL)
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
# GREEDY ALGORITHM
# =========================
def greedy_protein(data, kebutuhan_protein):
    solusi = []
    total_protein = 0
    total_harga = 0

    for item in data:
        if total_protein < kebutuhan_protein:
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
    st.set_page_config(
        page_title="Optimasi Protein Greedy",
        layout="wide"
    )

    st.title("🍽️ Optimasi Kombinasi Lauk Protein (Greedy Algorithm)")

    # SIDEBAR FIXED
    st.sidebar.title("📌 Panel Kontrol")
    menu = st.sidebar.radio(
        "Pilih Menu",
        ["Greedy Optimization", "View Dataset"],
        index=0  # default Greedy
    )

    df = load_data()

    # =========================
    # MENU: GREEDY (DEFAULT)
    # =========================
    if menu == "Greedy Optimization":

        st.subheader("⚙️ Operasi Algoritma Greedy")

        kebutuhan = st.number_input(
            "Kebutuhan Protein Harian (gram)",
            min_value=10,
            max_value=200,
            value=70
        )

        # Konversi DataFrame → list of dict
        data = df.to_dict(orient="records")

        # ===== TAHAP 1 =====
        st.markdown("### 🔹 Tahap 1: Perhitungan Fungsi Efisiensi")
        data = hitung_efisiensi(data)
        df_efisiensi = pd.DataFrame(data)
        st.dataframe(df_efisiensi)

        # ===== TAHAP 2 =====
        st.markdown("### 🔹 Tahap 2: Sorting Berdasarkan Harga/Protein (Ascending)")
        data_sorted = sort_manual(data.copy())
        df_sorted = pd.DataFrame(data_sorted)
        st.dataframe(df_sorted)

        # ===== TAHAP 3 =====
        st.markdown("### 🔹 Tahap 3: Hasil Operasi Greedy")
        solusi, total_protein, total_harga = greedy_protein(
            data_sorted, kebutuhan
        )

        if solusi:
            st.markdown("#### 📋 Himpunan Solusi")
            st.dataframe(pd.DataFrame(solusi))
        else:
            st.warning("Tidak ada kombinasi yang memenuhi kebutuhan protein.")

        st.markdown("#### 📊 Ringkasan Hasil")
        st.write(f"**Kebutuhan Protein Harian** : {kebutuhan} gram")
        st.write(f"**Total Protein Didapat**   : {total_protein:.2f} gram")
        st.write(f"**Total Harga**             : Rp {total_harga:,.0f}")

    # =========================
    # MENU: VIEW DATASET
    # =========================
    elif menu == "View Dataset":
        st.subheader("📊 Dataset Asli (Tanpa Efisiensi)")
        st.dataframe(df)


if __name__ == "__main__":
    main()