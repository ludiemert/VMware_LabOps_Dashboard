Projeto VMwre`s


Eu criaria um projeto de portfólio chamado VMware LabOps — Automação, Inventário e Observabilidade de Máquinas Virtuais.
A ideia é montar um laboratório com 1–3 VMs e desenvolver em Python uma ferramenta que:
- Descobre e inventaria VMs: nome, IP, sistema operativo, CPU, RAM, disco, estado.
- Liga, desliga e reinicia VMs com segurança.
- Cria snapshots antes de alterações e permite rollback.
- Executa verificações de saúde: espaço em disco, CPU, memória, serviços críticos e conectividade.
- Centraliza logs de automações e das VMs.
- Envia alertas quando algo falhar ou ultrapassar um limite.
- Gera relatórios simples em JSON/CSV/HTML.
O mais interessante para entrevista é que não será apenas “criei uma VM”: será uma pequena plataforma de operações, semelhante ao tipo de automação que equipas de infraestrutura usam no dia a dia.
Uma estrutura possível:
vmware-labops/
  scripts/
    inventory.py
    vm_power.py
    snapshot.py
    healthcheck.py
  logs/
  reports/
  config/
  tests/
  README.md
Tecnologias que eu usaria:
- VMware Workstation para o laboratório local. Se tiveres acesso a vCenter/ESXi, podes integrar depois com a API VMware (pyVmomi).
- Python com argparse ou Typer para criar uma CLI profissional.
- logging para registar ações, erros e auditoria.
- paramiko para executar comandos remotos por SSH nas VMs Linux.
- psutil para métricas locais e, mais tarde, Prometheus/Grafana para observabilidade.
- pytest para testes.
- Git/GitHub com um README claro e capturas de ecrã.
Eu começaria com duas VMs Linux pequenas:
1. monitoring-vm: corre os scripts Python.
2. target-vm: é a VM que vais monitorizar, configurar e recuperar.
Depois, evoluímos por fases:
1. Fundação — criar as VMs, rede, SSH por chave e Git.
2. Automação — script Python que entra na VM, recolhe métricas e grava logs estruturados.
3. Operações — snapshots, validações antes/depois de mudanças e rollback.
4. Alertas — por exemplo, alerta se disco passar 80%, serviço cair, ou SSH falhar.
5. Apresentação — dashboard ou relatório e uma demonstração de “incidente → deteção → correção → evidência nos logs”.
Uma demo excelente na entrevista seria:
“Eu simulei que o disco de uma VM ficou cheio. O LabOps detetou o problema, gravou o evento num log estruturado, enviou um alerta, executou uma rotina de diagnóstico e gerou um relatório da ação tomada. Antes de mudanças, cria um snapshot para permitir recuperação.”

Isso demonstra virtualização, Linux, Python, redes, automação, troubleshooting, logs, boas práticas e comunicação técnica — tudo num projeto pequeno, mas muito apresentável.
Eu evitaria começar logo por vCenter, Docker, Grafana e uma API web ao mesmo tempo. Primeiro fazemos uma versão funcional via terminal; depois adicionamos uma interface simples.


┌──────────────── VMware LabOps ────────────────┐
│  🟢 monitoring-vm       CPU 12%   RAM 46%     │
│  🟢 target-vm           CPU 34%   RAM 62%     │
│  🔴 web-server-vm       Disco 91%             │
├──────────────── Ação em execução ─────────────┤
│  14:32:05  Snapshot criado: target-vm         │
│  14:32:08  Reinício solicitado                │
│  14:32:28  SSH disponível — validação OK      │
└───────────────────────────────────────────────┘


Para o “tempo real”, o dashboard pode consultar as VMs a cada 3–10 segundos ou receber eventos imediatamente quando uma automação ocorre. Para um laboratório e entrevista, atualizar periodicamente já é ótimo e mais simples de explicar.
Sobre snapshots: pensa neles como uma “fotografia recuperável” do estado de uma VM naquele momento.
Antes de instalar algo, atualizar um sistema ou alterar uma configuração, a automação cria um snapshot:
VM saudável
   ↓
Snapshot: antes-da-atualizacao
   ↓
Alteração / atualização
   ↓
Funcionou? → manter a alteração
Falhou?    → rollback para o snapshot


Rollback significa voltar a VM para aquele estado guardado. Por exemplo: instalas uma atualização, o servidor deixa de arrancar ou a aplicação para de funcionar; então fazes rollback e a VM fica como estava antes da mudança.
Na prática, no projeto:
1. Clicas “Aplicar atualização”.
2. A ferramenta pede confirmação.
3. Cria um snapshot chamado pre-update-2026-10-14-1432.
4. Executa a mudança.
5. Verifica se a VM voltou a responder e se o serviço está ativo.
6. Se falhar, oferece ou executa o rollback.
7. Regista tudo nos logs e no dashboard.
Um detalhe técnico importante para mencionar numa entrevista: snapshots são excelentes para testes e recuperação rápida, mas não substituem backups. Deixar snapshots durante muito tempo pode consumir espaço e prejudicar desempenho.



O primeiro objetivo pode ser simples e já impressionante:
1. Dashboard lista duas VMs.
2. Mostra se estão ligadas ou desligadas.
3. Botões para ligar, desligar e reiniciar.
4. Cada ação fica gravada em logs.
5. O painel atualiza automaticamente e mostra o novo estado.
6. Depois adicionamos snapshots, health checks e gráficos de CPU/RAM/disco.
O Streamlit não substitui a automação; ele torna essa automação visível, controlável e apresentável.




Cronograma do VMware LabOps
Fase	Objetivo	Resultado
1. Ambiente	Instalar VMware e criar Ubuntu Server	Uma VM Linux real funcionando
2. Acesso remoto	Configurar rede, usuário e SSH	Você acessa a VM pelo terminal do Windows
3. Operação manual	Ligar, desligar, reiniciar e criar snapshot	Você entende cada ação antes de automatizar
4. Python CLI	Criar comandos Python e logs	Automação real pelo terminal
5. Monitoramento	Ler CPU, RAM, disco e estado da VM	Health check com dados reais
6. Dashboard	Criar interface Streamlit	Botões, cartões, métricas e logs ao vivo
7. Segurança	Confirmações, snapshots e rollback	Mudanças com recuperação segura
8. Portfólio	README, imagens e demonstração	Projeto pronto para entrevista



Ordem prática
Fase 1 — Criar o laboratório real
Assim que o VMware terminar de baixar, vamos:
1. Instalar o VMware Workstation Pro.
2. Baixar o Ubuntu Server.
3. Criar a VM labops-target.
4. Configurar RAM, CPU, disco e rede de modo leve.
5. Criar um snapshot inicial chamado clean-install.
Fase 2 — SSH
Vamos instalar e configurar o SSH no Ubuntu. Depois, do Windows, você fará algo como:
Windows terminal → conexão SSH → Ubuntu Server
Esse é um ponto muito importante para entrevista, porque é como administradores acessam servidores Linux remotamente.
Fase 3 — Automação com Python
Antes do dashboard, criaremos comandos pequenos:
python check_vm.py
python start_vm.py
python health_check.py
Eles vão:
- Verificar se a VM está ligada.
- Controlar a VM pelo VMware.
- Entrar por SSH no Ubuntu.
- Ler CPU, RAM e disco.
- Registrar cada resultado em logs.
Fase 4 — Dashboard real
Só depois de os comandos funcionarem no terminal, construiremos o Streamlit:
VMware LabOps Dashboard
 ├─ Status da VM
 ├─ Ligar / Desligar / Reiniciar
 ├─ Snapshot
 ├─ CPU / RAM / Disco
 └─ Logs ao vivo
Essa ordem é importante: primeiro fazemos a automação funcionar; depois criamos a tela bonita para controlá-la.
Meta inicial
Nossa primeira meta concreta será:
Criar uma VM Ubuntu Server, conectá-la por SSH pelo Windows e executar um comando Linux remotamente.

Quando isso estiver pronto, você já terá uma base real de virtualização, Linux, rede e administração remota.
Por enquanto, aguardamos o VMware terminar de baixar. Depois começamos a Fase 1.


Windows
└─ VMware Workstation
   └─ labops-target  ← nome do computador virtual
      └─ Ubuntu Server 26.04.1 LTS  ← Linux instalado dentro dele

      instal => ubuntu-26.04.1-live-server-amd64.iso

_______________________________________________
e a VMware =>

VMware Workstation Pro for Windows

https://support.broadcom.com/group/ecx/productfiles?subFamily=VMware%20Workstation%20Pro&displayGroup=VMware%20Workstation%20Pro%2026H1%20for%20Windows&release=26H1u1&os=&servicePk=546859&language=EN&freeDownloads=true


temos tudo o que precisamos:
- VMware Workstation Pro instalado.
- Ubuntu Server ISO baixado.

vamos criar o “computador virtual” chamado labops-target.
1. Abra o VMware Workstation.
2. Clique em Create a New Virtual Machine.
3. Não abra o ficheiro .iso diretamente pelo Windows.
4. Envie um print da próxima tela que aparecer.
Vamos configurar cada opção juntos: tipo de instalação, Ubuntu, disco, RAM, CPU e rede.

__________________________________________________

2 GB de RAM.
Por que 2 GB?
- Ubuntu Server não terá interface gráfica pesada.
- É suficiente para SSH, Python, logs e testes.
- Deixa bastante RAM para o Windows.
- Depois podemos reduzir para 1,5 GB se tudo funcionar bem.
____________________________________________
Use network address translation (NAT)
O NAT é a melhor escolha para nosso laboratório:
- A VM terá internet para instalar atualizações e ferramentas.
- Ela usa a conexão Wi‑Fi do seu Windows.
- Fica mais isolada e segura na sua rede doméstica.
- Ainda conseguiremos acessar a VM por SSH a partir do seu próprio Windows.
_______________________________________________
No trabalho, essa mesma decisão seria tomada conforme o tipo de servidor e a necessidade da empresa.
Exemplo:
Cenário	Disco virtual
Servidor pequeno de testes	20–40 GB, dinâmico
Servidor web	40–100 GB
Banco de dados	100 GB ou mais, com armazenamento rápido
Servidor de arquivos	Centenas de GB ou TB, com backup e espaço planejado


A lógica seria parecida:
Servidor físico / cluster VMware
└─ Datastore (armazenamento da empresa)
   └─ VM de produção
      ├─ Disco do sistema: Ubuntu + programas
      ├─ Disco de dados: aplicação ou ficheiros
      └─ Backup separado
No nosso laboratório, o “datastore” é simplesmente a pasta no disco do seu notebook. Em uma empresa, normalmente seria um armazenamento central da infraestrutura VMware.

__________________________________________

VM:
- Nome: labops-target
- Ubuntu 64-bit
- Disco: 20 GB dinâmico
- RAM: 2048 MB
- Rede: NAT
- ISO do Ubuntu conectada
Deixe marcada a opção:
Power on this virtual machine after creation
Ela fará a VM ligar logo após ser criada e iniciará a instalação do Ubuntu.
____________________________________
Já fizemos:
- VMware Workstation instalado.
- VM labops-target criada.
- Ubuntu Server instalado.
- 2 GB RAM, 1 CPU e disco virtual de 20 GB.
- Rede NAT configurada.
- OpenSSH instalado.
- Login no servidor pelo console VMware.
- SSH do Windows para a VM.

Ainda vamos implementar:
- Python para controlar e monitorar.
- Logs.
- Streamlit dashboard.
- Métricas, snapshots, rollback e relatórios.
_____________________________________________________________

Um snapshot não é uma foto comum e não é uma pasta criada para você usar. Pense nele como um ponto de retorno da VM:
Estado atual saudável da VM
        ↓
baseline-ssh-ready  ← ponto salvo
        ↓
Futuras mudanças: Python, automação, testes…

Ele registra o estado do disco virtual naquele momento e o VMware passa a guardar as mudanças futuras separadamente. Se algo der errado depois, poderemos voltar a este ponto.
Após clicar em Take Snapshot, veja-o em:
VM → Snapshot → Snapshot Manager
Ou use o atalho:
Ctrl + M
Lá aparecerá uma árvore com baseline-ssh-ready e o estado atual da VM.
Os arquivos técnicos do snapshot ficam junto dos arquivos internos da VM no Windows; não precisamos abrir, mover nem enviar esses arquivos ao Git. E lembre: snapshot é recuperação rápida para testes, não substitui backup — ele pode crescer e ocupar espaço conforme você altera a VM.


baseline-ssh-ready
→ antes de configurar uma ferramenta nova
→ antes de testar uma automação que altera o sistema
→ antes de mudanças grandes de rede ou serviços


snapshot => VMare
Os botões principais:
- Take Snapshot…: cria outro ponto de retorno.
- Go To: volta para o snapshot selecionado. Não clique agora, pois não precisamos reverter nada.
- Delete: remove um snapshot antigo; usaremos apenas quando ele deixar de ser útil.
- Close: fecha somente esta janela, sem alterar a VM.
_________________________________________
Hoje você entra usando senha:
Windows PowerShell → SSH → Ubuntu VM
Mas um programa Python não deve guardar sua senha. Então vamos configurar uma chave SSH:
Windows private key  ──> fica protegida no seu computador
Windows public key   ──> autorizada dentro da VM Ubuntu
Depois disso, o Python poderá consultar a VM sem pedir senha a cada execução. Isso é uma prática profissional e será a ponte entre a infraestrutura que você criou e a automação.
O caminho do projeto será:
1. Configurar chave SSH para automação
2. Criar o ambiente Python do projeto no Windows
3. Fazer um script pequeno de health check via SSH
4. Salvar resultados em logs
5. Mostrar as métricas no Streamlit
6. Adicionar controles de VM, snapshots e relatórios
Então, o próximo passo concreto é criar sua chave SSH no Windows e adicionar somente a chave pública à VM.
___________________________________________________________

Já temos:
Windows + VMware Workstation + Ubuntu VM + NAT + OpenSSH + SSH test + baseline snapshot

Agora vamos preparar o acesso que o Python usará no futuro:
Windows → SSH key → Ubuntu VM

Hoje você aprenderá o que é uma chave SSH, como ela substitui a senha do Ubuntu para conexões automatizadas e como testar esse acesso com segurança.

O primeiro passo é criar a chave no PowerShell do Windows, fora da sessão SSH. A VM pode estar ligada ou desligada para criar a chave; só precisaremos ligá-la na etapa de copiar a chave pública.

Digite:
ssh-keygen -t ed25519 -f "$HOME\.ssh\labops_ed25519" -C "labops-dashboard@windows"

Quando pedir uma passphrase, crie uma frase-senha forte. Não use nem envie a senha do Ubuntu e não mostre essa frase em captura de tela.

Ao terminar, mostre apenas a tela com o resultado. Em seguida, vamos:
1. Ligar a VM e confirmar seu IP atual
2. Copiar a chave pública para o Ubuntu
3. Testar o login SSH por chave
4. Só então iniciar o ambiente Python do projeto
_____________________________________________

Agora estamos prontos para copiar a chave pública para a VM. No PowerShell do Windows — não dentro do Ubuntu — execute:
scp "$HOME\.ssh\labops_ed25519.pub" labops@192.168.26.129:/tmp/labops_ed25519.pub

Ele pedirá a senha atual do usuário labops uma última vez para fazer a cópia. Essa operação envia somente a chave pública, nunca a chave privada.

_______________________________

A chave pública saiu do Windows e está agora, temporariamente, neste local dentro da VM:
/tmp/labops_ed25519.pub
Sua chave privada ficou protegida no Windows e não foi enviada.
Agora, no PowerShell, conecte novamente à VM:
ssh labops@192.168.26.129


Primeiro você precisa entrar na VM novamente. No PowerShell, digite:
ssh labops@192.168.26.129
Depois do login, o início da linha mudará para:
labops@labops-target:~$


PS C:\Users\user>                 ← Windows
ssh labops@192.168.26.129         ← abre conexão SSH
labops@labops-target:~$           ← agora você está na VM
mkdir -p ~/.ssh                   ← comando dentro da VM


Quando aparece:
labops@labops-target:~$
isso significa:
labops          = usuário conectado no Ubuntu
labops-target   = nome da VM Ubuntu
~               = pasta pessoal do usuário labops no Ubuntu
$               = usuário comum, não root


Então você está usando uma janela do PowerShell no Windows, mas os comandos enviados depois desse prompt são executados dentro da VM Ubuntu por SSH.
Seu computador físico
└── Windows
    └── PowerShell
        └── SSH pela rede
            └── VM VMware
                └── Ubuntu: labops@labops-target:~$
________________________________

Pense assim:
Senha do Ubuntu = senha normal da porta do servidor
Chave privada   = sua chave física, guardada no Windows
Chave pública   = autorização instalada na porta do Ubuntu
Passphrase      = senha para abrir o cofre onde sua chave física fica guardada

Hoje, o Ubuntu ainda aceita você pela senha normal:
PowerShell → SSH → senha de labops → Ubuntu
Estamos preparando uma segunda forma de entrada:
PowerShell/Python → chave privada no Windows
                → Ubuntu confere a chave pública autorizada
                → acesso como labops

_______________________________________________

Nossa sequência será:
1. Ligar a VM e descobrir o IP atual
2. Entrar na VM pelo PowerShell com a senha normal
3. Autorizar a chave pública dentro do Ubuntu
4. Sair e testar o acesso usando a chave
5. Criar um snapshot novo, se o teste funcionar

______________________________

criar a pasta segura onde o Ubuntu guarda as chaves autorizadas. Ainda dentro desse mesmo prompt, digite:
mkdir -p ~/.ssh
Esse comando cria a pasta oculta .ssh na pasta pessoal de labops. O -p significa que não dá erro se ela já existir.

___________________________________________
na VM, digite:

cat /tmp/labops_ed25519.pub >> ~/.ssh/authorized_keys

O que ele faz:
cat                           lê a chave pública temporária
>>                            adiciona o conteúdo ao final de um arquivo
~/.ssh/authorized_keys        lista de chaves autorizadas para entrar como labops
Depois disso, o Ubuntu saberá que a chave privada correspondente, guardada no seu Windows, pode autenticar o usuário labops.
Pressione Enter. Em seguida vamos proteger o arquivo authorized_keys

__________________________________________________________

na VM:

chmod 600 ~/.ssh/authorized_keys

Isso significa:
6 = o usuário labops pode ler e alterar o arquivo
0 = outros usuários não podem acessá-lo
0 = outros usuários não podem acessá-lo
É uma regra de segurança do SSH: se esse arquivo estiver aberto demais, o OpenSSH pode recusar usar a chave.

________________________________

Agora remova a cópia temporária da chave pública:
rm /tmp/labops_ed25519.pub
Isso não remove a autorização configurada em:
~/.ssh/authorized_keys
Remove apenas o arquivo temporário usado na transferência.

_______________________

o comando completo é necessário:

ssh -i "$HOME\.ssh\labops_ed25519" labops@192.168.26.129

Ele diz claramente:
use a chave privada labops_ed25519
para entrar como labops
na VM 192.168.26.129

_______________________________________________________________
Agora usamos só um comando completo para testar a chave.
Se sua tela mostra:
labops@labops-target:~$
digite:
exit
Quando voltar para:
PS C:\Users\user>
digite exatamente:
ssh -i "$HOME\.ssh\labops_ed25519" labops@192.168.26.129
Se pedir a passphrase, digite a frase-senha que você criou para a chave.
Não digite a senha do Ubuntu se ela for solicitada


Agora a conexão funciona assim:
Windows private key
        ↓
passphrase desbloqueia a chave no Windows
        ↓
Ubuntu public key em authorized_keys
        ↓
login como labops
____________________________________________

temos dois snapshots. ✅
1. baseline-ssh-ready
   Ubuntu, OpenSSH e SSH por senha validados

2. ssh-key-auth-ready
   Chave pública autorizada e login SSH por chave testado
A barra inferior mostra “Saving state… 30%”, então o segundo snapshot ainda está sendo finalizado. Apenas espere chegar a 100% e não desligue a VM nesse momento.
Depois você terá dois pontos de retorno:
Revert para baseline-ssh-ready
→ volta para antes da autenticação por chave

Revert para ssh-key-auth-ready
→ volta para depois da chave SSH configurada

_________________________________________________________
