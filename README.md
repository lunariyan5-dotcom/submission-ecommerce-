## Proyek ini merupakan hasil analisis dataset publik E-Commerce untuk mengidentifikasi tren pendapatan dan performa kategori produk. Hasil analisis kemudian disajikan dalam bentuk dashboard interaktif menggunakan Streamlit.

### Setup Environment - Anaconda

Langkah-langkah untuk menyiapkan lingkungan/environment menggunakan Anaconda:
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

### Setup Environment - Shell/Terminal

Setup Environment - Anaconda
mkdir proyek_analisis_data
cd proyek_analisis_data
pip install pipenv
pipenv install
pipenv shell
pip install -r requirements.txt

### Run streamlit app

streamlit run dashboard.py
