from geopy.geocoders import Nominatim
import pandas

# transforma o relatorio GESAC em um arquivo .txt, com os dados necessários para prosseguir com as buscas
def createListGesac(nomeArquivo):
    tabela = pandas.read_excel(nomeArquivo)

    #codgesac, situacao, codibge, logradouro, cidade, UF, bairro
    for (codgesac, situacao, codibge, logradouro, cidade, UF, bairro) in zip(tabela.CDGESAC, tabela.situacao, tabela.CDMunicipioIBGE, tabela.DSLogradouro, tabela.NOMunicipio, tabela.SGUnidadeFederacao, tabela.DSBairro):
        arq = open("listGesac.txt", "a")
        arq.write(str(codgesac)+","+str(situacao)+","+str(codibge)+","+str(logradouro)+","+str(cidade)+","+str(UF)+","+str(bairro)+"\n")
        arq.close()
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
            coluna = data.split(" ")
            arq1.write(coluna[9][:5]+"\n")
            arq1.close()
        elif data[:len(erro2):] == "Erro de carga: Coordenadas inválidas registro ":
            arq1 = open("tabelaErro-CodGesac.txt", "a")
            coluna = data.split(" ")
            arq1.write(coluna[6][:5]+"\n")
            arq1.close()
        elif data[:len(erro3):] == "Erro de carga: Registro contem coordenada com valor NULL:  ":
            arq1 = open("tabelaErro-CodGesac.txt", "a")   
            coluna = data.split(" ")
            arq1.write(coluna[10][:5]+"\n")
            arq1.close()
        
    f.close()
    return

#Compara 'listGesac.txt' com 'tabelaErro' e verifica quais elementos de 'tabelaErro'
#apresentam os status de situacao: 
#   'Aguardando Remanejamento', 
#   'Instalação Executada',
#   'Instalado', 
#   'Remanejamento Executado',
#   'Remanejamento Solicitado'.
def buscaPontosInstalados():
    f = open('tabelaErro-CodGesac.txt', 'r')
    tabelaErro = f.read()
    rowsTabelaErro = tabelaErro.split('\n')
    f.close()
    
    f = open('listGesac.txt', 'r')
    tabelaGesac = f.read()
    rowsTabelaGesac = tabelaGesac.split('\n')
    f.close()
    
    for erro in rowsTabelaErro:
        for gesac in rowsTabelaGesac:
            colunasGesac = gesac.split(",")
            if (erro == colunasGesac[0]) and colunasGesac[1] == 'Aguardando Remanejamento':
                arq = open('tabelaErro-Instalados.txt', 'a')
                arq.write(gesac+'\n')
                arq.close()
            elif (erro == colunasGesac[0]) and colunasGesac[1] == 'Instalação Executada':
                arq = open('tabelaErro-Instalados.txt', 'a')
                arq.write(gesac+'\n')
                arq.close()   
            elif (erro == colunasGesac[0]) and colunasGesac[1] == 'Instalado':
                arq = open('tabelaErro-Instalados.txt', 'a')
                arq.write(gesac+'\n')
                arq.close()
            elif (erro == colunasGesac[0]) and colunasGesac[1] == 'Remanejamento Executado':
                arq = open('tabelaErro-Instalados.txt', 'a')
                arq.write(gesac+'\n')
                arq.close()
            elif (erro == colunasGesac[0]) and colunasGesac[1] == 'Remanejamento Solicitado':
                arq = open('tabelaErro-Instalados.txt', 'a')
                arq.write(gesac+'\n')
                arq.close()
    
    return

def findLatLong(logradouro, cidade, UF, bairro):

    geolocator = Nominatim(user_agent="mccom")
    location = geolocator.geocode(logradouro + ", " + cidade +", "+ UF + " - " +bairro)

    return location.latitude, location.longitude



if __name__ == '__main__':
    # tabelaGesac = 'Relatório GESAC 2021-01-25 9h44min + Contatos.xlsx'
    # createListGesac(tabelaGesac)
    
    # tabelaErro = 'Resultado carga - 2021-01-23_06-01-42_GESAC.log'
    # filtroTabelaErroCodGesac(tabelaErro)
    
    # buscaPontosInstalados()
    
    latitude, longitude = findLatLong("", "Porto Velho", "RO", "-")
    print(latitude, longitude)
