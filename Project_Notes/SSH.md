Há dois jeitos de falar com o mesmo Ubuntu, e eles parecem parecidos porque ambos terminam em uma tela preta com comandos.

1. Console do VMware: acesso direto
Quando você clica na tela preta dentro do VMware e faz login, está usando o console da VM.
Você → VMware Workstation → tela do Ubuntu
Aqui, não precisa de SSH. É como se você tivesse um monitor, teclado e mouse ligados diretamente naquele servidor virtual.

2. PowerShell com SSH: acesso remoto
Quando abre o PowerShell do Windows e digita:
ssh labops@192.168.26.129
o PowerShell começa no Windows, mas depois do login o prompt muda para:
labops@labops-target:~$
A partir daí, os comandos são executados dentro do Ubuntu, remotamente.
Você → PowerShell do Windows → SSH pela rede → Ubuntu Server

Por isso whoami retornou labops, mesmo você estando sentada no Windows.

O que o SSH realmente faz?
SSH é um protocolo que cria uma conexão remota, autenticada e criptografada entre Windows e Ubuntu.
Ele dá acesso ao usuário autorizado — no nosso caso, labops — e respeita as permissões desse usuário.

SSH não dá acesso automático como root.

SSH não libera tudo sem limite.

SSH permite agir como o usuário labops dentro da VM.
Com SSH, você pode:
- abrir um terminal remoto;
- executar comandos;
- consultar RAM, disco e serviços;
- enviar ou receber arquivos com segurança;
- futuramente, permitir que o Python faça essas tarefas automaticamente.

A senha atual ou, depois, a chave SSH serve para provar ao Ubuntu que o Windows tem autorização para entrar como labops.

Python, SSH e VMware têm papéis diferentes
O Python rodará no Windows, não dentro da VM. Ele usará duas “portas” de comunicação:
Python → SSH → Ubuntu

Para monitorar o sistema interno: RAM, disco, serviço SSH e comandos Linux.
Python → VMware Workstation / vmrun → VM
Para controlar a máquina virtual: ligar, desligar, criar snapshot e verificar se está ligada.

Essa separação é muito importante para explicar em entrevista:
“VMware Workstation is the hypervisor that manages the virtual machine. SSH provides secure remote access to the Ubuntu guest. Python runs on the Windows host and uses SSH to collect Linux metrics, while VMware tools manage the VM lifecycle and snapshots.”

A partir de agora, quando você usar o PowerShell com ssh, pense: “estou no Windows, mas meus comandos estão trabalhando dentro do Ubuntu.”

_________________________________
