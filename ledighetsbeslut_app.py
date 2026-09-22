import streamlit as st

st.set_page_config(
    page_title="Beslutsstöd: Ledighetsansökan",
    page_icon="🏫",
    layout="centered"
)

st.title("🏫 Beslutsstöd för Ledighetsansökningar")
st.markdown("""
Detta verktyg hjälper dig som skolledare att göra en rättssäker, likvärdig och samlad bedömning vid ansökningar om ledighet enligt **skollagen (2010:800)** och dess förarbeten (**Prop. 2009/10:165**).
""")

st.divider()

# Formulär för ärende
st.header("1. Uppgifter om ansökan")

col1, col2 = st.columns(2)
with col1:
    elev_namn = st.text_input("Elevens namn/initialer (valfritt)", value="")
    klasselev = st.text_input("Klass/Årskurs (valfritt)", value="")
with col2:
    antal_dagar = st.number_input("Antal omsökta skoldagar", min_value=1, max_value=60, value=3)
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
    
    namn_str = f"för {elev_namn}" if elev_namn else "för eleven"
    
    if beslut == "Beviljas":
        beslutstext = f"""BESLUT OM LEDIGHET

Ansökan om ledighet {namn_str} omfattande {antal_dagar} skoldag(ar) BEVILJAS.

Lagstöd och motivering:
Enligt 7 kap. 17 § skollagen (2010:800) har elever i grundskolan närvaroplikt. Enligt 7 kap. 18 § samma lag får en elev beviljas kortare ledighet för enskilda angelägenheter. 

Skolan har gjort en samlad bedömning av elevens studiesituation, frånvarons längd samt ledighetens angelägenhet. Ansökan bedöms avse en sådan enskild angelägenhet som avses i skollagens förarbeten (Prop. 2009/10:165), och elevens skolsituation medger den sökta ledigheten.

Vårdnadshavare ansvarar för att eleven tar igen förlorat skolarbete under frånvaron.

Med vänlig hälsning,
Rektor / Skolledning"""
    else:
        beslutstext = f"""BESLUT OM LEDIGHET

Ansökan om ledighet {namn_str} omfattande {antal_dagar} skoldag(ar) AVSLÅS.

Lagstöd och motivering:
Elever i grundskolan omfattas av skolplikt och har närvaroplikt i skolan (7 kap. 17 § skollagen [2010:800]). Ledighet kan endast beviljas för enskilda angelägenheter vid kortare frånvaro eller om det föreligger synnerliga skäl (7 kap. 18 § skollagen).

Efter en samlad bedömning av elevens studiesituation, frånvarons längd, tidpunkten för ledigheten och det uppgivna skälet har skolan beslutat att avslå ansökan. Enligt skollagens förarbeten (Prop. 2009/10:165) ska bestämmelserna om ledighet tillämpas restriktivt för att värna elevens rätt till utbildning.

Detta beslut kan inte överklagas (15 kap. skolförordningen [2011:185]).

Med vänlig hälsning,
Rektor / Skolledning"""

    st.code(beslutstext, language="text")
    st.caption("Klicka på kopieringsikonen i övre högra hörnet av textrutan ovan för att klistra in i skolsystemet.")
