import os
import subprocess
import tempfile

def convert_to_opus_ogg(input_file, output_file=None, bitrate="32k", sample_rate=24000):
    """
    Converter um arquivo de áudio para formato Opus em um contêiner Ogg.
    
    Args:
        input_file (str): Caminho para o arquivo de áudio de entrada
        output_file (str, optional): Caminho para salvar o arquivo de saída. Se None, substitui a
                                    extensão do input_file por .ogg
        bitrate (str, optional): Taxa de bits alvo para codificação Opus (padrão: "32k")
        sample_rate (int, optional): Taxa de amostragem para a saída (padrão: 24000)
    
    Returns:
        str: Caminho para o arquivo convertido
        
    Raises:
        FileNotFoundError: Se o arquivo de entrada não existir
        RuntimeError: Se a conversão ffmpeg falhar
    """
    if not os.path.isfile(input_file):
        raise FileNotFoundError(f"Arquivo de entrada não encontrado: {input_file}")
    
    # If no output file is specified, replace the extension with .ogg
    if output_file is None:
        output_file = os.path.splitext(input_file)[0] + ".ogg"
    
    # Ensure the output directory exists
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Build the ffmpeg command
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-c:a", "libopus",
        "-b:a", bitrate,
        "-ar", str(sample_rate),
        "-application", "voip",  # Optimize for voice
        "-vbr", "on",           # Variable bitrate
        "-compression_level", "10",  # Maximum compression
        "-frame_duration", "60",     # 60ms frames (good for voice)
        "-y",                        # Overwrite output file if it exists
        output_file
    ]
    
    try:
        # Run the ffmpeg command and capture output
        process = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return output_file
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Falha ao converter áudio. Você provavelmente precisa instalar o ffmpeg {e.stderr}")


def convert_to_opus_ogg_temp(input_file, bitrate="32k", sample_rate=24000):
    """
    Converter um arquivo de áudio para formato Opus em um contêiner Ogg e armazenar em um arquivo temporário.
    
    Args:
        input_file (str): Caminho para o arquivo de áudio de entrada
        bitrate (str, optional): Taxa de bits alvo para codificação Opus (padrão: "32k")
        sample_rate (int, optional): Taxa de amostragem para a saída (padrão: 24000)
    
    Returns:
        str: Caminho para o arquivo temporário com o áudio convertido
        
    Raises:
        FileNotFoundError: Se o arquivo de entrada não existir
        RuntimeError: Se a conversão ffmpeg falhar
    """
    # Create a temporary file with .ogg extension
    temp_file = tempfile.NamedTemporaryFile(suffix=".ogg", delete=False)
    temp_file.close()
    
    try:
        # Convert the audio
        convert_to_opus_ogg(input_file, temp_file.name, bitrate, sample_rate)
        return temp_file.name
    except Exception as e:
        # Clean up the temporary file if conversion fails
        if os.path.exists(temp_file.name):
            os.unlink(temp_file.name)
        raise e


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python audio.py arquivo_entrada [arquivo_saida]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    try:
        result = convert_to_opus_ogg_temp(input_file)
        print(f"Convertido com sucesso para: {result}")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)
