# SEGA Rally Revo no ROG Ally

Perfil para jogar a edição europeia de PC de SEGA Rally (2007), também conhecida como SEGA Rally Revo, no Bazzite. O jogo usa Direct3D 9 via Proton e DXVK. O perfil pede tela cheia a 1920 × 1080, em 16:9, com limite de 60 FPS.

## Instalação

1. Copie o conteúdo de `program files/SEGA/SEGA Rally` do seu próprio DVD para a pasta `game` ao lado dos scripts. Confirme que `game/SEGA Rally_SSE1.exe` existe.
2. Disponibilize o Proton 11.0 na biblioteca principal da Steam. No terminal, execute `chmod +x preparar.sh jogar.sh` e depois `./preparar.sh`. A preparação cria um prefixo próprio e copia as preferências de vídeo na primeira instalação.
3. Adicione `jogar.sh` à Steam como jogo não Steam. Nas propriedades do atalho, escolha a resolução 1920 × 1080 e deixe a compatibilidade forçada desativada. O próprio script inicia o Proton.
4. Abra o jogo pela biblioteca. As preferências e os dados de jogador ficam em `compatdata/pfx/drive_c/users/steamuser/Documents/SEGA Rally/Saved Games`. Os dados compartilhados ficam em `compatdata/pfx/drive_c/users/Public/Documents/SEGA Rally/Shared Data`. Preserve `compatdata` ao atualizar estes scripts.

O painel do carro permite escolher km/h em **Options → Display**. No ROG Ally, o contador mostrou 60 FPS em nove leituras ao longo de 24 segundos de uma corrida rápida em 1080p.

Este repositório contém apenas scripts e configuração. Os arquivos do jogo e as artes pertencem aos respectivos titulares.
