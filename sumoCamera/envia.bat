@echo off
@REM scp -r * banana@192.168.1.129:~\seguidorCamera
@REM ssh banana@192.168.1.129 "killall main.py"
scp -r * banana@10.182.113.193:~\sumoCamera
ssh banana@10.182.113.193 "killall main.py"
@REM ssh banana@192.168.2.151 "bash ~/testeBanana/executa.sh" || (
@REM     echo "Interrupção detectada! Enviando sinal para o script remoto..."
@REM     ssh banana@192.168.2.151 "bash ~/testeBanana/stop.sh"
@REM )