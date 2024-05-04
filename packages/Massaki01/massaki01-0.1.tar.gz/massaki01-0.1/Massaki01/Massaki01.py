import streamlit as st
from types import FunctionType
#Ref colors: https://hexcolorpedia.com/color/?q=ffffff

def Versao():
    return "Massaki's language version 0.1"
def Indice():
    Configuracoes_de_Pagina = st.sidebar.popover("Configurações de Página")
    Configuracoes_de_Pagina.page_link("pages/Configurar_Pagina.py", label="	📄 Configurar_Pagina")
    Configuracoes_de_Pagina.page_link("pages/Barra_Lateral_Texto.py", label="⬜ Barra_Lateral_Texto")

    
#├──CONFIGURAÇÕES DE PÁGINA
#   └── Configurar_Pagina
#   └── Barra_Lateral_Texto
#   └── Barra_Lateral_Botao_M
#   └── Barra_Lateral_Botao_C
#   └── Barra_Lateral_Divisor
#   └── Divisor

def Configurar_Pagina(titulo  = "ACT - Soluções para Pessoas", layout="amplo", barra_lateral = "auto", ajuda = "https://docs.streamlit.io", bug = "mailto:informacoes.actsp@gmail.com",sobre="#### **ACT - Soluções para Pessoas**. Você pode usar formatação Markdown para adicionar informações neste espaço. Para mais informações acesse *https://www.markdownguide.org*", icone = "	©️"):
    #https://docs.streamlit.io/develop/concepts/architecture/app-chrome
    Configurar_Pagina.titulo = titulo    
    if layout == "amplo":
        Configurar_Pagina.layout = "wide"
    elif layout == "centralizado":
        Configurar_Pagina.layout = "centered"
    else:
        Configurar_Pagina.layout = "wide"
        
    Configurar_Pagina.barra_lateral = barra_lateral
    Configurar_Pagina.icone = icone
    st.set_page_config(page_title=titulo,                        
                        layout = Configurar_Pagina.layout,
                        initial_sidebar_state = barra_lateral,
                        menu_items={
                            'Get Help': (ajuda),
                            'Report a bug': (bug),
                            'About': (sobre)
                        },
                        page_icon=icone)

def Barra_Lateral_Texto(texto = "Texto exibido na Barra Lateral", estilo = "auto"):
    Barra_Lateral_Texto.texto = texto
    Barra_Lateral_Texto.estilo = estilo
    if estilo=="auto":
        st.sidebar.write(texto)
    elif estilo=="subcabecalho":
        st.sidebar.subheader(texto)
    elif estilo=="cabecalho":
        st.sidebar.header(texto)
    elif estilo=="titulo":
        st.sidebar.title(texto)
    elif estilo=="destaque1":
        st.sidebar.info(texto)          
    elif estilo=="destaque2":
        st.sidebar.warning(texto) 
    elif estilo=="destaque3":
        st.sidebar.success(texto)
    else:
        st.sidebar.write(texto)
  
def Barra_Lateral_Botao_M(texto):  
    Botao_M.rotulo = texto
    respBTNMonoL = st.sidebar.button(texto)
    return respBTNMonoL 

def Barra_Lateral_Botao_C(texto, cor = "#7e7b7b"):
    Botao_C.rotulo = texto
    Botao_C.cor = cor
    st.sidebar.markdown("""<style>  .element-container:has(style){display: none;} #button-afterL {display: none;}
                            .element-container:has(#button-afterL) {display: none;}
                            .element-container:has(#button-afterL) + div button {background-color: %s;font-weight: bolder; color:black;}
                </style>"""%(Botao_C.cor), unsafe_allow_html=True)
    st.sidebar.markdown('<span id="button-afterL"></span>', unsafe_allow_html=True)
    respBTNColorL = st.sidebar.button(texto)
    return respBTNColorL

def Barra_Lateral_Divisor():
    st.sidebar.divider()

def Colunas(ncol):
    return st.columns(ncol)
    
def Container(borda = True):
    return st.container(border = borda)
def Divisor():
    st.divider()

def Link(caminho, rotulo = "Link de Página"):
    Link.caminho = caminho
    Link.rotulo = rotulo
    st.page_link(caminho, label=rotulo)

def Mudar_Tema():
    #REF: https://discuss.streamlit.io/t/customize-theme/39156/4
    dark = '''
    <style>
        .stApp {
        background-color: black;  
        }
    </style>
    '''

    light = '''
    <style>
        .stApp {
        background-color: gray;
        }
    </style>
    '''
    st.markdown(light, unsafe_allow_html=True)

    # Create a toggle button
    toggle = st.button("Mudar Tema")

    # Use a global variable to store the current theme
    if "theme" not in st.session_state:
        st.session_state.theme = "light"

    # Change the theme based on the button state
    if toggle:
        if st.session_state.theme == "light":
            st.session_state.theme = "dark"
        else:
            st.session_state.theme = "light"

    # Apply the theme to the app
    if st.session_state.theme == "dark":
        st.markdown(dark, unsafe_allow_html=True)
    else:
        st.markdown(light, unsafe_allow_html=True)

    # Display some text
    st.write("This is a streamlit app with a toggle button for themes.")

#├──BOTÕES
#   └── Botao_M
#   └── Botao_C
def Botao_M(rotulo): 
    respBTNMono = st.button(rotulo)
    return respBTNMono
    
def Botao_C(rotulo, cor = "#7e7b7b"):
    Botao_C.cor = cor
    st.markdown("""<style>  .element-container:has(style){display: none;} #button-after {display: none;}
                            .element-container:has(#button-after) {display: none;}
                            .element-container:has(#button-after) + div button {background-color: %s;font-weight: bolder; color:black;}
                </style>"""%(Botao_C.cor), unsafe_allow_html=True)
    st.markdown('<span id="button-after"></span>', unsafe_allow_html=True)
    respBTNColor = st.button(rotulo)
    return respBTNColor

#├──RECURSOS
#   └── Escrever
#   └── Subcabecalho
#   └── Cabecalho
#   └── Texto_em_Coluna
#   └── Titulo

def Escrever(texto, estilo = "auto"):
    Escrever.texto = texto
    Escrever.estilo = estilo
    if estilo=="auto":
        st.write(texto)
    elif estilo =="codigo":
        st.code(texto)
    elif estilo=="subcabecalho":
        st.subheader(texto)
    elif estilo=="cabecalho":
        st.header(texto)
    elif estilo=="titulo":
        resp = st.title(texto)
    elif estilo=="destaque1":
        st.info(texto)          
    elif estilo=="destaque2":
        st.warning(texto) 
    elif estilo=="destaque3":
        st.success(texto)
    else:
        st.write(texto)
        
def Subcabecalho(texto):
    Subcabecalho.texto = texto
    st.subheader(texto)

def Cabecalho(texto):
    Cabecalho.texto = texto
    st.header(texto)
def MKD(texto, alinhamento = "left", tamanho_fonte = 48, cor_fonte = "black"):
    conteudo = '<p style="font-weight: bolder; color:%s; font-size: %spx;">%s</p>'%(cor_fonte, tamanho_fonte, texto)    
    st.markdown(conteudo, unsafe_allow_html=True)
    mystyle0 = '''<style> p{text-align:%s;}</style>'''%(alinhamento)
    st.markdown(mystyle0, unsafe_allow_html=True) 
def Texto_em_Colunas(TEXTO, estilo = "auto"):    
    ncol = len(TEXTO)
    if ncol>20:
        ncol = 20
    comando = []
    for c in range(ncol):
        label = TEXTO[c]
        if estilo=="auto":
            comando.append("st.write('%s')"%(label))
        elif estilo=="subcabecalho":
            comando.append("st.subheader('%s')"%(label))
        elif estilo=="cabecalho":
            comando.append("st.header('%s')"%(label))
        elif estilo=="titulo":
            comando.append("st.title('%s')"%(label)) 
        elif estilo=="destaque1":
            comando.append("st.info('%s')"%(label))           
        elif estilo=="destaque2":
            comando.append("st.warning('%s')"%(label))   
        elif estilo=="destaque3":
            comando.append("st.success('%s')"%(label)) 
        else:
            comando.append("st.write('%s')"%(label))
    colunas = st.columns(ncol) 
    for i in range(ncol):
        with colunas[i]:
            if i==0:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[0]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==1:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[1]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==2:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[2]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==3:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[3]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==4:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[4]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==5:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[5]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()           
            if i==6:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[6]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==7:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[7]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==8:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[8]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==9:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[9]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==10:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[10]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==11:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[11]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()  
            if i==12:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[12]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==13:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[13]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==14:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[14]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==15:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[15]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()           
            if i==16:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[16]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==17:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[17]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==18:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[18]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()
            if i==19:
                f_code = compile('''def FUNC(): 
                                        %s
                                '''%(comando[19]), "<int>", "exec") 
                f_func = FunctionType(f_code.co_consts[0], globals(), "FUNC")
                f_func()

def Titulo(texto):
    Titulo.texto = texto
    st.title(texto)
