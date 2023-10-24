import streamlit as st
import pandas as pd
import xml.etree.ElementTree as ET
import os
import zipfile
import time
import io
from io import StringIO
import base64
import plotly.express as px

st.set_page_config(
    page_title="Lector de archivos xml de los CFDIs - webapp",
    page_icon="📊",
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
    descuento = root.attrib.get('Descuento', '')
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
        'Descuento': descuento,
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

def cfd_conceptos(xml_file):
    # Crea un diccionario para almacenar los campos requeridos
    data33 = {
        'ClaveProdServ': [],
        'NoIdentificacion': [],
        'Cantidad': [],
        'ClaveUnidad': [],
        'Unidad': [],
        'Descripcion': [],
        'ValorUnitario': [],
        'Importe': [],
        'Descuento': [],
        'UUID': [],
        'Version': []
    }
    
    data40 = {
        'ClaveProdServ': [],
        'NoIdentificacion': [],
        'Cantidad': [],
        'ClaveUnidad': [],
        'Unidad': [],
        'Descripcion': [],
        'ValorUnitario': [],
        'Importe': [],
        'Descuento': [],
        'UUID': [],
        'Version': []
    }

    # Define the namespaces used in the XML file
    ns33 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    ns40 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    # Parsea el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extrae el UUID del atributo del elemento 'tfd:TimbreFiscalDigital'
    uuid33 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns33).attrib.get('UUID')
    version33 = root.attrib.get('Version', '')
    uuid40 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns40).attrib.get('UUID')
    version40 = root.attrib.get('Version', '')
    # Itera sobre cada elemento 'cfdi:Concepto'
    
    for concepto33 in root.findall('.//cfdi:Concepto', namespaces=ns33):
        data33['ClaveProdServ'].append(concepto33.attrib.get('ClaveProdServ', ''))
        data33['NoIdentificacion'].append(concepto33.attrib.get('NoIdentificacion', ''))
        data33['Cantidad'].append(concepto33.attrib.get('Cantidad', ''))
        data33['ClaveUnidad'].append(concepto33.attrib.get('ClaveUnidad', ''))
        data33['Unidad'].append(concepto33.attrib.get('Unidad', ''))
        data33['Descripcion'].append(concepto33.attrib.get('Descripcion', ''))
        data33['ValorUnitario'].append(concepto33.attrib.get('ValorUnitario', ''))
        data33['Importe'].append(concepto33.attrib.get('Importe', ''))
        data33['Descuento'].append(concepto33.attrib.get('Descuento', ''))
        data33['UUID'].append(uuid33)
        data33['Version'].append(version33)

    for concepto40 in root.findall('.//cfdi:Concepto', namespaces=ns40):
        data40['ClaveProdServ'].append(concepto40.attrib.get('ClaveProdServ', ''))
        data40['NoIdentificacion'].append(concepto40.attrib.get('NoIdentificacion', ''))
        data40['Cantidad'].append(concepto40.attrib.get('Cantidad', ''))
        data40['ClaveUnidad'].append(concepto40.attrib.get('ClaveUnidad', ''))
        data40['Unidad'].append(concepto40.attrib.get('Unidad', ''))
        data40['Descripcion'].append(concepto40.attrib.get('Descripcion', ''))
        data40['ValorUnitario'].append(concepto40.attrib.get('ValorUnitario', ''))
        data40['Importe'].append(concepto40.attrib.get('Importe', ''))
        data40['Descuento'].append(concepto40.attrib.get('Descuento', ''))
        data40['UUID'].append(uuid40)
        data40['Version'].append(version40)
    # Crea el DataFrame con el diccionario
    df33 = pd.DataFrame(data33)
    df40 = pd.DataFrame(data40)
    df = pd.concat([df33,df40])
    return df

def cfd_impuestosxconcepto(xml_file):
    # Crea un diccionario para almacenar los campos requeridos
    data33 = {
        'Base': [],
        'Impuesto': [],
        'TipoFactor': [],
        'TasaOCuota': [],
        'Importe': [],
        'UUID': [],
        'Version': []
    }
    
    data40 = {
        'Base': [],
        'Impuesto': [],
        'TipoFactor': [],
        'TasaOCuota': [],
        'Importe': [],
        'UUID': [],
        'Version': []
    }

    # Define the namespaces used in the XML file
    ns33 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    ns40 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    # Parsea el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extrae el UUID del atributo del elemento 'tfd:TimbreFiscalDigital'
    uuid33 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns33).attrib.get('UUID')
    version33 = root.attrib.get('Version', '')
    uuid40 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns40).attrib.get('UUID')
    version40 = root.attrib.get('Version', '')
    # Itera sobre cada elemento 'cfdi:Concepto'
    
    for impuestos33 in root.findall('.//cfdi:Concepto/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=ns33):
        data33['Base'].append(impuestos33.attrib.get('Base', ''))
        data33['Impuesto'].append(impuestos33.attrib.get('Impuesto', ''))
        data33['TipoFactor'].append(impuestos33.attrib.get('TipoFactor', ''))
        data33['TasaOCuota'].append(impuestos33.attrib.get('TasaOCuota', ''))
        data33['Importe'].append(impuestos33.attrib.get('Importe', ''))
        data33['UUID'].append(uuid33)
        data33['Version'].append(version33)

    for impuestos40 in root.findall('.//cfdi:Concepto/cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=ns40):
        data40['Base'].append(impuestos40.attrib.get('Base', ''))
        data40['Impuesto'].append(impuestos40.attrib.get('Impuesto', ''))
        data40['TipoFactor'].append(impuestos40.attrib.get('TipoFactor', ''))
        data40['TasaOCuota'].append(impuestos40.attrib.get('TasaOCuota', ''))
        data40['Importe'].append(impuestos40.attrib.get('Importe', ''))
        data40['UUID'].append(uuid40)
        data40['Version'].append(version40)
    # Crea el DataFrame con el diccionario
    df33 = pd.DataFrame(data33)
    df40 = pd.DataFrame(data40)
    df = pd.concat([df33,df40])
    return df

def cfd_impretxconcepto(xml_file):
    # Crea un diccionario para almacenar los campos requeridos
    data33 = {
        'BaseRet': [],
        'ImpuestoRet': [],
        'TipoFactorRet': [],
        'TasaOCuotaRet': [],
        'ImporteRet': [],
        'UUIDRet': [],
        'VersionRet': []
    }
    
    data40 = {
        'BaseRet': [],
        'ImpuestoRet': [],
        'TipoFactorRet': [],
        'TasaOCuotaRet': [],
        'ImporteRet': [],
        'UUIDRet': [],
        'VersionRet': []
    }

    # Define the namespaces used in the XML file
    ns33 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    ns40 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    # Parsea el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extrae el UUID del atributo del elemento 'tfd:TimbreFiscalDigital'
    uuid33 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns33).attrib.get('UUID')
    version33 = root.attrib.get('Version', '')
    uuid40 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns40).attrib.get('UUID')
    version40 = root.attrib.get('Version', '')
    # Itera sobre cada elemento 'cfdi:Concepto'
    
    for retenciones33 in root.findall('.//cfdi:Concepto/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=ns33):
        data33['BaseRet'].append(retenciones33.attrib.get('Base', ''))
        data33['ImpuestoRet'].append(retenciones33.attrib.get('Impuesto', ''))
        data33['TipoFactorRet'].append(retenciones33.attrib.get('TipoFactor', ''))
        data33['TasaOCuotaRet'].append(retenciones33.attrib.get('TasaOCuota', ''))
        data33['ImporteRet'].append(retenciones33.attrib.get('Importe', ''))
        data33['UUIDRet'].append(uuid33)
        data33['VersionRet'].append(version33)

    for impuestos40 in root.findall('.//cfdi:Concepto/cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=ns40):
        data40['BaseRet'].append(impuestos40.attrib.get('Base', ''))
        data40['ImpuestoRet'].append(impuestos40.attrib.get('Impuesto', ''))
        data40['TipoFactorRet'].append(impuestos40.attrib.get('TipoFactor', ''))
        data40['TasaOCuotaRet'].append(impuestos40.attrib.get('TasaOCuota', ''))
        data40['ImporteRet'].append(impuestos40.attrib.get('Importe', ''))
        data40['UUIDRet'].append(uuid40)
        data40['VersionRet'].append(version40)
    # Crea el DataFrame con el diccionario
    dfret33 = pd.DataFrame(data33)
    dfret40 = pd.DataFrame(data40)
    df = pd.concat([dfret33,dfret40])
    return df

def cfd_impuestos(xml_file):
    # Crea un diccionario para almacenar los campos requeridos
    data33 = {
        'Base': [],
        'Impuesto': [],
        'TipoFactor': [],
        'TasaOCuota': [],
        'Importe': [],
        'UUID': [],
        'Version': []
    }
    
    data40 = {
        'Base': [],
        'Impuesto': [],
        'TipoFactor': [],
        'TasaOCuota': [],
        'Importe': [],
        'UUID': [],
        'Version': []
    }

    # Define the namespaces used in the XML file
    ns33 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    ns40 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    # Parsea el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extrae el UUID del atributo del elemento 'tfd:TimbreFiscalDigital'
    uuid33 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns33).attrib.get('UUID')
    version33 = root.attrib.get('Version', '')
    uuid40 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns40).attrib.get('UUID')
    version40 = root.attrib.get('Version', '')
    # Itera sobre cada elemento 'cfdi:Concepto'
    
    for impuestos33 in root.findall('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=ns33):
        data33['Base'].append(impuestos33.attrib.get('Base', ''))
        data33['Impuesto'].append(impuestos33.attrib.get('Impuesto', ''))
        data33['TipoFactor'].append(impuestos33.attrib.get('TipoFactor', ''))
        data33['TasaOCuota'].append(impuestos33.attrib.get('TasaOCuota', ''))
        data33['Importe'].append(impuestos33.attrib.get('Importe', ''))
        data33['UUID'].append(uuid33)
        data33['Version'].append(version33)
    
    for impuestos40 in root.findall('cfdi:Impuestos/cfdi:Traslados/cfdi:Traslado', namespaces=ns40):
        data40['Base'].append(impuestos40.attrib.get('Base', ''))
        data40['Impuesto'].append(impuestos40.attrib.get('Impuesto', ''))
        data40['TipoFactor'].append(impuestos40.attrib.get('TipoFactor', ''))
        data40['TasaOCuota'].append(impuestos40.attrib.get('TasaOCuota', ''))
        data40['Importe'].append(impuestos40.attrib.get('Importe', ''))
        data40['UUID'].append(uuid40)
        data40['Version'].append(version40)
    # Crea el DataFrame con el diccionario
    df33 = pd.DataFrame(data33)
    df40 = pd.DataFrame(data40)
    df = pd.concat([df33,df40])
    return df

def cfd_impuestos_ret(xml_file):
    # Crea un diccionario para almacenar los campos requeridos
    data33 = {
        'BaseRet': [],
        'ImpuestoRet': [],
        'TipoFactorRet': [],
        'TasaOCuotaRet': [],
        'ImporteRet': [],
        'UUIDRet': [],
        'VersionRet': []
    }
    
    data40 = {
        'BaseRet': [],
        'ImpuestoRet': [],
        'TipoFactorRet': [],
        'TasaOCuotaRet': [],
        'ImporteRet': [],
        'UUIDRet': [],
        'VersionRet': []
    }

    # Define the namespaces used in the XML file
    ns33 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/3',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    ns40 = {
        'cfdi': 'http://www.sat.gob.mx/cfd/4',
        'tfd': 'http://www.sat.gob.mx/TimbreFiscalDigital'
    }
    # Parsea el archivo XML
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extrae el UUID del atributo del elemento 'tfd:TimbreFiscalDigital'
    uuid33 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns33).attrib.get('UUID')
    version33 = root.attrib.get('Version', '')
    uuid40 = root.find('.//tfd:TimbreFiscalDigital', namespaces=ns40).attrib.get('UUID')
    version40 = root.attrib.get('Version', '')
    # Itera sobre cada elemento 'cfdi:Concepto'
    
    for retenciones33 in root.findall('cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=ns33):
        data33['BaseRet'].append(retenciones33.attrib.get('Base', ''))
        data33['ImpuestoRet'].append(retenciones33.attrib.get('Impuesto', ''))
        data33['TipoFactorRet'].append(retenciones33.attrib.get('TipoFactor', ''))
        data33['TasaOCuotaRet'].append(retenciones33.attrib.get('TasaOCuota', ''))
        data33['ImporteRet'].append(retenciones33.attrib.get('Importe', ''))
        data33['UUIDRet'].append(uuid33)
        data33['VersionRet'].append(version33)

    for impuestos40 in root.findall('cfdi:Impuestos/cfdi:Retenciones/cfdi:Retencion', namespaces=ns40):
        data40['BaseRet'].append(impuestos40.attrib.get('Base', ''))
        data40['ImpuestoRet'].append(impuestos40.attrib.get('Impuesto', ''))
        data40['TipoFactorRet'].append(impuestos40.attrib.get('TipoFactor', ''))
        data40['TasaOCuotaRet'].append(impuestos40.attrib.get('TasaOCuota', ''))
        data40['ImporteRet'].append(impuestos40.attrib.get('Importe', ''))
        data40['UUIDRet'].append(uuid40)
        data40['VersionRet'].append(version40)
    # Crea el DataFrame con el diccionario
    dfret33 = pd.DataFrame(data33)
    dfret40 = pd.DataFrame(data40)
    df = pd.concat([dfret33,dfret40])
    return df

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

EFOS = pd.read_csv('http://omawww.sat.gob.mx/cifras_sat/Documents/Listado_Completo_69-B.csv', encoding='latin1', skiprows=2, header=0)


if 'metadata' not in st.session_state:
    st.session_state.metadata = None

if 'CFDIs' not in st.session_state:
    st.session_state.CFDIs = None

if 'df_conceptos' not in st.session_state:
    st.session_state.df_conceptos = None

if 'df_impxconc' not in st.session_state:
    st.session_state.df_impxconc = None

if 'df_impretxcon' not in st.session_state:
    st.session_state.df_impretxcon = None

if 'df_impuestos' not in st.session_state:
    st.session_state.df_impuestos = None

if 'df_impuestos_ret' not in st.session_state:
    st.session_state.df_impuestos_ret = None

if 'rfc_filtro' not in st.session_state:
    st.session_state.rfc_filtro = None



def main():
    
    st.image("https://www.kellanovaus.com/content/dam/NorthAmerica/kellanova-us/images/logo.svg", width=150)
    st.title("Plataforma Web para extraer datos de los CFDIs")
    with st.sidebar.expander("Instrucciones"):
        st.subheader("Instrucciones")
        st.write('1. Para una carga más ágil, juntar todos los archivos xml que desean procesar en uno o varios archivos zip.')
        st.write('1. Para una carga más ágil, juntar todos los archivos xml que desean procesar en uno o varios archivos zip.')
        # st.image("https://static.streamlit.io/examples/dice.jpg")
        # st.divider()
        
        st.write("Para una carga más ágil, juntar todos los archivos xml que desean procesar en uno o varios archivos zip.")
        st.caption("Se pueden procesar los archivos xml de una o varias entidades legales, posteriormente podrán realizar filtros")
        st.write("Seleccionar el o los archivo zip o arrastrarlos y soltarlos.")
        
        st.divider()
    # Upload multiple zip files
    uploaded_zip_files = st.sidebar.file_uploader("Carga los archivos zip que contienen los archivos xml", type=["zip"], accept_multiple_files=True)
    uploaded_txt_files = st.sidebar.file_uploader("Carga los archivos txt que contienen la metadata del SAT", type=["txt"], accept_multiple_files=True)
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
            
            conceptos = []
            for xml_file in extracted_files:
                data_frame = cfd_conceptos(xml_file)
                conceptos.append(data_frame)
            df_conceptos = pd.concat(conceptos, ignore_index=True)

            #codigocopiado
            impxconc = []
            for xml_file in extracted_files:
                data_frame_imp = cfd_impuestosxconcepto(xml_file)
                impxconc.append(data_frame_imp)
            df_impxconc = pd.concat(impxconc, ignore_index=True)

            impretxconc = []
            for xml_file in extracted_files:
                data_frame_imp_retxcon = cfd_impretxconcepto(xml_file)
                impretxconc.append(data_frame_imp_retxcon)


            impuestos = []
            for xml_file in extracted_files:
                data_frame_impuestos = cfd_impuestos(xml_file)
                impuestos.append(data_frame_impuestos)
            df_impuestos = pd.concat(impuestos, ignore_index=True)
            
            
            impuestos_ret = []
            for xml_file in extracted_files:
                data_frame_impuestos_ret = cfd_impuestos_ret(xml_file)
                impuestos_ret.append(data_frame_impuestos_ret)
            df_impuestos_ret = pd.concat(impuestos_ret, ignore_index=True)

            df_impretxcon = pd.concat(impretxconc, ignore_index=True)
            
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
            metadata = pd.DataFrame(txt_appended)
            metadata[['FechaEmision_Meta', 'HoraEmision_Meta']] = metadata['FechaEmision_Meta'].str.split(' ', n=1, expand=True)
            metadata[['FechaEmision_Meta']] = metadata[['FechaEmision_Meta']].apply(pd.to_datetime)
            metadata['Año_Meta'] = metadata['FechaEmision_Meta'].dt.year
            metadata['Mes_Meta'] = metadata['FechaEmision_Meta'].dt.month
            metadata['Día_Meta'] = metadata['FechaEmision_Meta'].dt.day
            metadata[['Año_Meta', 'Mes_Meta', 'Día_Meta']] = metadata[['Año_Meta', 'Mes_Meta', 'Día_Meta']].astype('string')
            metadata[['Monto_Meta']] = metadata[['Monto_Meta']].apply(pd.to_numeric)
            metadata[['FechaCancelacion_Meta', 'HoraCancelacion_Meta']] = metadata['FechaCancelacion_Meta'].str.split(' ', n=1, expand=True)
            metadata['FechaCancelacion_Meta'] = pd.to_datetime(metadata['FechaCancelacion_Meta'], errors='coerce')
            metadata[['FechaCancelacion_Meta']] = metadata[['FechaCancelacion_Meta']].apply(pd.to_datetime)
            metadata['Año_Canc_Meta'] = metadata['FechaCancelacion_Meta'].dt.year
            metadata['Mes_Canc_Meta'] = metadata['FechaCancelacion_Meta'].dt.month
            metadata['Día_Canc_Meta'] = metadata['FechaCancelacion_Meta'].dt.day
            metadata[['Año_Canc_Meta', 'Mes_Canc_Meta', 'Día_Canc_Meta']] = metadata[['Año_Canc_Meta', 'Mes_Canc_Meta', 'Día_Canc_Meta']].astype('string')
            metadata[['Monto_Meta']] = metadata[['Monto_Meta']].apply(pd.to_numeric)
            def monto_vigente(row):
                if row['Estatus_Meta'] == '1':
                    return row['Monto_Meta']
                else:
                    return None
                
            def monto_cancelado(row):
                if row['Estatus_Meta'] == '0':
                    return row['Monto_Meta']
                else:
                    return None
            metadata['Monto_Meta_Vig'] = metadata.apply(monto_vigente, axis=1)
            metadata['Monto_Meta_Canc'] = metadata.apply(monto_cancelado, axis=1)

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
            CFDIs['UUID'] = CFDIs['UUID'].str.upper()
            CFDIs['TipoDeComprobante'] = CFDIs['TipoDeComprobante'].str.upper()
            CFDIs = CFDIs.merge(metadata, left_on='UUID', right_on='UUID_Meta', how='left')



            CFDIs.drop(['UsoCFDI4','UsoCFDI33','RegimenFiscal4','RegimenFiscal33','RfcEmisor4', 'RfcEmisor33','NombreEmisor4','NombreEmisor33','RfcReceptor4','RfcReceptor33','NombreReceptor4',
                        'NombreReceptor33','TotalImpuestosRet4','TotalImpuestosRet33','TotalImpuestosTrasl4','TotalImpuestosTrasl33','UUID4','UUID33','FechaPagoP4','FechaPagoP33','FormaDePagoP4',
                        'FormaDePagoP33','MonedaP4','MonedaP33','MontoP4','MontoP33','DocRelacionado4','DocRelacionado33','MonedaDR4','MonedaDR33','NumParcialidad4','NumParcialidad33',
                        'ImporteSaldoAnt4','ImporteSaldoAnt33','ImportePagado4','ImportePagado33','ImprteSaldoInsoluto4','ImprteSaldoInsoluto33','Version4','Version33','RfcReceptor_Meta',
                        'NombreReceptor_Meta','RfcPac_Meta','FechaEmision_Meta','FechaCertificacionSat_Meta','EfectoComprobante_Meta'], axis = 1, inplace=True)
            CFDIs[['SubTotal', 'Total', 'ImpuestosRetenidos', 'ImpuestosTrasladados', 'MontoP', 'ImporteSaldoAnterior', 'ImportePagado', 'ImporteSaldoInsoluto']] = CFDIs[['SubTotal', 'Total',
                        'ImpuestosRetenidos', 'ImpuestosTrasladados', 'MontoP', 'ImporteSaldoAnterior', 'ImportePagado', 'ImporteSaldoInsoluto']].apply(pd.to_numeric)
            
            # cfdi_ingresos = pd.DataFrame(CFDIs)
            # cfdi_ingresos = cfdi_ingresos[(cfdi_ingresos['RFCEmisor'] == rfc_filtro) & ((cfdi_ingresos['TipoDeComprobante'] == "I"))]
            # resumen_ing = cfdi_ingresos[cfdi_ingresos['Estatus_Meta'] != "0"]
            # resumen_ing = resumen_ing.groupby(by=['RFCEmisor', 'Año', 'Mes'], as_index=False).agg({'SubTotal': 'sum','Total': 'sum'})

            #session state
            if st.session_state.metadata is None and metadata is not None:
                st.session_state.metadata = metadata

            if st.session_state.CFDIs is None and CFDIs is not None:
                st.session_state.CFDIs = CFDIs

            if st.session_state.df_conceptos is None and df_conceptos is not None:
                st.session_state.df_conceptos = df_conceptos

            if st.session_state.df_impxconc is None and df_impxconc is not None:
                st.session_state.df_impxconc = df_impxconc

            if st.session_state.df_impretxcon is None and df_impretxcon is not None:
                st.session_state.df_impretxcon = df_impretxcon

            if st.session_state.df_impuestos is None and df_impuestos is not None:
                st.session_state.df_impuestos = df_impuestos

            if st.session_state.df_impuestos_ret is None and df_impuestos_ret is not None:
                st.session_state.df_impuestos_ret = df_impuestos_ret

            if st.session_state.rfc_filtro is None and rfc_filtro is not None:
                st.session_state.rfc_filtro = rfc_filtro


            
            st.divider()
            
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12 = st.tabs(["RESUMEN", "Total CFDIs", "Ingresos", "Egresos", "Nomina", "Complementos de Pago", "Metadata",
                                                                                            "Conceptos", "Imp x Concepto", "Imp Ret x Conc", "Impuestos Totales", "Impuestos Retenidos"])

            with tab1:
                st.header("Resumen")
                resumen_ing_chart = pd.DataFrame(CFDIs)
                resumen_ing_chart = resumen_ing_chart[(resumen_ing_chart['RFCEmisor'] == rfc_filtro) & ((resumen_ing_chart['TipoDeComprobante'] == "I"))]
                resumen_ing_chart = resumen_ing_chart[resumen_ing_chart['Estatus_Meta'] != "0"]
                resumen_ing_chart = resumen_ing_chart.groupby(by=['Año', 'Mes'], as_index=False)['SubTotal'].sum()
                fig = px.bar(resumen_ing_chart, x='Mes', y='SubTotal', color='Año', barmode='group', labels={'SubTotal': 'Suma del SubTotal', 'Mes': 'Mes', 'Año': 'Año'}, title='Suma del Subtotal por Mes y Año', height=400, width=800)
                # barmode='group',
                # Muestra el gráfico
                st.write(fig)
            
            with tab2:
                st.subheader("Total de CFDIs")
                st.caption('Detalle de los CFDIs procesados')
                st.caption('CFDIs Version 3.3 y 4.0')
                st.write(CFDIs.shape)
                st.dataframe(CFDIs, height=600)
                st.subheader("EFOS")
                st.caption('EFOS')
                st.caption('EFOS')
                st.write(EFOS.shape)
                st.dataframe(EFOS, height=600)

                
            with tab3:
                st.subheader("CFDIs de Ingresos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_ingresos = pd.DataFrame(CFDIs)
                cfdi_ingresos = cfdi_ingresos[(cfdi_ingresos['RFCEmisor'] == rfc_filtro) & ((cfdi_ingresos['TipoDeComprobante'] == "I"))]
                st.write(cfdi_ingresos.shape)
                st.dataframe(cfdi_ingresos, height=600)
                resumen_ing = cfdi_ingresos[cfdi_ingresos['Estatus_Meta'] != "0"]
                resumen_ing = resumen_ing.groupby(by=['RFCEmisor', 'Año', 'Mes'], as_index=False).agg({'SubTotal': 'sum','Total': 'sum'})
                st.dataframe(resumen_ing, height=600)
                
            with tab4:
                st.subheader("CFDIs de Egresos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_egresos = pd.DataFrame(CFDIs)
                cfdi_egresos = cfdi_egresos[(cfdi_egresos['RFCReceptor'] == rfc_filtro) & (cfdi_egresos['TipoDeComprobante'] != "P")]
                st.write(cfdi_egresos.shape)
                st.dataframe(cfdi_egresos, height=600)
                resumen_eg = cfdi_egresos[cfdi_egresos['Estatus_Meta'] != "0"]
                resumen_eg = resumen_eg.groupby(by=['RFCReceptor', 'Año', 'Mes'], as_index=False).agg({'SubTotal': 'sum','Total': 'sum'})
                st.dataframe(resumen_eg, height=600)
                
            with tab5:
                st.subheader("CFDIs de Nomina")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_nomina = pd.DataFrame(CFDIs)
                cfdi_nomina = cfdi_nomina[(cfdi_nomina['RFCEmisor'] == rfc_filtro) & (cfdi_nomina['TipoDeComprobante'] == "N")]
                st.write(cfdi_nomina.shape)
                st.dataframe(cfdi_nomina, height=600)

            with tab6:
                st.subheader("CFDIs Complementos de Pago Recibidos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_comp_pago = pd.DataFrame(CFDIs)
                cfdi_comp_pago = cfdi_comp_pago[(cfdi_comp_pago['RFCReceptor'] == rfc_filtro) & (cfdi_comp_pago['TipoDeComprobante'] == "P")]
                st.write(cfdi_comp_pago.shape)
                st.dataframe(cfdi_comp_pago, height=600)
                resumen_comp_pago = pd.DataFrame(cfdi_comp_pago)
                resumen_comp_pago = resumen_comp_pago.groupby(by=['DocRelacionado', 'Año', 'Mes'], as_index=False).agg({'SubTotal': 'sum','Total': 'sum','ImportePagado': 'sum'})
                st.dataframe(resumen_comp_pago)

            with tab7:
                st.subheader("Metadata")
                st.caption('Detalle de la Metadata')
                st.write(metadata.shape)
                st.dataframe(metadata)
                st.divider()

                st.caption('Metadata Ing')
                metadata_ing = metadata[metadata['RfcEmisor_Meta'] == rfc_filtro]
                st.dataframe(metadata_ing)
                st.divider()
                
                st.caption('Metadata Eg')
                metadata_eg = metadata[metadata['RfcReceptor_Meta'] == rfc_filtro]
                st.dataframe(metadata_eg)
                st.divider()
                
                st.caption('Resumen Metadata Ing')
                def monto_nomina(row):
                    if row['EfectoComprobante_Meta'] == 'N':
                        return row['Monto_Meta']
                    else:
                        return None
                resumen_metadata_ing = pd.DataFrame(metadata_ing)
                resumen_metadata_ing['Monto_Meta_Nom'] = resumen_metadata_ing.apply(monto_nomina, axis=1)
                resumen_metadata_ing = resumen_metadata_ing.groupby(by=['RfcEmisor_Meta', 'Año_Meta', 'Mes_Meta'], as_index=False).agg({'Monto_Meta_Vig': 'sum','Monto_Meta_Canc': 'sum','Monto_Meta_Nom': 'sum'})
                st.dataframe(resumen_metadata_ing)
                
                st.caption('Resumen Metadata Eg')
                resumen_metadata_eg = metadata_eg.groupby(by=['RfcReceptor_Meta', 'Año_Meta', 'Mes_Meta'], as_index=False).agg({'Monto_Meta_Vig': 'sum','Monto_Meta_Canc': 'sum'})
                st.dataframe(resumen_metadata_eg)

            with tab8:
                st.subheader("Conceptos")
                st.caption('Detalle de la Metadata')
                df_conceptos = pd.concat(conceptos, ignore_index=True)
                st.write(df_conceptos.shape)
                st.dataframe(df_conceptos)

            with tab9:
                st.subheader("Impuestos por concepto")
                st.caption('Detalle de la Metadata')
                
                st.write(df_impxconc.shape)
                st.dataframe(df_impxconc)

            with tab10:
                st.subheader("Impuestos Retenidos por concepto")
                st.caption('Detalle de la Metadata')
                st.write(df_impretxcon.shape)
                st.dataframe(df_impretxcon)

            with tab11:
                st.subheader("Impuestos Totales")
                st.caption('Detalle de la Metadata')
                st.write(df_impuestos.shape)
                st.dataframe(df_impuestos)

            with tab12:
                st.subheader("Impuestos Retenidos")
                st.caption('Detalle de la Metadata')
                st.write(df_impuestos_ret.shape)
                st.dataframe(df_impuestos_ret)


            
            
            # st.write(df_conceptos.shape)
            # st.dataframe(df_conceptos)

            # st.write(df_impxconc.shape)
            # st.dataframe(df_impxconc)

            # st.write(df_impretxcon.shape)
            # st.dataframe(df_impretxcon)

            # st.write(df_impuestos.shape)
            # st.dataframe(df_impuestos)

            # st.write(df_impuestos_ret.shape)
            # st.dataframe(df_impuestos_ret)


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
                    metadata.to_excel(writer, sheet_name='Metadata')
                    metadata_ing.to_excel(writer, sheet_name='Metadata Ing')
                    metadata_eg.to_excel(writer, sheet_name='Metadata Eg')
                    resumen_metadata_ing.to_excel(writer, sheet_name='Resumen Meta Ing')
                    resumen_metadata_eg.to_excel(writer, sheet_name='Resumen Meta Eg')
                    df_conceptos.to_excel(writer, sheet_name='Conceptos')
                    df_impxconc.to_excel(writer, sheet_name='Imp x Conc')
                    df_impretxcon.to_excel(writer, sheet_name='Imp Ret x Conc')
                    df_impuestos.to_excel(writer, sheet_name='Impuestos Tot')
                    df_impuestos_ret.to_excel(writer, sheet_name='Impuestos Ret Tot')



                    # Close the Pandas Excel writer and output the Excel file to the buffer
                    writer.save()

                # Set up download link
                b64 = base64.b64encode(buffer.getvalue()).decode()
                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="CFDIs_{rfc_filtro}.xlsx">Download Excel File</a>'
                st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
