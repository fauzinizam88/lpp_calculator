# LPP Calculator (PPKM)
# Copyright (c) 2026 Poji
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re

import streamlit as st


# =========================
# Page + Style
# =========================
st.set_page_config(page_title="LPP Calculator (PPKM)", page_icon="📊", layout="wide")

APP_CSS = """
<style>
/* Hide Streamlit chrome that can crop custom header */
header[data-testid="stHeader"] { visibility: hidden; height: 0px; }
div[data-testid="stToolbar"] { visibility: hidden; height: 0px; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Compact layout */
div.block-container { padding-top: 0.9rem; padding-bottom: 0.9rem; }
div[data-testid="stVerticalBlock"] > div { padding-top: 0.10rem; padding-bottom: 0.10rem; }
hr { margin: 0.55rem 0; }

/* App bar */
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

/* Pills */
.pill {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 999px;
  font-size: 0.90rem;
  font-weight: 900;
  border: 1px solid rgba(0,0,0,0.08);
}

/* Label typography */
.label-main { font-weight: 780; }
.label-sub  { font-size: 0.82rem; color: rgba(0,0,0,0.70); line-height: 1.20; margin-top: 3px; }

/* Slightly smaller selectbox font */
div[data-baseweb="select"] * { font-size: 0.92rem !important; }

/* Sidebar width */
section[data-testid="stSidebar"] { min-width: 320px; max-width: 320px; }

/* Sidebar KPI blocks */
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
# HARD-CODED MODEL (no Excel needed)
# =========================

# Grade selector (B2) and grade output formula (C2)
GRADE_LABEL = "Gred Jawatan"
GRADE_OPTIONS = ["Pensyarah", "Profesor Madya", "Profesor"]
GRADE_DEFAULT = "Pensyarah"
GRADE_FORMULA_C2 = '=IF(B2="","",_xlfn.IFS(B2="Pensyarah",170,B2="Profesor Madya",200,B2="Profesor",200))'

# Dropdown rows, options, and mark mapping (C{row} -> D{row})
DROPDOWN_ITEMS = [
    dict(
        row=4,
        label="X1: M1 1 Penerbitan Q1&Q2 (Syarat Universiti)",
        options=["Capai", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"Capai": 50.0},
        default_mark=0.0,
    ),
    dict(
        row=5,
        label="X1: M1 1 Penerbitan Q1-Q4 (Syarat Universiti)",
        options=["Capai", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"Capai": 50.0},
        default_mark=0.0,
    ),
    dict(
        row=6,
        label="X1: M1 1 Geran (Syarat Universiti)",
        options=["Aktif", "Dimohon", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"Aktif": 100.0, "Dimohon": 100.0, "Tidak Capai": 0.0},
        default_mark=0.0,
    ),
    dict(
        row=7,
        label="X1: M2 Penyeliaan (Syarat PTJ)",
        options=["1 PG Aktif", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"1 PG Aktif": 100.0, "Tidak Capai": 0.0},
        default_mark=0.0,
    ),
    dict(
        row=8,
        label="X1: M2 Pengajaran (Syarat PTJ)",
        options=["5 Jam Pengajaran", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"5 Jam Pengajaran": 100.0, "Tidak Capai": 0.0},
        default_mark=0.0,
    ),
    dict(
        row=10,
        label="X2: M1 Kualiti Penerbitan 1",
        options=[
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
        default_option="Tiada Penerbitan",
        mapping={
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
        default_mark=0.0,
    ),
    dict(
        row=11,
        label="X2: M1 Kualiti Penerbitan 2",
        options=[
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
        default_option="Tiada Penerbitan",
        mapping={
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
        default_mark=0.0,
    ),
    dict(
        row=12,
        label="X2: M1 Geran (Kualiti)",
        options=["Aktif", "Dimohon", "Co-Researcher", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"Aktif": 100.0, "Dimohon": 40.0, "Co-Researcher": 30.0, "Tidak Capai": 0.0},
        default_mark=0.0,
    ),
    dict(
        row=16,
        label=(
            "M3 (1 Kepimpinan Akademik)\n"
            "Academic Awards, Awards for Innovation, Academic Assessor, External Assessor (Promotion), "
            "External Examiner, Internal Examiner, Journal Editor, Board of Studies Member, Assessor "
            "Board of Director, Editorial Board Fellowship, Invited Speaker, Keynote Speaker, Professional "
            "Association Member, Academic Association Member, Panel Member, Discussion/Forum, Recognition "
            "(Professional Bodies), Reviewing Articles/Journal"
        ),
        options=["Capai", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"Capai": 100.0},
        default_mark=0.0,
    ),
    dict(
        row=17,
        label="M4 (1 Perundingan)",
        options=[
            "Gifts",
            "Endowment",
            "Consultancy",
            "Testing",
            "Product Commercialization",
            "Training Course",
            "Micro-Credential",
            "None Above",
        ],
        default_option="None Above",
        mapping={
            "Gifts": 100.0,
            "Endowment": 100.0,
            "Consultancy": 100.0,
            "Testing": 100.0,
            "Product Commercialization": 100.0,
            "Training Course": 100.0,
            "Micro-Credential": 100.0,
            "None Above": 0.0,
        },
        default_mark=0.0,
    ),
    dict(
        row=18,
        label=(
            "M5 (3 Khidmat Universiti)\n"
            "OBE committee, SRR committee, IQA committee, SWA committee, Curriculum Review committee, "
            "EAC/MQA audit activities, Internal panel for grants applications, Activities related to academic "
            "for UG and PG"
        ),
        options=["Capai 1", "Capai 2", "Capai 3", "Tidak Capai"],
        default_option="Tidak Capai",
        mapping={"Capai 1": 33.33, "Capai 2": 66.66, "Capai 3": 100.0, "Tidak Capai": 0.0},
        default_mark=0.0,
    ),
]

ROWS_X1 = [4, 5, 6, 7, 8]
ROWS_X2 = [10, 11, 12]
ROWS_XQ = [16, 17, 18]

# Numeric inputs (D{row}) and their scaling to E{row}
NUMERIC_ITEMS = [
    dict(
        row=21,
        section_label="Y (20%)",
        label="Hasil Kerja di PTJ-Y1\nMarkah daripada PPP & PPK",
        default=10.0,
        max_input=10.0,
        max_output=10.0,
    ),
    dict(
        row=22,
        section_label="",
        label=(
            "Naratif impak pada Human Development/ Sustainability/ Industry-Y2\n"
            "PYD must indicate the narrative\n"
            "achievement for one (1) of the best\n"
            "components, not exceeding 200 words\n"
            "(1000 characters), before the LPP\n"
            "evaluation. Proof of evidence is optional."
        ),
        default=10.0,
        max_input=10.0,
        max_output=10.0,
    ),
    dict(
        row=24,
        section_label="Z (10%)",
        label="CPD",
        default=30.0,
        max_input=30.0,
        max_output=10.0,
    ),
]

# Formula evaluation order and formulas (hard-coded from the new Excel)
FORM_ORDER = ["C2", "D19", "E9", "E13", "E14", "E19", "E20", "E21", "E22", "E23", "E24", "E25", "E26"]

FORMULA_MAP = {
    "C2": GRADE_FORMULA_C2,
    "D19": "=(SUM(D16:D18)-MIN(D16:D18))/2",
    "E9": "=(D4+D5+D6+D7+D8)/400*60",
    "E13": "=((((D10+D11)/C2)+(D12/100))/2)*40",
    "E14": "=(E9+E13)/100*42",
    "E19": "=D19*0.28",
    "E20": "=E14+E19",
    "E21": "=D21/10*10",
    "E22": "=D22/10*10",
    "E23": "=E21+E22",
    "E24": "=D24/30*10",
    "E25": "=E24",
    "E26": "=E20+E21+E22+E24",
}

ADDR_TOTAL_X = "E20"
ADDR_TOTAL_Y = "E23"
ADDR_TOTAL_Z = "E25"
ADDR_TOTAL_MARKS = "E26"


# =========================
# Formula evaluator (Excel-like)
# =========================
CELL_REF_RE = re.compile(r'(?<![A-Z0-9_])\$?[A-Z]{1,3}\$?\d+(?![A-Z0-9_])')
RANGE_RE = re.compile(r'(\$?[A-Z]{1,3}\$?\d+:\$?[A-Z]{1,3}\$?\d+)')
STR_RE = re.compile(r'"([^"]*)"')


def _col_row(a):
    a = a.replace("$", "")
    m = re.match(r"^([A-Z]{1,3})(\d+)$", a)
    return m.group(1), int(m.group(2))


def _range_values(values: dict, rng: str):
    rng = rng.replace("$", "")
    a, b = rng.split(":")
    col_a, row_a = _col_row(a)
    col_b, row_b = _col_row(b)

    if col_a == col_b:
        start, end = sorted([row_a, row_b])
        out = []
        for r in range(start, end + 1):
            v = values.get(f"{col_a}{r}", 0.0)
            try:
                out.append(float(v))
            except Exception:
                out.append(0.0)
        return out

    return []


def _SUM_(*args):
    out = 0.0
    for a in args:
        out += sum(a) if isinstance(a, list) else float(a)
    return out


def _MIN_(*args):
    flat = []
    for a in args:
        flat.extend(a) if isinstance(a, list) else flat.append(float(a))
    return min(flat) if flat else 0.0


def _IF_(cond, vt, vf):
    return vt if cond else vf


def _IFS_(*args):
    for i in range(0, len(args), 2):
        if i + 1 >= len(args):
            break
        if args[i]:
            return args[i + 1]
    return 0.0


def eval_excel_formula(formula: str, values: dict):
    if not formula:
        return 0.0

    f = formula.strip()
    if f.startswith("="):
        f = f[1:]
    f = f.replace("$", "").replace("\n", "").replace("_xlfn.", "")

    f = RANGE_RE.sub(lambda m: f'R("{m.group(1)}")', f)

    strings = []

    def mask_str(m):
        strings.append(m.group(0))
        return f"__STR{len(strings)-1}__"

    f = STR_RE.sub(mask_str, f)

    f = (
        f.replace("SUM(", "SUM_(")
         .replace("MIN(", "MIN_(")
         .replace("IF(", "IF_(")
         .replace("IFS(", "IFS_(")
    )

    f = f.replace("<>", "!=")
    f = re.sub(r'(?<![<>=!])=(?![=])', "==", f)

    f = CELL_REF_RE.sub(lambda m: f'V("{m.group(0)}")', f)

    for i, s in enumerate(strings):
        f = f.replace(f"__STR{i}__", s)

    env = {
        "SUM_": _SUM_,
        "MIN_": _MIN_,
        "IF_": _IF_,
        "IFS_": _IFS_,
        "R": lambda rng: _range_values(values, rng),
        "V": lambda addr: values.get(addr.replace("$", ""), 0.0),
    }
    return eval(f, {"__builtins__": {}}, env)


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


def mark_pill(x: float) -> str:
    if x <= 0:
        bg, fg = "#fee2e2", "#991b1b"
    elif x < 50:
        bg, fg = "#ffedd5", "#9a3412"
    elif x < 100:
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


DD_BY_ROW = {it["row"]: it for it in DROPDOWN_ITEMS}


def ensure_defaults():
    # Grade default
    if "sel_B2" not in st.session_state:
        st.session_state["sel_B2"] = GRADE_DEFAULT if GRADE_DEFAULT in GRADE_OPTIONS else (GRADE_OPTIONS[0] if GRADE_OPTIONS else "")

    # Dropdown defaults
    for it in DROPDOWN_ITEMS:
        key = f"sel_C{it['row']}"
        if key not in st.session_state:
            if it["default_option"] in it["options"]:
                st.session_state[key] = it["default_option"]
            elif it["options"]:
                st.session_state[key] = it["options"][0]
            else:
                st.session_state[key] = ""

    # Numeric defaults + clamp
    for it in NUMERIC_ITEMS:
        key = f"num_D{it['row']}"
        max_in = float(it.get("max_input", 100.0))
        default_val = float(it.get("default", 0.0))
        default_val = max(0.0, min(default_val, max_in))

        if key not in st.session_state:
            st.session_state[key] = default_val
        else:
            try:
                st.session_state[key] = max(0.0, min(float(st.session_state[key]), max_in))
            except Exception:
                st.session_state[key] = default_val


def render_dropdown_row(r: int, values: dict):
    it = DD_BY_ROW[r]
    key = f"sel_C{r}"

    c1, c2, c3 = st.columns([7, 3, 2], vertical_alignment="center")
    with c1:
        render_label(it["label"])
    with c2:
        sel = st.selectbox(
            label=f"C{r}",
            options=it["options"] if it["options"] else [""],
            key=key,
            label_visibility="collapsed",
        )
    with c3:
        mark = float(it["mapping"].get(sel, it["default_mark"]))
        st.markdown(mark_pill(mark), unsafe_allow_html=True)

    values[f"C{r}"] = sel
    values[f"D{r}"] = mark


def render_numeric_row(it, values: dict):
    r = it["row"]
    key = f"num_D{r}"

    max_in = float(it.get("max_input", 100.0))   # e.g., 10 / 30
    max_out = float(it.get("max_output", 10.0))  # usually 10

    step = 1.0 if abs(max_in - round(max_in)) < 1e-9 else 0.1

    c1, c2, c3 = st.columns([7, 3, 2], vertical_alignment="center")
    with c1:
        render_label(it["label"])
    with c2:
        val = st.number_input(
            label=f"D{r}",
            min_value=0.0,
            max_value=max_in,
            step=step,
            key=key,
            label_visibility="collapsed",
        )
    with c3:
        preview = (float(val) / max_in) * max_out if max_in > 0 else 0.0
        st.markdown(mark_pill(preview), unsafe_allow_html=True)

    values[f"D{r}"] = float(val)


def compute_totals(values: dict):
    for addr in FORM_ORDER:
        f = FORMULA_MAP.get(addr)
        if f:
            values[addr] = eval_excel_formula(f, values)


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
values = {}

g1, g2, g3 = st.columns([3, 5, 2], vertical_alignment="center")
with g1:
    st.markdown(f"**{GRADE_LABEL}**")
with g2:
    st.selectbox(
        "Gred Jawatan",
        GRADE_OPTIONS if GRADE_OPTIONS else [""],
        key="sel_B2",
        label_visibility="collapsed",
    )
with g3:
    tmp = {"B2": st.session_state["sel_B2"]}
    c2_val = float(eval_excel_formula(GRADE_FORMULA_C2, tmp)) if GRADE_FORMULA_C2 else 0.0
    st.markdown(mark_pill(c2_val), unsafe_allow_html=True)

values["B2"] = st.session_state["sel_B2"]


# =========================
# Tabs
# =========================
tab_dash, tab_x, tab_y, tab_z = st.tabs(["Dashboard", "X (70%)", "Y (20%)", "Z (10%)"])

with tab_x:
    st.subheader("X (70%)")

    if ROWS_X1:
        render_header_row()
        for r in ROWS_X1:
            render_dropdown_row(r, values)
        st.markdown("---")

    if ROWS_X2:
        render_header_row()
        for r in ROWS_X2:
            render_dropdown_row(r, values)
        st.markdown("---")

    if ROWS_XQ:
        render_header_row()
        for r in ROWS_XQ:
            render_dropdown_row(r, values)

with tab_y:
    st.subheader("Y (20%)")
    for it in NUMERIC_ITEMS:
        if it["row"] in (21, 22):
            if it.get("section_label"):
                st.markdown(f"**{it['section_label']}**")
            render_numeric_row(it, values)

with tab_z:
    st.subheader("Z (10%)")
    for it in NUMERIC_ITEMS:
        if it["row"] >= 24:
            if it.get("section_label"):
                st.markdown(f"**{it['section_label']}**")
            render_numeric_row(it, values)

# Compute totals
compute_totals(values)

total_x = float(values.get(ADDR_TOTAL_X, 0.0))
total_y = float(values.get(ADDR_TOTAL_Y, 0.0))
total_z = float(values.get(ADDR_TOTAL_Z, 0.0))
total_marks = float(values.get(ADDR_TOTAL_MARKS, 0.0))


# =========================
# Sidebar: show X/Y/Z current marks + Total Marks + SKT link + Reset
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
# Dashboard tab: KPIs only
# =========================
with tab_dash:
    st.subheader("Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("TOTAL X (70%)", f"{total_x:.2f}")
    c2.metric("TOTAL Y (20%)", f"{total_y:.2f}")
    c3.metric("TOTAL Z (10%)", f"{total_z:.2f}")
    c4.metric("Total Marks", f"{total_marks:.2f}")
