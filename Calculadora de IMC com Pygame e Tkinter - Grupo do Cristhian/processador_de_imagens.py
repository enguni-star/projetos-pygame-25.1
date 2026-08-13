# Arquivo: processador_de_imagens.py

from PIL import Image
import os

def processar_imagens():
    print("Iniciando processamento das imagens...")
    nomes_originais = ["abaixo", "ideal", "sobrepeso", "obesidade"]

    # MODIFICADO AQUI: O tamanho final das imagens que serão criadas
    tamanho_final = (350, 350)

    for nome in nomes_originais:
        arquivo_original = f"{nome}.png"
        arquivo_final = f"{nome}_final.png"

        try:
            print(f"Processando '{arquivo_original}'...")
            with Image.open(arquivo_original) as img:
                img_rgba = img.convert("RGBA")
                bbox = img_rgba.getbbox()

                if bbox:
                    img_cortada = img.crop(bbox)
                else:
                    img_cortada = img

                nova_imagem = Image.new("RGBA", tamanho_final, (0, 0, 0, 0))

                largura_cortada, altura_cortada = img_cortada.size
                pos_x = (tamanho_final[0] - largura_cortada) // 2
                pos_y = (tamanho_final[1] - altura_cortada) // 2

                nova_imagem.paste(img_cortada, (pos_x, pos_y), img_cortada.convert("RGBA"))
                nova_imagem.save(arquivo_final)
                print(f"  => '{arquivo_final}' criada com sucesso!")

        except FileNotFoundError:
            print(f"ERRO: Arquivo '{arquivo_original}' não encontrado.")
        except Exception as e:
            print(f"ERRO ao processar '{arquivo_original}': {e}")

    print("\nProcessamento concluído!")

if __name__ == "__main__":
    processar_imagens()