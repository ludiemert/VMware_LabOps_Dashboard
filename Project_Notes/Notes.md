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

