import pytest
from project import coletar, selecionar_formato, exportar_csv, exportar_excel

data = [{'CRM': '12882-BA', 'Nome': 'Ademar Ferreira da Silva Júnior', 'Inscrição': 'Principal', 'Situação': 'Regular'}]
pesquisa = ['são paulo', 'neurocirurgia', 'principal', 'ativo']

def test_selecionar_formato():
    assert selecionar_formato('csv', data, pesquisa) == "⭐ EXPORTADO PARA .CSV COM SUCESSO ⭐"
    assert selecionar_formato('excel', data, pesquisa) == "⭐ EXPORTADO PARA .XLSX COM SUCESSO ⭐"
    with pytest.raises(ValueError):
        selecionar_formato('xlsx', data, pesquisa)

def test_exportar_csv():
    assert exportar_csv(data, pesquisa) == 'cfm_neurocirurgia_sp.csv'
    with pytest.raises(ValueError):
        exportar_csv(pesquisa, data)

def test_exportar_excel():
    assert exportar_excel(data, pesquisa) == 'cfm_neurocirurgia_sp.xlsx'
    with pytest.raises(ValueError):
        exportar_csv(pesquisa, data)