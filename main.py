from geopy.geocoders import Nominatim
import pandas

# transforma o relatorio GESAC em um arquivo .txt, com os dados necessários para prosseguir com as buscas
def createListGesac(nomeArquivo):
    tabela = pandas.read_excel(nomeArquivo)

    #codgesac, situacao, codibge, logradouro, cidade, UF, bairro
    for (codgesac, situacao, codibge, logradouro, cidade, UF, bairro) in zip(tabela.CDGESAC, tabela.situacao, tabela.CDMunicipioIBGE, tabela.DSLogradouro, tabela.NOMunicipio, tabela.SGUnidadeFederacao, tabela.DSBairro):
        arq1 = open("listGesac.txt", "a")
        arq1.write(str(codgesac)+","+str(situacao)+","+str(codibge)+","+str(logradouro)+","+str(cidade)+","+str(UF)+","+str(bairro)+"\n")
        arq1.close()
    return

# pega apenas os CODGESAC do log de erro
def filtroTabelaErroCodGesac(nomeArquivo):
    f = open(nomeArquivo, 'r')
    arq = f.read()
    rows = arq.split('\n')
    
    erro1 = "Erro de carga: Não encontrei o setor no registro "
    erro2 = "Erro de carga: Coordenadas inválidas registro "
    erro3 = "Erro de carga: Registro contem coordenada com valor NULL:  "
    
    for data in rows:
        if data[:len(erro1):] == "Erro de carga: Não encontrei o setor no registro ":
            arq1 = open("tabelaErro-CodGesac.txt", "a")
            data1 = data.split(" ")
            arq1.write(data1[9][:5]+"\n")
            arq1.close()
        elif data[:len(erro2):] == "Erro de carga: Coordenadas inválidas registro ":
            arq2 = open("tabelaErro-CodGesac.txt", "a")
            data1 = data.split(" ")
            arq2.write(data1[6][:5]+"\n")
            arq2.close()
        elif data[:len(erro3):] == "Erro de carga: Registro contem coordenada com valor NULL:  ":
            arq3 = open("tabelaErro-CodGesac.txt", "a")   
            data1 = data.split(" ")
            arq3.write(data1[10][:5]+"\n")
            arq3.close()
        
    f.close()
    return

def buscaPontosInstalados():
    
    return

def findLatLong(logradouro, cidade, UF, bairro):

    geolocator = Nominatim(user_agent="mccom")
    location = geolocator.geocode(logradouro + ", " + cidade +", "+ UF + " - " +bairro)

    return location.latitude, location.longitude



if __name__ == '__main__':
    # tabelaGesac = 'Relatório GESAC 2021-01-25 9h44min + Contatos.xlsx'
    # createListGesac(tabelaGesac)
    
    tabelaErro = 'Resultado carga - 2021-01-23_06-01-42_GESAC.log'
    filtroTabelaErroCodGesac(tabelaErro)
    
    # location = findLatLong("", "Taguatinga", "TO", "Zona Rural")
    # print(location)
