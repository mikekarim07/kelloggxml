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
    page_icon="<svg xmlns="http://www.w3.org/2000/svg" width="2500" height="917" viewBox="0 .004 823 301.996" id="kellogg"><path fill="#fff" d="M674.031 137.043c0-.15-.129-.336-.129-.521.186.093.371.121.521.215-.085.155-.278.22-.392.306m100.844-31.841c-10.035-10.621-24.849-13.978-38.77-8.778-2.921 1.107-5.728 2.343-8.521 3.664.058-.307.179-.671.207-1.043 0 .058.243-1.171.243-1.171.957-4.807 2.192-11.521-1.443-20.542-8.006-19.556-20.513-21.927-32.641-22.599h-.1c-12.778-.679-28.263 9.514-32.577 21.37-1.785 4.614-2.649 9.179-2.649 13.578 0 6.742 2.271 13.12 6.5 18.999-1.693 3.114-3.172 6.649-3.172 10.807v.313c-.343-.221-.65-.343-.985-.557-2.864-10.406-11.643-17.242-21.956-16.721-21.37 1.079-42.434 9.606-59.989 23.342a24.822 24.822 0 0 0-2.649-6.343c-4.743-8.192-13.421-12.721-23.148-11.885-2.5.243-5.021.893-7.55 1.722-2.064-1.415-4.528-2.864-8.128-3.664-15.156-3.329-27.349 1.507-37.141 5.385-7.879 3.114-14.742 5.764-23.435 5.021-3.192-.308-8.242-1.693-12.778-3.015-7.449-2.093-14.471-4.192-21.091-3.664-1.136.029-2.157.215-3.229.429-5.671-4.156-12.813-5.878-20.785-4.614-2.593.4-5.206 1.021-7.82 1.665.335-.4.543-.736.707-1.2l5.6-8.835c8.042-12.507 16.999-26.513 16.999-46.533a85.26 85.26 0 0 0-.271-6.593c-1.078-10.685-6.043-16.813-10.014-20.013-5.357-4.278-12.35-6.157-19.613-5.328-20.685 2.492-39.883 13.949-56.568 29.748-3.235-5.821-8.249-9.364-13.185-11.578-41.568-18.32-83.267 33.934-104.758 73.538-.586-.585-1.078-1.207-1.664-1.728-5.171-4.436-11.457-6.929-18.199-7.45 16.813-13.456 32.184-29.284 43.727-50.075 3.264-5.907 4.906-12.313 4.906-18.478 0-4.828-.993-9.449-3.021-13.699C249.015 4.385 234.387-2.729 219.51.971c-10.964 2.707-18.749 9.606-23.428 14.842 0 .028-16.906 19.984-16.906 19.984-3.699 4.4-7.356 8.714-11.206 13.057-.214-1.321-.679-2.614-1.171-3.907-2.771-6.221-8.186-10.692-14.6-11.892l-1.535-.278-1.729.035c-19.549.186-34.148 9.764-47.083 18.228-5.207 3.45-10.128 6.686-15.399 9.393l-4.864 2.557-8.035 4.222-7.913 3.942c-16.935 8.464-34.42 17.148-48.369 33.748-6.935 8.156-10.378 17.427-10.378 26.205 0 6.621 1.843 12.899 5.692 18.385 3.079 4.25 7.058 7.386 11.707 9.485-8.8 9.299-16.756 19.948-21.92 33.104C.793 196.267 0 200.575 0 204.796c0 12.685 6.957 24.484 18.6 29.312 13.577 5.671 28.912 3.393 40.09-5.878 6.621-5.543 12.378-11.55 17.557-17.863.149 8.935 2.307 18.105 7.542 27.349 6.007 10.471 17.128 17.334 30.548 18.905 14.628 1.729 29.105-3.078 37.912-12.534 4.371-4.679 6.621-9.485 6.621-14.285 0-1.571-.314-3.143-.714-4.714 8.257 3.979 17.221 5.485 24.362 6.128 15.613 1.421 28.484-5.757 38.855-11.514.714-.436 1.414-.893 2.128-1.264 6.314 5.478 13.735 9.206 22.327 10.628 16.221 2.678 32.941-2.564 46.619-10.136 5.692 6.593 13.521 11.393 21.398 13.363 13.335 3.2 27.562 0 39.141-8.863a57.95 57.95 0 0 0 4-3.485c4.749 5.264 10.777 9.392 17.556 11.671 14.535 4.807 29.099 3.235 42.033-4.586 10.378-6.192 19.47-13.799 26.892-22.299 1.328 2.371 2.957 4.5 4.863 6.5-16.748 9.113-33.227 21.648-42.583 38.897-3.235 5.907-4.835 12.592-4.835 19.178 0 6.192 1.507 12.292 4.464 17.306 4.8 8.35 13.149 13.242 22.777 13.492 41.697 1.015 66.946-25.312 80.896-44.126-1.043 4.436-1.693 9.143-1.693 14.257v1.842c.278 13.521 10.285 25.534 23.806 28.577 26.763 6.129 45.697-10.156 55.925-18.999 13.186-11.206 23.092-24.662 32.584-37.69l11.271-14.935c2.928-3.692 10.777-8.928 18.812-13.856 1.479 2.771 3.136 5.328 5.328 7.942 5.021 6.071 11 10.192 17.648 12.32 18.257 5.821 37.412 2.894 52.662-7.82 14.499-10.192 24.291-23.87 30.112-41.762 2.192-6.985 2.649-13.792 2.649-20.106 0-2.307-.064-4.621-.093-6.771-.063-2.1-.063-4.064-.063-5.942 0-1.607.063-3.114.092-4.558 6.593-.957 16.471-3.635 21.492-14.627 1.664-3.515 2.507-7.243 2.507-10.907-.028-6.399-2.536-12.691-7.213-17.741"></path><path fill="#e2001a" d="M109.315 131.479c3.264 4.985 3.571 10.928 2 16.478-7.086 26.541-28.577 54.41-13.149 81.537 7.971 13.893 32.055 13.893 41.904 3.265 7.45-7.942-7.178 2-9.757-11.735-5.32-28.327 22.356-58.289 8.25-91.237 36.77-24.941 78.038-45.575 100.943-86.994 2.743-4.9 4.008-11.606 1.443-16.936-3.164-6.527-9.692-10.685-17.478-8.749-5.979 1.479-11.128 5.356-14.878 9.671-27.991 31.934-54.297 68.581-93.337 94.137l-5.941 10.563M107.565 128.922c-19.435 27.312-31.198 62.946-59.525 86.53-6.528 5.45-15.37 6.5-23.099 3.357-7.999-3.357-9.999-13.307-7.07-20.635 16.135-41.111 66.081-55.582 78.645-98.044.215-1.021-1.35-2.25-3.478-1.571-22.728 7.143-27.499 38.77-50.933 45.762-5.607 1.628-12.257.8-16.014-4.407-5.606-8.007-1.479-18.006 3.85-24.291C43.677 99.266 62.497 91.51 81.088 81.961c4.101-2.064 8.964-4.679 13.028-6.807 19.513-10.1 33.748-25.592 54.996-25.835 2.157.493 3.722 3.972 2.301 6.371-13.514 21.527-25.271 39.94-37.741 61.653-.408.822-6.478 10.958-6.107 11.579M692.959 71.268c9.299.557 13.892 1.414 18.198 12.32 2.064 4.957 1.2 7.729.25 12.499-1.729 9.364-22.605 30.698-32.298 24.606-1.943-1.336 2.021-6.164 4.114-9.7 1.521-2.621 1.114-5.728-.265-6.992-9.514-8.528-8.535-15.642-6.1-22.206 2.029-5.32 10.829-10.77 16.101-10.527"></path><path fill="#e2001a" d="M561.844 257.7c9.479-7.114 16.313-17.863 20.935-25.406 1.236-2.035-1.871.308-6.686 1.657-5.842 1.664-29.469 17.678-26.448 27.013.129.15 2.129 1.629 2.5 1.629 3.871-.358 6.578-2.58 9.699-4.893m141.492-64.825c11.979-8.807 18.35-29.869 14.014-45.019-8.442 3.2-23.349 15.764-33.291 25.37-11.892 11.521-1.85 2.492 4.258 4.192 5.628 1.629 13.541 9.636 9.691 13.735-1.414 1.508 2.771 3.601 5.328 1.722m-63.439-73.774c5.728-.308 7.578 9.913 2.55 11.978-16.871 7.149-47.391 15.428-48.348 41.568-.186 1.943 4.008 6.843 10.035 4.25 18.235-7.999 22.913-29.776 38.648-42.212 8.893-6.928 17.956 3.107 14.599 12.164-4.285 11.485-10.535 21.677-17.185 32.084-3.199 5.05 3.442 2 4.957 1.078 34.526-21.156 58.725-53.64 96.852-67.996 6.807-2.55 14.748-1.785 20.756 4.564 2.428 2.643 3.471 6.436 1.721 10.371-2.75 6.07-10.035 4.835-16.17 5.949-2.222.364-4.557 3.171-5.271 5.542-4.15 13.886.864 28.635-3.436 42.341-4.285 13.428-11.578 24.634-23.87 33.312-11.206 7.978-24.941 9.613-37.94 5.55-4.057-1.293-7.271-3.851-10.07-7.179-17.149-20.448 10.478-32.762-5.143-23.77-12.814 7.356-36.619 19.862-44.748 30.048-14.077 17.956-25.155 36.248-41.697 50.354-11.941 10.406-24.412 19.277-41.419 15.363-6.742-1.508-10.678-7.757-10.813-12.871-1.264-41.633 54.818-51.361 77.695-70.889-2.307-1.106-13.393 7.235-22.941 6.778-4.742-.186-12.092-1.021-15.856-6.936-6.406-10.277-5.05-21.056 0-30.354 14.89-27.589 44.174-49.401 77.094-51.087M192.867 160.334c4.1-5.635 8.042-12.163 8.285-18.384.093-3.636-.129-4.25-3.785-4-5.664.485-23.042 20.749-21.156 32.669.336 1.972 7.114-.771 7.793-1.235 3.349-2.593 6.884-6.25 8.863-9.05m92.623-44.804c9.057-12.164 16.32-21.835 19.928-30.584.242-.643-1.144-3.386-3.515-3.265-11.635.407-28.27 22.456-37.169 39.02-3.136 5.792-8.778 20.57-7.878 23.956 2.8 2.092 20.842-18.635 28.634-29.127m76.588-3.243c12.321-16.656 27.777-40.34 20.978-41.141-7.764-.214-36.44 30.791-46.626 61.775-.679 1.757-1.35 5.914-.679 5.6 4.922-1.786 18.813-16.042 26.327-26.234m-158.183 5.642c11.478-2.835 20.17 6.649 19.277 16.663-2.101 23.342-13.949 37.319-35.998 53.79-2.1 1.692.364 3.264 1.878 3.3 15.214.243 34.698-16.692 36.27-21.342 2.621-7.328 4.899-19.678 7.114-25.862 2.1-5.821 5.264-12.479 7.792-17.863 17.463-35.627 56.232-88.902 87.98-74.896 7.143 3.143 7.764 9.028 5.229 18.756-11.885 44.962-49.454 81.517-75.688 101.223-17.156 12.992 22.191 11.264 32.763 2.771 2.828-2.279 9.021-5.143 9.849-9.55 7.914-42.247 53.154-123.664 106.215-130.014 5.386-.643 10.407 2.007 11.242 10.442 2.058 21.956-9.734 34.334-20.091 51.946-18.413 31.105-42.155 49.861-65.061 73.511-4.192 4.399-3.114 15.605 9.078 16.963 5.207.557 10.163-2.336 14.228-2.679-.436 19.585-19.742 35.541-38.227 31.069-8.685-2.093-16.963-10.099-16.749-17.334.372-10.964-1.721-4.957-3.05-3.757-18.105 15.678-54.439 29.841-70.024 3.328-11.984 2.8-27.198 17.856-43.911 16.292-11.085-1.086-22.077-3.765-28.02-11.735-2.157-2.929-9.8 3.507-14.906.8-6.972-3.729-4.929-7.635-1.851-11.057 3.386-3.914 13.214-4.092 13.8-11.299 2.692-28.925 22.12-56.387 50.861-63.466"></path><path fill="#e2001a" d="M456.615 258.535c6.528-4.592 26.542-25.655 21.221-25.069-5.793.557-26.334 12.378-32.734 21.677-2.128 3.05-.899 5.914 2.243 6.436 3.264.221 6.621-1.144 9.27-3.044M538.318 129.9c-9.422 1.507-36.713 21.313-45.955 36.52-2.028 3.356-3.264 7.635-1.649 11.271 1.686 3.636 5.449 5.021 9.471 3.543 19.592-7.086 23.069-29.806 34.962-44.497 1.657-4.372 20.728-19.557 26.913-8.9 7.3 12.721-17.271 43.541-29.749 64.418-1.014 1.664-1.164 4.071 1.271 3.086 6.215-2.343 12.686-9.429 16.078-12.014 8.928 4.436-13.057 36.033-38.712 42.711-7.271 1.851-27.006 58.726-82.402 57.433-11.456-.243-13.578-15.492-8.192-25.47 14.32-26.513 52.354-40.983 70.703-46.525.307-.064 6.649-5.851 7.664-8.871.893-2.922-.579-1.757-1.515-1.386-12.62 5.699-24.284 8.313-33.798 1.414-19.377-13.885-.371-42.891 15.663-54.775-9.82.985-17.585.614-24.349-3.485-1.942-1.257-4.842 5.143-5.428 9.949-2.743 25.155-20.999 46.255-41.291 58.476-8.87 5.356-18.441 6.249-28.27 2.985-9.949-3.293-16.228-12.714-17.148-22.077-3.486-34.984 24.755-66.482 59.182-72.053 5.793-.957 10.071 1.292 12.75 7.506l-1.351 1.329c-16.077 5.328-27.862 21.613-33.105 33.562-2.557 5.792-7.299 22.391 5.357 19.862 19.677-3.878 29.534-31.655 26.142-45.204l.278-4.343c5.257-3.571 10.964-8.406 12.042-8.406h.336c7.085-.493 21.162 5.792 31.255 6.649 25.384 2.286 38.227-15.149 58.64-10.685 1.721.399 3.113 1.757 4.492 2.899 1.757 1.229 2.164 5.106 1.414 4.893-.157 0-1.242.129-1.699.185"></path><path d="M823 96.51c0-8.699-6.506-13.764-13.842-13.764-7.313-.021-13.792 5.014-13.792 13.714-.057 8.728 6.472 13.764 13.735 13.764 7.321-.008 13.821-5.044 13.899-13.714m-16.12-1.393v-3.593l2.229.078c1.214 0 2.786.051 2.786 1.622 0 1.614-.808 1.893-2.207 1.893h-2.808zm0 2.557h1.464l3.422 6.2h3.742l-3.742-6.479c1.942-.129 3.543-1.114 3.543-3.793 0-3.442-2.25-4.578-6.05-4.578h-5.543v14.85h3.164v-6.2zm12.099-1.164c0 6.35-4.536 10.549-9.871 10.549v-.05c-5.442.05-9.843-4.199-9.785-10.549 0-6.3 4.393-10.521 9.843-10.521 5.306-.001 9.813 4.214 9.813 10.571"></path></svg>",
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
    metodos_pago = pd.read_csv("mp.csv")
    prov69B = pd.read_excel("Listado_Completo_69-B.xlsx", engine='openpyxl')
    
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
            
            
            
            st.divider()
            
            tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11 = st.tabs(["Total CFDIs", "Ingresos", "Egresos", "Nomina", "Complementos de Pago", "Metadata",
                                                                                           "Conceptos", "Imp x Concepto", "Imp Ret x Conc", "Impuestos Totales", "Impuestos Retenidos"])
            
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
                resumen_ing = resumen_ing.groupby(by=['RFCEmisor', 'Año', 'Mes'], as_index=False).agg({'SubTotal': 'sum','Total': 'sum'})
                st.dataframe(resumen_ing, height=600)
                
            with tab3:
                st.subheader("CFDIs de Egresos")
                st.caption('Detalle de los CFDIs procesados')
                cfdi_egresos = pd.DataFrame(CFDIs)
                cfdi_egresos = cfdi_egresos[(cfdi_egresos['RFCReceptor'] == rfc_filtro) & (cfdi_egresos['TipoDeComprobante'] != "P")]
                st.write(cfdi_egresos.shape)
                st.dataframe(cfdi_egresos, height=600)
                resumen_eg = cfdi_egresos[cfdi_egresos['Estatus_Meta'] != "0"]
                resumen_eg = resumen_eg.groupby(by=['RFCReceptor', 'Año', 'Mes'], as_index=False).agg({'SubTotal': 'sum','Total': 'sum'})
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

            with tab7:
                st.subheader("Conceptos")
                st.caption('Detalle de la Metadata')
                df_conceptos = pd.concat(conceptos, ignore_index=True)
                st.write(df_conceptos.shape)
                st.dataframe(df_conceptos)

            with tab8:
                st.subheader("Impuestos por concepto")
                st.caption('Detalle de la Metadata')
                
                st.write(df_impxconc.shape)
                st.dataframe(df_impxconc)

            with tab9:
                st.subheader("Impuestos Retenidos por concepto")
                st.caption('Detalle de la Metadata')
                st.write(df_impretxcon.shape)
                st.dataframe(df_impretxcon)

            with tab10:
                st.subheader("Impuestos Totales")
                st.caption('Detalle de la Metadata')
                st.write(df_impuestos.shape)
                st.dataframe(df_impuestos)

            with tab11:
                st.subheader("Impuestos Retenidos")
                st.caption('Detalle de la Metadata')
                st.write(df_impuestos_ret.shape)
                st.dataframe(df_impuestos_ret)


            
            st.dataframe(metodos_pago)
            st.dataframe(prov69B)


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
