import streamlit as st

st.set_page_config(
    page_title="Beslutsstöd: Ledighetsansökan",
    page_icon="🏫",
    layout="centered"
)

# Bakgrundsstil: Konstnärlig bakgrund med färgglada linjer, vågor och glassmorphism
st.markdown("""
<style>
/* Appens huvudbakgrund med färgglada toningsvågor och mörk kontrast */
.stApp {
    background: 
        radial-gradient(ellipse at 15% 15%, rgba(236, 72, 153, 0.35) 0%, transparent 45%),
        radial-gradient(ellipse at 85% 85%, rgba(56, 189, 248, 0.35) 0%, transparent 45%),
        radial-gradient(ellipse at 50% 50%, rgba(168, 85, 247, 0.25) 0%, transparent 55%),
        linear-gradient(135deg, #090d16 0%, #0f172a 35%, #1e1b4b 70%, #111827 100%);
    background-attachment: fixed;
    color: #f8fafc;
}

/* Konstnärligt linjemönster med färgglada diagonala stråk */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-image: 
        repeating-linear-gradient(45deg, rgba(236, 72, 153, 0.08) 0px, rgba(236, 72, 153, 0.08) 2px, transparent 2px, transparent 35px),
        repeating-linear-gradient(-45deg, rgba(56, 189, 248, 0.08) 0px, rgba(56, 189, 248, 0.08) 2px, transparent 2px, transparent 35px),
        repeating-linear-gradient(120deg, rgba(168, 85, 247, 0.07) 0px, rgba(168, 85, 247, 0.07) 3px, transparent 3px, transparent 50px);
    pointer-events: none;
    z-index: 0;
}

/* Innehållskontainer med glaseffekt (glassmorphism) för perfekt läsbarhet */
.main .block-container {
    background: rgba(15, 23, 42, 0.82);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 35px rgba(168, 85, 247, 0.2);
    margin-top: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
    z-index: 1;
}

/* Rubriker */
h1, h2, h3, h4 {
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* Textingångar och menyer */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background-color: rgba(30, 41, 59, 0.85) !important;
    border-color: rgba(148, 163, 184, 0.3) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

label {
    color: #e2e8f0 !important;
    font-weight: 500 !important;
}

/* Avskiljare */
hr {
    border-color: rgba(255, 255, 255, 0.15) !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🏫 Beslutsstöd för Ledighetsansökningar")
st.markdown("""
Detta verktyg hjälper dig som skolledare att göra en rättssäker, likvärdig och samlad bedömning vid ansökningar om ledighet enligt **skollagen (2010:800)** och dess förarbeten (**Prop. 2009/10:165**).
""")

st.divider()

# Formulär för ärende
st.header("1. Uppgifter om ansökan")

col1, col2 = st.columns(2)
with col1:
    klasselev = st.text_input("Klass/Årskurs (valfritt)", value="")
    antal_dagar = st.number_input("Antal omsökta skoldagar", min_value=1, max_value=60, value=3)
with col2:
    tidigare_dagar = st.number_input("Tidigare beviljad ledighet detta läsår (dagar)", min_value=0, max_value=60, value=0)

st.subheader("Anledning & Omständigheter")

orsak = st.selectbox(
    "Huvudsaklig anledning till ledigheten:",
    [
        "Familjehögtid (t.ex. bröllop, begravning, jubileum)",
        "Religiös högtid",
        "Tävling / Evenemang på hög nivå (idrott/kultur)",
        "Synnerliga personliga skäl / Sjukvård",
        "Semesterresa / Familjesemester",
        "Övrigt"
    ]
)

studiesituation = st.radio(
    "Elevens nuvarande studiesituation och måluppfyllelse:",
    [
        "God / Följer utbildningens mål utan anmärkning",
        "Har viss frånvaro eller behöver stöd i vissa ämnen",
        "Hög frånvaro / Risk för att inte nå kunskapskraven"
    ]
)

kompensation = st.radio(
    "Möjlighet att kompensera förlorad undervisning:",
    [
        "God (eleven/hemmet kan enkelt ta igen skolarbetet)",
        "Begränsad (vissa viktiga moment missas)",
        "Mycket svår (viktiga praktiska/provmoment missas)"
    ]
)

känslig_period = st.radio(
    "Sammanfaller ledigheten med särskilt känslig period?",
    [
        "Nej",
        "Ja, nationella prov / Betygsgrundande prov",
        "Ja, terminsstart / Viktiga introduktionsmoment"
    ]
)

st.divider()

# Analys & Beslut
st.header("2. Bedömning & Beslutsförslag")

if st.button("Generera bedömning och beslutstext", type="primary"):
    totalt_dagar = antal_dagar + tidigare_dagar
    is_over_10 = totalt_dagar > 10
    
    # Flag checks
    is_semester = (orsak == "Semesterresa / Familjesemester")
    is_prov = ("nationella prov" in känslig_period.lower())
    is_risk_study = ("Hög frånvaro" in studiesituation)
    is_enskild_angelagenhet = orsak in [
        "Familjehögtid (t.ex. bröllop, begravning, jubileum)",
        "Religiös högtid",
        "Synnerliga personliga skäl / Sjukvård",
        "Tävling / Evenemang på hög nivå (idrott/kultur)"
    ]
    
    # Decision logic
    beslut = "Avslås"
    skal_kategori = ""
    motivering_intern = []
    
    if is_over_10:
        # Kräver synnerliga skäl
        if orsak == "Synnerliga personliga skäl / Sjukvård":
            if not is_prov and not is_risk_study:
                beslut = "Beviljas"
                skal_kategori = "Synnerliga skäl"
                motivering_intern.append("Ledigheten överstiger 10 dagar men grundar sig på beaktansvärda synnerliga personliga skäl/sjukvård.")
            else:
                beslut = "Avslås"
                motivering_intern.append("Ledigheten överstiger 10 dagar. Trots angivna skäl görs bedömningen att elevens studiesituation eller provperiod hindrar beviljande.")
        else:
            beslut = "Avslås"
            motivering_intern.append("Ledigheten överstiger 10 dagar totalt under läsåret. För ledighet över 10 dagar krävs synnerliga skäl (7 kap. 18 § skollagen). Vanliga resor eller familjehögtider uppnår inte detta krav.")
    else:
        # Under/lika med 10 dagar: Kräver enskild angelägenhet
        if is_semester:
            beslut = "Avslås"
            motivering_intern.append("Semester- eller nöjesresor räknas enligt skollagens förarbeten (Prop. 2009/10:165) i normalfallet inte som en enskild angelägenhet.")
        elif is_prov:
            beslut = "Avslås"
            motivering_intern.append("Frånvaro under nationella prov eller betygsgrundande moment äventyrar elevens rätt till utbildning och rättvis bedömning.")
        elif is_risk_study:
            beslut = "Avslås"
            motivering_intern.append("Elevens nuvarande studiesituation och tidigare frånvaro gör att ytterligare frånvaro bedöms påverka måluppfyllelsen negativt.")
        elif is_enskild_angelagenhet:
            beslut = "Beviljas"
            skal_kategori = "Enskild angelägenhet"
            motivering_intern.append("Orsaken utgör en enskild angelägenhet (t.ex. familjehögtid/religiös högtid) och elevens studiesituation medger kortare frånvaro.")
        else:
            beslut = "Avslås"
            motivering_intern.append("Skälet bedöms efter en samlad värdering inte utgöra en sådan enskild angelägenhet som motiverar undantag från skolplikten.")

    # Visa resultatet
    if beslut == "Beviljas":
        st.success("### Förslag till beslut: BEVILJAS")
    else:
        st.error("### Förslag till beslut: AVSLÅS")
        
    st.markdown("**Intern motivering för beslut:**")
    for m in motivering_intern:
        st.write(f"- {m}")
        
    st.divider()
    st.header("3. Officiell beslutstext (att kopiera)")
    
    if beslut == "Beviljas":
        beslutstext = f"""BESLUT OM LEDIGHET

Ansökan om ledighet för eleven omfattande {antal_dagar} skoldag(ar) BEVILJAS.

Lagstöd och motivering:
Enligt 7 kap. 17 § skollagen (2010:800) har elever i grundskolan närvaroplikt. Enligt 7 kap. 18 § samma lag får en elev beviljas kortare ledighet för enskilda angelägenheter. 

Skolan har gjort en samlad bedömning av elevens studiesituation, frånvarons längd samt ledighetens angelägenhet. Ansökan bedöms avse en sådan enskild angelägenhet som avses i skollagens förarbeten (Prop. 2009/10:165), och elevens skolsituation medger den sökta ledigheten.

Vårdnadshavare ansvarar för att eleven tar igen förlorat skolarbete under frånvaron.

Med vänlig hälsning,
Rektor / Skolledning"""
    else:
        beslutstext = f"""BESLUT OM LEDIGHET

Ansökan om ledighet för eleven omfattande {antal_dagar} skoldag(ar) AVSLÅS.

Lagstöd och motivering:
Elever i grundskolan omfattas av skolplikt och har närvaroplikt i skolan (7 kap. 17 § skollagen [2010:800]). Ledighet kan endast beviljas för enskilda angelägenheter vid kortare frånvaro eller om det föreligger synnerliga skäl (7 kap. 18 § skollagen).

Efter en samlad bedömning av elevens studiesituation, frånvarons längd, tidpunkten för ledigheten och det uppgivna skälet har skolan beslutat att avslå ansökan. Enligt skollagens förarbeten (Prop. 2009/10:165) ska bestämmelserna om ledighet tillämpas restriktivt för att värna elevens rätt till utbildning.

Detta beslut kan inte överklagas (15 kap. skolförordningen [2011:185]).

Med vänlig hälsning,
Rektor / Skolledning"""

    st.code(beslutstext, language="text")
    st.caption("Klicka på kopieringsikonen i övre högra hörnet av textrutan ovan för att klistra in i skolsystemet.")
