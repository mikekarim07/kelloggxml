import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import os
import zipfile
import time
import io
from io import StringIO
import base64

st.set_page_config(
    page_title="Lector de archivos xml de los CFDIs - webapp",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'mailto:miguel.karim@karimortega.com'
    }
)


def extract_xml_files(zip_files):
    extracted_files = set()

    for zip_file in zip_files:
        with zipfile.ZipFile(zip_file, 'r') as zf:
            # Extract XML files to a temporary folder
            extract_folder = 'temp'
            zf.extractall(extract_folder)
            
            # Add extracted XML files to the set
            for root, _, files in os.walk(extract_folder):
                for file in files:
                    if file.endswith('.xml'):
                        extracted_files.add(os.path.join(root, file))

    return list(extracted_files)

def cfdv33(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    namespaces4 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        "pago20": "http://www.sat.gob.mx/Pagos20",
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    ns33 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        "pago10": "http://www.sat.gob.mx/Pagos",
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital',
    }
    version = root.attrib.get('Version', '')
    forma_de_pago = root.attrib.get('FormaPago', '')
    serie = root.attrib.get('Serie', '')
    folio = root.attrib.get('Folio', '')
    fechadoc = root.attrib.get('Fecha', '')
    tipo = root.attrib.get('TipoDeComprobante', '')
    subtotal = root.attrib.get('SubTotal', '')
    moneda = root.attrib.get('Moneda', '')
    total = root.attrib.get('Total', '')

    #Campos versión 4.0
    regimen4 = root.find('cfdi:Emisor', namespaces=namespaces4).attrib.get('RegimenFiscal', '') if root.find('cfdi:Emisor', namespaces=namespaces4) is not None else ''
    rfc_emisor4 = root.find('cfdi:Emisor', namespaces=namespaces4).attrib.get('Rfc', '') if root.find('cfdi:Emisor', namespaces=namespaces4) is not None else ''
    nombre_emisor4 = root.find('cfdi:Emisor', namespaces=namespaces4).attrib.get('Nombre', '') if root.find('cfdi:Emisor', namespaces=namespaces4) is not None else ''
    rfc_receptor4 = root.find('cfdi:Receptor', namespaces=namespaces4).attrib.get('Rfc', '') if root.find('cfdi:Receptor', namespaces=namespaces4) is not None else ''
    nombre_receptor4 = root.find('cfdi:Receptor', namespaces=namespaces4).attrib.get('Nombre', '') if root.find('cfdi:Receptor', namespaces=namespaces4) is not None else ''
    domicilio_receptor4 = root.find('cfdi:Receptor', namespaces=namespaces4).attrib.get('DomicilioFiscalReceptor', '') if root.find('cfdi:Receptor', namespaces=namespaces4) is not None else ''
    uuid4 = root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=namespaces4).attrib.get('UUID', '') if root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=namespaces4) is not None else ''
    pagos_version4 = root.find('cfdi:Complemento/pago20:Pagos', namespaces=namespaces4).attrib.get('Version', '') if root.find('cfdi:Complemento/pago20:Pagos', namespaces=namespaces4) is not None else ''
    usocfdi4 = root.find('cfdi:Receptor', namespaces=namespaces4).attrib.get('UsoCFDI', '') if root.find('cfdi:Receptor', namespaces=namespaces4) is not None else ''
    fechapagop4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4).attrib.get('FechaPago', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4) is not None else ''
    formapagop4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4).attrib.get('FormaDePagoP', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4) is not None else ''
    monedap4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4).attrib.get('MonedaP', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4) is not None else ''
    montop4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4).attrib.get('Monto', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4) is not None else ''
    iddocp4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4).attrib.get('IdDocumento', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4) is not None else ''
    monedadr4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4).attrib.get('MonedaDR', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4) is not None else ''
    numparcialidadp4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4).attrib.get('NumParcialidad', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4) is not None else ''
    impsdoantp4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4).attrib.get('ImpSaldoAnt', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4) is not None else ''
    imppag4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4).attrib.get('ImpPagado', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4) is not None else ''
    impsdoinsoluto4 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4).attrib.get('ImpSaldoInsoluto', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago/pago20:DoctoRelacionado', namespaces=namespaces4) is not None else ''
    impuesto_ret4 = root.find('cfdi:Impuestos', namespaces=namespaces4).attrib.get('TotalImpuestosRetenidos', '') if root.find('cfdi:Impuestos', namespaces=namespaces4) is not None else ''
    impuesto_trasl4 = root.find('cfdi:Impuestos', namespaces=namespaces4).attrib.get('TotalImpuestosTrasladados', '') if root.find('cfdi:Impuestos', namespaces=namespaces4) is not None else ''

    #Campos versión 3.3
    regimen33 = root.find('cfdi:Emisor', namespaces=ns33).attrib.get('RegimenFiscal', '') if root.find('cfdi:Emisor', namespaces=ns33) is not None else ''
    rfc_emisor33 = root.find('cfdi:Emisor', namespaces=ns33).attrib.get('Rfc', '') if root.find('cfdi:Emisor', namespaces=ns33) is not None else ''
    nombre_emisor33 = root.find('cfdi:Emisor', namespaces=ns33).attrib.get('Nombre', '') if root.find('cfdi:Emisor', namespaces=ns33) is not None else ''
    rfc_receptor33 = root.find('cfdi:Receptor', namespaces=ns33).attrib.get('Rfc', '') if root.find('cfdi:Receptor', namespaces=ns33) is not None else ''
    nombre_receptor33 = root.find('cfdi:Receptor', namespaces=ns33).attrib.get('Nombre', '') if root.find('cfdi:Receptor', namespaces=ns33) is not None else ''
    # domicilio_receptor33 = root.find('cfdi:Receptor', namespaces=ns33).attrib.get('DomicilioFiscalReceptor', '') if root.find('cfdi:Receptor', namespaces=ns33) is not None else ''
    uuid33 = root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=ns33).attrib.get('UUID', '') if root.find('cfdi:Complemento/tfd:TimbreFiscalDigital', namespaces=ns33) is not None else ''
    pagos_version33 = root.find('cfdi:Complemento/pago10:Pagos', namespaces=ns33).attrib.get('Version', '') if root.find('cfdi:Complemento/pago10:Pagos', namespaces=ns33) is not None else ''
    usocfdi33 = root.find('cfdi:Receptor', namespaces=ns33).attrib.get('UsoCFDI', '') if root.find('cfdi:Receptor', namespaces=ns33) is not None else ''
    fechapagop33 = root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4).attrib.get('FechaPago', '') if root.find('cfdi:Complemento/pago20:Pagos/pago20:Pago', namespaces=namespaces4) is not None else ''

    formapagop33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago', namespaces=ns33).attrib.get('FormaDePagoP', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago', namespaces=ns33) is not None else ''
    monedap33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago', namespaces=ns33).attrib.get('MonedaP', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago', namespaces=ns33) is not None else ''
    montop33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago', namespaces=ns33).attrib.get('Monto', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago', namespaces=ns33) is not None else ''
    iddocp33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('IdDocumento', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    monedadr33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('MonedaDR', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    metodopagodr33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    numparcialidadp33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('NumParcialidad', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    impsdoantp33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('ImpSaldoAnt', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    imppag33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('ImpPagado', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    impsdoinsoluto33 = root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33).attrib.get('ImpSaldoInsoluto', '') if root.find('cfdi:Complemento/pago10:Pagos/pago10:Pago/pago10:DoctoRelacionado', namespaces=ns33) is not None else ''
    impuesto_ret33 = root.find('cfdi:Impuestos', namespaces=ns33).attrib.get('TotalImpuestosRetenidos', '') if root.find('cfdi:Impuestos', namespaces=ns33) is not None else ''
    impuesto_trasl33 = root.find('cfdi:Impuestos', namespaces=ns33).attrib.get('TotalImpuestosTrasladados', '') if root.find('cfdi:Impuestos', namespaces=ns33) is not None else ''
    fecha_emision = root.attrib.get('Fecha', '')

    return {
        'Version': version,
        'FormaPago': forma_de_pago,
        'Serie': serie,
        'Folio': folio,
        'UsoCFDI4': usocfdi4,
        'UsoCFDI33': usocfdi33,
        'FechaDoc': fechadoc,
        'RegimenFiscal4': regimen4,
        'RegimenFiscal33': regimen33,
        'TipoDeComprobante': tipo,
        'RfcEmisor4': rfc_emisor4,
        'RfcEmisor33': rfc_emisor33,
        'NombreEmisor4': nombre_emisor4,
        'NombreEmisor33': nombre_emisor33,
        'RfcReceptor4': rfc_receptor4,
        'RfcReceptor33': rfc_receptor33,
        'NombreReceptor4': nombre_receptor4,
        'NombreReceptor33': nombre_receptor33,
        'SubTotal': subtotal,
        'Total': total,
        'TotalImpuestosRet4': impuesto_ret4,
        'TotalImpuestosRet33': impuesto_ret33,
        'TotalImpuestosTrasl4': impuesto_trasl4,
        'TotalImpuestosTrasl33': impuesto_trasl33,
        'Moneda': moneda,
        'UUID4': uuid4,
        'UUID33': uuid33,
        'FechaEmision': fecha_emision,
        #
        'DomReceptor': domicilio_receptor4,
        
        'UsoCFDI4': usocfdi4,
        'UsoCFDI33': usocfdi33,
        'FechaPagoP4': fechapagop4,
        'FechaPagoP33': fechapagop33,
        'FormaDePagoP4': formapagop4,
        'FormaDePagoP33': formapagop33,
        'MonedaP4': monedap4,
        'MonedaP33': monedap33,
        'MontoP4': montop4,
        'MontoP33': montop33,
        'DocRelacionado4': iddocp4,
        'DocRelacionado33': iddocp33,
        'MonedaDR4': monedadr4,
        'MonedaDR33': monedadr33,
        'NumParcialidad4': numparcialidadp4,
        'NumParcialidad33': numparcialidadp33,
        'ImporteSaldoAnt4': impsdoantp4,
        'ImporteSaldoAnt33': impsdoantp33,
        'ImportePagado4': imppag4,
        'ImportePagado33': imppag33,
        'ImprteSaldoInsoluto4': impsdoinsoluto4,
        'ImprteSaldoInsoluto33': impsdoinsoluto33,

        #
        'Version4': pagos_version4,
        'Version33': pagos_version33
    }

def read_and_append_txt_files(uploaded_txt_files):
    all_txt_data = []
    
    for uploaded_file in uploaded_txt_files:
        content = uploaded_file.read()
        decoded_content = content.decode("utf-8")  # Decode the bytes to string using the appropriate encoding

        # Append the content of each file to the list
        all_txt_data.append(decoded_content)
    
    # Concatenate the contents of all files
    concatenated_data = '\n'.join(all_txt_data)
    
    # Create a DataFrame from the concatenated data
    df = pd.read_csv(StringIO(concatenated_data), sep='~')
    return df

def main():
    
    st.image("https://www.kelloggs.com/content/dam/NorthAmerica/kelloggs/en_US/images/logoMain.png", width=150)
    st.title("Plataforma Web para extraer datos de los CFDIs")
    st.divider()
    st.subheader("Instrucciones")
    st.write("Para una carga más ágil, juntar todos los archivos xml que desean procesar en uno o varios archivos zip.")
    st.caption("Se pueden procesar los archivos xml de una o varias entidades legales, posteriormente podrán realizar filtros")
    st.write("Seleccionar el o los archivo zip o arrastrarlos y soltarlos.")
    
    st.divider()
    # Upload multiple zip files
    uploaded_zip_files = st.file_uploader("Carga los archivos zip que contienen los archivos xml", type=["zip"], accept_multiple_files=True)
    uploaded_txt_files = st.file_uploader("Carga los archivos txt que contienen la metadata del SAT", type=["txt"], accept_multiple_files=True)
    rfc_filtro = st.text_input('Ingresa el RFC de la sociedad que deseas hacer el análisis:', value='', key='rfc_filtro')
    st.write("Selecciona la casilla Procesar 👇")
    if st.checkbox("Procesar"):
        if uploaded_zip_files and uploaded_txt_files:
            # Extract XML files from zip files
            extracted_files = extract_xml_files(uploaded_zip_files)
            # st.dataframe(extracted_files)
            total_archivos = len(extracted_files)
            st.info(f'Total de archivos en la carpeta: {total_archivos}')
            # st.text({os.path.abspath('temp')})

            # with st.expander("List of Extracted XML Files", expanded=False):
            #     for xml_file in extracted_files:
            #         st.text(xml_file)

            start_time = time.time()
            

            data_parse_cfd33 = []
            cfdv33_not_processed = []
                        
            df_cfdv33 = pd.DataFrame()
            txt_appended = read_and_append_txt_files(uploaded_txt_files)
            
            if txt_appended is not None:
                txt_appended = txt_appended[txt_appended['Uuid'] != 'Uuid']
                
            else:
                st.warning("No data to display. Please upload valid TXT files.")

                        
            for xml_path in extracted_files:
                try:
                    xml_data_parse_cfdv33 = cfdv33(xml_path)
                    data_parse_cfd33.append(xml_data_parse_cfdv33)
                except Exception as e:
                    cfdv33_not_processed.append(xml_path)
            
            end_time = time.time()
            processing_time = end_time - start_time
            processing_time_formatted = "{:.4f}".format(processing_time)
            st.info(f'Se encontraron un total de {total_archivos} archivos, los cuales fueron procesados en un tiempo total de: {processing_time_formatted} segundos')
            
            df_cfdv33 = pd.DataFrame(data_parse_cfd33)
                        
            # st.caption('CFDIs Version 3.3 y 4.0')
            
            # Meta4merge = pd.DataFrame(txt_appended)
            # Meta4merge.drop([RfcEmisor,NombreEmisor,RfcReceptor,NombreReceptor,,,,,])
            txt_appended.rename(columns = {'Uuid':'UUID_Meta','RfcEmisor':'RfcEmisor_Meta', 'NombreEmisor':'NombreEmisor_Meta',
                              'RfcReceptor':'RfcReceptor_Meta', 'NombreReceptor':'NombreReceptor_Meta', 'RfcPac':'RfcPac_Meta',
                              'FechaEmision':'FechaEmision_Meta','FechaCertificacionSat':'FechaCertificacionSat_Meta',
                              'Monto':'Monto_Meta','EfectoComprobante':'EfectoComprobante_Meta','Estatus':'Estatus_Meta',
                              'FechaCancelacion':'FechaCancelacion_Meta'}, inplace = True)


            CFDIs = pd.DataFrame(df_cfdv33)
            CFDIs['UsoCFDI'] = CFDIs['UsoCFDI4']+CFDIs['UsoCFDI33']
            CFDIs['RegimenFiscal'] = CFDIs['RegimenFiscal4']+CFDIs['RegimenFiscal33']
            CFDIs['RFCEmisor'] = CFDIs['RfcEmisor4']+CFDIs['RfcEmisor33']
            CFDIs['NombreEmisor'] = CFDIs['NombreEmisor4']+CFDIs['NombreEmisor33']
            CFDIs['RFCReceptor'] = CFDIs['RfcReceptor4']+CFDIs['RfcReceptor33']
            CFDIs['NombreReceptor'] = CFDIs['NombreReceptor4']+CFDIs['NombreReceptor33']
            CFDIs['ImpuestosRetenidos'] = CFDIs['TotalImpuestosRet4']+CFDIs['TotalImpuestosRet33']
            CFDIs['ImpuestosTrasladados'] = CFDIs['TotalImpuestosTrasl4']+CFDIs['TotalImpuestosTrasl33']
            CFDIs['UUID'] = CFDIs['UUID4']+CFDIs['UUID33']
            CFDIs['FechaPagoP'] = CFDIs['FechaPagoP4']+CFDIs['FechaPagoP33']
            CFDIs['FormaPagoP'] = CFDIs['FormaDePagoP4']+CFDIs['FormaDePagoP33']
            CFDIs['MonedaP'] = CFDIs['MonedaP4']+CFDIs['MonedaP33']
            CFDIs['MontoP'] = CFDIs['MontoP4']+CFDIs['MontoP33']
            CFDIs['DocRelacionado'] = CFDIs['DocRelacionado4']+CFDIs['DocRelacionado33']
            CFDIs['MonedaDR'] = CFDIs['MonedaDR4']+CFDIs['MonedaDR33']
            CFDIs['NumParcialidad'] = CFDIs['NumParcialidad4']+CFDIs['NumParcialidad33']
            CFDIs['ImporteSaldoAnterior'] = CFDIs['ImporteSaldoAnt4']+CFDIs['ImporteSaldoAnt33']
            CFDIs['ImportePagado'] = CFDIs['ImportePagado4']+CFDIs['ImportePagado33']
            CFDIs['ImporteSaldoInsoluto'] = CFDIs['ImprteSaldoInsoluto4']+CFDIs['ImprteSaldoInsoluto33']
            CFDIs['VersionP'] = CFDIs['Version4']+CFDIs['Version33']
            CFDIs[['FechaEmision', 'HoraEmision']] = CFDIs['FechaEmision'].str.split('T', n=1, expand=True)
            CFDIs[['FechaEmision']] = CFDIs[['FechaEmision']].apply(pd.to_datetime)
            CFDIs['Año'] = CFDIs['FechaEmision'].dt.year
            CFDIs['Mes'] = CFDIs['FechaEmision'].dt.month
            CFDIs['Día'] = CFDIs['FechaEmision'].dt.day
            CFDIs[['Año', 'Mes', 'Día']] = CFDIs[['Año', 'Mes', 'Día']].astype('string')
            CFDIs = CFDIs.merge(txt_appended, left_on='UUID', right_on='UUID_Meta', how='left')



            CFDIs.drop(['UsoCFDI4','UsoCFDI33','RegimenFiscal4','RegimenFiscal33','RfcEmisor4', 'RfcEmisor33','NombreEmisor4','NombreEmisor33','RfcReceptor4','RfcReceptor33','NombreReceptor4',
                        'NombreReceptor33','TotalImpuestosRet4','TotalImpuestosRet33','TotalImpuestosTrasl4','TotalImpuestosTrasl33','UUID4','UUID33','FechaPagoP4','FechaPagoP33','FormaDePagoP4',
                        'FormaDePagoP33','MonedaP4','MonedaP33','MontoP4','MontoP33','DocRelacionado4','DocRelacionado33','MonedaDR4','MonedaDR33','NumParcialidad4','NumParcialidad33',
                        'ImporteSaldoAnt4','ImporteSaldoAnt33','ImportePagado4','ImportePagado33','ImprteSaldoInsoluto4','ImprteSaldoInsoluto33','Version4','Version33','RfcReceptor_Meta',
                        'NombreReceptor_Meta','RfcPac_Meta','FechaEmision_Meta','FechaCertificacionSat_Meta','Monto_Meta','EfectoComprobante_Meta'], axis = 1, inplace=True)
            CFDIs[['SubTotal', 'Total', 'ImpuestosRetenidos', 'ImpuestosTrasladados', 'MontoP', 'ImporteSaldoAnterior', 'ImportePagado', 'ImporteSaldoInsoluto']] = CFDIs[['SubTotal', 'Total',
                     'ImpuestosRetenidos', 'ImpuestosTrasladados', 'MontoP', 'ImporteSaldoAnterior', 'ImportePagado', 'ImporteSaldoInsoluto']].apply(pd.to_numeric)
            
            
            
            st.divider()
            
            tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Total CFDIs", "Ingresos", "Egresos", "Nomina", "Complementos de Pago", "Metadata"])
            
            with tab1:
                st.subheader("Total de CFDIs")
                st.caption('Detalle de los CFDIs procesados')
                st.caption('CFDIs Version 3.3 y 4.0')
                st.write(CFDIs.shape)
                st.dataframe(CFDIs, height=600)
                
            with tab2:
                st.subheader("CFDIs de Ingresos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_ingresos = pd.DataFrame(CFDIs)
                cfdi_ingresos = cfdi_ingresos[(cfdi_ingresos['RFCEmisor'] == rfc_filtro) & ((cfdi_ingresos['TipoDeComprobante'] == "I"))]
                st.write(cfdi_ingresos.shape)
                st.dataframe(cfdi_ingresos, height=600)
                resumen_ing = cfdi_ingresos[cfdi_ingresos['Estatus_Meta'] != "0"]
                resumen_ing = resumen_ing.groupby(by=['RFCEmisor', 'Año', 'Mes'], as_index=False)['SubTotal'].sum()
                st.dataframe(resumen_ing, height=600)
                
            with tab3:
                st.subheader("CFDIs de Egresos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_egresos = pd.DataFrame(CFDIs)
                cfdi_egresos = cfdi_egresos[(cfdi_egresos['RFCReceptor'] == rfc_filtro) & (cfdi_egresos['TipoDeComprobante'] != "P")]
                st.write(cfdi_egresos.shape)
                st.dataframe(cfdi_egresos, height=600)
                resumen_eg = cfdi_egresos[cfdi_egresos['Estatus_Meta'] != "0"]
                resumen_eg = resumen_eg.groupby(by=['RFCReceptor', 'Año', 'Mes'], as_index=False)['SubTotal'].sum()
                st.dataframe(resumen_eg, height=600)
                
            with tab4:
                st.subheader("CFDIs de Nomina")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_nomina = pd.DataFrame(CFDIs)
                cfdi_nomina = cfdi_nomina[(cfdi_nomina['RFCEmisor'] == rfc_filtro) & (cfdi_nomina['TipoDeComprobante'] == "N")]
                st.write(cfdi_nomina.shape)
                st.dataframe(cfdi_nomina, height=600)

            with tab5:
                st.subheader("CFDIs Complementos de Pago Recibidos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_comp_pago = pd.DataFrame(CFDIs)
                cfdi_comp_pago = cfdi_comp_pago[(cfdi_comp_pago['RFCReceptor'] == rfc_filtro) & (cfdi_comp_pago['TipoDeComprobante'] == "P")]
                st.write(cfdi_comp_pago.shape)
                st.dataframe(cfdi_comp_pago, height=600)

            with tab6:
                st.subheader("Metadata")
                st.caption('Detalle de la Metadata')
                st.write(txt_appended.shape)
                st.dataframe(txt_appended)

            if st.session_state.rfc_filtro:
                buffer = io.BytesIO()

                # Create a Pandas Excel writer using XlsxWriter as the engine.
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    CFDIs.to_excel(writer, sheet_name='CFDIs')
                    cfdi_ingresos.to_excel(writer, sheet_name='Ingresos')
                    cfdi_egresos.to_excel(writer, sheet_name='Egresos')
                    cfdi_nomina.to_excel(writer, sheet_name='Nomina')
                    cfdi_comp_pago.to_excel(writer, sheet_name='Comp Pago')
                    resumen_ing.to_excel(writer, sheet_name='Resumen Ing')
                    resumen_eg.to_excel(writer, sheet_name='Resumen Eg')

                    # Close the Pandas Excel writer and output the Excel file to the buffer
                    writer.save()

                # Set up download link
                b64 = base64.b64encode(buffer.getvalue()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="CFDIs_datos.xlsx">Download Excel File</a>'
                st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

