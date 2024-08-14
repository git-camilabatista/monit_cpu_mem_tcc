# sudo apt install sysstat
# ➜ pidstat -r -u -p 24038 10 > monit_fastapi.log 
# Temos que pegar a coluna RSS e não VSZ
import matplotlib.pyplot as plt


def main():
    memory_x = []
    memory_y = []

    cpu = {}

    with open('monit_fastapi.log', 'r') as arquivo:
        #ignora a primeira linha
        next(arquivo)
        #ignora a segunda linha que é vazia
        next(arquivo)
        linhas = arquivo.readlines()
        for linha in linhas:
            # Ignora quebra de linha e a média
            if linha == '\n' or 'Average' in linha:
                continue

            if 'CPU' in linha:
                _type = 'cpu'
                continue
            elif 'MEM' in linha:
                _type = 'men'
                continue

            list_linha = linha.replace('\n', '').split()
            if _type == 'cpu':
                if cpu.get(list_linha[9]):
                    cpu[list_linha[9]]['x'].append(list_linha[0])
                    cpu[list_linha[9]]['y'].append(list_linha[8])
                else:
                    cpu[list_linha[9]] = {'x': [list_linha[0]], 'y': [list_linha[8]]}
            else:
                memory_x.append(list_linha[0])
                memory_y.append(round(int(list_linha[7])/1024, 2))

    # Combine e ordene os valores do eixo X
    all_x_values = sorted(set(x for v in cpu.values() for x in v['x']))

    # Função para alinhar os valores de y com os valores combinados e ordenados de x
    def align_series(x, y, all_x):
        y_dict = dict(zip(x, y))
        return [float(y_dict.get(x, 'nan').replace(',', '.')) if y_dict.get(x) is not None else float('nan') for x in all_x]

    # Criação da figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

    for key, value in cpu.items():
        serie_y_aligned = align_series(cpu[key]['x'], cpu[key]['y'], all_x_values)
        ax1.plot(all_x_values, serie_y_aligned, marker='o')
        x_values = value['x']
        y_values = [float(y.replace(',', '.')) for y in value['y']]  # Convertendo para float e trocando vírgula por ponto
        ax1.plot(x_values, y_values, label=f'CPU {key}', marker='o')

    # Gráfico para a Série 1
    ax1.set_title('CPU Consume')
    # ax1.set_xlabel('Time')
    ax1.set_ylabel('%')
    ax1.legend()
    ax1.grid(True)
    ax1.set_xticks(all_x_values)  # Define os rótulos do eixo X explicitamente
    ax1.set_xticklabels(all_x_values, rotation=35, ha='right')

    ax2.plot(memory_x, memory_y, label='Memory Consume', marker='o')
    ax2.set_title('Memory Consume')
    # ax2.set_xlabel('Time')
    ax2.set_ylabel('MB')
    ax2.legend()
    ax2.grid(True)
    ax2.set_xticks(memory_x)  # Define os rótulos do eixo X explicitamente
    ax2.set_xticklabels(memory_x, rotation=35, ha='right')

    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    main()