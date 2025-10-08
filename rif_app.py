import streamlit as st
import pandas as pd
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="RIF Protocol Assistant",
    page_icon="🔬",
    layout="wide"
)

# Título e introdução
st.title("🔬 Protocolo de Conduta para Falhas Repetidas de Implantação (RIF)")
st.markdown("""
**Definição RIF**: Falha de implantação após ≥3 transferências de embriões de boa qualidade 
ou transferência de ≥10 embriões em múltiplos ciclos.

*Baseado em evidências atualizadas e guidelines internacionais (ESHRE 2023, ASRM 2024)*
""")

# Sidebar para dados do paciente
st.sidebar.header("📋 Dados da Paciente")
nome_paciente = st.sidebar.text_input("Nome da paciente", "")
idade = st.sidebar.number_input("Idade", 18, 50, 35)
num_falhas = st.sidebar.number_input("Número de falhas", 3, 20, 3)
imc = st.sidebar.number_input("IMC", 15.0, 50.0, 23.0)
tipo_embrioes = st.sidebar.selectbox("Tipo de embriões transferidos", 
                                      ["Blastocistos", "D3", "Ambos"])
qualidade_embrionaria = st.sidebar.selectbox("Qualidade embrionária", 
                                              ["Excelente (AA/AB)", "Boa (BA/BB)", "Regular"])

# Aviso de IMC
if imc < 18.5:
    st.sidebar.warning("⚠️ IMC abaixo do ideal. Considerar suporte nutricional.")
elif imc > 30:
    st.sidebar.warning("⚠️ IMC elevado. Redução de peso recomendada antes do ciclo.")

# Tabs principais
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🧬 Avaliação Genética", 
    "🦠 Fatores Infecciosos", 
    "🔥 Fatores Inflamatórios/Imunológicos",
    "🏥 Fatores Anatômicos",
    "📊 Análise Laboratorial",
    "📝 Protocolo Personalizado"
])

# Inicializar variáveis de recomendações
recomendacoes = []
alertas_criticos = []

# ==================== TAB 1: AVALIAÇÃO GENÉTICA ====================
with tab1:
    st.header("🧬 Avaliação Genética")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Testes Recomendados")
        
        cariótipo_casal = st.checkbox("Cariótipo do casal realizado")
        cariótipo_resultado = st.selectbox("Resultado do cariótipo", 
                                           ["Não aplicável", "Normal", "Alterado"])
        
        pgt_a = st.checkbox("PGT-A (Teste Genético Pré-implantacional)")
        pgt_a_resultado = st.selectbox("Resultado PGT-A", 
                                       ["Não aplicável", "Todos aneuploides", 
                                        "Maioria aneuploides", "Maioria euploides"])
        
        trombofilia = st.checkbox("Painel de Trombofilia Hereditária")
        hla = st.checkbox("Tipagem HLA (DQ-alpha)")
        
        st.info("""
        **Indicações PGT-A em RIF:**
        - Idade materna ≥37 anos
        - ≥2 falhas com embriões não testados
        - Histórico de aneuploidias
        - Alteração no cariótipo do casal
        
        **Ref**: ESHRE PGT Consortium 2023
        """)
        
        if idade >= 37 and not pgt_a:
            recomendacoes.append("PGT-A: Fortemente recomendado devido à idade materna ≥37 anos")
        
        if pgt_a_resultado in ["Todos aneuploides", "Maioria aneuploides"]:
            alertas_criticos.append("Alta taxa de aneuploidias - investigar causas e considerar uso de DHEA/CoQ10")
    
    with col2:
        st.subheader("Mutações de Trombofilia")
        
        fator_v = st.selectbox("Fator V Leiden", 
                               ["Não testado", "Normal", "Heterozigoto", "Homozigoto"])
        protrombina = st.selectbox("Mutação Protrombina G20210A", 
                                   ["Não testado", "Normal", "Heterozigoto", "Homozigoto"])
        mthfr = st.selectbox("MTHFR C677T", 
                            ["Não testado", "Normal", "Heterozigoto", "Homozigoto"])
        
        pai_ii = st.selectbox("PAI-1 4G/5G", 
                              ["Não testado", "5G/5G", "4G/5G", "4G/4G"])
        
        # Avaliar trombofilia
        trombofilia_presente = False
        if fator_v in ["Heterozigoto", "Homozigoto"]:
            trombofilia_presente = True
            st.error("🔴 **Fator V Leiden detectado**")
        if protrombina in ["Heterozigoto", "Homozigoto"]:
            trombofilia_presente = True
            st.error("🔴 **Mutação Protrombina G20210A detectada**")
        if mthfr == "Homozigoto":
            st.warning("⚠️ **MTHFR homozigoto** - suplementar ácido fólico (metilfolato)")
        
        if trombofilia_presente:
            st.markdown("""
            ### 💊 **Protocolo de Anticoagulação**
            
            **Pré-transferência:**
            - AAS 100mg/dia (iniciar com preparo endometrial)
            
            **Pós-transferência:**
            - Enoxaparina 40mg/dia SC (iniciar no dia da transferência)
            - Manter até 12 semanas de gestação
            - AAS 100mg/dia (manter até 34-36 semanas se gestação)
            
            **Suplementação:**
            - Ácido fólico 5mg/dia (ou metilfolato se MTHFR+)
            
            **Ref**: ACOG Practice Bulletin 2023
            """)
            recomendacoes.append("Anticoagulação profilática: Enoxaparina 40mg/dia + AAS 100mg/dia")
            alertas_criticos.append("TROMBOFILIA DETECTADA - Anticoagulação obrigatória")
        
        st.subheader("Compatibilidade HLA")
        if hla:
            hla_compartilhado = st.number_input("Alelos HLA-DQ compartilhados", 0, 4, 0)
            if hla_compartilhado >= 2:
                st.warning("⚠️ Alta compatibilidade HLA pode afetar tolerância imunológica")
                recomendacoes.append("Considerar imunoterapia (controverso - discutir com especialista)")

# ==================== TAB 2: FATORES INFECCIOSOS ====================
with tab2:
    st.header("🦠 Avaliação de Fatores Infecciosos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Endometrite Crônica")
        
        st.info("""
        **Prevalência em RIF**: 14-30%
        
        **Gold Standard**: Biópsia endometrial com CD138+ (>5 células/campo)
        
        **Ref**: Cicinelli et al., Fertility & Sterility 2023
        """)
        
        histeroscopia = st.selectbox("Histeroscopia diagnóstica", 
                                     ["Não realizada", "Normal", "Micropolipos", 
                                      "Hiperemia focal", "Edema estromal"])
        biopsia_endometrial = st.selectbox("Biópsia endometrial com CD138", 
                                           ["Não realizada", "Negativa (<5 células)", 
                                            "Positiva (5-10 células)", "Positiva (>10 células)"])
        
        endometrite_detectada = False
        if biopsia_endometrial in ["Positiva (5-10 células)", "Positiva (>10 células)"]:
            endometrite_detectada = True
            st.error("🔴 **ENDOMETRITE CRÔNICA CONFIRMADA**")
            
            st.markdown("""
            ### 💊 **Protocolo de Tratamento Completo**
            
            #### **Fase 1: Antibioticoterapia (14 dias)**
            - **Doxiciclina 100mg** 12/12h (ou Azitromicina 500mg/dia se contraindicação)
            - **Metronidazol 400mg** 8/8h (ou 500mg 12/12h)
            - **Ciprofloxacino 500mg** 12/12h (se cultura positiva para gram-negativos)
            
            #### **Fase 2: Probióticos (30 dias)**
            - **Lactobacilos vaginais** 1 cápsula/dia via vaginal
            - Iniciar após fim dos antibióticos
            
            #### **Fase 3: Controle (30-60 dias após tratamento)**
            - Repetir histeroscopia + biópsia com CD138
            - Taxa de cura: 70-90% no primeiro ciclo
            - Se persistir: repetir antibióticos por 21 dias
            
            #### **Antes do próximo ciclo:**
            - Aguardar pelo menos 1 ciclo menstrual após fim do tratamento
            - Confirmar cura com nova biópsia
            
            **Ref**: Kitaya et al., Reproductive Medicine 2024
            """)
            
            alertas_criticos.append("ENDOMETRITE CRÔNICA - Tratamento obrigatório antes de novo ciclo")
            recomendacoes.append("Antibioticoterapia completa + repetir biópsia antes de transferência")
        
        elif histeroscopia in ["Micropolipos", "Hiperemia focal", "Edema estromal"]:
            st.warning("⚠️ Achados sugestivos de endometrite - Biópsia com CD138 é mandatória")
            recomendacoes.append("Realizar biópsia endometrial com imuno-histoquímica CD138")
    
    with col2:
        st.subheader("Infecções Genitais")
        
        ureaplasma = st.selectbox("Ureaplasma urealyticum", 
                                  ["Não testado", "Negativo", "Positivo"])
        mycoplasma = st.selectbox("Mycoplasma hominis", 
                                  ["Não testado", "Negativo", "Positivo"])
        chlamydia = st.selectbox("Chlamydia trachomatis (PCR)", 
                                 ["Não testado", "Negativo", "Positivo"])
        
        tratamento_necessario = []
        
        if ureaplasma == "Positivo":
            tratamento_necessario.append("Ureaplasma")
            st.warning("⚠️ Ureaplasma detectado")
        if mycoplasma == "Positivo":
            tratamento_necessario.append("Mycoplasma")
            st.warning("⚠️ Mycoplasma detectado")
        if chlamydia == "Positivo":
            tratamento_necessario.append("Chlamydia")
            st.error("🔴 Chlamydia detectada")
        
        if len(tratamento_necessario) > 0:
            st.markdown(f"""
            ### 💊 **Tratamento para: {', '.join(tratamento_necessario)}**
            
            **Casal (ambos devem tratar):**
            - **Azitromicina 1g** dose única, repetir após 7 dias
            - OU **Doxiciclina 100mg** 12/12h por 14 dias
            
            **Se Chlamydia:**
            - **Azitromicina 1g** dose única (preferencial)
            - OU **Doxiciclina 100mg** 12/12h por 21 dias
            
            **Teste de cura:** 30 dias após término
            
            **Abstinência sexual** ou uso de preservativo durante tratamento
            """)
            alertas_criticos.append(f"Infecção detectada: {', '.join(tratamento_necessario)} - Tratar casal")
            recomendacoes.append("Tratamento antimicrobiano completo + teste de cura")
        
        st.subheader("Outras Avaliações")
        
        cultura_endometrial = st.selectbox("Cultura endometrial", 
                                           ["Não realizada", "Negativa", "Positiva"])
        if cultura_endometrial == "Positiva":
            germe = st.text_input("Germe isolado:")
            if germe:
                st.warning(f"Germe detectado: {germe} - Antibioticoterapia conforme antibiograma")
        
        microbioma = st.selectbox("Análise de microbioma endometrial (ALICE/EMMA)", 
                                  ["Não realizada", "Lactobacillus >90%", 
                                   "Lactobacillus 50-90%", "Lactobacillus <50%"])
        if microbioma == "Lactobacillus <50%":
            st.warning("⚠️ Disbiose endometrial - Considerar probióticos + antibióticos")
            recomendacoes.append("Probióticos vaginais (Lactobacillus) por 30-60 dias")

# ==================== TAB 3: FATORES IMUNOLÓGICOS ====================
with tab3:
    st.header("🔥 Avaliação Imunológica e Inflamatória")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Síndrome Antifosfolípide (SAF)")
        
        st.info("""
        **Critérios diagnósticos** (2 testes positivos com ≥12 semanas intervalo):
        - Anticardiolipina IgG/IgM >40 GPL/MPL
        - Anti-β2GP1 IgG/IgM >40 U/mL
        - Anticoagulante lúpico positivo
        
        **Ref**: Sydney Criteria 2024
        """)
        
        anticardiolipina_igg = st.number_input("Anticardiolipina IgG (GPL)", 0.0, 200.0, 0.0)
        anticardiolipina_igm = st.number_input("Anticardiolipina IgM (MPL)", 0.0, 200.0, 0.0)
        anticoagulante_lupico = st.selectbox("Anticoagulante Lúpico", 
                                             ["Não testado", "Negativo", "Positivo"])
        anti_b2gp1_igg = st.number_input("Anti-β2-glicoproteína I IgG (U/mL)", 0.0, 200.0, 0.0)
        anti_b2gp1_igm = st.number_input("Anti-β2-glicoproteína I IgM (U/mL)", 0.0, 200.0, 0.0)
        
        # Avaliar critérios SAF
        saf_criteria = []
        if anticardiolipina_igg > 40:
            saf_criteria.append("Anticardiolipina IgG >40")
        if anticardiolipina_igm > 40:
            saf_criteria.append("Anticardiolipina IgM >40")
        if anticoagulante_lupico == "Positivo":
            saf_criteria.append("Anticoagulante lúpico positivo")
        if anti_b2gp1_igg > 40:
            saf_criteria.append("Anti-β2GP1 IgG >40")
        if anti_b2gp1_igm > 40:
            saf_criteria.append("Anti-β2GP1 IgM >40")
        
        if len(saf_criteria) > 0:
            st.error(f"🔴 **CRITÉRIOS PARA SAF PRESENTES** ({len(saf_criteria)} critérios)")
            for criterio in saf_criteria:
                st.markdown(f"- {criterio}")
            
            st.markdown("""
            ### 💊 **Protocolo SAF em RIF**
            
            #### **Esquema completo:**
            1. **AAS 100mg/dia** (iniciar com preparo endometrial)
            2. **Enoxaparina 40mg/dia SC** (iniciar na transferência)
            3. **Hidroxicloroquina 400mg/dia** (considerar 2 meses antes)
            4. **Prednisona 5-10mg/dia** (se múltiplos critérios)
            
            #### **Seguimento:**
            - Repetir sorologias em 12 semanas
            - Manter anticoagulação até 6 semanas pós-parto se gestação
            - Encaminhar para reumatologista
            
            **Ref**: ASRM Committee Opinion 2024
            """)
            alertas_criticos.append("SÍNDROME ANTIFOSFOLÍPIDE - Anticoagulação + hidroxicloroquina")
            recomendacoes.append("Protocolo SAF: AAS + Enoxaparina + Hidroxicloroquina")
        
        # Outros autoanticorpos
        st.subheader("Outros Autoanticorpos")
        fan = st.selectbox("FAN (Fator Antinuclear)", 
                          ["Não testado", "Negativo", "1:80", "1:160", "1:320", ">1:320"])
        anti_dna = st.selectbox("Anti-DNA dupla hélice", ["Não testado", "Negativo", "Positivo"])
        
        if fan in ["1:160", "1:320", ">1:320"] or anti_dna == "Positivo":
            st.warning("⚠️ Marcadores de autoimunidade - Avaliar com reumatologista")
            recomendacoes.append("Avaliação reumatológica - possível doença autoimune sistêmica")
    
    with col2:
        st.subheader("Células NK (Natural Killer)")
        
        st.info("""
        **Controvérsia:** Tratamento de NK elevadas é controverso.
        
        **Valores de referência:**
        - NK periféricas: <12-18%
        - NK endometriais (CD56+): <5%
        
        **Evidências limitadas para tratamento**
        
        **Ref**: ESHRE Guideline 2023 - Não recomenda rotineiramente
        """)
        
        nk_cells = st.number_input("Células NK periféricas (CD56+CD16+) %", 0.0, 50.0, 12.0)
        nk_endometrial = st.selectbox("NK endometriais (CD56+)", 
                                      ["Não testado", "Normal (<5%)", 
                                       "Levemente elevado (5-10%)", 
                                       "Moderadamente elevado (10-15%)", 
                                       "Muito elevado (>15%)"])
        
        nk_elevado = False
        if nk_cells > 18:
            nk_elevado = True
            st.warning(f"⚠️ **Células NK periféricas elevadas: {nk_cells}%**")
        
        if nk_endometrial in ["Moderadamente elevado (10-15%)", "Muito elevado (>15%)"]:
            nk_elevado = True
            st.warning(f"⚠️ **Células NK endometriais elevadas: {nk_endometrial}**")
        
        if nk_elevado:
            st.markdown("""
            ### ⚠️ **Opções terapêuticas (CONTROVERSO)**
            
            **AVISO**: Evidências limitadas. Discutir riscos/benefícios.
            
            #### **Opções (em ordem de evidência):**
            
            1. **Corticoides** (mais utilizado)
               - Prednisona 5-10mg/dia
               - Iniciar 7 dias antes da transferência
               - Manter até 12 semanas se gestação
               - ⚠️ Risco: diabetes gestacional, hipertensão
            
            2. **Intralipid 20%**
               - 100mL IV em 2h
               - Antes da transferência e repetir mensalmente
               - ⚠️ Evidências fracas
            
            3. **Imunoglobulina IV (IVIG)**
               - 400mg/kg
               - ⚠️ Caro, evidências limitadas, não recomendado ESHRE
            
            4. **Hidroxicloroquina 400mg/dia**
               - Iniciar 2 meses antes
               - Possível efeito imunomodulador
            
            **NÃO RECOMENDADO pela ESHRE/ASRM sem evidências robustas**
            
            **Considerar apenas em casos selecionados com falhas múltiplas**
            """)
            recomendacoes.append("NK elevadas: Discutir prednisona (controverso) - Considerar apenas após múltiplas falhas")
        
        st.subheader("Função Tireoidiana")
        tsh = st.number_input("TSH (mUI/L)", 0.0, 10.0, 2.5)
        t4_livre = st.number_input("T4 livre (ng/dL)", 0.0, 3.0, 1.0)
        anti_tpo = st.selectbox("Anti-TPO (antitireoperoxidase)", 
                                ["Não testado", "Negativo (<35)", "Positivo (35-100)", "Muito elevado (>100)"])
        anti_tg = st.selectbox("Anti-tireoglobulina", ["Não testado", "Negativo", "Positivo"])
        
        problema_tireoide = False
        if tsh > 2.5:
            problema_tireoide = True
            st.warning(f"⚠️ **TSH elevado: {tsh} mUI/L** (alvo <2.5 para FIV)")
        if tsh < 0.5:
            problema_tireoide = True
            st.warning(f"⚠️ **TSH suprimido: {tsh} mUI/L**")
        if anti_tpo in ["Positivo (35-100)", "Muito elevado (>100)"]:
            problema_tireoide = True
            st.warning("⚠️ **Anti-TPO positivo** - Tireoidite autoimune")
        
        if problema_tireoide:
            st.markdown("""
            ### 💊 **Otimização Tireoidiana**
            
            **Meta para FIV:**
            - TSH entre 0.5-2.5 mUI/L (ideal <2.0)
            - T4 livre na metade superior da normalidade
            
            **Tratamento:**
            - **Levotiroxina** (ajustar dose para atingir meta)
            - Controle de TSH a cada 4-6 semanas
            - Se anti-TPO+: monitorar mais de perto
            - Considerar Selênio 200mcg/dia se autoimunidade
            
            **Encaminhar para endocrinologista**
            
            **Ref**: ATA Guidelines 2024
            """)
            alertas_criticos.append("Disfunção tireoidiana - Otimizar antes do ciclo (TSH <2.5)")
            recomendacoes.append("Otimização tireoidiana: TSH alvo <2.5 mUI/L antes da transferência")

# ==================== TAB 4: FATORES ANATÔMICOS ====================
with tab4:
    st.header("🏥 Avaliação Anatômica e Receptividade Endometrial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Exames de Imagem Realizados")
        
        ultrassom = st.checkbox("Ultrassom transvaginal 3D")
        histeroscopia_realizada = st.checkbox("Histeroscopia diagnóstica")
        histerossalpingografia = st.checkbox("Histerossalpingografia")
        ressonancia = st.checkbox("Ressonância magnética pélvica")
        
        st.subheader("Alterações Anatômicas Detectadas")
        
        alteracoes = st.multiselect(
            "Selecione todas as alterações encontradas:",
            ["Nenhuma alteração",
             "Pólipo endometrial",
             "Pólipo endocervical",
             "Mioma submucoso (FIGO 0-1-2)",
             "Mioma intramural >4cm próximo ao endométrio",
             "Mioma intramural >4cm distante do endométrio",
             "Septo uterino",
             "Útero bicorno",
             "Sinéquia uterina (Asherman)",
             "Adenomiose focal",
             "Adenomiose difusa",
             "Hidrossalpinge unilateral",
             "Hidrossalpinge bilateral",
             "Endometrioma ovariano",
             "Endometriose profunda",
             "Espessamento endometrial irregular"]
        )
        
        # Avaliar cada alteração
        cirurgia_necessaria = []
        tratamento_clinico = []
        
        for alt in alteracoes:
            if alt == "Pólipo endometrial":
                cirurgia_necessaria.append("Polipectomia histeroscópica")
                st.error("🔴 **Pólipo endometrial** - Polipectomia mandatória")
                st.markdown("""
                - Remover antes do próximo ciclo
                - Aguardar 1-2 ciclos menstruais após procedimento
                - Taxa de gestação aumenta 10-15% após remoção
                """)
            
            elif alt == "Mioma submucoso (FIGO 0-1-2)":
                cirurgia_necessaria.append("Miomectomia histeroscópica")
                st.error("🔴 **Mioma submucoso** - Miomectomia mandatória")
                st.markdown("""
                - FIGO 0-1-2: Impacto significativo na implantação
                - Remoção histeroscópica
                - Aguardar 2-3 ciclos após procedimento
                """)
            
            elif alt == "Mioma intramural >4cm próximo ao endométrio":
                cirurgia_necessaria.append("Miomectomia laparoscópica/aberta")
                st.warning("⚠️ **Mioma intramural grande** - Considerar miomectomia")
                st.markdown("""
                - Se >4cm e distorce cavidade: remover
                - Aguardar 3-6 meses após cirurgia
                - Avaliar risco cirúrgico vs. benefício
                """)
            
            elif alt == "Septo uterino":
                cirurgia_necessaria.append("Septoplastia histeroscópica")
                st.error("🔴 **Septo uterino** - Septoplastia recomendada")
                st.markdown("""
                - Septoplastia histeroscópica
                - Melhora taxa de implantação
                - Aguardar 2 ciclos após procedimento
                """)
            
            elif alt == "Sinéquia uterina (Asherman)":
                cirurgia_necessaria.append("Lise de sinéquias histeroscópica")
                st.error("🔴 **Síndrome de Asherman** - Lise de sinéquias")
                st.markdown("""
                - Histeroscopia operatória
                - Estradiol alta dose após (2-3 meses)
                - Pode necessitar múltiplos procedimentos
                - Considerar balão intrauterino
                """)
            
            elif "Hidrossalpinge" in alt:
                cirurgia_necessaria.append("Salpingectomia laparoscópica")
                st.error("🔴 **HIDROSSALPINGE** - Salpingectomia obrigatória")
                st.markdown("""
                **CRÍTICO**: Reduz taxa de implantação em 50%!
                
                - Salpingectomia laparoscópica bilateral se bilateral
                - Fluido tóxico para embriões
                - OBRIGATÓRIO remover antes de FIV
                - Aguardar 1-2 meses após cirurgia
                
                **Ref**: ASRM - Salpingectomia aumenta taxa de gestação em 2x
                """)
                alertas_criticos.append("HIDROSSALPINGE - Salpingectomia OBRIGATÓRIA antes do ciclo")
            
            elif "Adenomiose" in alt:
                tratamento_clinico.append("Análogo GnRH pré-tratamento")
                st.warning("⚠️ **Adenomiose** - Considerar pré-tratamento")
                st.markdown("""
                **Protocolo para adenomiose:**
                - Análogo GnRH (Leuprolide) por 2-3 meses antes da transferência
                - OU Dienogest 2mg/dia por 2-3 meses
                - Melhora receptividade endometrial
                - Reduz inflamação local
                
                **Ref**: Cochrane Review 2024
                """)
            
            elif "Endometriose" in alt or "Endometrioma" in alt:
                st.warning("⚠️ **Endometriose** - Avaliar necessidade de tratamento")
                st.markdown("""
                **Conduta:**
                - Endometrioma <3cm: não drenar (piora reserva ovariana)
                - Endometrioma >4cm com sintomas: considerar cistectomia
                - Endometriose profunda: tratar cirurgicamente se sintomática
                - Considerar GnRH análogo 2-3 meses pré-FIV
                """)
        
        # Resumo de cirurgias necessárias
        if len(cirurgia_necessaria) > 0:
            st.error("### 🔪 **CIRURGIAS NECESSÁRIAS ANTES DO PRÓXIMO CICLO:**")
            for cirurgia in cirurgia_necessaria:
                st.markdown(f"- {cirurgia}")
                recomendacoes.append(f"Cirurgia: {cirurgia}")
        
        if len(tratamento_clinico) > 0:
            st.warning("### 💊 **TRATAMENTO CLÍNICO RECOMENDADO:**")
            for tratamento in tratamento_clinico:
                st.markdown(f"- {tratamento}")
                recomendacoes.append(f"Tratamento: {tratamento}")
    
    with col2:
        st.subheader("Avaliação Endometrial")
        
        espessura_endometrial = st.number_input("Espessura endometrial máxima (mm)", 
                                                0.0, 20.0, 9.0, step=0.5)
        padrao_endometrial = st.selectbox("Padrão endometrial no ultrassom", 
                                          ["Trilaminar (ideal)", "Homogêneo", "Irregular/heterogêneo"])
        fluxo_endometrial = st.selectbox("Fluxo sanguíneo endometrial (Doppler)", 
                                         ["Não avaliado", "Adequado", "Reduzido"])
        
        # Avaliar espessura endometrial
        if espessura_endometrial < 7:
            st.error(f"🔴 **Endométrio fino: {espessura_endometrial}mm** (ideal ≥7mm)")
            st.markdown("""
            ### 💊 **Protocolo para Endométrio Fino**
            
            #### **Linha 1: Otimização hormonal**
            - Estradiol oral: aumentar dose (6-8mg/dia)
            - Estradiol vaginal adicional: 2mg 12/12h
            - Estradiol transdérmico: adicionar 100-200mcg patches
            
            #### **Linha 2: Suplementos**
            - **Vitamina E** 800 UI/dia (antioxidante)
            - **L-arginina** 6g/dia (vasodilatador)
            - **Pentoxifilina** 800mg/dia (melhora fluxo)
            - **AAS** 100mg/dia (antiagregante)
            - **Vitamina C** 1g/dia
            
            #### **Linha 3: Terapias adjuvantes**
            - **Sildenafil vaginal** 25mg 6/6h (controverso)
            - **G-CSF intrauterino** (Filgrastim) - em estudo
            - **Scratching endometrial** (controverso)
            
            #### **Considerar:**
            - Descartar sinéquias (histeroscopia)
            - Avaliar fluxo uterino (Doppler)
            - Ciclo natural se possível
            
            **Ref**: Fertility & Sterility 2024
            """)
            alertas_criticos.append("Endométrio fino - Protocolo de otimização necessário")
            recomendacoes.append("Endométrio fino: Aumentar estradiol + suplementos vasodilatadores")
        
        elif espessura_endometrial >= 7 and espessura_endometrial < 9:
            st.warning(f"⚠️ **Endométrio limítrofe: {espessura_endometrial}mm** (ideal ≥9mm)")
            st.markdown("- Considerar otimização com estradiol vaginal adicional")
            recomendacoes.append("Endométrio limítrofe: Adicionar estradiol vaginal")
        
        else:
            st.success(f"✅ **Endométrio adequado: {espessura_endometrial}mm**")
        
        if padrao_endometrial == "Irregular/heterogêneo":
            st.warning("⚠️ Padrão endometrial irregular - Investigar pólipos, sinéquias ou endometrite")
        
        st.subheader("Janela de Implantação")
        
        era_test = st.selectbox("ERA Test (Endometrial Receptivity Array)", 
                                ["Não realizado", "Receptivo", "Pré-receptivo", "Pós-receptivo"])
        
        st.info("""
        **ERA Test**: Análise molecular da janela de implantação
        
        **Indicação em RIF:**
        - ≥3 falhas com embriões euploides
        - Endométrio aparentemente normal
        - Considerar se disponível
        
        **Custo-efetividade**: Controverso
        
        **Ref**: Fertility & Sterility 2023
        """)
        
        if era_test == "Pré-receptivo":
            st.error("🔴 **Janela de implantação DESLOCADA: Pré-receptivo**")
            st.markdown("""
            ### ⏰ **Ajuste de Timing**
            
            - Endométrio ainda não está receptivo
            - **Transferir 12-24h MAIS TARDE**
            - Aumentar tempo de progesterona antes da transferência
            - Exemplo: Se P+5 → fazer P+6
            
            **Melhora taxa de implantação em 20-25%**
            """)
            alertas_criticos.append("ERA: Janela pré-receptiva - Transferir 12-24h mais tarde")
            recomendacoes.append("ERA Test: Ajustar timing da transferência (+12-24h)")
        
        elif era_test == "Pós-receptivo":
            st.error("🔴 **Janela de implantação DESLOCADA: Pós-receptivo**")
            st.markdown("""
            ### ⏰ **Ajuste de Timing**
            
            - Endométrio já passou do período ideal
            - **Transferir 12-24h MAIS CEDO**
            - Reduzir tempo de progesterona antes da transferência
            - Exemplo: Se P+5 → fazer P+4
            
            **Melhora taxa de implantação em 20-25%**
            """)
            alertas_criticos.append("ERA: Janela pós-receptiva - Transferir 12-24h mais cedo")
            recomendacoes.append("ERA Test: Ajustar timing da transferência (-12-24h)")
        
        elif era_test == "Receptivo":
            st.success("✅ **Janela de implantação normal** - Manter protocolo atual")

# ==================== TAB 5: ANÁLISE LABORATORIAL ====================
with tab5:
    st.header("📊 Análise Laboratorial Complementar")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Perfil Hormonal")
        
        vitamina_d = st.number_input("Vitamina D (ng/mL)", 0.0, 100.0, 30.0)
        prolactina = st.number_input("Prolactina (ng/mL)", 0.0, 100.0, 15.0)
        progesterona = st.number_input("Progesterona fase lútea (ng/mL)", 0.0, 50.0, 10.0)
        estradiol = st.number_input("Estradiol (pg/mL)", 0, 500, 200)
        
        if vitamina_d < 20:
            st.error(f"🔴 **Deficiência de Vitamina D: {vitamina_d} ng/mL**")
            st.markdown("- **Suplementar 4000-6000 UI/dia** até atingir >30 ng/mL")
            recomendacoes.append(f"Vitamina D baixa ({vitamina_d}): Suplementar 4000-6000 UI/dia")
        elif vitamina_d < 30:
            st.warning(f"⚠️ **Vitamina D insuficiente: {vitamina_d} ng/mL**")
            st.markdown("- **Suplementar 2000-4000 UI/dia** (alvo >30 ng/mL)")
            recomendacoes.append(f"Vitamina D insuficiente ({vitamina_d}): Suplementar 2000-4000 UI/dia")
        else:
            st.success(f"✅ Vitamina D adequada: {vitamina_d} ng/mL")
        
        if prolactina > 25:
            st.warning(f"⚠️ **Hiperprolactinemia: {prolactina} ng/mL**")
            st.markdown("""
            - Investigar causas (prolactinoma, medicamentos)
            - Considerar **Cabergolina** 0.25-0.5mg 2x/semana
            - RM de sela túrcica se >100 ng/mL
            """)
            alertas_criticos.append("Hiperprolactinemia - Investigar e tratar antes do ciclo")
            recomendacoes.append("Hiperprolactinemia: Cabergolina + investigação")
        
        if progesterona < 10:
            st.warning(f"⚠️ Progesterona baixa: {progesterona} ng/mL")
            st.markdown("- Considerar aumentar suporte de progesterona")
            recomendacoes.append("Suporte de progesterona: Considerar dose mais alta ou via adicional")
    
    with col2:
        st.subheader("Perfil Metabólico")
        
        glicemia = st.number_input("Glicemia de jejum (mg/dL)", 0, 200, 90)
        hba1c = st.number_input("Hemoglobina glicada (%)", 0.0, 15.0, 5.5)
        insulina = st.number_input("Insulina de jejum (µU/mL)", 0.0, 50.0, 10.0)
        
        # Calcular HOMA-IR
        if glicemia > 0 and insulina > 0:
            homa_ir = (glicemia * insulina) / 405
            st.metric("HOMA-IR (Resistência Insulínica)", f"{homa_ir:.2f}")
            
            if homa_ir > 2.5:
                st.error(f"🔴 **Resistência insulínica presente** (HOMA-IR: {homa_ir:.2f})")
                st.markdown("""
                ### 💊 **Protocolo para Resistência Insulínica**
                
                - **Metformina 1500-2000mg/dia** (dividido em 2-3 doses)
                - Iniciar pelo menos 2 meses antes do ciclo
                - Dieta baixo índice glicêmico
                - Exercício físico regular
                - Myo-inositol 2g + D-chiro-inositol 50mg 2x/dia
                
                **Melhora qualidade oocitária e taxa de implantação**
                """)
                alertas_criticos.append("Resistência insulínica - Metformina + modificação estilo de vida")
                recomendacoes.append("Resistência insulínica: Metformina 1500-2000mg/dia + inositol")
            elif homa_ir > 1.9:
                st.warning(f"⚠️ Resistência insulínica limítrofe (HOMA-IR: {homa_ir:.2f})")
                recomendacoes.append("HOMA-IR limítrofe: Considerar metformina + inositol")
        
        if glicemia >= 100 and glicemia < 126:
            st.warning("⚠️ Glicemia de jejum alterada (pré-diabetes)")
        elif glicemia >= 126:
            st.error("🔴 Diabetes - Encaminhar para endocrinologista")
            alertas_criticos.append("DIABETES - Controle glicêmico obrigatório antes do ciclo")
        
        if hba1c >= 5.7 and hba1c < 6.5:
            st.warning("⚠️ HbA1c elevada (pré-diabetes)")
        elif hba1c >= 6.5:
            st.error("🔴 HbA1c compatível com diabetes")
    
    with col3:
        st.subheader("Marcadores Inflamatórios")
        
        pcr = st.number_input("Proteína C Reativa (mg/L)", 0.0, 50.0, 3.0)
        vhs = st.number_input("VHS (mm/h)", 0, 100, 10)
        homocisteina = st.number_input("Homocisteína (µmol/L)", 0.0, 50.0, 10.0)
        
        if pcr > 10:
            st.error(f"🔴 **PCR muito elevada: {pcr} mg/L** - Processo inflamatório ativo")
            st.markdown("- Investigar foco infeccioso/inflamatório antes do ciclo")
            alertas_criticos.append("PCR elevada - Investigar processo inflamatório antes do ciclo")
        elif pcr > 3:
            st.warning(f"⚠️ PCR elevada: {pcr} mg/L")
            recomendacoes.append("PCR elevada: Investigar causas de inflamação")
        
        if homocisteina > 15:
            st.warning(f"⚠️ **Homocisteína elevada: {homocisteina} µmol/L**")
            st.markdown("""
            - **Ácido fólico 5mg/dia** (ou metilfolato)
            - **Vitamina B12** 1000mcg/dia
            - **Vitamina B6** 50mg/dia
            - Reavaliar em 2-3 meses
            """)
            recomendacoes.append("Homocisteína elevada: Vitaminas B (folato, B12, B6)")
        
        st.subheader("Estresse Oxidativo")
        
        considerar_antioxidantes = st.checkbox("Considerar suplementação antioxidante")
        
        if considerar_antioxidantes or idade >= 37:
            st.info("""
            ### 🍊 **Protocolo Antioxidante**
            
            **Especialmente recomendado se:**
            - Idade ≥37 anos
            - Má qualidade embrionária prévia
            - Baixa reserva ovariana
            - Histórico de aneuploidias
            
            **Suplementos (iniciar 2-3 meses antes):**
            - **CoQ10** 200-600mg/dia
            - **Melatonina** 3mg antes de dormir
            - **DHEA** 25-75mg/dia (se indicado)
            - **Ômega-3** 1-2g/dia
            - **Resveratrol** 500mg/dia
            - **Vitamina E** 400-800 UI/dia
            - **Vitamina C** 1000mg/dia
            - **NAC** 600mg 2x/dia
            
            **Ref**: Fertility & Sterility 2024
            """)
            if idade >= 37:
                recomendacoes.append("Idade ≥37 anos: Protocolo antioxidante completo (CoQ10, melatonina, DHEA)")

    # Seção adicional: Perfil Espermático
    st.subheader("📊 Avaliação do Fator Masculino")
    
    col1, col2 = st.columns(2)
    
    with col1:
        espermograma = st.selectbox("Espermograma", 
                                    ["Não realizado", "Normal (OMS 2021)", 
                                     "Oligozoospermia leve", "Oligozoospermia moderada/grave",
                                     "Astenozoospermia", "Teratozoospermia", 
                                     "Oligoastenoteratozoospermia"])
        
        fragmentacao_dna = st.selectbox("Fragmentação de DNA espermático", 
                                        ["Não realizado", "<15% (excelente)", 
                                         "15-25% (bom)", "25-30% (limítrofe)", ">30% (alto)"])
        
        if fragmentacao_dna in ["25-30% (limítrofe)", ">30% (alto)"]:
            st.error("🔴 **Fragmentação de DNA espermático elevada**")
            st.markdown("""
            ### 💊 **Protocolo para Fragmentação DNA**
            
            **Parceiro masculino:**
            - **Antioxidantes** por 3 meses:
              - Vitamina C 1000mg/dia
              - Vitamina E 400 UI/dia
              - Zinco 30mg/dia
              - Selênio 200mcg/dia
              - CoQ10 200mg/dia
              - L-carnitina 2g/dia
            - Evitar calor excessivo (saunas, laptops)
            - Reduzir tabagismo/álcool
            - Exercício moderado
            
            **Técnicas laboratoriais:**
            - Seleção espermática avançada (MACS, PICSI)
            - Uso de espermatozoides testiculares (TESE) em casos graves
            - ICSI obrigatório
            
            **Ref**: Andrology 2024
            """)
            alertas_criticos.append("Fragmentação DNA espermático elevada - Antioxidantes 3 meses")
            recomendacoes.append("Fator masculino: Antioxidantes + técnicas de seleção espermática avançada")
    
    with col2:
        if espermograma != "Não realizado" and espermograma != "Normal (OMS 2021)":
            st.warning(f"⚠️ Alteração espermática: {espermograma}")
            st.markdown("""
            **Avaliações adicionais recomendadas:**
            - Fragmentação de DNA espermático
            - Avaliação hormonal masculina (testosterona, FSH, LH)
            - Ultrassom de bolsa escrotal
            - Avaliação urológica
            """)
            recomendacoes.append("Espermograma alterado: Avaliação urológica completa")

# ==================== TAB 6: PROTOCOLO PERSONALIZADO ====================
with tab6:
    st.header("📝 Protocolo Personalizado para o Próximo Ciclo")
    
    st.markdown(f"""
    ## Resumo do Caso
    
    **Paciente**: {nome_paciente if nome_paciente else "Não informado"}  
    **Idade**: {idade} anos  
    **Número de falhas**: {num_falhas}  
    **IMC**: {imc:.1f} kg/m²  
    **Tipo de embriões**: {tipo_embrioes}  
    **Qualidade**: {qualidade_embrionaria}  
    """)
    
    # ALERTAS CRÍTICOS
    if len(alertas_criticos) > 0:
        st.error("## 🚨 ALERTAS CRÍTICOS - AÇÃO OBRIGATÓRIA")
        for i, alerta in enumerate(alertas_criticos, 1):
            st.markdown(f"**{i}.** {alerta}")
        st.markdown("---")
    
    # RECOMENDAÇÕES PRIORITÁRIAS
    if len(recomendacoes) > 0:
        st.warning("## ⚠️ RECOMENDAÇÕES PRIORITÁRIAS")
        for i, rec in enumerate(recomendacoes, 1):
            st.markdown(f"**{i}.** {rec}")
        st.markdown("---")
    
    # PROTOCOLO STEP-BY-STEP
    st.success("## ✅ PROTOCOLO PASSO A PASSO PARA O PRÓXIMO CICLO")
    
    st.markdown("""
    ### **FASE 1: PRÉ-CICLO (2-3 meses antes)**
    
    #### **Investigações pendentes:**
    """)
    
    investigacoes_pendentes = []
    if not cariótipo_casal:
        investigacoes_pendentes.append("- [ ] Cariótipo do casal")
    if not pgt_a and idade >= 37:
        investigacoes_pendentes.append("- [ ] Considerar PGT-A nos próximos embriões")
    if not trombofilia:
        investigacoes_pendentes.append("- [ ] Painel completo de trombofilia")
    if biopsia_endometrial == "Não realizada":
        investigacoes_pendentes.append("- [ ] Biópsia endometrial com CD138 (endometrite crônica)")
    if histeroscopia == "Não realizada":
        investigacoes_pendentes.append("- [ ] Histeroscopia diagnóstica")
    if era_test == "Não realizado" and num_falhas >= 3:
        investigacoes_pendentes.append("- [ ] Considerar ERA Test (janela de implantação)")
    if ureaplasma == "Não testado":
        investigacoes_pendentes.append("- [ ] Pesquisa Ureaplasma/Mycoplasma (casal)")
    if fragmentacao_dna == "Não realizado":
        investigacoes_pendentes.append("- [ ] Fragmentação de DNA espermático")
    
    if len(investigacoes_pendentes) > 0:
        for inv in investigacoes_pendentes:
            st.markdown(inv)
    else:
        st.markdown("✅ Todas as investigações essenciais realizadas")
    
    st.markdown("""
    #### **Tratamentos/Cirurgias necessários:**
    """)
    
    if len(alertas_criticos) > 0:
        st.markdown("⚠️ **Veja alertas críticos acima - tratamento obrigatório**")
    else:
        st.markdown("✅ Nenhuma intervenção crítica pendente")
    
    st.markdown("""
    #### **Suplementação pré-ciclo (iniciar agora):**
    
    **Para a mulher:**
    - [ ] Ácido fólico 5mg/dia (ou metilfolato se MTHFR+)
    - [ ] Vitamina D 2000-4000 UI/dia (se <30 ng/mL)
    - [ ] Ômega-3 (DHA) 1-2g/dia
    - [ ] Multivitamínico pré-natal
    """)
    
    if idade >= 35:
        st.markdown("""
    - [ ] CoQ10 200-600mg/dia
    - [ ] Melatonina 3mg à noite
    - [ ] Considerar DHEA 25-75mg/dia (avaliar com médico)
        """)
    
    if vitamina_d < 30:
        st.markdown("- [ ] **Vitamina D**: dose terapêutica até normalizar")
    
    if homa_ir > 2.5:
        st.markdown("- [ ] **Metformina** 1500-2000mg/dia")
        st.markdown("- [ ] **Myo-inositol 2g + D-chiro-inositol 50mg** 2x/dia")
    
    st.markdown("""
    **Para o homem (se fator masculino presente):**
    - [ ] Multivitamínico com antioxidantes
    - [ ] Vitamina C 1000mg/dia
    - [ ] Vitamina E 400 UI/dia
    - [ ] Zinco 30mg/dia
    - [ ] Selênio 200mcg/dia
    - [ ] CoQ10 200mg/dia
    - [ ] L-carnitina 2g/dia
    """)
    
    st.markdown("""
    ---
    ### **FASE 2: PREPARO ENDOMETRIAL**
    
    #### **Protocolo de estimulação/preparo:**
    """)
    
    # Protocolo básico
    st.markdown("""
    - [ ] Estradiol (dose ajustada para atingir endométrio ≥8mm)
    - [ ] Monitoramento ultrassonográfico seriado
    - [ ] Meta: Endométrio trilaminar ≥8-9mm
    """)
    
    if espessura_endometrial < 7:
        st.markdown("""
    - [ ] **Protocolo endométrio fino:**
      - Estradiol oral dose alta (6-8mg/dia)
      - Estradiol vaginal adicional 2mg 12/12h
      - Vitamina E 800 UI/dia
      - L-arginina 6g/dia
      - Pentoxifilina 800mg/dia
      - AAS 100mg/dia
        """)
    
    # Medicações específicas baseadas nos achados
    if trombofilia_presente or len([c for c in saf_criteria if c]) > 0:
        st.markdown("""
    - [ ] **AAS 100mg/dia** (iniciar com preparo endometrial)
        """)
    
    if "Adenomiose" in str(alteracoes):
        st.markdown("""
    - [ ] **Considerar GnRH análogo** 2-3 meses antes (Leuprolide)
        """)
    
    st.markdown("""
    ---
    ### **FASE 3: TRANSFERÊNCIA EMBRIONÁRIA**
    
    #### **Dia da transferência:**
    """)
    
    if trombofilia_presente or len(saf_criteria) > 0:
        st.markdown("""
    - [ ] Iniciar **Enoxaparina 40mg/dia SC** (no dia da transferência)
    - [ ] Manter **AAS 100mg/dia**
        """)
    
    if len([c for c in saf_criteria if c]) > 0 and anticoagulante_lupico == "Positivo":
        st.markdown("""
    - [ ] **Hidroxicloroquina 400mg/dia** (se não iniciado antes)
        """)
    
    if nk_elevado and num_falhas >= 4:
        st.markdown("""
    - [ ] **Considerar Prednisona 5-10mg/dia** (controverso - discutir riscos/benefícios)
    - [ ] Ou **Intralipid 20% 100mL IV** antes da transferência (controverso)
        """)
    
    if era_test == "Pré-receptivo":
        st.markdown("""
    - [ ] **Ajustar timing:** Transferir 12-24h MAIS TARDE que o habitual
        """)
    elif era_test == "Pós-receptivo":
        st.markdown("""
    - [ ] **Ajustar timing:** Transferir 12-24h MAIS CEDO que o habitual
        """)
    
    st.markdown("""
    #### **Suporte de fase lútea:**
    
    - [ ] Progesterona micronizada 600-800mg/dia (vaginal)
    - [ ] OU Progesterona injetável 50-100mg/dia IM
    - [ ] OU Combinação das vias
    - [ ] Estradiol 2-6mg/dia (manter)
    """)
    
    if progesterona < 10:
        st.markdown("""
    - [ ] **Aumentar dose de progesterona** ou adicionar via adicional
        """)
    
    st.markdown("""
    ---
    ### **FASE 4: PÓS-TRANSFERÊNCIA**
    
    #### **Cuidados pós-transferência:**
    
    - [ ] Manter todas as medicações prescritas
    - [ ] Beta-hCG em 10-12 dias
    - [ ] Ultrassom em 5-6 semanas (se beta positivo)
    - [ ] Repouso relativo primeiras 24-48h
    - [ ] Evitar exercícios intensos por 2 semanas
    - [ ] Evitar relações sexuais por 2 semanas
    """)
    
    if trombofilia_presente or len(saf_criteria) > 0:
        st.markdown("""
    - [ ] **Manter anticoagulação até 12 semanas se gestação positiva**
    - [ ] Seguimento com hematologista/reumatologista
        """)
    
    if problema_tireoide:
        st.markdown("""
    - [ ] **Controle de TSH a cada 4 semanas** (meta <2.5)
    - [ ] Ajustar levotiroxina conforme necessário
        """)
    
    st.markdown("""
    ---
    ### **FASE 5: SEGUIMENTO E PRÓXIMOS PASSOS**
    
    #### **Se beta-hCG negativo:**
    - Reavaliar protocolo com médico
    - Considerar investigações adicionais não realizadas
    - Ajustar estratégia para próximo ciclo
    
    #### **Se beta-hCG positivo:**
    - Manter todas as medicações
    - Ultrassom precoce (5-6 semanas)
    - Seguimento pré-natal de alto risco
    - Manter anticoagulação se indicada
    - Screening de diabetes gestacional precoce
    - Suplementação continuar até 12 semanas mínimo
    """)
    
    # REFERÊNCIAS
    st.markdown("""
    ---
    ## 📚 REFERÊNCIAS CIENTÍFICAS UTILIZADAS
    
    1. **ESHRE Guideline on Recurrent Implantation Failure** (2023)
    2. **ASRM Practice Committee Opinion on RIF** (2024)
    3. **Cochrane Review: Interventions for RIF** (2024)
    4. **Fertility & Sterility**: Multiple articles on specific interventions
    5. **ESHRE PGT Consortium Guidelines** (2023)
    6. **Sydney Criteria for Antiphospholipid Syndrome** (2024)
    7. **ATA Thyroid Guidelines in Pregnancy** (2024)
    8. **ACOG Practice Bulletin on Thrombophilia** (2023)
    9. **WHO Semen Analysis Manual** (2021)
    10. **Andrology Guidelines on DNA Fragmentation** (2024)
    
    ---
    ## ⚠️ AVISOS IMPORTANTES
    
    ⚠️ **Este aplicativo é uma ferramenta de apoio à decisão clínica e NÃO substitui a avaliação médica individualizada.**
    
    ⚠️ **Todas as recomendações devem ser discutidas com seu médico especialista em reprodução humana.**
    
    ⚠️ **Alguns tratamentos mencionados (especialmente imunoterapias) são controversos e possuem evidências limitadas.**
    
    ⚠️ **A conduta final deve ser personalizada considerando histórico completo, custos e preferências da paciente.**
    
    ---
    **Desenvolvido com base em evidências científicas atualizadas.**  
    **Última atualização: Outubro 2025**
    """)
    
    # BOTÃO PARA GERAR RELATÓRIO
    st.markdown("---")
    if st.button("📄 Gerar Relatório Completo (PDF)", type="primary"):
        st.info("""
        **Funcionalidade de geração de PDF será implementada em versão futura.**
        
        Por enquanto, você pode:
        1. Usar a função de impressão do navegador (Ctrl+P)
        2. Salvar como PDF
        3. Ou fazer screenshots das seções relevantes
        """)
    
    # BOTÃO PARA SALVAR DADOS
    if st.button("💾 Salvar Dados do Caso"):
        dados_caso = {
            "nome": nome_paciente,
            "idade": idade,
            "num_falhas": num_falhas,
            "imc": imc,
            "data_avaliacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "alertas_criticos": alertas_criticos,
            "recomendacoes": recomendacoes
        }
        
        st.download_button(
            label="📥 Download JSON",
            data=json.dumps(dados_caso, indent=2, ensure_ascii=False),
            file_name=f"caso_rif_{nome_paciente.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json"
        )

# FOOTER
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9em;'>
    <p><strong>RIF Protocol Assistant v1.0</strong></p>
    <p>Ferramenta de apoio à decisão clínica baseada em evidências</p>
    <p><em>⚠️ Não substitui avaliação médica especializada</em></p>
</div>
""", unsafe_allow_html=True)
