# LPP Calculator (PPKM)
This is a Streamlit web application designed to calculate Key Performance Indicators (KPIs) for the LPP (Laporan Penilaian Prestasi) process, specifically tailored for the PPKM context.

Live app: https://lppcalculator.streamlit.app/

## Run locally
pip install -r requirements.txt
streamlit run app.py

Install dependencies:
pip install streamlit

Start the app:
streamlit run app.py
Streamlit will print a local URL (typically http://localhost:8501).

## App Structure
The application is divided into several tabs:

    Dashboard: A high-level summary of the Total X, Y, Z scores and the final Total Marks.

    X (70%): Detailed inputs for Research & Publication components (X1, X2) and other academic contributions (M3, M4, M5).

    Y (20%): Inputs for PTJ-specific contributions and narrative impacts.

    Z (10%): Inputs for Continuous Professional Development (CPD).

A sidebar provides a persistent view of the current scores and a link to the "Garis Panduan" document.

## License & Redistribution (Compliance Checklist)
This project is licensed under the **Apache License 2.0**.

If you **redistribute** this project (original or modified), you must:
1. Include the `LICENSE` file (Apache 2.0).
2. Keep the `NOTICE` file (or reproduce its contents in an appropriate place).
3. Keep existing copyright and attribution notices in the source.
4. If you modify files, add a clear note that you changed them.

If you cannot meet these requirements, you are not permitted to redistribute the code.

## Disclaimer
This tool is provided for educational and informational purposes only. It is provided **"AS IS"** without warranties or conditions of any kind. Use at your own risk.


## Project Structure

```text
.
├── app.py
├── requirements.txt
└── README.md

