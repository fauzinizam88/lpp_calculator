import streamlit as st


# =========================
# Page + Style
# =========================
st.set_page_config(page_title="LPP Calculator (PPKM)", page_icon="📊", layout="wide")

APP_CSS = """
<style>
header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
div[data-testid="stToolbar"] { visibility: hidden; height: 0px; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

div.block-container { padding-top: 0.9rem; padding-bottom: 0.9rem; }
div[data-testid="stVerticalBlock"] > div { padding-top: 0.10rem; padding-bottom: 0.10rem; }
hr { margin: 0.55rem 0; }

.appbar {
  padding: 14px 16px;
  border-radius: 14px;
  background: linear-gradient(90deg, #1f6feb 0%, #7c3aed 55%, #f59e0b 100%);
  color: #ffffff;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  margin-top: 0.2rem;
}
.appbar-title { font-size: 1.2rem; font-weight: 900; margin: 0; }
.appbar-sub { font-size: 0.9rem; opacity: 0.95; margin: 2px 0 0 0; }

.pill {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 0.90rem;
  font-weight: 900;
  border: 1px solid rgba(0,0,0,0.08);
}

.label-main { font-weight: 780; }
.label-sub  { font-size: 0.82rem; color: rgba(0,0,0,0.70); line-height: 1.20; margin-top: 3px; }

div[data-baseweb="select"] * { font-size: 0.92rem !important; }

section[data-testid="stSidebar"] { min-width: 320px; max-width: 320px; }

.sb-kpi {
  background: #ffffff;
  border: 1px solid rgba(0,0,0,0.07);
  border-radius: 14px;
  padding: 10px 12px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.04);
  margin-bottom: 10px;
}
.sb-kpi-title { font-size: 12px; color: rgba(0,0,0,0.65); font-weight: 800; margin: 0; }
.sb-kpi-value { font-size: 22px; font-weight: 950; margin: 2px 0 0 0; }
</style>
"""
st.markdown(APP_CSS, unsafe_allow_html=True)


# =========================
# HARD-CODED "EXCEL" CONFIG
# (from your uploaded LPP Calculator PPKM.xlsx - sheet USM (2))
# =========================

GRADE_LABEL = "Gred Jawatan"
GRADE_OPTIONS = ["Pensyarah", "Profesor Madya", "Profesor"]
GRADE_DEFAULT = "Pensyarah"

# Excel C2 formula:
# =IF(B2="","",IFS(B2="Pensyarah",170,B2="Profesor Madya",200,B2="Profesor",200))
GRADE_TO_C2 = {"Pensyarah": 170.0, "Profesor Madya": 200.0, "Profesor": 200.0}

DROPDOWNS = [
    # X1 rows (4-8)
    {
        "row": 4,
        "label": "X1: M1 1 Penerbitan Q1&Q2 (Syarat Universiti)",
        "options": ["Capai", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"Capai": 50.0, "Tidak Capai": 0.0},
    },
    {
        "row": 5,
        "label": "X1: M1 1 Penerbitan Q1-Q4 (Syarat Universiti)",
        "options": ["Capai", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"Capai": 50.0, "Tidak Capai": 0.0},
    },
    {
        "row": 6,
        "label": "X1: M1 1 Geran (Syarat Universiti)",
        "options": ["Aktif", "Dimohon", "Co-Researcher", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"Aktif": 100.0, "Dimohon": 100.0, "Co-Researcher": 100.0, "Tidak Capai": 0.0},
    },
    {
        "row": 7,
        "label": "X1: M2 Penyeliaan (Syarat PTJ)",
        "options": ["1 PG Aktif", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"1 PG Aktif": 100.0, "Tidak Capai": 0.0},
    },
    {
        "row": 8,
        "label": "X1: M2 Pengajaran (Syarat PTJ)",
        "options": ["5 Jam Pengajaran", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"5 Jam Pengajaran": 100.0, "Tidak Capai": 0.0},
    },

    # X2 rows (10-12)
    {
        "row": 10,
        "label": "X2: M1 Kualiti Penerbitan 1",
        "options": [
            "Q1/2 (W/S) - 1st/Cor/Sole",
            "Book (Idx/MAPIM) - 1st",
            "Q3/4 (W/S) - 1st/Cor/Sole",
            "Book (Idx/MAPIM) - Co",
            "Chp Book (Idx/MAPIM) - 1st",
            "Chp Book (Idx/MAPIM) - Co",
            "ERA/MyCite - 1st/Cor/Sole",
            "Q1/2 (W/S) - Co",
            "Q3/4 (W/S) - Co",
            "ERA/MyCite - Co",
            "Non-Index Jnl - 1st/Cor/Sole",
            "Idx Proc - 1st/Cor/Sole",
            "Tiada Penerbitan",
        ],
        "default": "Tiada Penerbitan",
        "mapping": {
            "Q1/2 (W/S) - 1st/Cor/Sole": 100.0,
            "Book (Idx/MAPIM) - 1st": 100.0,
            "Q3/4 (W/S) - 1st/Cor/Sole": 70.0,
            "Book (Idx/MAPIM) - Co": 50.0,
            "Chp Book (Idx/MAPIM) - 1st": 50.0,
            "Chp Book (Idx/MAPIM) - Co": 25.0,
            "ERA/MyCite - 1st/Cor/Sole": 50.0,
            "Q1/2 (W/S) - Co": 50.0,
            "Q3/4 (W/S) - Co": 40.0,
            "ERA/MyCite - Co": 30.0,
            "Non-Index Jnl - 1st/Cor/Sole": 30.0,
            "Idx Proc - 1st/Cor/Sole": 10.0,
            "Tiada Penerbitan": 0.0,
        },
    },
    {
        "row": 11,
        "label": "X2: M1 Kualiti Penerbitan 2",
        "options": [
            "Q1/2 (W/S) - 1st/Cor/Sole",
            "Book (Idx/MAPIM) - 1st",
            "Q3/4 (W/S) - 1st/Cor/Sole",
            "Book (Idx/MAPIM) - Co",
            "Chp Book (Idx/MAPIM) - 1st",
            "Chp Book (Idx/MAPIM) - Co",
            "ERA/MyCite - 1st/Cor/Sole",
            "Q1/2 (W/S) - Co",
            "Q3/4 (W/S) - Co",
            "ERA/MyCite - Co",
            "Non-Index Jnl - 1st/Cor/Sole",
            "Idx Proc - 1st/Cor/Sole",
            "Tiada Penerbitan",
        ],
        "default": "Tiada Penerbitan",
        "mapping": {
            "Q1/2 (W/S) - 1st/Cor/Sole": 100.0,
            "Book (Idx/MAPIM) - 1st": 100.0,
            "Q3/4 (W/S) - 1st/Cor/Sole": 70.0,
            "Book (Idx/MAPIM) - Co": 50.0,
            "Chp Book (Idx/MAPIM) - 1st": 50.0,
            "Chp Book (Idx/MAPIM) - Co": 25.0,
            "ERA/MyCite - 1st/Cor/Sole": 50.0,
            "Q1/2 (W/S) - Co": 50.0,
            "Q3/4 (W/S) - Co": 40.0,
            "ERA/MyCite - Co": 30.0,
            "Non-Index Jnl - 1st/Cor/Sole": 30.0,
            "Idx Proc - 1st/Cor/Sole": 10.0,
            "Tiada Penerbitan": 0.0,
        },
    },
    {
        "row": 12,
        "label": "X2: M1 Geran (Kualiti)",
        "options": ["Aktif", "Dimohon", "Co-Researcher", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"Aktif": 100.0, "Dimohon": 40.0, "Co-Researcher": 30.0, "Tidak Capai": 0.0},
    },

    # M3/M4/M5 rows (16-18)
    {
        "row": 16,
        "label": "M3 (1 Kepimpinan Akademik)\nAcademic Awards, Awards for In... Recognition (Professional Bodies), Reviewing Articles/Journal",
        "options": ["Capai", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"Capai": 100.0, "Tidak Capai": 0.0},
    },
    {
        "row": 17,
        "label": "M4 (1 Perundingan)",
        "options": [
            "Gifts",
            "Endowment",
            "Consultancy",
            "Testing",
            "Product Commercialization",
            "Training Course",
            "Micro-Credential",
            "None Above",
        ],
        "default": "None Above",
        "mapping": {
            "Gifts": 100.0,
            "Endowment": 100.0,
            "Consultancy": 100.0,
            "Testing": 100.0,
            "Product Commercialization": 100.0,
            "Training Course": 100.0,
            "Micro-Credential": 100.0,
            "None Above": 0.0,
        },
    },
    {
        "row": 18,
        "label": "M5 (3 Khidmat Universiti)\nOBE committee, SRR committee, I...nts applications, Activities related to academic for UG and PG",
        "options": ["Capai 1", "Capai 2", "Capai 3", "Tidak Capai"],
        "default": "Tidak Capai",
        "mapping": {"Capai 1": 33.33, "Capai 2": 66.66, "Capai 3": 100.0, "Tidak Capai": 0.0},
    },
]

# Numeric inputs reflect your NEW Excel for Y/Z:
NUMERICS = [
    {
        "row": 21,
        "section_label": "Y (20%)",
        "label": "Hasil Kerja di PTJ-Y1\nMarkah daripada PPP & PPK",
        "default": 10.0,
        "max_input": 10.0,   # D21 max 10
        "max_output": 10.0,  # E21 = D21/10*10
    },
    {
        "row": 22,
        "section_label": "",
        "label": "Naratif impak pada Human Development/ Sustainability/ Industry-Y2\n"
                 "PYD must indicate the narrative\n"
                 "achievement for one (1) of the best\n"
                 "components, not exceeding 200 words\n"
                 "(1000 characters), before the LPP\n"
                 "evaluation. Proof of evidence is optional.",
        "default": 10.0,
        "max_input": 10.0,   # D22 max 10
        "max_output": 10.0,  # E22 = D22/10*10
    },
    {
        "row": 24,
        "section_label": "Z (10%)",
        "label": "CPD",
        "default": 30.0,
        "max_input": 30.0,   # D24 max 30
        "max_output": 10.0,  # E24 = D24/30*10
    },
]

ROWS_X1 = [4, 5, 6, 7, 8]
ROWS_X2 = [10, 11, 12]
ROWS_M  = [16, 17, 18]


# =========================
# UI helpers
# =========================
def render_label(label: str):
    lines = (label or "").splitlines()
    main = lines[0] if lines else ""
    sub = "<br>".join(lines[1:]) if len(lines) > 1 else ""
    html = f"<div><div class='label-main'>{main}</div>"
    if sub:
        html += f"<div class='label-sub'>{sub}</div>"
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def mark_pill(x: float, scale: float | None = None) -> str:
    # Small heuristic so 0–10 and 0–100 both look reasonable
    if scale is None:
        if x <= 10:
            scale = 10.0
        elif x <= 30:
            scale = 30.0
        elif x <= 70:
            scale = 70.0
        else:
            scale = 100.0

    if x <= 0:
        bg, fg = "#fee2e2", "#991b1b"
    elif x < 0.5 * scale:
        bg, fg = "#ffedd5", "#9a3412"
    elif x < 0.8 * scale:
        bg, fg = "#dbeafe", "#1e40af"
    else:
        bg, fg = "#dcfce7", "#166534"
    return f"<span class='pill' style='background:{bg}; color:{fg};'>{x:.2f}</span>"


def render_header_row():
    c1, c2, c3 = st.columns([7, 3, 2])
    with c1:
        st.caption("Komponen")
    with c2:
        st.caption("Self Check")
    with c3:
        st.caption("Markah")


def ensure_defaults():
    if "sel_grade" not in st.session_state:
        st.session_state["sel_grade"] = GRADE_DEFAULT if GRADE_DEFAULT in GRADE_OPTIONS else (GRADE_OPTIONS[0] if GRADE_OPTIONS else "")

    for dd in DROPDOWNS:
        key = f"sel_C{dd['row']}"
        if key not in st.session_state:
            default = dd.get("default", "")
            if default in dd["options"]:
                st.session_state[key] = default
            else:
                st.session_state[key] = dd["options"][0] if dd["options"] else ""

    for it in NUMERICS:
        key = f"num_D{it['row']}"
        max_in = float(it["max_input"])
        default = float(it.get("default", 0.0))
        default = max(0.0, min(default, max_in))
        if key not in st.session_state:
            st.session_state[key] = default
        else:
            try:
                st.session_state[key] = max(0.0, min(float(st.session_state[key]), max_in))
            except Exception:
                st.session_state[key] = default


def render_dropdown_row(dd):
    r = dd["row"]
    key = f"sel_C{r}"

    c1, c2, c3 = st.columns([7, 3, 2], vertical_alignment="center")
    with c1:
        render_label(dd["label"])
    with c2:
        st.selectbox(
            label=f"C{r}",
            options=dd["options"] if dd["options"] else [""],
            key=key,
            label_visibility="collapsed",
        )
    with c3:
        sel = st.session_state.get(key, "")
        mark = float(dd["mapping"].get(sel, 0.0))
        st.markdown(mark_pill(mark, scale=100.0), unsafe_allow_html=True)


def render_numeric_row(it):
    r = it["row"]
    key = f"num_D{r}"
    max_in = float(it["max_input"])
    max_out = float(it["max_output"])

    step = 1.0 if abs(max_in - round(max_in)) < 1e-9 else 0.1

    c1, c2, c3 = st.columns([7, 3, 2], vertical_alignment="center")
    with c1:
        render_label(it["label"])
    with c2:
        st.number_input(
            label=f"D{r}",
            min_value=0.0,
            max_value=max_in,
            step=step,
            key=key,
            label_visibility="collapsed",
        )
    with c3:
        val = float(st.session_state.get(key, 0.0))
        preview = (val / max_in) * max_out if max_in > 0 else 0.0
        st.markdown(mark_pill(preview, scale=max_out), unsafe_allow_html=True)


# =========================
# HARD-CODED "EXCEL" CALCULATIONS
# =========================
def get_mark_for_row(row: int) -> float:
    dd = next((x for x in DROPDOWNS if x["row"] == row), None)
    if not dd:
        return 0.0
    sel = st.session_state.get(f"sel_C{row}", dd.get("default", ""))
    return float(dd["mapping"].get(sel, 0.0))


def compute_all():
    # Grade output (Excel C2)
    grade = st.session_state.get("sel_grade", "")
    c2 = float(GRADE_TO_C2.get(grade, 0.0))

    # Dropdown marks (Excel D4..D8, D10..D12, D16..D18)
    d4 = get_mark_for_row(4)
    d5 = get_mark_for_row(5)
    d6 = get_mark_for_row(6)
    d7 = get_mark_for_row(7)
    d8 = get_mark_for_row(8)

    d10 = get_mark_for_row(10)
    d11 = get_mark_for_row(11)
    d12 = get_mark_for_row(12)

    d16 = get_mark_for_row(16)
    d17 = get_mark_for_row(17)
    d18 = get_mark_for_row(18)

    # Excel E9: =(D4+D5+D6+D7+D8)/400*60
    e9 = (d4 + d5 + d6 + d7 + d8) / 400.0 * 60.0

    # Excel E13: =((((D10+D11)/C2)+(D12/100))/2)*40
    if c2 > 0:
        e13 = ((((d10 + d11) / c2) + (d12 / 100.0)) / 2.0) * 40.0
    else:
        e13 = 0.0

    # Excel E14: =(E9+E13)/100*42
    e14 = (e9 + e13) / 100.0 * 42.0

    # Excel D19: =(SUM(D16:D18)-MIN(D16:D18))/2
    d19 = ((d16 + d17 + d18) - min(d16, d17, d18)) / 2.0

    # Excel E19: =D19*0.28
    e19 = d19 * 0.28

    # Excel E20 (TOTAL X): =E14+E19
    total_x = e14 + e19

    # Numeric inputs -> Excel E21/E22/E24
    d21 = float(st.session_state.get("num_D21", 0.0))
    d22 = float(st.session_state.get("num_D22", 0.0))
    d24 = float(st.session_state.get("num_D24", 0.0))

    # Excel E21: =D21/10*10
    e21 = (d21 / 10.0) * 10.0

    # Excel E22: =D22/10*10
    e22 = (d22 / 10.0) * 10.0

    # Excel E24: =D24/30*10
    e24 = (d24 / 30.0) * 10.0

    total_y = e21 + e22         # Excel E23
    total_z = e24               # Excel E25
    total_marks = total_x + e21 + e22 + e24  # Excel E26

    return {
        "c2": c2,
        "total_x": total_x,
        "total_y": total_y,
        "total_z": total_z,
        "total_marks": total_marks,
    }


# =========================
# Header
# =========================
st.markdown(
    """
<div class="appbar">
  <div class="appbar-title">LPP Calculator (PPKM)</div>
  <div class="appbar-sub">This app is designed to help lecturers estimate their marks based on their SKT planning</div>
</div>
""",
    unsafe_allow_html=True,
)

ensure_defaults()

# =========================
# Grade selector
# =========================
values = compute_all()

g1, g2, g3 = st.columns([3, 5, 2], vertical_alignment="center")
with g1:
    st.markdown(f"**{GRADE_LABEL}**")
with g2:
    st.selectbox("Gred Jawatan", GRADE_OPTIONS if GRADE_OPTIONS else [""], key="sel_grade", label_visibility="collapsed")
with g3:
    values = compute_all()  # refresh after selection
    st.markdown(mark_pill(values["c2"], scale=200.0), unsafe_allow_html=True)

# =========================
# Tabs
# =========================
tab_dash, tab_x, tab_y, tab_z = st.tabs(["Dashboard", "X (70%)", "Y (20%)", "Z (10%)"])

with tab_x:
    st.subheader("X (70%)")

    st.markdown("**X1**")
    render_header_row()
    for r in ROWS_X1:
        dd = next(x for x in DROPDOWNS if x["row"] == r)
        render_dropdown_row(dd)
    st.markdown("---")

    st.markdown("**X2**")
    render_header_row()
    for r in ROWS_X2:
        dd = next(x for x in DROPDOWNS if x["row"] == r)
        render_dropdown_row(dd)
    st.markdown("---")

    st.markdown("**M3/M4/M5**")
    render_header_row()
    for r in ROWS_M:
        dd = next(x for x in DROPDOWNS if x["row"] == r)
        render_dropdown_row(dd)

with tab_y:
    st.subheader("Y (20%)")
    for it in NUMERICS:
        if it["row"] in (21, 22):
            if it.get("section_label"):
                st.markdown(f"**{it['section_label']}**")
            render_numeric_row(it)

with tab_z:
    st.subheader("Z (10%)")
    for it in NUMERICS:
        if it["row"] == 24:
            if it.get("section_label"):
                st.markdown(f"**{it['section_label']}**")
            render_numeric_row(it)

# recompute totals after inputs render
values = compute_all()
total_x = float(values["total_x"])
total_y = float(values["total_y"])
total_z = float(values["total_z"])
total_marks = float(values["total_marks"])


# =========================
# Sidebar
# =========================
with st.sidebar:
    st.markdown("### Current Marks")

    st.markdown(
        f"""
        <div class="sb-kpi">
          <p class="sb-kpi-title">TOTAL X (70%)</p>
          <p class="sb-kpi-value">{total_x:.2f}</p>
        </div>
        <div class="sb-kpi">
          <p class="sb-kpi-title">TOTAL Y (20%)</p>
          <p class="sb-kpi-value">{total_y:.2f}</p>
        </div>
        <div class="sb-kpi">
          <p class="sb-kpi-title">TOTAL Z (10%)</p>
          <p class="sb-kpi-value">{total_z:.2f}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div style="text-align:center; margin-top: 6px;">
          <div style="font-size: 12px; color: rgba(0,0,0,0.65); font-weight: 800;">Total Marks</div>
          <div style="font-size: 38px; font-weight: 950; line-height: 1.0;">{total_marks:.2f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("### Garis Panduan")
    st.markdown(
        """
        <a href="https://drive.google.com/file/d/1vLXPaINzEI2969U8i7Mhhufdn9voYkxa/view?usp=sharing" target="_blank">
          Download Garis Panduan SKT
        </a>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")
    if st.button("Reset all inputs", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# =========================
# Dashboard tab
# =========================
with tab_dash:
    st.subheader("Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TOTAL X (70%)", f"{total_x:.2f}")
    c2.metric("TOTAL Y (20%)", f"{total_y:.2f}")
    c3.metric("TOTAL Z (10%)", f"{total_z:.2f}")
    c4.metric("Total Marks", f"{total_marks:.2f}")
